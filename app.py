import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Converter", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Video & Audio Converter")

url = st.text_input("Enter YouTube URL")
format_choice = st.radio("Select format", ("MP4", "MP3"))
start = st.button("Start Conversion")

if start and url:
    st.info("Processing... Please wait!")

    try:
        file_name = "output.mp3" if format_choice == "MP3" else "output.mp4"
        if os.path.exists(file_name):
            os.remove(file_name)

        # ✅ Try to use cookies if available
        cookie_file = "cookies.txt" if os.path.exists("cookies.txt") else None

        ydl_opts = {
            "outtmpl": file_name,
            "noplaylist": True,
            "writethumbnail": True,
            "format": "bestaudio/best" if format_choice == "MP3" else "bestvideo+bestaudio/best",
        }

        if cookie_file:
            ydl_opts["cookiefile"] = cookie_file   # ✅ Use cookies.txt automatically

        if format_choice == "MP3":
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                {"key": "EmbedThumbnail"},
                {"key": "FFmpegMetadata"},
            ]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        st.success("✅ Download complete!")

        with open(file_name, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {format_choice}",
                data=f,
                file_name=file_name,
                mime="audio/mpeg" if format_choice == "MP3" else "video/mp4",
            )

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
