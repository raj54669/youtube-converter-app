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
            if format_option == "MP3":
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'postprocessor_args': [
                        '-ar', '44100',   # set sample rate
                        '-ac', '2'        # set audio channels
                    ],
                    'prefer_ffmpeg': True,
                    'ffmpeg_location': '/usr/bin',  # Streamlit Cloud ffmpeg path
                }

            else:  # MP4
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': '%(title)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    'prefer_ffmpeg': True,
                    'ffmpeg_location': '/usr/bin',
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                if format_option == "MP3":
                    filename = filename.rsplit(".", 1)[0] + ".mp3"
                else:
                    filename = filename.rsplit(".", 1)[0] + ".mp4"

                st.success("Download finished! ✅")
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
