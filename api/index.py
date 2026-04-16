from flask import Flask, request, jsonify
import yt_dlp
import json

app = Flask(__name__)

@app.route('/info')
def get_info():
    url = request.args.get('url')
    if not url: 
        return jsonify({"error": "No URL provided"}), 400
    try:
        # Use yt_dlp library directly for better performance on Vercel
        ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=False)
            formats = []
            for f in data.get('formats', []):
                h = f.get('height')
                if h in [360, 480, 720, 1080] and f.get('url'):
                    formats.append({'quality': f"{h}p", 'url': f['url']})
            
            if not formats:
                formats.append({'quality': "HD Video", 'url': data.get('url')})
            
            # Filter unique qualities
            unique = {f['quality']: f for f in formats}.values()
            return jsonify({
                "title": data.get('title'), 
                "thumbnail": data.get('thumbnail'), 
                "formats": list(unique)
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
