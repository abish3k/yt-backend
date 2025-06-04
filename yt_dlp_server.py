from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/info")
def info():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify({"error": "Missing url parameter"}), 400

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "extractor_args": {
            "youtube": ["client=web"]  # Avoid SABR client
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            formats = []
            for fmt in info.get("formats", []):
                if fmt.get("ext") == "mp4" and fmt.get("url"):
                    quality = fmt.get("format_note") or str(fmt.get("height") or "Unknown")
                    formats.append({
                        "quality": f"{quality}p" if quality.isdigit() else quality,
                        "url": fmt["url"]
                    })

            formats = sorted(
                formats,
                key=lambda x: int(x["quality"].replace("p", "")) if x["quality"].endswith("p") else 0,
                reverse=True
            )

            return jsonify({
                "title": info.get("title", "Unknown"),
                "formats": formats
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "CojyneTube backend is running.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
