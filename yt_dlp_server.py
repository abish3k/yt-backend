from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

from urllib.parse import urlparse, parse_qs

@app.route("/info")
def info():
    raw_url = request.args.get("url")
    if not raw_url:
        return jsonify({"error": "Missing url parameter"}), 400

    # Rebuild the URL to isolate video param
    if "youtube.com" not in raw_url and "http" not in raw_url:
        # Assume raw_url is just a video ID or partial
        raw_url = f"https://www.youtube.com/watch?v={raw_url}"

    # Optional: strip playlist if present
    parsed = urlparse(raw_url)
    qs = parse_qs(parsed.query)
    if "v" in qs:
        video_id = qs["v"][0]
        raw_url = f"https://www.youtube.com/watch?v={video_id}"

    ...


@app.route("/")
def home():
    return "CojyneTube backend is running.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
