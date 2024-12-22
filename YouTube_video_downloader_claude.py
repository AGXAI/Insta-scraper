from pytube import YouTube
import os

def download_youtube_video():
    # Ask the user for the YouTube video link
    video_url = input("Please enter the YouTube video link: ")

    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get available streams
        streams = yt.streams.filter(progressive=True, file_extension='mp4')

        # List available resolutions
        print("\nAvailable resolutions:")
        for i, stream in enumerate(streams, 1):
            print(f"{i}. {stream.resolution}")

        # Ask user to select resolution
        while True:
            try:
                choice = int(input("\nEnter the number of the resolution you want to download: "))
                if 1 <= choice <= len(streams):
                    selected_stream = streams[choice - 1]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        # Get the current working directory
        current_dir = os.getcwd()

        # Download the video
        print(f"\nDownloading: {yt.title}")
        selected_stream.download(output_path=current_dir)
        print(f"\nDownload complete! Video saved in: {current_dir}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    download_youtube_video()