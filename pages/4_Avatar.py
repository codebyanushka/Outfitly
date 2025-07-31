import streamlit as st
import urllib.parse
import requests
import os
from PIL import Image
from utils import render_sidebar

AVATAR_BASE = "https://avataaars.io/"

if "username" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

username = st.session_state["username"]
render_sidebar()

st.title("🧑‍🎨 Customize Your Avatar")

# Avatar options
skin = st.selectbox("Skin Color", ["Light", "Brown", "DarkBrown", "Black"])
hair = st.selectbox("Hair Style", ["ShortHairShortFlat", "LongHairStraight", "Hat"])
eyes = st.selectbox("Eye Type", ["Default", "Happy", "Squint"])
mouth = st.selectbox("Mouth Type", ["Smile", "Serious", "Disbelief"])
clothes = st.selectbox("Clothing", ["BlazerShirt", "GraphicShirt", "Hoodie"])
bg_color = st.color_picker("Background Color", "#E0E0E0")

# Build URL
params = {
    "avatarStyle": "Circle",
    "topType": hair,
    "skinColor": skin,
    "eyeType": eyes,
    "mouthType": mouth,
    "clotheType": clothes,
    "backgroundColor": bg_color.replace("#", ""),
    "accessoriesType": "Blank"
}

avatar_url = AVATAR_BASE + "?" + urllib.parse.urlencode(params)

st.image(avatar_url, width=200, caption="Your Avatar")

if st.button("Save Avatar"):
    img_data = requests.get(avatar_url).content
    avatar_dir = "images/avatars"
    os.makedirs(avatar_dir, exist_ok=True)
    file_path = os.path.join(avatar_dir, f"{username}_avatar.png")
    with open(file_path, "wb") as f:
        f.write(img_data)
    st.success("Avatar saved!")
