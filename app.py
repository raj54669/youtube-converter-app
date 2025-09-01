import streamlit as st
import yt_dlp
from pathlib import Path
import os
import uuid

# Page config
st.set_page_config(page_title="YouTube Converter", page_icon="🎬", layout="centered")

# Download directory
output_path = Path("downloads")
output_path.mkdir(exist_ok=True)

# Title
st.markdown(
    "<h2 style='text-align:center; color:#4A90E2;'>🎬 YouTube Video & Audio Converter</h2>",
    unsafe_allow_html=True,
)

url = st.text_input("🔗 Enter YouTube URL")
format_choice = st.radio("🎚 Select format", ("MP4", "MP3"))
quality = st.selectbox("🎵 Select quality", ["128", "192", "320"] if format_choice == "MP3" else ["360p", "480p", "720p", "1080p", "best"])

if st.button("🚀 Start Conversion") and url:
    st.info("⏳ Processing... Please wait!")
    try:
        # unique filename
        unique_id = str(uuid.uuid4())
        file_template = str(output_path / f"{unique_id}.%(ext)s")

        cookies_file = "cookies.txt" if os.path.exists("cookies.txt") else None

        base_opts = {
            "outtmpl": file_template,
            "noplaylist": True,
            "cookies": cookies_file,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
            "extractor_args": {"youtube": {"player_client": ["web"]}},
        }

        if format_choice == "MP3":
            ydl_opts = {
                **base_opts,
                "format": "bestaudio/best",
                "postprocessors": [
                    {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": quality},
                    {"key": "FFmpegMetadata"},
                    {"key": "EmbedThumbnail"},
                ],
                "writethumbnail": True,
            }
        else:  # MP4
            quality_map = {
                "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "best": "bestvideo+bestaudio/best"
            }
            ydl_opts = {
                **base_opts,
                "format": quality_map[quality],
                "merge_output_format": "mp4",
                "postprocessors": [
                    {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
                ],
            }

        # Run yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if format_choice == "MP3":
                filename = filename.rsplit(".", 1)[0] + ".mp3"
            else:
                filename = filename.rsplit(".", 1)[0] + ".mp4"

        # Show success
        st.success("✅ Conversion complete!")

        # Provide download
        with open(filename, "rb") as f:
            st.download_button("⬇️ Download File", f, file_name=os.path.basename(filename))

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
