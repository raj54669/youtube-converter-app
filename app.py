import streamlit as st
import yt_dlp
import tempfile
import os

# -----------------------------
# Download function using yt-dlp
# -----------------------------
def download_video(url, format_choice):
    # Create a temporary file for download
    suffix = ".mp3" if format_choice == "MP3" else ".mp4"
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    file_path = temp_file.name
    temp_file.close()

    # yt-dlp options
    ydl_opts = {
        'outtmpl': file_path,
        'format': 'bestaudio/best' if format_choice == "MP3" else 'bestvideo+bestaudio/best',
        'quiet': True,
    }

    # Add postprocessing for MP3
    if format_choice == "MP3":
        ydl_opts.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Unknown Title')
        description = info.get('description', '')
        thumbnail_url = info.get('thumbnail', '')

    return file_path, title, description, thumbnail_url


# -----------------------------
# Streamlit App UI
# -----------------------------
def main():
    st.set_page_config(page_title="YouTube Converter", page_icon="🎥", layout="centered")

    st.title("🎬 YouTube Video & Audio Converter")

    url = st.text_input("Enter YouTube URL")

    format_choice = st.radio("Select format", ("MP4", "MP3"))

    if st.button("Start Conversion"):
        if not url:
            st.error("Please enter a valid YouTube URL")
        else:
            try:
                with st.spinner("Downloading..."):
                    file_path, title, description, thumbnail_url = download_video(url, format_choice)

                # Show video info
                st.success("Download completed!")
                st.subheader(title)

                if thumbnail_url:
                    st.image(thumbnail_url, use_column_width=True)

                st.write(description)

                # Provide download button
                with open(file_path, "rb") as f:
                    btn = st.download_button(
                        label=f"⬇️ Download {format_choice}",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="audio/mpeg" if format_choice == "MP3" else "video/mp4"
                    )

            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
