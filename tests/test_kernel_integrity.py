import hashlib
import io
import os
from pathlib import Path

import pytest

from scripts import bootstrap_kernels
from src.al2 import geometry
from src.al2.kernel_manifest import (
    KernelIntegrityError,
    KernelManifestError,
    KernelSpec,
    read_kernel_manifest,
)


REAL_SPECS = read_kernel_manifest()


class SpiceSpy:
    def __init__(self, fail_on_furnsh=None):
        self.fail_on_furnsh = fail_on_furnsh
        self.furnsh_calls = []
        self.kclear_calls = 0
        self.loaded = []

    def kclear(self):
        self.kclear_calls += 1
        self.loaded.clear()

    def furnsh(self, path):
        self.furnsh_calls.append(path)
        if len(self.furnsh_calls) == self.fail_on_furnsh:
            raise RuntimeError("simulated SPICE load failure")
        self.loaded.append(path)


def create_kernel_stack(directory: Path):
    directory.mkdir()
    specs = []
    for index, real_spec in enumerate(REAL_SPECS):
        content = f"verified test kernel {index}".encode()
        specs.append(KernelSpec(
            real_spec.filename,
            real_spec.archive_path,
            hashlib.sha256(content).hexdigest(),
        ))
        (directory / real_spec.filename).write_bytes(content)
    return tuple(specs)


def write_manifest(path: Path, specs):
    rows = [
        "# Kernel Manifest",
        "",
        "## Required files (DE421 stack)",
        "",
        "| Filename | Official NAIF archive path | SHA-256 |",
        "|---|---|---|",
    ]
    rows.extend(
        f"| {spec.filename} | `{spec.archive_path}` | `{spec.sha256}` |"
        for spec in specs
    )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def install_spice_spy(monkeypatch, fail_on_furnsh=None):
    spy = SpiceSpy(fail_on_furnsh)
    monkeypatch.setattr(geometry, "spice", spy)
    monkeypatch.setattr(geometry, "_KERNELS_LOADED", False)
    return spy


def test_missing_kernel_does_not_call_furnsh(tmp_path, monkeypatch):
    kernel_dir = tmp_path / "kernels"
    specs = create_kernel_stack(kernel_dir)
    manifest = write_manifest(tmp_path / "manifest.md", specs)
    (kernel_dir / specs[2].filename).unlink()
    spy = install_spice_spy(monkeypatch)

    with pytest.raises(KernelIntegrityError, match="missing"):
        geometry.load_kernels(kernel_dir, manifest)

    assert spy.furnsh_calls == []
    assert not geometry._KERNELS_LOADED
    with pytest.raises(KernelIntegrityError, match="not been loaded"):
        geometry.compute(0, -89.9, "2026-11-15 00:00:00 UTC", "SUN")


def test_modified_kernel_does_not_call_furnsh(tmp_path, monkeypatch):
    kernel_dir = tmp_path / "kernels"
    specs = create_kernel_stack(kernel_dir)
    manifest = write_manifest(tmp_path / "manifest.md", specs)
    (kernel_dir / specs[0].filename).write_bytes(b"modified")
    spy = install_spice_spy(monkeypatch)

    with pytest.raises(KernelIntegrityError, match="SHA-256 mismatch"):
        geometry.load_kernels(kernel_dir, manifest)

    assert spy.furnsh_calls == []


def test_incorrect_manifest_hash_does_not_call_furnsh(tmp_path, monkeypatch):
    kernel_dir = tmp_path / "kernels"
    specs = create_kernel_stack(kernel_dir)
    incorrect_specs = (
        KernelSpec(specs[0].filename, specs[0].archive_path, "0" * 64),
        *specs[1:],
    )
    manifest = write_manifest(tmp_path / "manifest.md", incorrect_specs)
    spy = install_spice_spy(monkeypatch)

    with pytest.raises(KernelIntegrityError, match="SHA-256 mismatch"):
        geometry.load_kernels(kernel_dir, manifest)

    assert spy.furnsh_calls == []


def test_incomplete_manifest_does_not_call_furnsh(tmp_path, monkeypatch):
    kernel_dir = tmp_path / "kernels"
    specs = create_kernel_stack(kernel_dir)
    manifest = write_manifest(tmp_path / "manifest.md", specs[:-1])
    spy = install_spice_spy(monkeypatch)

    with pytest.raises(KernelManifestError, match="Expected 5 kernel entries"):
        geometry.load_kernels(kernel_dir, manifest)

    assert spy.furnsh_calls == []


def test_unexpected_kernel_directory_entry_does_not_call_furnsh(tmp_path, monkeypatch):
    kernel_dir = tmp_path / "kernels"
    specs = create_kernel_stack(kernel_dir)
    (kernel_dir / "unexpected.bin").write_bytes(b"extra")
    manifest = write_manifest(tmp_path / "manifest.md", specs)
    spy = install_spice_spy(monkeypatch)

    with pytest.raises(KernelIntegrityError, match="Unexpected entries"):
        geometry.load_kernels(kernel_dir, manifest)

    assert spy.furnsh_calls == []


def test_spice_load_failure_clears_partial_pool(tmp_path, monkeypatch):
    kernel_dir = tmp_path / "kernels"
    specs = create_kernel_stack(kernel_dir)
    manifest = write_manifest(tmp_path / "manifest.md", specs)
    spy = install_spice_spy(monkeypatch, fail_on_furnsh=3)

    with pytest.raises(RuntimeError, match="simulated SPICE"):
        geometry.load_kernels(kernel_dir, manifest)

    assert len(spy.furnsh_calls) == 3
    assert spy.kclear_calls == 2
    assert spy.loaded == []
    assert not geometry._KERNELS_LOADED


def test_successfully_loads_only_complete_verified_stack(tmp_path, monkeypatch):
    kernel_dir = tmp_path / "kernels"
    specs = create_kernel_stack(kernel_dir)
    manifest = write_manifest(tmp_path / "manifest.md", specs)
    spy = install_spice_spy(monkeypatch)

    geometry.load_kernels(kernel_dir, manifest)

    assert spy.furnsh_calls == [str(kernel_dir / spec.filename) for spec in specs]
    assert spy.loaded == spy.furnsh_calls
    assert spy.kclear_calls == 1
    assert geometry._KERNELS_LOADED


def test_download_verifies_before_atomic_replacement(tmp_path, monkeypatch):
    content = b"downloaded verified content"
    spec = KernelSpec("test.kernel", "test/test.kernel", hashlib.sha256(content).hexdigest())
    destination_dir = tmp_path / "kernels"
    destination_dir.mkdir()
    destination = destination_dir / spec.filename
    destination.write_bytes(b"existing destination")
    monkeypatch.setattr(
        bootstrap_kernels.urllib.request,
        "urlopen",
        lambda _url: io.BytesIO(content),
    )
    real_replace = os.replace
    replace_observations = []

    def assert_verified_before_replace(source, target):
        assert Path(source).parent == destination_dir
        assert hashlib.sha256(Path(source).read_bytes()).hexdigest() == spec.sha256
        assert Path(target).read_bytes() == b"existing destination"
        replace_observations.append(True)
        real_replace(source, target)

    monkeypatch.setattr(bootstrap_kernels.os, "replace", assert_verified_before_replace)
    installed = bootstrap_kernels.download_kernel(spec, destination_dir)

    assert installed == destination
    assert destination.read_bytes() == content
    assert replace_observations == [True]
    assert list(destination_dir.iterdir()) == [destination]


def test_failed_download_preserves_destination_and_cleans_temporary_file(
    tmp_path, monkeypatch
):
    content = b"wrong downloaded content"
    spec = KernelSpec("test.kernel", "test/test.kernel", "0" * 64)
    destination_dir = tmp_path / "kernels"
    destination_dir.mkdir()
    destination = destination_dir / spec.filename
    destination.write_bytes(b"existing verified destination")
    monkeypatch.setattr(
        bootstrap_kernels.urllib.request,
        "urlopen",
        lambda _url: io.BytesIO(content),
    )

    with pytest.raises(KernelIntegrityError, match="SHA-256 mismatch"):
        bootstrap_kernels.download_kernel(spec, destination_dir)

    assert destination.read_bytes() == b"existing verified destination"
    assert list(destination_dir.iterdir()) == [destination]
