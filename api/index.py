from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__, template_folder='../')

# This handles the main page
@app.route('/')
def index():
    return render_template('index.html')

# This handles the download logic
@app.route('/api/info')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # We create a clean list of video links
            formats_list = []
            # Just get the top 2