from flask import Flask, request, send_file, jsonify
import subprocess
import json

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/info')
def get_info():
    url = request.args.get('url')
    if not url: return jsonify({"error": "No URL"}), 400
    try:
        command = ['yt-dlp', '-j', '--no-warnings', '--user-agent', 'Mozilla/5.0', url]
        result = subprocess.run(command, capture_output=True, text=True)
        data = json.loads(result.stdout)
        formats = []
        for f in data.get('formats', []):
            h = f.get('height')
            if h in [360, 480, 720, 1080] and f.get('url'):
                formats.append({'quality': f"{h}p", 'url': f['url']})
        if not formats:
            formats.append({'quality': "High Quality", 'url': data.get('url')})
        unique = {f['quality']: f for f in formats}.values()
        return jsonify({"title": data.get('title'), "thumbnail": data.get('thumbnail'), "formats": list(unique)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
