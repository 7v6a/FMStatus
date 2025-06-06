# 🎧 FMStatus

**FMStatus** is a lightweight, modern Python script for retrieving and displaying detailed statistics about any Last.fm user account using the official Last.fm API.

It provides real-time and historical data such as account creation date, play count, currently/last played track, and an estimate of total listening time.

---

## 📌 Features

- 📛 Account username and country
- 🗓️ Registration date
- 🔢 Total playcount
- 🎵 Currently playing track
- ⏪ Last played track
- ⏱️ Total time spent listening (based on top tracks)
- 💅 Clean, styled terminal output using `rich`

---

## 🧰 Requirements

- Python 3.8 or higher
- A free [Last.fm API key](https://www.last.fm/api/account/create)

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/FMStatus.git
cd FMStatus
pip install -r requirements.txt
```
If ``requirements.txt`` is not included yet, simply run:
```bash
pip install requests rich
```

---

## 🔑 API Key Setup 

1. Visit [LastFM Api Account Request](https://www.last.fm/api/account/create)
2. Log in or register your Last.fm account
3. Create an API key (no approval needed for read-only access)
4. Replace the placeholder in FMStatus.py:
```python
API_KEY = '6C6F7665'
```

---

## ▶️ Usage 

```bash
python FMStatus.py
```
You’ll be prompted to enter a Last.fm username. The script will then fetch and display user stats in a visually structured layout.

--- 

## 🖼️ Preview
![{8156DC22-3A32-4CC1-8714-ED421FEE2DED}](https://github.com/user-attachments/assets/4ca514dd-baf0-4202-87d5-f1f2bcd4d26f)

