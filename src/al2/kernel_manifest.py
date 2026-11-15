"""Read and verify the authoritative SPICE kernel manifest."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


DEFAULT_MANIFEST_PATH = Path(__file__).resolve().parents[2] / "docs" / "KERNEL_MANIFEST.md"
EXPECTED_KERNEL_COUNT = 5
_MANIFEST_HEADERS = ("Filename", "Official NAIF archive path", "SHA-256")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")


class KernelIntegrityError(RuntimeError):
    """A kernel stack is missing or does not match the manifest."""


class KernelManifestError(KernelIntegrityError):
    """The authoritative kernel manifest is missing or invalid."""


@dataclass(frozen=True)
class KernelSpec:
    filename: str
    archive_path: str
    sha256: str


def _table_cells(line: str) -> list[str] | None:
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        return None
    return [cell.strip().strip("`").strip() for cell in line[1:-1].split("|")]


def read_kernel_manifest(manifest_path: str | Path = DEFAULT_MANIFEST_PATH) -> tuple[KernelSpec, ...]:
    """Parse the kernel inventory and hashes from docs/KERNEL_MANIFEST.md."""
    path = Path(manifest_path)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise KernelManifestError(f"Cannot read kernel manifest {path}: {exc}") from exc

    section = "## Required files (DE421 stack)"
    try:
        section_index = lines.index(section)
    except ValueError as exc:
        raise KernelManifestError(f"Required kernel section missing from {path}") from exc

    header_index = None
    for index in range(section_index + 1, len(lines)):
        if _table_cells(lines[index]) == list(_MANIFEST_HEADERS):
            header_index = index
            break
    if header_index is None:
        raise KernelManifestError(f"Kernel table header missing from {path}")

    separator = _table_cells(lines[header_index + 1]) if header_index + 1 < len(lines) else None
    if separator is None or len(separator) != len(_MANIFEST_HEADERS) or not all(
        _SEPARATOR_RE.fullmatch(cell) for cell in separator
    ):
        raise KernelManifestError(f"Kernel table separator is invalid in {path}")

    specs: list[KernelSpec] = []
    for line in lines[header_index + 2:]:
        if not line.strip() or not line.lstrip().startswith("|"):
            break
        cells = _table_cells(line)
        if cells is None or len(cells) != len(_MANIFEST_HEADERS):
            raise KernelManifestError(f"Malformed kernel table row in {path}: {line}")

        filename, archive_path, expected_hash = cells
        archive = PurePosixPath(archive_path)
        if (
            not filename
            or "/" in filename
            or "\\" in filename
            or filename in {".", ".."}
            or archive.is_absolute()
            or not archive.parts
            or any(part in {".", ".."} for part in archive.parts)
            or archive.name != filename
        ):
            raise KernelManifestError(f"Invalid kernel filename or archive path in {path}: {line}")
        if not _SHA256_RE.fullmatch(expected_hash):
            raise KernelManifestError(f"Invalid SHA-256 for {filename} in {path}")
        specs.append(KernelSpec(filename, archive_path, expected_hash))

    if len(specs) != EXPECTED_KERNEL_COUNT:
        raise KernelManifestError(
            f"Expected {EXPECTED_KERNEL_COUNT} kernel entries in {path}, found {len(specs)}"
        )
    filenames = [spec.filename for spec in specs]
    archive_paths = [spec.archive_path for spec in specs]
    if len(set(filenames)) != len(filenames) or len(set(archive_paths)) != len(archive_paths):
        raise KernelManifestError(f"Duplicate kernel filename or archive path in {path}")
    return tuple(specs)


def sha256_file(path: str | Path) -> str:
    """Return a file's SHA-256 digest."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_kernel_files(
    kernel_dir: str | Path,
    specs: tuple[KernelSpec, ...],
) -> tuple[Path, ...]:
    """Verify an exact kernel directory before returning paths in manifest order."""
    directory = Path(kernel_dir)
    if not directory.is_dir():
        raise KernelIntegrityError(f"Kernel directory does not exist: {directory}")

    try:
        entries = tuple(directory.iterdir())
    except OSError as exc:
        raise KernelIntegrityError(f"Cannot inspect kernel directory {directory}: {exc}") from exc

    expected_names = {spec.filename for spec in specs}
    unexpected = sorted(entry.name for entry in entries if entry.name not in expected_names)
    if unexpected:
        raise KernelIntegrityError(
            f"Unexpected entries in kernel directory {directory}: {', '.join(unexpected)}"
        )

    paths: list[Path] = []
    for spec in specs:
        path = directory / spec.filename
        if path.is_symlink() or not path.is_file():
            raise KernelIntegrityError(f"Required kernel missing or not a regular file: {path}")
        try:
            actual_hash = sha256_file(path)
        except OSError as exc:
            raise KernelIntegrityError(f"Cannot read kernel {path}: {exc}") from exc
        if actual_hash != spec.sha256:
            raise KernelIntegrityError(
                f"SHA-256 mismatch for {path}: expected {spec.sha256}, got {actual_hash}"
            )
        paths.append(path)
    return tuple(paths)


def verify_kernel_directory(
    kernel_dir: str | Path,
    manifest_path: str | Path = DEFAULT_MANIFEST_PATH,
) -> tuple[Path, ...]:
    """Read the authoritative manifest and verify the complete kernel directory."""
    return verify_kernel_files(kernel_dir, read_kernel_manifest(manifest_path))
