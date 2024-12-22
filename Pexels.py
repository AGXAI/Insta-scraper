import os
import requests
from urllib.parse import quote_plus

def download_pexels_media():
    # Ask user for Pexels API key
    api_key = input("Please enter your Pexels API key: ")

    # Ask user for search query
    query = input("Enter the search term for images and videos you want to download: ")

    # Create folders for the search query
    base_folder = query.replace(" ", "_")
    image_folder = os.path.join(base_folder, "images")
    video_folder = os.path.join(base_folder, "videos")
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(video_folder, exist_ok=True)

    # Construct the API URLs
    base_url = "https://api.pexels.com/v1/search"
    image_url = f"{base_url}?query={quote_plus(query)}&per_page=80"
    video_url = f"https://api.pexels.com/videos/search?query={quote_plus(query)}&per_page=80"

    headers = {"Authorization": api_key}

    # Function to download media
    def download_media(url, folder, file_name):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(folder, file_name), 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        return False

    # Function to process API response
    def process_response(url, media_type):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            total_media = data['total_results']
            available_media = len(data[media_type])
            print(f"Found {total_media} {media_type} in total. {available_media} {media_type} available for download.")
            num_to_download = int(input(f"How many {media_type} do you want to download (max {available_media})? "))
            num_to_download = min(num_to_download, available_media)

            for i, item in enumerate(data[media_type][:num_to_download]):
                if media_type == 'photos':
                    url = item['src']['original']
                    file_name = f'image_{i+1}.jpg'
                    folder = image_folder
                else:  # videos
                    url = max(item['video_files'], key=lambda x: x['width'])['link']
                    file_name = f'video_{i+1}.mp4'
                    folder = video_folder

                if download_media(url, folder, file_name):
                    print(f"Downloaded {media_type[:-1]} {i+1}/{num_to_download}")
                else:
                    print(f"Failed to download {media_type[:-1]} {i+1}")
        else:
            print(f"Failed to fetch {media_type}. Status code: {response.status_code}")
            if response.status_code == 401:
                print("Please check if your API key is correct.")

    # Download images and videos
    process_response(image_url, 'photos')
    process_response(video_url, 'videos')

    print("You are all set!")

    # Ask if user wants to download more
    return input("Do you want to download again? (yes/no): ").lower() == 'yes'

# Main loop
while True:
    if not download_pexels_media():
        break

print("Thank you for using the Pexels media downloader!")