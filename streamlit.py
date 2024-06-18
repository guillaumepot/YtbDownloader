import streamlit as st
import os

from script import get_file


audio_path = './storage/audio/'
video_path = './storage/video/'


available_keys = {
    'Guillaume' : '1234',
    'Fanny' : '5678'
}

# Initialize 'key' & 'name' in session_state if it doesn't exist
if 'key' not in st.session_state:
    st.session_state['key'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None



def validate_key():
    # This function will be called when the "Valider" button is pressed
    key = st.session_state.key_input  # Use the input directly from session_state
    if key not in available_keys.values():
        st.error("Clé invalide")
    else:
        st.session_state['key'] = key  # Update the session state with the validated key

# Ask for Key only if it's not validated yet
if st.session_state['key'] is None:
    st.subheader("Insérez votre clé")
    # The text_input widget automatically updates st.session_state['key_input']
    # No need to manually set st.session_state['key_input'] here
    st.text_input("Clé:", key='key_input')

    # Use the 'on_click' parameter to specify a callback function for the button
    st.button("Valider", on_click=validate_key)

# If the key is validated, display the content
if st.session_state['key'] is not None:
    # Affichage du nom de la personne
    for name, key_value in available_keys.items():
        if key_value == st.session_state['key']:
            st.write(f"Bonjour {name}")
            st.session_state['name'] = name

    # Affichage du contenu de la page
    links = st.text_area("Ajoutez vos liens ici, un lien par ligne")
    format = st.radio("Choisissez le format", ["Vidéo", "Audio"])

    if st.button("Charger", key="download"):
        links_list = links.split('\n')
        for link in links_list:
            st.write(f'Telechargement de ..: {link} \n')
            if format == "Vidéo":
                get_file(link, name, audio=False)
            elif format == "Audio":
                get_file(link, name, audio=True)


    # List files in the directories
    audio_files = os.listdir(audio_path)
    video_files = os.listdir(video_path)

    # Create a section for downloading audio files if they exist
    if audio_files:
        st.subheader("Télécharger les fichiers audio")
        for file_name in audio_files:
            file_path = os.path.join(audio_path, file_name)
            with open(file_path, "rb") as file:
                download_audio = st.download_button(label=f"{file_name}",
                                   data=file,
                                   file_name=file_name,
                                   mime="audio/mpeg")
                
                if download_audio:
                    try:
                        os.remove(file)
                    except Exception as e:
                        st.error(f"Error deleting file: {e}")                


    # Create a section for downloading video files if they exist
    if video_files:
        st.subheader("Télécharger les fichiers vidéo")
        for file_name in video_files:
            file_path = os.path.join(video_path, file_name)
            with open(file_path, "rb") as file:
                download_video = st.download_button(label=f"{file_name}",
                                   data=file,
                                   file_name=file_name,
                                   mime="video/mp4")

                if download_video:
                    try:
                        os.remove(file)
                    except Exception as e:
                        st.error(f"Error deleting file: {e}")      