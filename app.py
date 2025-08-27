import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip
import requests
from io import BytesIO
from PIL import Image
import shutil
import os
import tempfile
import ffmpeg

# Function to get video metadata (title, description, thumbnail)
def get_video_metadata(url):
    try:
        yt = YouTube(url)
        title = yt.title
        description = yt.description
        thumbnail_url = yt.thumbnail_url
        return yt, title, description, thumbnail_url
    except Exception as e:
        st.error(f"Error: Unable to fetch video details. {str(e)}")
        return None, None, None, None

# Function to download video/audio based on user choice
def download_video(url, format_choice):
    yt, title, description, thumbnail_url = get_video_metadata(url)
    
    if format_choice == "MP4":
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            file_path = temp_file.name
            stream.download(filename=file_path)
    elif format_choice == "MP3":
        stream = yt.streams.filter(only_audio=True).first()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            file_path = temp_file.name
            stream.download(filename=file_path)
    
    return file_path, title, description, thumbnail_url

# Function to embed metadata and thumbnail into the MP4 file
def embed_metadata_and_thumbnail(mp4_file_path, title, description, thumbnail_url):
    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save("thumbnail.jpg")

        # Process the video file and add metadata
        clip = VideoFileClip(mp4_file_path)
        clip.write_videofile("output_with_metadata.mp4", codec="libx264", audio_codec="aac", metadata={"title": title, "description": description})

        # Embed the thumbnail into the MP4 file using ffmpeg
        ffmpeg.input("output_with_metadata.mp4").output("final_video.mp4", vcodec='libx264', acodec='aac', metadata="title={}".format(title)).run()
        return "final_video.mp4"
    except Exception as e:
        st.error(f"Error embedding metadata: {str(e)}")
        return None

# Function to embed metadata into MP3 file
def embed_mp3_metadata(mp3_file_path, title, description):
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(mp3_file_path)
        audio.export(mp3_file_path, format="mp3", tags={"title": title, "artist": description})
        return mp3_file_path
    except Exception as e:
        st.error(f"Error embedding MP3 metadata: {str(e)}")
        return None

# Streamlit App UI
def main():
    st.title("YouTube Video & Audio Converter")

    url = st.text_input("Enter YouTube URL", "")
    format_choice = st.radio("Select format", ("MP4", "MP3"))

    if st.button("Start Conversion") and url:
        with st.spinner("Downloading and Converting..."):
            # Download video/audio and extract metadata
            file_path, title, description, thumbnail_url = download_video(url, format_choice)

            # Embed metadata and thumbnail for MP4 files
            if format_choice == "MP4":
                output_file = embed_metadata_and_thumbnail(file_path, title, description, thumbnail_url)
            elif format_choice == "MP3":
                output_file = embed_mp3_metadata(file_path, title, description)

            if output_file:
                st.success("Conversion Completed!")
                st.markdown(f"[Download {format_choice} File](./{output_file})")
                
                # Clean up temporary files after serving them
                shutil.move(output_file, "/assets/")
                os.remove(file_path)
                os.remove("thumbnail.jpg")
            else:
                st.error("Conversion failed")

if __name__ == "__main__":
    main()
