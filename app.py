import streamlit as st
import yt_dlp

st.set_page_config(page_title="YouTube Converter", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Video & Audio Converter")

url = st.text_input("Enter YouTube URL")

format_option = st.radio("Select format", ("MP4", "MP3"))

if st.button("Get Download Link") and url:
    st.info("Fetching video info...")

    try:
        ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title", "Unknown Title")
        thumbnail = info.get("thumbnail")
        uploader = info.get("uploader", "Unknown Channel")
        duration = info.get("duration", 0)

        # choose stream url
        if format_option == "MP4":
            stream_url = info["url"]  # direct video+audio stream
        else:  # MP3 case → best audio-only stream
            audio_format = next((f for f in info["formats"] if f.get("acodec") != "none"), None)
            stream_url = audio_format["url"] if audio_format else None

        # Show metadata
        st.subheader(title)
        st.write(f"Uploader: **{uploader}**")
        st.write(f"Duration: {duration // 60}:{duration % 60:02d}")
        if thumbnail:
            st.image(thumbnail, width=300)

        # Show direct download link
        if stream_url:
            st.success("✅ Direct download link ready!")
            st.markdown(f"[Click here to download]({stream_url})", unsafe_allow_html=True)
        else:
            st.error("Could not get stream URL.")

        # Show yt-dlp local command for proper MP3 with metadata
        st.subheader("Convert to MP3 with metadata & thumbnail (Run locally):")
        st.code(
            f'yt-dlp -x --audio-format mp3 --embed-thumbnail --add-metadata "{url}"',
            language="bash"
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")
