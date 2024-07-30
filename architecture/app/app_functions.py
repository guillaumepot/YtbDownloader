import json
from pytubefix import YouTube
from pytubefix.cli import on_progress
import traceback




def control_link(link:str) -> bool:
    """
    Check if the provided link is a valid YouTube URL.

    Args:
        link (str): The YouTube URL to be checked.

    Returns:
        bool: True if the link is valid, False otherwise.
    """
    if not link or not link.strip():
        print('ERROR!' + ' Please provide a valid YouTube URL')
        print(f'Bad link: "{link}"')
        return False

    if not link.startswith("https://www.youtube.com/") and not link.startswith("https://youtu.be/"):
        print('ERROR!' + ' Please provide a valid YouTube URL')
        print(f'Bad link: "{link}"')
        return False
    
    return True


def get_youtube_video_informations(link:str, file_type:str = "video") -> tuple:
    """
    Retrieves information about a YouTube video.

    Args:
        link (str): The URL of the YouTube video.

    Returns:
        tuple: A tuple containing a dictionary with the video information and the video stream.

    Raises:
        SomeException: Description of the exception raised.

    """
    video = YouTube(link, on_progress_callback = on_progress)

    if file_type == "video":
        stream = video.streams.get_highest_resolution()
    else:
        stream = video.streams.get_audio_only()

    filesize_in_mb = stream.filesize / 1024 / 1024  # Convert bytes to megabytes
    video_infos = {
        "title": video.title,
        "duration": video.length,
        "size": filesize_in_mb,
        "thumbnail": video.thumbnail_url
    }

    return video_infos, stream


def download_youtube_video(stream, file_type: str = "video") -> None:
    """
    Downloads a YouTube video or audio stream.

    Args:
        stream: The YouTube stream to download.
        audio_only: A boolean indicating whether to download only the audio (default: True).

    Raises:
        Exception: If an unexpected exception occurs during the download process.

    Returns:
        None
    """
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            output_folder = config["output_path"]

        if file_type == "video":
            stream.download(output_path=output_folder, mp3=False)
        else:
            stream.download(output_path=output_folder, mp3=True)


    except Exception as e:
        traceback.print_exc()
        print(f'ERROR! Unexpected exception occurred: {e}')