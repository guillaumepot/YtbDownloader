import os

from src.LoggerManager import LoggerManager
from src.YtbVideoDownloader import YtbVideoDownloader


def main():
    # Set Logger
    logger = LoggerManager.configure_logger(name='script', verbose=True)

    # Get URL file path & set downloader
    print("Download video from file or playlist ?")
    print("1. File")
    print("2. Playlist")

    while True:
        try:
            choice = int(input("Choice: "))
            if choice in [1, 2]:
                video_source = 'file' if choice == 1 else 'playlist'
                break
            else:
                print("Invalid choice, please choose 1 or 2.")
        except ValueError:
            print("Invalid input, please enter a number (1 or 2).")




    url_path = input("Enter the path or url to the video URL file: ")
    if video_source == 'file' and not os.path.exists(video_source):
        logger.error(f"File {video_source} does not exist.")
        exit(1)



    print("Download video or audio only?")
    print("1. Video")
    print("2. Audio")

    while True:
        try:
            choice = int(input("Choice: "))
            if choice in [1, 2]:
                output_dir = './storage/videos' if choice == 1 else './storage/audios'
                type = 'video' if choice == 1 else 'audio'
                break
            else:
                print("Invalid choice, please choose 1 or 2.")
        except ValueError:
            print("Invalid input, please enter a number (1 or 2).")



    downloader = YtbVideoDownloader(
        video_source = video_source,
        url_path = url_path,
        output_dir = output_dir,
        type = type
        )

    downloader.download_videos()



if __name__ == "__main__":
    main()