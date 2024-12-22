from pytube import YouTube

def download_youtube_video():
    # Ask the user for the YouTube video link
    video_url = input("Enter the YouTube video link: ")
    
    # Create a YouTube object
    yt = YouTube(video_url)
    
    # Get all the available video streams
    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    
    # List all available resolutions
    print("Available video resolutions:")
    for i, stream in enumerate(streams):
        print(f"{i + 1}. {stream.resolution}")
    
    # Ask the user to select a resolution
    choice = int(input("Enter the number of the desired resolution: "))
    
    # Get the selected stream
    selected_stream = streams[choice - 1]
    
    # Download the video
    print(f"Downloading {yt.title} in {selected_stream.resolution} resolution...")
    selected_stream.download()
    print("Download complete!")

if __name__ == "__main__":
    download_youtube_video()
