import os
import requests
from urllib.parse import quote_plus

def download_unsplash_images():
    # Ask user for Unsplash API key
    api_key = input("Please enter your Unsplash Access key: ")

    # Ask user for search query
    query = input("Enter the search term for images you want to download: ")

    # Create a folder for the search query
    folder_name = query.replace(" ", "_")
    os.makedirs(folder_name, exist_ok=True)

    # Construct the API URL
    base_url = "https://api.unsplash.com/search/photos"
    url = f"{base_url}?query={quote_plus(query)}&client_id={api_key}&per_page=30"

    # Send GET request to the API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        total_images = data['total']
        available_images = len(data['results'])

        print(f"Found {total_images} images in total. {available_images} images available for download.")

        # Ask user how many images to download
        num_to_download = int(input(f"How many images do you want to download (max {available_images})? "))
        num_to_download = min(num_to_download, available_images)

        # Download images
        for i, img_data in enumerate(data['results'][:num_to_download]):
            img_url = img_data['urls']['full']
            try:
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(os.path.join(folder_name, f'image_{i+1}.jpg'), 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded {i+1}/{num_to_download}")
                else:
                    print(f"Failed to download image {i+1}")
            except Exception as e:
                print(f"Error downloading image {i+1}: {e}")

        print("You are all set!")
    else:
        print(f"Failed to fetch images. Status code: {response.status_code}")
        if response.status_code == 401:
            print("Please check if your API key is correct.")

    # Ask if user wants to download more
    return input("Do you want to download more images? (yes/no): ").lower() == 'yes'

# Main loop
while True:
    if not download_unsplash_images():
        break

print("Thank you for using the Unsplash image downloader!")