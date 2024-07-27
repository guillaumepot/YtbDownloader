from pytube import YouTube
from script import *
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def search_url(event=None):
    url = url_entry.get()
    print(f"Searching for: {url}")
    
    try:
        video = YouTube(url)
        stream = video.streams.get_highest_resolution()
        filesize_in_mb = stream.filesize / 1024 / 1024  # Convert bytes to megabytes
        
        video_title = video.title
        video_thumbnail_url = video.thumbnail_url
        video_length = video.length

        # Display video details
        print(f"Titre: {video_title}   |   Durée: {video_length} secondes   |   Taille: {filesize_in_mb:.2f} Mo")

        response = requests.get(video_thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = ImageTk.PhotoImage(img)
        thumbnail_label = tk.Label(root, image=img)
        thumbnail_label.image = img  # Keep a reference to avoid garbage collection
        thumbnail_label.pack()


    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", "An error occurred while searching for the video. Please check the URL and try again.")
        return














# Main Windows
root = tk.Tk()
root.title("Youtube Downloader")

# URL Entry
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)
url_entry.bind("<Return>", search)
# Search button
search_button = tk.Button(root, text="Search", command=search_url)
search_button.pack(pady=10)





# Variable to store the selected format
format_var = tk.StringVar(value="Vidéo mp4")

# Radio buttons for format selection
radio_video = tk.Radiobutton(root, text="Vidéo mp4", variable=format_var, value="Vidéo mp4")
radio_audio = tk.Radiobutton(root, text="Audio mp3", variable=format_var, value="Audio mp3")

# Pack the radio buttons
radio_video.pack(anchor=tk.W)
radio_audio.pack(anchor=tk.W)





# Main loop
root.mainloop()