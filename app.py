import streamlit as st
import yt_dlp
import os

def download_youtube(url, format_option):
    """Download and convert YouTube video/audio with metadata + thumbnail."""
    filename = "output.%(ext)s"
    ydl_opts = {
        "format": "bestaudio/best" if format_option == "MP3" else "bestvideo+bestaudio/best",
        "outtmpl": filename,
        "noplaylist": True,
        "writethumbnail": True,  # download thumbnail
    }

    if format_option == "MP3":
        ydl_opts["postprocessors"] = [
            {  # convert to mp3
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {  # embed thumbnail into mp3
                "key": "EmbedThumbnail"
            },
            {  # write metadata (title, artist, etc.)
                "key": "FFmpegMetadata"
            }
        ]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "youtube_video")
        ext = "mp3" if format_option == "MP3" else "mp4"
        filename = f"output.{ext}"

    return filename, title, ext


# ---------------- Streamlit UI ----------------

st.title("🎬 YouTube Video & Audio Converter")

url = st.text_input("Enter YouTube URL")
format_option = st.radio("Select format", ("MP4", "MP3"))

if st.button("Start Conversion"):
    if url:
        with st.spinner("Downloading & processing..."):
            try:
                filename, title, ext = download_youtube(url, format_option)

                with open(filename, "rb") as f:
                    st.download_button(
                        label="⬇️ Download File",
                        data=f,
                        file_name=f"{title}.{ext}",
                        mime="audio/mpeg" if ext == "mp3" else "video/mp4",
                    )

                os.remove(filename)  # clean temp file

                st.success("✅ File ready for download!")

            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a YouTube URL")
