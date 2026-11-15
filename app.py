"""Minimal web application for Ashura's Light 2."""

from flask import Flask, jsonify, render_template, request
from src.al2.geometry import compute, load_kernels
import os

app = Flask(__name__)

KERNEL_DIR = os.environ.get("AL2_KERNEL_DIR", "kernels")

try:
    load_kernels(KERNEL_DIR)
    KERNELS_OK = True
except FileNotFoundError as exc:
    KERNELS_OK = False
    KERNEL_ERROR = str(exc)


@app.route("/")
def index():
    return render_template("index.html", kernels_ok=KERNELS_OK)


@app.route("/api/compute", methods=["POST"])
def api_compute():
    if not KERNELS_OK:
        return jsonify({"error": "Kernels not loaded. See docs/KERNEL_MANIFEST.md"}), 503
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
