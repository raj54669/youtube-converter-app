import streamlit as st
import yt_dlp
import os
from pathlib import Path

def download_video(url, format_choice):
    output_path = Path("downloads")
    output_path.mkdir(exist_ok=True)

    ydl_opts = {
        'cookiefile': 'cookies.txt',  # ✅ force using cookies
        'format': 'bestaudio/best' if format_choice == "mp3" else 'best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'merge_output_format': format_choice,
        'http_headers': {   # ✅ mimic browser headers
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    if format_choice == "mp3":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_choice == "mp3":
                filename = os.path.splitext(filename)[0] + ".mp3"
            return filename
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("🎬 YouTube Video & Audio Converter")

url = st.text_input("Enter YouTube URL")
format_choice = st.radio("Select format", ("mp4", "mp3"))
if st.button("Start Conversion"):
    if url:
        with st.spinner("Processing... Please wait!"):
            file_path = download_video(url, format_choice)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.download_button("Download File", f, file_name=os.path.basename(file_path))
            else:
                st.error(f"Error: {file_path}")
    else:
        st.warning("Please enter a valid YouTube URL")
