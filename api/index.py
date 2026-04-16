from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/info')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
        
    try:
        # Direct library usage is better than subprocess on Vercel
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            
            for f in info.get('formats', []):
                if f.get('height') and f.get('url'):
                    formats.append({
                        'quality': f"{f['height']}p",
                        'url': f['url']
                    })
            
            # Fallback if no specific heights are found
            if not formats:
                formats.append({'quality': "Default HD", 'url': info.get('url')})

            return jsonify({
                "title": info.get('title', 'Video'),
                "formats": formats[:5] # Limit to top 5 links
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
