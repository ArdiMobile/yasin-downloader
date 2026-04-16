from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/info')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
        
    try:
        # Configuration for yt-dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                # Filter for standard video resolutions
                if f.get('height') in [360, 480, 720, 1080] and f.get('url'):
                    formats.append({
                        'quality': f"{f['height']}p",
                        'url': f['url'],
                        'ext': f.get('ext', 'mp4')
                    })
            
            # Fallback if no specific resolutions found
            if not formats:
                formats.append({'quality': "High Quality", 'url': info.get('url'), 'ext': 'mp4'})
            
            # Remove duplicates
            unique_formats = {f['quality']: f for f in formats}.values()
            
            return jsonify({
                "title": info.get('title', 'Video'),
                "thumbnail": info.get('thumbnail'),
                "formats": list(unique_formats)
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Entry point for local testing only; Vercel ignores this
if __name__ == "__main__":
    app.run()
