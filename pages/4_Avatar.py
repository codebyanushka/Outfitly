import streamlit as st
import urllib.parse
import requests
from PIL import Image
import os
import io
import pandas as pd

st.set_page_config(page_title="Create Your Avatar", page_icon="🧍")

AVATAR_BASE = "https://avataaars.io/"

# Create avatars folder if it doesn't exist
os.makedirs("images/avatars", exist_ok=True)

# Get current user
if 'username' not in st.session_state:
    st.error("You need to log in first.")
    st.stop()

username = st.session_state.username

st.title("🧍 Create Your Avatar")

# Avatar options
skin_options = ["Light", "Brown", "DarkBrown", "Black", "Pale"]
hair_options = ["ShortHairShortFlat", "ShortHairShortRound", "LongHairStraight", "LongHairCurvy"]
eye_options = ["Default", "Happy", "Squint", "Surprised"]
mouth_options = ["Smile", "Serious", "Sad", "Disbelief"]
accessory_options = ["Blank", "Prescription01", "Kurt", "Round"]
hair_color_options = ["Black", "Brown", "Blonde", "Red", "SilverGray"]

# Sidebar form
skin = st.selectbox("Skin Color", skin_options)
top = st.selectbox("Hair Style", hair_options)
hair = st.selectbox("Hair Color", hair_color_options)
eyes = st.selectbox("Eye Type", eye_options)
mouth = st.selectbox("Mouth Type", mouth_options)
accessory = st.selectbox("Accessories", accessory_options)

# Construct avatar URL (with PNG format!)
params = {
    "avatarStyle": "Transparent",
    "skinColor": skin,
    "topType": top,
    "hairColor": hair,
    "eyeType": eyes,
    "mouthType": mouth,
    "accessoriesType": accessory,
    "format": "png"  # ✅ This is CRITICAL
}
avatar_url = f"{AVATAR_BASE}?{urllib.parse.urlencode(params)}"

# Show avatar
st.image(avatar_url, width=200, caption="Your Avatar")

# Save button
if st.button("💾 Save Avatar"):
    try:
        response = requests.get(avatar_url)
        response.raise_for_status()
        avatar_image = Image.open(io.BytesIO(response.content))
        avatar_path = f"images/avatars/{username}_avatar.png"
        avatar_image.save(avatar_path)

        # Update user_data.csv
        user_data_file = "user_data.csv"
        if os.path.exists(user_data_file):
            df = pd.read_csv(user_data_file)
            df.loc[df["username"] == username, "avatar_url"] = avatar_path
            df.to_csv(user_data_file, index=False)
        else:
            df = pd.DataFrame({"username": [username], "avatar_url": [avatar_path]})
            df.to_csv(user_data_file, index=False)

        st.success("Avatar saved successfully!")
    except Exception as e:
        st.error(f"Failed to save avatar: {e}")
