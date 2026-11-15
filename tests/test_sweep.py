"""Regression tests for the 30-day viability sweep."""

import os
import pytest

from src.al2.geometry import compute, load_kernels, sweep

KERNEL_DIR = os.environ.get("AL2_KERNEL_DIR", "kernels")


@pytest.fixture(scope="module", autouse=True)
def kernels():
    if not os.path.isdir(KERNEL_DIR):
        pytest.skip("Kernels not present")
    load_kernels(KERNEL_DIR)


def test_sweep_basic_shape():
    result = sweep(0.0, -89.9, "2026-11-15 00:00:00 UTC", days=2, step_hours=6.0)
    assert "sun_up_percent" in result
    assert "earth_visible_percent" in result
    assert "times" in result
    assert len(result["times"]) == len(result["sun_elevations"])
    assert len(result["times"]) == len(result["earth_elevations"])
    assert 0.0 <= result["sun_up_percent"] <= 100.0
    assert 0.0 <= result["earth_visible_percent"] <= 100.0


def test_sweep_matches_single_epoch():
    utc = "2026-11-15 00:00:00 UTC"
    single_sun = compute(0.0, -89.9, utc, "SUN")
    result = sweep(0.0, -89.9, utc, days=1, step_hours=24.0)
    assert abs(result["sun_elevations"][0] - single_sun.elevation_deg) < 0.01
    assert abs(result["earth_elevations"][0] - compute(0.0, -89.9, utc, "EARTH").elevation_deg) < 0.01


def test_sweep_rejects_bad_params():
    with pytest.raises(ValueError):
        sweep(0.0, -89.9, "2026-11-15 00:00:00 UTC", days=0)
    with pytest.raises(ValueError):
        sweep(0.0, -89.9, "2026-11-15 00:00:00 UTC", step_hours=-1)


def test_sweep_near_pole_percentages_finite():
    result = sweep(-89.67, 129.78, "2026-11-15 00:00:00 UTC", days=5, step_hours=2.0)
    assert isinstance(result["sun_up_percent"], float)
    assert isinstance(result["earth_visible_percent"], float)
    assert result["limitations"]
