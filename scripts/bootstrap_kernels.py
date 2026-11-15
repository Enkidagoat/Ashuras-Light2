#!/usr/bin/env python3
"""Download and verify the DE421 kernels listed in the project manifest."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.al2.kernel_manifest import (  # noqa: E402
    DEFAULT_MANIFEST_PATH,
    KernelIntegrityError,
    KernelSpec,
    read_kernel_manifest,
    sha256_file,
    verify_kernel_files,
)

BASE_URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/"


def download_kernel(
    spec: KernelSpec,
    destination_dir: str | Path,
    base_url: str = BASE_URL,
) -> Path:
    """Download one kernel to a same-directory temporary file and atomically install it."""
    destination_dir = Path(destination_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / spec.filename
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{spec.filename}.",
        suffix=".part",
        dir=destination_dir,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as target:
            url = base_url.rstrip("/") + "/" + spec.archive_path
            with urllib.request.urlopen(url) as response:
                shutil.copyfileobj(response, target, length=1024 * 1024)
            target.flush()
            os.fsync(target.fileno())

        actual_hash = sha256_file(temporary_path)
        if actual_hash != spec.sha256:
            raise KernelIntegrityError(
                f"SHA-256 mismatch for {spec.filename}: "
                f"expected {spec.sha256}, got {actual_hash}"
            )
        os.replace(temporary_path, destination)
        return destination
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def bootstrap(
    destination_dir: str | Path,
    manifest_path: str | Path = DEFAULT_MANIFEST_PATH,
) -> tuple[Path, ...]:
    """Acquire each manifest entry and verify the resulting exact file set."""
    specs = read_kernel_manifest(manifest_path)
    destination_dir = Path(destination_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        print(f"Fetching {spec.filename} ...")
        installed = download_kernel(spec, destination_dir)
        print(f"  verified {sha256_file(installed)}")
    return verify_kernel_files(destination_dir, specs)


def main() -> None:
    destination = Path(os.environ.get("AL2_KERNEL_DIR", "kernels"))
    verified = bootstrap(destination)
    print(f"All {len(verified)} kernels verified in {destination}")


if __name__ == "__main__":
    main()
