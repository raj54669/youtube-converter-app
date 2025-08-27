import streamlit as st
import yt_dlp
from pathlib import Path
import os

# Page settings
st.set_page_config(page_title="YouTube Converter", page_icon="🎬", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #4A90E2;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 20px;
            color: #555;
        }
        .card {
            padding: 20px;
            border-radius: 15px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stDownloadButton > button {
            width: 100%;
            font-size: 1rem;
            padding: 12px;
            border-radius: 10px;
            background-color: #4A90E2 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title & subtitle
st.markdown('<div class="title">🎬 YouTube Video & Audio Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Convert YouTube videos into high-quality MP4 or MP3 with thumbnails & metadata</div>', unsafe_allow_html=True)

# Input section
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    url = st.text_input("🔗 Enter YouTube URL")

    format_choice = st.radio("🎚 Select format", ("🎬 MP4 (Video)", "🎵 MP3 (Audio)"))

    if "MP4" in format_choice:
        quality_choice = st.selectbox("📹 Select video quality", ["360p", "480p", "720p", "1080p", "Best"])
    else:
        quality_choice = st.selectbox("🎵 Select audio quality", ["128 kbps", "192 kbps", "320 kbps"])

    start_button = st.button("🚀 Start Conversion")

    st.markdown('</div>', unsafe_allow_html=True)

# Output path
output_path = Path("downloads")
output_path.mkdir(exist_ok=True)

if start_button and url:
    st.info("⏳ Processing... Please wait!")

    try:
        file_template = str(output_path / '%(title)s.%(ext)s')
        cookies_file = "cookies.txt" if os.path.exists("cookies.txt") else None

        base_opts = {
            "outtmpl": file_template,
            "noplaylist": True,
            "cookiefile": cookies_file,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
            },
        }

        # Decide format string
        if "MP4" in format_choice:
            quality_map = {
                "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "best": "bestvideo+bestaudio/best"
            }
            ydl_opts = {
                **base_opts,
                "format": quality_map[quality_choice],
                "merge_output_format": "mp4",
                "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
            }

        else:  # MP3
            quality_map = {
                "128 kbps": "128",
                "192 kbps": "192",
                "320 kbps": "320",
            }
            ydl_opts = {
                **base_opts,
                "format": "bestaudio/best",
                "postprocessors": [
                    {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": quality_map[quality_choice]},
                    {"key": "FFmpegMetadata"},
                    {"key": "EmbedThumbnail"},
                ],
                "writethumbnail": True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if "MP3" in format_choice:
                filename = filename.rsplit(".", 1)[0] + ".mp3"
            else:
                filename = filename.rsplit(".", 1)[0] + ".mp4"

        st.success("✅ Conversion complete!")

        with open(filename, "rb") as f:
            st.download_button("⬇️ Download File", f, file_name=os.path.basename(filename))

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
