import gradio as gr
import yt_dlp
import os
import tempfile
import json

def download_video(url):
    """Download video from Facebook or Instagram with audio"""
    if not url:
        return None, json.dumps({"status": "error", "message": "No URL provided"})
    
    # Check if valid URL
    if not any(domain in url for domain in ['facebook.com', 'fb.com', 'fb.watch', 'instagram.com', 'instagr.am']):
        return None, json.dumps({"status": "error", "message": "Please enter a valid Facebook or Instagram URL"})
    
    try:
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, 'video.mp4')
        
        # Format strategy for merged video+audio
        if 'instagram.com' in url or 'instagr.am' in url:
            format_str = 'bestvideo+bestaudio/best'
        else:
            format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        
        ydl_opts = {
            'outtmpl': output_path,
            'format': format_str,
            'merge_output_format': 'mp4',
            'quiet': True,
            'noplaylist': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Video')
            uploader = info.get('uploader', '')
            duration = info.get('duration', 0)
            
            result = {
                "status": "success",
                "title": title,
                "uploader": uploader,
                "duration": f"{int(duration//60)}:{int(duration%60):02d}",
                "filename": "video.mp4"
            }
            
            if os.path.exists(output_path):
                return output_path, json.dumps(result)
            
            # Try with .mkv extension
            alt_path = os.path.join(temp_dir, 'video.mkv')
            if os.path.exists(alt_path):
                return alt_path, json.dumps(result)
            
            # Try other extensions
            for ext in ['.webm', '.mp4', '.mkv']:
                check_path = os.path.join(temp_dir, f'video{ext}')
                if os.path.exists(check_path):
                    return check_path, json.dumps(result)
            
            return None, json.dumps({"status": "error", "message": "Download failed - try another video"})
            
    except Exception as e:
        error_msg = str(e)
        if "private" in error_msg.lower():
            return None, json.dumps({"status": "error", "message": "This video is private or not accessible"})
        elif "login" in error_msg.lower():
            return None, json.dumps({"status": "error", "message": "Login required - only public videos work"})
        elif "not available" in error_msg.lower():
            return None, json.dumps({"status": "error", "message": "Video not available - it may be deleted"})
        else:
            return None, json.dumps({"status": "error", "message": error_msg[:150]})

# Gradio Interface
with gr.Blocks(
    title="Galmee - Facebook & Instagram Video Downloader",
    theme=gr.themes.Soft(primary_hue="green", secondary_hue="emerald"),
    css="""
    .galmee-header { text-align: center; padding: 20px; }
    .galmee-header h1 { font-size: 2.5em; font-weight: 800; background: linear-gradient(135deg, #009959, #00cc6a); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .download-btn { background: linear-gradient(135deg, #009959, #00cc6a) !important; border: none !important; font-weight: 700 !important; }
    """
) as demo:
    
    with gr.Column(elem_classes="galmee-header"):
        gr.HTML("""
        <div style="text-align:center; padding: 10px 0 20px;">
            <h1 style="font-size:2.2em; font-weight:800; margin-bottom:5px;">
                <span style="background:linear-gradient(135deg,#009959,#00cc6a); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">🎬 Galmee</span>
            </h1>
            <p style="color:#666; font-size:1.1em;">Facebook & Instagram Video Downloader</p>
            <p style="color:#999; font-size:0.9em;">Fast • Free • HD Quality • No Registration</p>
        </div>
        """)
    
    with gr.Row():
        with gr.Column(scale=4):
            url_input = gr.Textbox(
                label="📎 Video URL",
                placeholder="Paste Facebook or Instagram video link here...",
                lines=2,
                show_label=True
            )
    
    with gr.Row():
        download_btn = gr.Button(
            "⬇️ Download Video",
            variant="primary",
            size="lg",
            elem_classes="download-btn"
        )
    
    with gr.Row():
        video_output = gr.Video(
            label="📺 Your Video",
            height=400,
            show_label=True
        )
    
    info_output = gr.JSON(
        label="📋 Video Info",
        visible=True
    )
    
    download_btn.click(
        fn=download_video,
        inputs=[url_input],
        outputs=[video_output, info_output]
    )
    
    gr.HTML("""
    <div style="text-align:center; margin-top:20px; padding:15px; background:#f5f5f5; border-radius:10px;">
        <h3>📖 How to Use</h3>
        <p>1️⃣ Copy video link from Facebook or Instagram</p>
        <p>2️⃣ Paste it in the box above</p>
        <p>3️⃣ Click <strong>Download Video</strong></p>
        <p>4️⃣ Save to your device</p>
        <br>
        <p style="color:#e74c3c; font-size:0.85em;">⚠️ Only <strong>public</strong> videos can be downloaded</p>
        <br>
        <p style="color:#666;">Made with ❤️ by <strong>Yasin Gelma</strong> | Galmee Inc © 2026</p>
    </div>
    """)

if __name__ == "__main__":
    demo.launch()