from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download_video():
    # Your Facebook downloading logic here
    return jsonify({"status": "success"})

# This is important for Vercel
if __name__ == "__main__":
    app.run()
