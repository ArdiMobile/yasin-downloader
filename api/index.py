from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__, template_folder='../')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL"}), 400

    ydl_opts = {'quiet': True, 'no_warnings': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # This is the "label" the button will show
            # We use 'format_note' because it usually says 'High Quality' or '720p'
            formats = []
            for f in info.get('formats', []):
                if f.get('url') and (f.get('vcodec') != 'none'):
                    formats.append({
                        'quality_label': f.get('format_note') or f.get('resolution') or 'Download',
                        'direct_url': f.get('url'),
                        'extension': f.get('ext')
                    })
            
            return jsonify({
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "formats": formats[:3] # Show the top 3 best links
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500