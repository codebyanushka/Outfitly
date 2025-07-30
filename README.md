# 👗 Outfitly: Your AI Stylist

Outfitly is a smart fashion assistant built with **Streamlit**. It helps users plan stylish outfits based on their wardrobe, the weather, and the occasion — all while offering a fun and personalized experience with avatars!

---

## ✨ Features

- ✅ **User Authentication** (Sign up & Login)
- 🧍 **Custom Avatars** (Skin tone, hairstyle, eyes, etc.)
- 🧳 **My Closet** – Upload and organize your wardrobe
- 🧠 **Create Your Fit** – Outfit suggestions based on:
  - Current weather
  - Occasion (Casual, Formal, Date, etc.)
- ❤️ **Favorite Fits** – Save the outfits you love
- 📸 **Outfit History** – Track past looks
- 🗑️ **Closet Management** – Delete clothes easily
- 🔁 **Outfit Regeneration** – Don’t like the fit? Get a new one!

---

## 🛠️ Tech Stack

- **Frontend & Backend**: [Streamlit](https://streamlit.io/)
- **Avatar API**: [Avataaars API](https://avataaars.io/)
- **Data Handling**: `pandas`, `csv`
- **Sentiment/Mood Analysis** (future scope): `TextBlob`

---

## 📁 Folder Structure

outfitly_your_ai_stylist/
│
├── app.py # Main login/signup and routing
├── pages/
│ ├── 1_Closet.py # Wardrobe management
│ ├── 2_create_your_fit.py # Outfit recommendation
│ ├── 3_History.py # Outfit history & favorites
│ └── 4_Avatar.py # Avatar customization
│
├── user_data.csv # Stores usernames & passwords
├── wardrobe_data.csv # Clothing data per user
├── closet_data.csv # Images uploaded to closet
├── outfit_history.csv # Outfit history logs
├── images/ # Uploaded clothing images
└── README.md

yaml
Copy
Edit

---

## 🚀 How to Run

1. **Clone the repo**:
   ```bash
   git clone https://github.com/codebyanushka/Outfitly.git
   cd Outfitly
2) install dependancies
   pip install streamlit pandas textblob
3) run the app
   streamlit run app.py
or python3 -m streamlit run app.py

🔮 Future Additions
Weather API integration
Style suggestions from current fashion trends
Personalized fashion tips
Mood-based outfit curation
convertion into a mobile app for both andoird and IOS 

 About the Creator
Made by Anushka
BTech CSE (AI & ML) | Passionate about AI/ML , Product Design & Tech

🪪 License
This project is open-source and free to use under the MIT License.

---
Let me know if you want to add screenshots, badges, or deployment instructions for platforms like **Streamlit Community Cloud** or **Render**.




