import re
import csv
import io
import os
import signal
import threading
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def normalize_phone(phone: str) -> str:
    """Normalize to French format: XX XX XX XX XX. Returns '' if invalid."""
    if not phone:
        return ""
    c = re.sub(r"[\s\-\.\(\)]", "", phone)
    if len(c) < 9:          # ignore short/special numbers like 3631
        return ""
    if c.startswith("+33"):
        c = "0" + c[3:]
    elif c.startswith("0033"):
        c = "0" + c[4:]
    if not re.match(r"^0\d{9}$", c):
        return ""
    return " ".join(c[i : i + 2] for i in range(0, 10, 2))


def mask_phone(normalized: str) -> str:
    """02 41 21 09 21 → 02 ** ** ** **"""
    if not normalized:
        return ""
    parts = normalized.split(" ")
    if len(parts) != 5:
        return ""
    return parts[0] + " " + " ".join("**" for _ in parts[1:])


def parse_json_response(data: dict) -> list:
    records = []
    for el in data.get("elements", []):
        tags = el.get("tags", {})

        if el["type"] == "node":
            lat, lon = el.get("lat"), el.get("lon")
        else:
            center = el.get("center", {})
            lat, lon = center.get("lat"), center.get("lon")

        phone_raw = (
            tags.get("phone")
            or tags.get("contact:phone")
            or tags.get("telephone")
            or ""
        )
        phone_norm = normalize_phone(phone_raw)
        phone_mask = mask_phone(phone_norm)

        place_type = (
            tags.get("amenity")
            or tags.get("shop")
            or tags.get("tourism")
            or tags.get("office")
            or tags.get("leisure")
            or tags.get("craft")
            or ""
        )

        records.append(
            {
                "name": tags.get("name", ""),
                "phone_raw": phone_raw,
                "phone_normalized": phone_norm,
                "phone_masked": phone_mask,
                "type": place_type,
                "lat": lat,
                "lon": lon,
            }
        )
    return records


def parse_csv_response(text: str) -> list:
    """Parse Overpass [out:csv] tab-separated response."""
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    records = []
    for row in reader:
        # phone: try both tag names
        phone_raw = row.get("phone") or row.get("contact:phone") or ""
        phone_norm = normalize_phone(phone_raw)
        phone_mask = mask_phone(phone_norm)

        place_type = (
            row.get("amenity") or row.get("shop") or row.get("tourism")
            or row.get("office") or row.get("leisure") or row.get("craft") or ""
        )

        # coordinates: Overpass CSV exports ::lat/::lon as "@lat"/"@lon" headers
        raw_lat = row.get("@lat") or row.get("::lat") or row.get("lat") or ""
        raw_lon = row.get("@lon") or row.get("::lon") or row.get("lon") or ""

        try:
            lat = float(raw_lat) if raw_lat else None
        except ValueError:
            lat = None
        try:
            lon = float(raw_lon) if raw_lon else None
        except ValueError:
            lon = None

        records.append(
            {
                "name": row.get("name", ""),
                "phone_raw": phone_raw,
                "phone_normalized": phone_norm,
                "phone_masked": phone_mask,
                "type": place_type,
                "lat": lat,
                "lon": lon,
            }
        )
    return records


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
def run_query():
    query = (request.json or {}).get("query", "").strip()
    if not query:
        return jsonify({"success": False, "error": "Requête vide"}), 400

    try:
        resp = requests.post(OVERPASS_URL, data={"data": query}, timeout=60)
        resp.raise_for_status()

        if "json" in resp.headers.get("content-type", ""):
            records = parse_json_response(resp.json())
        else:
            records = parse_csv_response(resp.text)

        return jsonify({"success": True, "records": records, "count": len(records)})
    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "Timeout (60s) — réduisez la zone ou la requête"}), 408
    except requests.exceptions.HTTPError as e:
        return jsonify({"success": False, "error": f"Erreur Overpass API : {e}"}), 502
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/quit", methods=["POST"])
def quit_app():
    def shutdown():
        import time
        time.sleep(0.4)
        os.kill(os.getpid(), signal.SIGINT)
    threading.Thread(target=shutdown, daemon=True).start()
    return jsonify({"ok": True})


if __name__ == "__main__":
    import webbrowser

    def open_browser():
        webbrowser.open("http://localhost:5000")

    threading.Timer(1.0, open_browser).start()
    app.run(debug=False, port=5000)
