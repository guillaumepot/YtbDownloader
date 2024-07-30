from app_functions import control_link, get_youtube_video_informations, download_youtube_video
from io import BytesIO
import json
import os
from PIL import Image, ImageTk
import requests
import tkinter as tk
from tkinter import messagebox, filedialog


# Define the function to set the output path
def set_output_path():
    # Open a file dialog to select a directory
    output_path = filedialog.askdirectory()
    if output_path:
        # Save the selected path to a configuration file
        config = {"output_path": output_path}
        with open("config.json", "w") as config_file:
            json.dump(config, config_file)
        messagebox.showinfo("Configuration", f"Output path set to: {output_path}")


def get_video_datas(file_type) -> None:
    """
    Retrieves video information from a YouTube URL and displays it in the application.

    This function gets the URL from the entry field, validates it, and then retrieves the video information
    such as title, duration, size, and thumbnail URL. It then displays the video information and thumbnail image
    in the application window. Finally, it creates a download button for the video.

    Raises:
        Exception: If an error occurs while getting the video data.

    """

    # Get the URL from the entry field
    url = url_entry.get()

    # Control if link is the correct format (youtube)
    valid_link = control_link(url)
    if not valid_link:
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return

    try:
        videos_infos, stream = get_youtube_video_informations(url, file_type)

        # Extract video information
        title = videos_infos["title"]
        duration = videos_infos["duration"]
        size = videos_infos["size"]
        thumbnail_url = videos_infos["thumbnail"]

        # Display the video information
        video_info_display.config(text=f"Title: {title} \n\n"
                            f"Duration: {duration} seconds \n\n"
                            f"Size: {size:.2f} MB")

        # Download and display the thumbnail image
        response = requests.get(thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo


        # Create and place the download button
        download_button = tk.Button(root, text="Download", command=lambda: download_video(stream, download_option.get()), font=("Helvetica", 12))
        download_button.grid(row=5, column=2, columnspan=2, pady=10)


    except Exception as e:
        status_label.config(text="Error occurred while getting video datas.")
        messagebox.showerror("Error", str(e))



def download_video(stream, file_type:str) -> None:
    """
    Downloads a video from YouTube using the provided stream.

    Args:
        stream: The YouTube stream object representing the video to be downloaded.

    Returns:
        None

    Raises:
        Exception: If an error occurs while downloading the video.

    """

    print("fletype:", file_type)
    try:
        status_label.config(text="Downloading...")
        download_youtube_video(stream, file_type)
        status_label.config(text="Download complete!")

    except Exception as e:
        status_label.config(text="Error occurred while downloading the video.")
        messagebox.showerror("Error", str(e))



# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Check if output path is set, if not, force the user to set it
if not os.path.exists("config.json"):
    set_output_path()



# Configure grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


# Configuration button
config_button = tk.Button(root, text="config", command=set_output_path, font=("Helvetica", 12))
config_button.grid(row=0, column=2, columnspan=2, pady=10)


# Load and place the image using PIL
image = Image.open("ytb_downloader.jpeg")
image = image.resize((200, 200), Image.LANCZOS)  # Resize the image to 200x200 pixels
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create and place the URL entry field
url_label = tk.Label(root, text="YouTube URL:", font=("Helvetica", 14, "bold"))
url_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
url_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")

# Create and place download option (radio button)
download_option = tk.StringVar(value="video")

audio_radio = tk.Radiobutton(root, text="Audio", variable=download_option, value="audio", font=("Helvetica", 12))
audio_radio.grid(row=1, column=2, padx=10, pady=10, sticky="w")

video_radio = tk.Radiobutton(root, text="Video", variable=download_option, value="video", font=("Helvetica", 12))
video_radio.grid(row=1, column=3, padx=10, pady=10, sticky="w")

# Create and place the search button
search_button = tk.Button(root, text="Search", command=lambda: get_video_datas(download_option), font=("Helvetica", 12))
search_button.grid(row=2, column=0, columnspan=2, pady=20)

# Create and place the video_info_display
video_info_display = tk.Label(root, text="", font=("Helvetica", 12))
video_info_display.grid(row=3, column=0, columnspan=2, pady=10)

# Create and place the status label
status_label = tk.Label(root, text="", font=("Helvetica", 12))
status_label.grid(row=6, column=0, columnspan=2, pady=10)


# Run the application
root.mainloop()