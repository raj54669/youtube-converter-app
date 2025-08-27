import streamlit as st
import yt_dlp
from pathlib import Path
import os

st.set_page_config(page_title="YouTube Converter", page_icon="🎬", layout="centered")
st.title("🎬 YouTube Video & Audio Converter")

url = st.text_input("Enter YouTube URL")
format_choice = st.radio("Select format", ("mp4", "mp3"))
start_button = st.button("Start Conversion")

output_path = Path("downloads")
output_path.mkdir(exist_ok=True)

if start_button and url:
    st.info("⏳ Processing... Please wait!")

    try:
        file_template = str(output_path / '%(title)s.%(ext)s')

        # Use cookies.txt if exists, else try browser-cookie3 (Google Chrome)
        cookies_file = "cookies.txt" if os.path.exists("cookies.txt") else None

        ydl_opts = {
            "outtmpl": file_template,
            "noplaylist": True,
            "merge_output_format": format_choice,
            "cookiefile": cookies_file,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
            },
            "extractor_args": {
                "youtube": {"player_client": ["android"]}
            }
        }

        if format_choice == "mp3":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [
                    {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
                    {"key": "FFmpegMetadata"},
                    {"key": "EmbedThumbnail"},
                ],
                "writethumbnail": True,
            })
        else:
            ydl_opts.update({
                "format": "bestvideo+bestaudio/best",
                "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_choice == "mp3":
                filename = filename.rsplit(".", 1)[0] + ".mp3"
            else:
                filename = filename.rsplit(".", 1)[0] + ".mp4"

        st.success("✅ Conversion complete!")
        with open(filename, "rb") as f:
            st.download_button("⬇️ Download File", f, file_name=os.path.basename(filename))

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
