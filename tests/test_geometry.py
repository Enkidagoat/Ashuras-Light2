"""Tests for geometry engine (kernels required)."""

import os
import pytest
from src.al2.geometry import compute, load_kernels, site_vector

KERNEL_DIR = os.environ.get("AL2_KERNEL_DIR", "kernels")

@pytest.fixture(scope="module", autouse=True)
def kernels():
    if not os.path.isdir(KERNEL_DIR):
        pytest.skip("Kernels not present")
    load_kernels(KERNEL_DIR)


def test_site_vector_shape():
    v = site_vector(0.0, -89.9, 0.0)
    assert v.shape == (3,)
    assert abs(v[2]) > 1700


def test_compute_sun_earth():
    r = compute(0.0, -89.9, "2026-11-15 00:00:00 UTC", "SUN")
    assert 0 <= r.azimuth_deg < 360
    assert -90 <= r.elevation_deg <= 90
    e = compute(0.0, -89.9, "2026-11-15 00:00:00 UTC", "EARTH")
    assert 0 <= e.azimuth_deg < 360


def test_pole_raises():
    with pytest.raises(ValueError):
        compute(0.0, -90.0, "2026-11-15 00:00:00 UTC", "SUN")
