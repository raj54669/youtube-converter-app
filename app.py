import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Video & Audio Converter", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Video & Audio Converter")

# Input URL
url = st.text_input("Enter YouTube URL")

# Select format
format_option = st.radio("Select format", ["MP4", "MP3"])

if st.button("Start Conversion"):
    if url:
        st.info("Downloading...")

        try:
            common_opts = {
                "outtmpl": "%(title)s.%(ext)s",
                "prefer_ffmpeg": True,
                "ffmpeg_location": "/usr/bin",
                "nocheckcertificate": True,   # 👈 bypass SSL issues
                "force_ipv4": True,           # 👈 force IPv4
                "retries": 5,                 # 👈 retry if failed
                "http_headers": {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/112.0.0.0 Safari/537.36"
                    )
                }
            }

            if format_option == "MP3":
                ydl_opts = {
                    **common_opts,
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                }

            else:  # MP4
                ydl_opts = {
                    **common_opts,
                    "format": "bestvideo+bestaudio/best",
                    "merge_output_format": "mp4",
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                if format_option == "MP3":
                    filename = filename.rsplit(".", 1)[0] + ".mp3"
                else:
                    filename = filename.rsplit(".", 1)[0] + ".mp4"

                st.success("✅ Download finished!")
                with open(filename, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download {format_option}",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="audio/mpeg" if format_option == "MP3" else "video/mp4"
                    )

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
