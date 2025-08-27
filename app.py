import requests
import streamlit as st
import yt_dlp

def download_youtube(url, format_option):
    ydl_opts = {
        "format": "bestaudio/best" if format_option == "MP3" else "bestvideo+bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info["url"]
        title = info.get("title", "youtube_video")

    return stream_url, title


# Streamlit app
st.title("🎬 YouTube Video & Audio Converter")

url = st.text_input("Enter YouTube URL")
format_option = st.radio("Select format", ("MP4", "MP3"))

if st.button("Start Conversion"):
    if url:
        with st.spinner("Fetching download link..."):
            try:
                stream_url, title = download_youtube(url, format_option)

                # Get file content into memory
                response = requests.get(stream_url, stream=True)
                filename = f"{title}.{ 'mp4' if format_option == 'MP4' else 'mp3'}"

                st.success("✅ Download ready!")

                st.download_button(
                    label="⬇️ Download File",
                    data=response.content,
                    file_name=filename,
                    mime="audio/mpeg" if format_option=="MP3" else "video/mp4"
                )

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a YouTube URL")
