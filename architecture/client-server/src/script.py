import os
import math
import traceback
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import AudioFileClip


# Define storage paths
audio_storage = os.getenv("AUDIO_PATH")
video_storage = os.getenv("VIDEO_PATH")

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 
    percentage_of_completion = math.floor((bytes_downloaded / total_size) * 100)
    print(f'Downloading: {percentage_of_completion}% complete', end='\r')


def control_link(link) -> None:
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


def check_file_exists(filepath) -> None:
    """
    Check if a file already exists at the given path.

    Parameters:
    output_file_path (str): The path to the file to be checked.

    Raises:
    FileExistsError: If a file already exists at the given path.
    """
    if os.path.exists(filepath):
        print(f'ERROR! File already exists at "{filepath}" and we don\'t want to accidentally overwrite it')
        raise FileExistsError()
    else:
        pass


def convert_to_audio(input_file):
    """
    Converts a video file to an audio file.

    Args:
        output_folder (str): The path to the output folder where the audio file will be saved.

    Returns:
        None

    Raises:
        FileNotFoundError: If the video file specified by `output_folder` does not exist.

    """
    # Ensure the output file is an .mp3 file
    output_file = os.path.splitext(input_file)[0] + '.mp3'
    
    try:
        with AudioFileClip(input_file) as audio_clip:
            audio_clip.write_audiofile(output_file, codec='mp3', verbose=True, logger=None)
        print(f'SUCCESS! Converted to audio: "{output_file}"')
        os.remove(input_file)
    except Exception as e:
        print(f'ERROR! Failed to convert to audio: {e}')


def download_media(youtube, output_folder, audio=False):
    """
    Downloads a video or audio from YouTube using the provided YouTube object.

    Args:
        youtube (YouTube): The YouTube object representing the video to download.
        output_folder (str): The path to the folder where the downloaded media will be saved.
        audio (bool, optional): Specifies whether to download the audio only. Defaults to False.

    Raises:
        Exception: If an unexpected exception occurs during the download process.

    Returns:
        None
    """
    try:
        # Get Video
        media = youtube.streams.get_audio_only() if audio else youtube.streams.get_highest_resolution()

        # Register the progress callback
        youtube.register_on_progress_callback(progress_function)

        filename = media.download(output_path=output_folder)
        print(f'SUCCESS! Downloaded {"audio" if audio else "video"} from "{youtube.watch_url}" to "{output_folder}"')
        

        # Convert if audio
        if audio == True:    
            convert_to_audio(filename)

        else:
            pass


    except Exception as e:
        traceback.print_exc()
        print(f'ERROR! Unexpected exception occurred: {e}')


def get_file(link, name, audio=False):
    """
    Downloads a file from a given YouTube link.

    Args:
        link (str): The YouTube link of the video.
        name (str): The name of the file.
        audio (bool, optional): Specifies whether to download the audio only. Defaults to False.

    Returns:
        None

    Raises:
        None
    """
    # Control the link
    check_link = control_link(link)
    if check_link == False:
        return print("Modifier mauvais lien(s)")
    
    # Get youtube object from link
    youtube = YouTube(link, on_progress_callback = on_progress)

    
    # Check if file exists
    title = str(youtube.title)
    title = title.lower().replace(' ', '_')

    output_file_path = audio_storage if audio==True else video_storage
    filepath = os.path.join(output_file_path, title, '.mp3' if audio else '.mp4')
    check_file_exists(filepath)

    # Download Media
    download_media(youtube, output_folder = output_file_path, audio=audio)