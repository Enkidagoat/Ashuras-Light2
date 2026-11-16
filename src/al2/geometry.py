"""Ashura's Light 2 — geometric calculation engine.

Terrain-free centre-direction azimuth/elevation for Sun and Earth
from a lunar surface site using the DE421 / MOON_ME_DE421 stack.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from pathlib import Path

import numpy as np
import spiceypy as spice

from .kernel_manifest import (
    DEFAULT_MANIFEST_PATH,
    KernelIntegrityError,
    verify_kernel_directory,
)

FRAME = "MOON_ME_DE421"
REFERENCE_RADIUS_KM = 1737.4
CORRECTION = "NONE"  # geometric; documented
_KERNELS_LOADED = False


@dataclass
class Result:
    target: str
    azimuth_deg: float
    elevation_deg: float
    range_km: float
    utc: str
    et: float
    frame: str
    correction: str
    site_lon_deg: float
    site_lat_deg: float
    site_alt_km: float
    limitations: str


def load_kernels(
    kernel_dir: str | Path,
    manifest_path: str | Path = DEFAULT_MANIFEST_PATH,
) -> None:
    """Verify the complete manifest-listed stack before loading any SPICE kernels."""
    global _KERNELS_LOADED
    _KERNELS_LOADED = False
    spice.kclear()
    try:
        kernel_paths = verify_kernel_directory(kernel_dir, manifest_path)
        for path in kernel_paths:
            spice.furnsh(str(path))
    except Exception:
        spice.kclear()
        raise
    _KERNELS_LOADED = True


def site_vector(lon_deg: float, lat_deg: float, alt_km: float = 0.0) -> np.ndarray:
    """Planetocentric site vector in MOON_ME_DE421 (km)."""
    lon = np.deg2rad(lon_deg)
    lat = np.deg2rad(lat_deg)
    return spice.georec(lon, lat, alt_km, REFERENCE_RADIUS_KM, 0.0)


def local_enu(site_bf: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Radial up, east, north basis. Azimuth undefined at exact pole."""
    up = site_bf / np.linalg.norm(site_bf)
    # Near-pole guard
    if abs(up[2]) > 0.999999:
        raise ValueError(
            "Exact or near-exact pole: azimuth is undefined until an explicit "
            "tangent basis is supplied. Provide a non-polar latitude."
        )
    east = np.cross(np.array([0.0, 0.0, 1.0]), up)
    east /= np.linalg.norm(east)
    north = np.cross(up, east)
    return east, north, up


def compute(
    lon_deg: float,
    lat_deg: float,
    utc: str,
    target: str,
    alt_km: float = 0.0,
) -> Result:
    """Geometric centre-direction AZ/EL for SUN or EARTH."""
    if not _KERNELS_LOADED:
        raise KernelIntegrityError("Verified kernels have not been loaded")
    if target not in ("SUN", "EARTH"):
        raise ValueError("target must be SUN or EARTH")
    et = spice.str2et(utc)
    site = site_vector(lon_deg, lat_deg, alt_km)
    state, _ = spice.spkpos(target, et, FRAME, CORRECTION, "MOON")
    vec = state - site
    east, north, up = local_enu(site)
    local = np.array([np.dot(vec, east), np.dot(vec, north), np.dot(vec, up)])
    r = float(np.linalg.norm(local))
    elev = float(np.rad2deg(np.arcsin(local[2] / r)))
    az = float(np.rad2deg(np.arctan2(local[0], local[1])) % 360.0)
    limitations = (
        "Terrain-free centre-direction geometry only. "
        "Does not establish usable electrical power, "
        "operational communication availability, "
        "terrain-masked visibility, or landing safety."
    )
    return Result(
        target=target,
        azimuth_deg=az,
        elevation_deg=elev,
        range_km=r,
        utc=utc,
        et=et,
        frame=FRAME,
        correction=CORRECTION,
        site_lon_deg=lon_deg,
        site_lat_deg=lat_deg,
        site_alt_km=alt_km,
        limitations=limitations,
    )


def sweep(
    lon_deg: float,
    lat_deg: float,
    start_utc: str,
    days: int = 30,
    step_hours: float = 1.0,
    alt_km: float = 0.0,
) -> Dict[str, Any]:
    """Sample Sun and Earth elevation over a time span.

    Returns percentages of time above horizon and countdowns to next set.
    """
    if days <= 0 or step_hours <= 0:
        raise ValueError("days and step_hours must be positive")
    start_et = spice.str2et(start_utc)
    step_sec = step_hours * 3600.0
    n_steps = int(days * 24.0 / step_hours) + 1
    times: List[str] = []
    sun_els: List[float] = []
    earth_els: List[float] = []
    sun_up_count = 0
    earth_vis_count = 0
    next_sunset_et: Optional[float] = None
    next_earthset_et: Optional[float] = None
    prev_sun_up: Optional[bool] = None
    prev_earth_up: Optional[bool] = None

    site = site_vector(lon_deg, lat_deg, alt_km)
    east, north, up = local_enu(site)

    for i in range(n_steps):
        et = start_et + i * step_sec
        utc = spice.et2utc(et, "ISOC", 0)
        times.append(utc)

        # Sun
        state, _ = spice.spkpos("SUN", et, FRAME, CORRECTION, "MOON")
        vec = state - site
        local = np.array([np.dot(vec, east), np.dot(vec, north), np.dot(vec, up)])
        r = float(np.linalg.norm(local))
        elev = float(np.rad2deg(np.arcsin(local[2] / r)))
        sun_els.append(elev)
        sun_up = elev > 0.0
        if sun_up:
            sun_up_count += 1
        if prev_sun_up is True and not sun_up and next_sunset_et is None:
            next_sunset_et = et
        prev_sun_up = sun_up

        # Earth
        state, _ = spice.spkpos("EARTH", et, FRAME, CORRECTION, "MOON")
        vec = state - site
        local = np.array([np.dot(vec, east), np.dot(vec, north), np.dot(vec, up)])
        r = float(np.linalg.norm(local))
        elev = float(np.rad2deg(np.arcsin(local[2] / r)))
        earth_els.append(elev)
        earth_up = elev > 0.0
        if earth_up:
            earth_vis_count += 1
        if prev_earth_up is True and not earth_up and next_earthset_et is None:
            next_earthset_et = et
        prev_earth_up = earth_up

    total = len(times)
    sun_up_pct = (sun_up_count / total) * 100.0 if total else 0.0
    earth_vis_pct = (earth_vis_count / total) * 100.0 if total else 0.0

    def countdown_hours(next_et: Optional[float]) -> Optional[float]:
        if next_et is None:
            return None
        return round((next_et - start_et) / 3600.0, 1)

    return {
        "times": times,
        "sun_elevations": sun_els,
        "earth_elevations": earth_els,
        "sun_up_percent": round(sun_up_pct, 1),
        "earth_visible_percent": round(earth_vis_pct, 1),
        "next_sunset_hours": countdown_hours(next_sunset_et),
        "next_earthset_hours": countdown_hours(next_earthset_et),
        "start_utc": start_utc,
        "days": days,
        "step_hours": step_hours,
        "limitations": (
            "Terrain-free centre-direction geometry only. "
            "Percentages do not establish usable power or operational communications."
        ),
    }
