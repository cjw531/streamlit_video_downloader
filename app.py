import streamlit as st
import subprocess
import time
import os

def download_youtube_clip(url, start_time, end_time, output_filename="clip.mp4"):
    """
    Downloads a YouTube video clip using yt-dlp with enhanced quality settings.
    """
    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "--merge-output-format", "mp4",
        "-o", output_filename,
        "--download-sections", f"*{start_time}-{end_time}",
        "--format-sort", "resolution,codec:avc",
        "--prefer-free-formats",
        url
    ]
    
    progress_bar = st.progress(0)
    progress_placeholder = st.empty()

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    i = 0
    while process.poll() is None:
        time.sleep(0.5)  # Update progress every 0.5 seconds
        i = min(i + 5, 100)  # Increment progress gradually
        progress_bar.progress(i)
        progress_placeholder.text(f"Fetching... {i}%")

    progress_bar.progress(100)
    progress_placeholder.text("Done")
    
    if process.returncode == 0:
        st.success(f"Video extraction completed: {output_filename}")

        with open(output_filename, "rb") as file:
            st.download_button(
                label="Download Video",
                data=file,
                file_name=os.path.basename(output_filename),
                mime="video/mp4"
            )
        
        st.video(output_filename)  # Show video preview
    else:
        st.error("Error downloading video.")


st.title("YouTube Clip Downloader")

st.header("1. Enter YouTube Video URL")
url = st.text_input(label="Enter YouTube Video URL")

st.header("2. Set Timeframe")
col1, col2 = st.columns(2)
start_time = col1.text_input(label="Start Time (HH:MM:SS or seconds)")
end_time = col2.text_input(label="End Time (HH:MM:SS or seconds)")

st.header("3. Extract Video Clip")
if st.button("Extract Clip"):
    if url and start_time and end_time:
        download_youtube_clip(url, start_time, end_time)
    else:
        st.warning("Please fill in all fields.")
