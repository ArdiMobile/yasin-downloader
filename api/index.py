from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__, template_folder='../')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/info')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {'quiet': True, 'no_warnings': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats_list = []
            for f in info.get('formats', []):
                if f.get('url') and f.get('vcodec') != 'none':
                    formats_list.append({
                        'quality': f.get('format_note') or f.get('resolution') or 'HD',
                        'url': f.get('url')
                    })

            return jsonify({
                "title": info.get('title'),
                "uploader": info.get('uploader') or "Social Media User", # Added this
                "thumbnail": info.get('thumbnail'),
                "formats": formats_list[:2]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500