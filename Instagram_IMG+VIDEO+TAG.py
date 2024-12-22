import instaloader
import os

def sanitize_filename(filename):
    # Remove characters that are invalid in filenames
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def download_instagram_content():
    L = instaloader.Instaloader(save_metadata=False, download_video_thumbnails=False, 
                                download_geotags=False, download_comments=False, 
                                post_metadata_txt_pattern='')

    while True:
        # Step 1: Ask for Instagram username
        username = input("Enter the Instagram username to download content from: ")

        try:
            # Get profile and post count
            profile = instaloader.Profile.from_username(L.context, username)
            post_count = profile.mediacount

            # Step 2: Display number of posts to download
            print(f"Number of posts to download: {post_count}")

            # Step 3: Create folder for downloads
            folder_name = username
            os.makedirs(folder_name, exist_ok=True)

            # Download posts
            count = 0
            for post in profile.get_posts():
                count += 1
                print(f"Downloading post {count}/{post_count}")

                # Download the post (image or video)
                L.download_post(post, target=folder_name)

                # Download description
                if post.caption:
                    # Sanitize the title for use as a filename
                    title = sanitize_filename(post.caption.split('\n')[0])[:50]  # Use first line, max 50 chars
                    if not title:
                        title = f"post_{post.date_utc:%Y-%m-%d_%H-%M-%S}"
                    
                    description_filename = os.path.join(folder_name, f"{title}.txt")
                    with open(description_filename, 'w', encoding='utf-8') as f:
                        f.write(post.caption)

            # Step 4: Print completion message
            print("You are all set!")

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"The profile {username} does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Step 5: Ask if user wants to download another
        another = input("Do you want to download another Instagram page? (yes/no): ").lower()
        if another != 'yes':
            break

if __name__ == "__main__":
    download_instagram_content()