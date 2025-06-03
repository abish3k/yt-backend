from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/get_stream')
def get_stream():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing YouTube URL'}), 400

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        'skip_download': True,
        'cookiefile': os.path.join(os.getcwd(), 'cookies.txt')
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'stream_url': info['url'], 'title': info.get('title', 'Unknown')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
