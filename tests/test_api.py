"""API regression tests (requires kernels)."""

import os
import pytest

from app import app

KERNEL_DIR = os.environ.get("AL2_KERNEL_DIR", "kernels")


@pytest.fixture
def client():
    if not os.path.isdir(KERNEL_DIR):
        pytest.skip("Kernels not present")
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_compute_ok(client):
    rv = client.post("/api/compute", json={
        "lon": 0.0,
        "lat": -89.9,
        "utc": "2026-11-15 00:00:00 UTC",
        "alt": 0.0,
    })
    assert rv.status_code == 200
    data = rv.get_json()
    assert "sun" in data and "earth" in data
    assert "azimuth_deg" in data["sun"]
    assert "elevation_deg" in data["earth"]


def test_compute_bad_input(client):
    rv = client.post("/api/compute", json={
        "lon": "not-a-number",
        "lat": -89.9,
        "utc": "2026-11-15 00:00:00 UTC",
    })
    assert rv.status_code == 400


def test_sweep_ok(client):
    rv = client.post("/api/sweep", json={
        "lon": 0.0,
        "lat": -89.9,
        "utc": "2026-11-15 00:00:00 UTC",
        "days": 1,
        "step_hours": 12.0,
    })
    assert rv.status_code == 200
    data = rv.get_json()
    assert "sun_up_percent" in data
    assert "earth_visible_percent" in data
    assert "times" in data
    assert len(data["times"]) > 0
    # Endpoint must return real timestamps, not a placeholder
    assert data["times"][0].startswith("2026-11-15")
    assert "next_sunset_hours" in data or data.get("next_sunset_hours") is None
    assert "sun_elevations" in data
    assert len(data["sun_elevations"]) == len(data["times"])


def test_sweep_30_days(client):
    rv = client.post("/api/sweep", json={
        "lon": 0.0,
        "lat": -89.9,
        "utc": "2026-11-15 00:00:00 UTC",
        "days": 30,
        "step_hours": 1.0,
    })
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["days"] == 30
    assert data["step_hours"] == 1.0
    assert len(data["times"]) == 721
    assert len(data["sun_elevations"]) == len(data["times"])
    assert len(data["earth_elevations"]) == len(data["times"])


def test_sweep_bad_input(client):
    rv = client.post("/api/sweep", json={
        "lon": 0.0,
        "lat": -89.9,
        "utc": "2026-11-15 00:00:00 UTC",
        "days": -5,
    })
    assert rv.status_code == 400
