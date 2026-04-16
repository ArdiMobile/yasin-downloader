from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

# We point one level up for the HTML since index.py is in the /api folder
app = Flask(__name__, template_folder='../', static_folder='../')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info', methods=['GET'])
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best', # Gets the best single file with audio + video
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return jsonify({
                "title": info.get('title', 'Facebook Video'),
                "thumbnail": info.get('thumbnail'),
                "video_url": info.get('url')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
