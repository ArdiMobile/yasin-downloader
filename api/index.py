from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__, template_folder='../')

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
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                # Filter for useful formats with direct links
                if f.get('url'):
                    formats.append({
                        'format_id': f.get('format_id'),
                        'extension': f.get('ext'),
                        'resolution': f.get('resolution') or f.get('format_note'),
                        'url': f.get('url')
                    })
            
            return jsonify({
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "formats": formats
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DO NOT add app.run() here. Vercel handles the execution.
