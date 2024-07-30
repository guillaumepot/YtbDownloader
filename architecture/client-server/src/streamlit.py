"""
### STREAMLIT APP - Main file ###
"""

from datetime import datetime
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from script import get_file
import streamlit as st


audio_path = os.getenv("AUDIO_PATH")
video_path = os.getenv("VIDEO_PATH")
available_keys_str = os.getenv("AVAILABLE_KEYS")
available_keys_list = available_keys_str.split(',')
available_keys = {item.split(':')[0]: item.split(':')[1] for item in available_keys_list}



# Initialize 'key' & 'name' in session_state if it doesn't exist
if 'key' not in st.session_state:
    st.session_state['key'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None
if 'show_download_button' not in st.session_state:
    st.session_state['show_download_button'] = False
if 'get_file_section' not in st.session_state:
    st.session_state['get_file_section'] = False



def validate_key():
    # This function will be called when the "Valider" button is pressed
    key = st.session_state.key_input  # Use the input directly from session_state
    if key not in available_keys.values():
        st.error("Clé invalide")
    else:
        st.session_state['key'] = key  # Update the session state with the validated key


def add_to_logs(name, title, link, size, duration) -> None:
    """
    Add the video name and link to the logs file.

    Args:
        youtube: An object representing a YouTube video.

    Returns:
        None
    """
    # Create folder if not exists
    if not os.path.exists(f'./logs/{name}'):
        os.makedirs(f'./logs/{name}')
    
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Add to logs
    with open(f'./logs/{name}/logs.txt', 'a') as f:
        f.write(f'{date} - {title} - {duration}secs - {size:.2f}Mo \n{link} \n\n')




# Authentication panel
if st.session_state['key'] is None:
    st.sidebar.title("Authentication")
    st.sidebar.write("Insérez votre clé")
    # The text_input widget automatically updates st.session_state['key_input']
    # No need to manually set st.session_state['key_input'] here
    st.sidebar.text_input("Clé:", type="password", key='key_input')
    # Use the 'on_click' parameter to specify a callback function for the button
    st.sidebar.button("Valider", on_click=validate_key)
else:
    for name, key_value in available_keys.items():
        if key_value == st.session_state['key']:
            st.sidebar.write(f"Bonjour {name}")
            st.session_state['name'] = name


# If the key is validated, display the content
if st.session_state['key'] is not None:

    pages=["Telecharger", "Historique"]
    page=st.sidebar.radio("Navigation", pages)


    # TELECHARGER
    if page == pages[0]:

        # Link bar & format choice
        link = st.text_input("Insérer lien Youtube:")
        format = st.radio("Format souhaité", ["Vidéo mp4", "Audio mp3"])



        if st.button("Rechercher", key="search_content"):
            video = YouTube(link, on_progress_callback = on_progress)
            stream = video.streams.get_highest_resolution()
            filesize_in_mb = stream.filesize / 1024 / 1024  # Convert bytes to megabytes

            # Store video details in session_state
            st.session_state['video_title'] = video.title
            st.session_state['video_thumbnail_url'] = video.thumbnail_url
            st.session_state['video_length'] = video.length
            st.session_state['filesize_in_mb'] = filesize_in_mb

            # Display video details
            st.write(f"Titre: {video.title}   |   Durée: {video.length} secondes   |   Taille: {filesize_in_mb:.2f} Mo")
            st.image(video.thumbnail_url)

            # If file too big, warn user
            if filesize_in_mb > 30:
                st.warning("Attention! La taille du fichier est supérieure à 50 Mo, fichier trop volumineux pour être téléchargé.")
                st.stop()
            else:
                st.session_state['show_download_button'] = True



        if st.session_state.get('show_download_button', False):
            if st.button("Pré-charger et convertir", key="preload_content"):
                video_title = st.session_state.get('video_title', 'Unknown Video')
                st.write(f'Telechargement de {video_title}... \n Format: {format} \n')

                # Download File
                if format == "Vidéo mp4":
                    get_file(link, st.session_state['name'], audio=False)
                elif format == "Audio mp3":
                    get_file(link, st.session_state['name'], audio=True)
                    

                st.write(f'Téléchargement terminé! \n')

                # Log
                add_to_logs(name = st.session_state['name'],
                            title = st.session_state['video_title'],
                            link = link,
                            size = st.session_state['filesize_in_mb'],
                            duration = st.session_state['video_length'])



                st.session_state['show_download_button'] = False
                st.session_state['get_file_section'] = True


        if st.session_state.get('get_file_section', False):

            # List files in the directories
            audio_files = os.listdir(audio_path)
            video_files = os.listdir(video_path)

            # Create a section for downloading audio files if they exist
            if audio_files:
                st.subheader("Télécharger le fichier audio")
                for file_name in audio_files:
                    file_path = os.path.join(audio_path, file_name)
                    with open(file_path, "rb") as file:
                        download_audio = st.download_button(label=f"{file_name}",
                                        data=file,
                                        file_name=file_name,
                                        mime="audio/mpeg")
                        
                        if download_audio:
                            try:
                                os.remove(file_path)
                                st.session_state['get_file_section'] = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting file: {e}")        
                                    


            # Create a section for downloading video files if they exist
            if video_files:
                st.subheader("Télécharger le fichier vidéo")
                for file_name in video_files:
                    file_path = os.path.join(video_path, file_name)
                    with open(file_path, "rb") as file:
                        download_video = st.download_button(label=f"{file_name}",
                                        data=file,
                                        file_name=file_name,
                                        mime="video/mp4")

                        if download_video:
                            try:
                                os.remove(file_path)
                                st.session_state['get_file_section'] = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting file: {e}")      


    # HISTORIQUE
    if page == pages[1]:
        st.subheader("Historique des téléchargements")
        logs = f'./logs/{st.session_state["name"]}/logs.txt'
        with open(logs , 'r') as f:
            for line in f:
                st.write(line)
