import instaloader
import os

def download_instagram_images():
    L = instaloader.Instaloader(save_metadata=False, download_video_thumbnails=False, 
                                download_geotags=False, download_comments=False, 
                                post_metadata_txt_pattern='', download_videos=False)

    while True:
        # Step 1: Ask for Instagram username
        username = input("Enter the Instagram username to download images from: ")

        try:
            # Get profile and post count
            profile = instaloader.Profile.from_username(L.context, username)
            post_count = profile.mediacount

            # Step 2: Display number of posts to download
            print(f"Number of posts to process: {post_count}")

            # Step 3: Create folder for downloads
            folder_name = username
            os.makedirs(folder_name, exist_ok=True)

            # Download posts
            count = 0
            image_count = 0
            for post in profile.get_posts():
                count += 1
                if not post.is_video:
                    L.download_post(post, target=folder_name)
                    image_count += 1
                    print(f"Downloaded image {image_count} (post {count}/{post_count})")
                else:
                    print(f"Skipped video post {count}/{post_count}")

            # Step 4: Print completion message
            print(f"You are all set! Downloaded {image_count} images.")

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"The profile {username} does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Step 5: Ask if user wants to download another
        another = input("Do you want to download another Instagram page? (yes/no): ").lower()
        if another != 'yes':
            break

if __name__ == "__main__":
    download_instagram_images()