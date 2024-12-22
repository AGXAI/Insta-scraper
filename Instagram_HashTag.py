import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests

def download_instagram_images():
    # Ask user for hashtag
    hashtag = input("Enter the Instagram hashtag you want to download images from: ")

    # Create a folder for the hashtag
    folder_name = f"#{hashtag}"
    os.makedirs(folder_name, exist_ok=True)

    # Set up Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the hashtag page
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    driver.get(url)

    # Wait for images to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))

    # Scroll to load more images
    for i in range(3):  # Adjust this number to load more or fewer images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Find all image elements
    img_elements = driver.find_elements(By.TAG_NAME, "img")

    # Extract image URLs
    img_urls = [img.get_attribute('src') for img in img_elements if 'scontent' in img.get_attribute('src')]

    print(f"Found {len(img_urls)} images for #{hashtag}")

    if len(img_urls) == 0:
        print("No images found. The hashtag might be empty or restricted.")
        driver.quit()
        return True

    # Ask user how many images to download
    num_to_download = int(input(f"How many images do you want to download (max {len(img_urls)})? "))

    # Download images
    for i, img_url in enumerate(img_urls[:num_to_download]):
        try:
            img_data = requests.get(img_url).content
            with open(os.path.join(folder_name, f'image_{i+1}.jpg'), 'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {i+1}/{num_to_download}")
            time.sleep(random.uniform(1, 3))  # Random delay to avoid being blocked
        except Exception as e:
            print(f"Error downloading image: {e}")

    print("You are all set!")

    driver.quit()

    # Ask if user wants to download more
    return input("Do you want to download another Instagram hash tagged images? (yes/no): ").lower() == 'yes'

# Main loop
while True:
    if not download_instagram_images():
        break

print("Thank you for using the Instagram image downloader!")