# yt_dlp_server.py
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/resolve")
def resolve():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Missing id parameter"}), 400

    try:
        result = subprocess.run([
            "yt-dlp", "-f", "best", "-g", f"https://www.youtube.com/watch?v={video_id}"
        ], capture_output=True, text=True, check=True)

        stream_url = result.stdout.strip()
        return jsonify({"url": stream_url})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "yt-dlp failed", "details": e.stderr}), 500

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
