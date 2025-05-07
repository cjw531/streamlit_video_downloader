import streamlit as st
import subprocess
import time
import os

def download_youtube_clip(url, start_time, end_time, output_filename="clip.mp4"):
    """
    Downloads a YouTube video clip using yt-dlp with enhanced quality settings.
    
    Args:
        url (str): YouTube video URL.
        start_time (str): Start time in HH:MM:SS or seconds.
        end_time (str): End time in HH:MM:SS or seconds.
        output_filename (str): Name of the output file (ensure .mp4 extension).
    """
    command = [
        "yt-dlp",
        # "--list-formats",
        # "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", output_filename,
        "--download-sections", f"*{start_time}-{end_time}",
        "--format-sort", "resolution,codec:avc",
        # "--prefer-free-formats",
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

# st.warning("경고: \
#            다운로드 받은 동영상의 저작권 및 모든 관련 권리는 해당 크리에이터에게 귀속됩니다. \
#            본 도구를 통해 획득한 영상을 무단 배포, 복제 또는 공개 공유하는 행위는 관련 저작권법을 위반할 수 있습니다. \
#            관련법 위반에 따라 발생하는 모든 법적 책임은 전적으로 이용자에게 있습니다.")

# st.markdown("YouTube 구간 다운로더에 오신 것을 환영합니다! YouTube 동영상 URL을 입력하고, 다운로드할 구간을 지정하세요.")

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
