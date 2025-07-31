import os
from PIL import Image, UnidentifiedImageError
import streamlit as st


AVATAR_FOLDER = "images/avatars"


def get_avatar_path(username):
    """Returns the path to the user's avatar image."""
    return os.path.join(AVATAR_FOLDER, f"{username}_avatar.png")


def avatar_exists(username):
    """Checks if an avatar exists for the given user."""
    return os.path.exists(get_avatar_path(username))


def load_avatar(username, size=150):
    """Loads and displays the avatar image for the user, or shows a warning."""
    path = get_avatar_path(username)
    if os.path.exists(path):
        try:
            st.image(Image.open(path), width=size)
        except UnidentifiedImageError:
            st.warning("⚠️ Cannot preview avatar image. Please recreate it.")
    else:
        st.warning("⚠️ No avatar found. Please customize one.")


def clear_session():
    """Logs out the user by clearing session state."""
    st.session_state["username"] = None
