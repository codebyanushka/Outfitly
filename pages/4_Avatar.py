import streamlit as st
import urllib.parse
import os
import requests
import cairosvg

st.set_page_config(page_title="Customize Avatar", page_icon="🧍‍♀️")

AVATAR_BASE = "https://avataaars.io/"

# Sidebar
with st.sidebar:
    st.page_link("pages/1_Closet.py", label="👚 My Closet")
    st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
    st.page_link("pages/3_History.py", label="📸 Outfit History")
    st.page_link("4_Avatar.py", label="🧍 Customize Avatar")
    st.page_link("app.py", label="🔒 Logout")

st.title("🧍 Customize Your Avatar")

if "username" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

username = st.session_state.username

# Create avatars directory if not exists
os.makedirs("avatars", exist_ok=True)

# Define customization options
skin_colors = [
    "Tanned", "Yellow", "Pale", "Light", "Brown", "DarkBrown", "Black"
]
hair_styles = [
    "ShortHairShortFlat", "ShortHairShortCurly", "ShortHairFrizzle",
    "LongHairStraight", "LongHairCurly", "LongHairBigHair", "NoHair"
]
eye_types = [
    "Default", "Happy", "Squint", "Wink", "Cry", "Dizzy", "EyeRoll"
]
mouth_types = [
    "Smile", "Serious", "Sad", "Tongue", "Twinkle", "Disbelief"
]
clothing_types = [
    "BlazerShirt", "Hoodie", "Overall", "ShirtCrewNeck", "GraphicShirt", "BlazerSweater"
]
accessories_types = [
    "Blank", "Round", "Sunglasses", "Prescription01", "Kurt", "Wayfarers"
]

# Get selections
skin = st.selectbox("Skin Color", skin_colors)
hair = st.selectbox("Hair Style", hair_styles)
eyes = st.selectbox("Eye Type", eye_types)
mouth = st.selectbox("Mouth Type", mouth_types)
clothing = st.selectbox("Clothing", clothing_types)
accessories = st.selectbox("Accessories", accessories_types)

# Generate avatar URL
params = {
    "avatarStyle": "Circle",
    "topType": hair,
    "accessoriesType": accessories,
    "clotheType": clothing,
    "eyeType": eyes,
    "mouthType": mouth,
    "skinColor": skin
}
avatar_url = AVATAR_BASE + "?" + urllib.parse.urlencode(params)

# Show the avatar
st.image(avatar_url, caption="Your Avatar", use_column_width=False)

# Save avatar button
if st.button("Save Avatar"):
    try:
        avatar_response = requests.get(avatar_url)
        if avatar_response.status_code == 200:
            avatar_path = os.path.join("avatars", f"{username}_avatar.png")
            cairosvg.svg2png(bytestring=avatar_response.content, write_to=avatar_path)
            st.success("✅ Avatar saved successfully!")
        else:
            st.error("❌ Failed to fetch avatar image.")
    except Exception as e:
        st.error(f"❌ Failed to save avatar: {e}")

# Show avatar in sidebar if already saved
avatar_path = os.path.join("avatars", f"{username}_avatar.png")
if os.path.exists(avatar_path):
    with st.sidebar:
        st.image(avatar_path, width=100, caption="👤 Your Avatar")
