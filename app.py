"""Minimal web application for Ashura's Light 2."""

import os

from flask import Flask, jsonify, render_template, request
from src.al2.geometry import compute, load_kernels, sweep
from src.al2.kernel_manifest import KernelIntegrityError

app = Flask(__name__)

KERNEL_DIR = os.environ.get("AL2_KERNEL_DIR", "kernels")

try:
    load_kernels(KERNEL_DIR)
    KERNELS_OK = True
    KERNEL_ERROR = None
except KernelIntegrityError as exc:
    KERNELS_OK = False
    KERNEL_ERROR = str(exc)


@app.route("/")
def index():
    return render_template("index.html", kernels_ok=KERNELS_OK)


@app.route("/api/compute", methods=["POST"])
def api_compute():
    if not KERNELS_OK:
        return jsonify({
            "error": KERNEL_ERROR or "Kernels not loaded. See docs/KERNEL_MANIFEST.md"
        }), 503
    data = request.get_json(force=True)
    try:
        lon = float(data["lon"])
        lat = float(data["lat"])
        utc = data["utc"]
        alt = float(data.get("alt", 0.0))
        sun = compute(lon, lat, utc, "SUN", alt)
        earth = compute(lon, lat, utc, "EARTH", alt)
        return jsonify({
            "sun": sun.__dict__,
            "earth": earth.__dict__,
            "provenance": {
                "frame": "MOON_ME_DE421",
                "correction": "NONE (geometric)",
                "radius_km": 1737.4,
                "kernels": "DE421 stack (see KERNEL_MANIFEST.md)",
            },
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/sweep", methods=["POST"])
def api_sweep():
    if not KERNELS_OK:
        return jsonify({
            "error": (
                "Verified kernels are unavailable. From the project folder, run "
                "'python scripts/bootstrap_kernels.py', then restart the app. If "
                "you use another kernel folder, set AL2_KERNEL_DIR before launch."
            )
        }), 503
    data = request.get_json(force=True)
    try:
        lon = float(data["lon"])
        lat = float(data["lat"])
        utc = data["utc"]
        alt = float(data.get("alt", 0.0))
        days = int(data.get("days", 30))
        step = float(data.get("step_hours", 1.0))
        if not (1 <= days <= 90):
            return jsonify({"error": "days must be between 1 and 90"}), 400
        if not (0.25 <= step <= 24):
            return jsonify({"error": "step_hours must be between 0.25 and 24"}), 400
        result = sweep(lon, lat, utc, days, step, alt)
        result["provenance"] = {
            "frame": "MOON_ME_DE421",
            "correction": "NONE (geometric)",
            "radius_km": 1737.4,
            "kernels": "DE421 stack (see KERNEL_MANIFEST.md)",
        }
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
