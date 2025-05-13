
import os
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress


from src.LoggerManager import LoggerManager


class YtbVideoDownloader():
    def __init__(self, video_source: str, url_path:str, output_dir:str, type:str):
        if type not in ['video', 'audio']:
            raise ValueError("Invalid type. Must be 'video' or 'audio'.")
        self.video_source = video_source
        self.url_path = url_path
        self.output_dir = output_dir
        self.type = type
        self.extension = '.mp4' if self.type == 'video' else '.mp3'
        self.logger = LoggerManager.configure_logger(name='YtbVideoDownloader', log_dir='./logs/', verbose=True)


        # Create the output directories if they do not exist
        if not os.path.exists(self.output_dir):
            self.logger.info(f"Creating output video directory: {self.output_dir}")
            os.makedirs(self.output_dir, exist_ok=True)
        if not os.path.exists(self.output_dir):
            self.logger.info(f"Creating output video directory: {self.output_dir}")
            os.makedirs(self.output_dir, exist_ok=True)


    def control_link(self, link:str) -> bool:
        """
        Check if the provided link is a valid YouTube URL.

        Args:
            link (str): The YouTube URL to be checked.

        Returns:
            bool: True if the link is valid, False otherwise.
        """
        if not link.startswith("https://www.youtube.com/") and not link.startswith("https://youtu.be/"):
            return False
        return True
    

    def check_duplicated_links(self, link:str) -> bool:
        """
        Check if the provided link already exists in the video URL file.

        Args:
            link (str): The YouTube URL to be checked.

        Returns:
            bool: True if the link is duplicated, False otherwise.
        """
        with open(self.url_path, 'r') as file:
            for line in file:
                if line.strip() == link:
                    
                    return True
        return False


    def get_youtube_video_data(self, link:str):
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
        stream = video.streams.get_highest_resolution() if self.type == 'video' else video.streams.get_audio_only()


        video_data = {
            "title": video.title,
            "duration": video.length,
            "size": stream.filesize / 1024 / 1024,
            "thumbnail": video.thumbnail_url,
            "stream": stream
        }

        return video_data    

    

    def download_videos(self) -> None:
        """
        Download videos from the provided YouTube URLs.

        Args:
            None

        Returns:
            None
        """

        # Load links
        if self.video_source == 'file':
            bad_links:list[str] = []
            links:list[str] = []
            duplicated_links_counter = 0
            with open(self.url_path, 'r') as file:
                for line in file:
                    link = line.strip()
                    if not self.control_link(link):
                        self.logger.error(f'Bad link: "{link}"')
                        bad_links.append(link)
                    elif link in links:
                        self.logger.warning(f'Duplicated link found: "{link}", skipping.')
                        duplicated_links_counter +=1
                    else:
                        links.append(link)

            # Download links
            for link in links:
                self.logger.info(f"Retrieving video data from: {link}")
                video_data = self.get_youtube_video_data(link)
                self.logger.info(f"Dowloading video: {video_data['title']}, duration: {video_data['duration']} seconds, size: {video_data['size']} MB")
                try:
                    video_data['stream'].download(output_path=self.output_dir, filename=video_data['title'] + self.extension)
                    self.logger.info("Video downloaded successfully")
                except Exception as e:
                    self.logger.error(f"Error downloading video: {video_data['title']}, Error: {e}")

            self.logger.info("Finished downloading files.")
            self.logger.warning(f"Skipped {duplicated_links_counter} duplicated links")
            self.logger.warning(f"Bad links: {'\n'.join(bad_links)}")


        elif self.video_source == 'playlist':
            pl = Playlist(self.url_path)
            for video in pl.videos:
                self.logger.info(f"Retrieving video data from: {video.watch_url}")
                video_data = self.get_youtube_video_data(video.watch_url)
                self.logger.info(f"Dowloading video: {video_data['title']}, duration: {video_data['duration']} seconds, size: {video_data['size']} MB")
                try:
                    video_data['stream'].download(output_path=self.output_dir, filename=video_data['title'] + self.extension)
                    self.logger.info("Video downloaded successfully")
                except Exception as e:
                    self.logger.error(f"Error downloading video: {video_data['title']}, Error: {e}")