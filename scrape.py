from googleapiclient.discovery import build
import pandas as pd
import isodate
import datetime
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

# Setup YouTube API
API_KEY = "AIzaSyD3zOFfaBB_9dpALUBWrtPYm2Ygy53hZ_8"
youtube = build('youtube', 'v3', developerKey=API_KEY)

# --- Helper Functions ---

def parse_duration(duration):
    return int(isodate.parse_duration(duration).total_seconds())

def get_thumbnail_brightness(thumbnail_url):
    try:
        response = requests.get(thumbnail_url, timeout=5)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        brightness = np.mean(np.array(img))  # Mean of all RGB values
        return brightness
    except Exception as e:
        print("Brightness error:", e)
        return None

def detect_faces_in_thumbnail(thumbnail_url):
    try:
        response = requests.get(thumbnail_url, timeout=5)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        np_img = np.array(img)
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        return len(faces)
    except Exception as e:
        print("Face detection error:", e)
        return None

def get_channel_info(channel_id):
    try:
        response = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        ).execute()

        if not response['items']:
            return {}

        channel = response['items'][0]
        snippet = channel['snippet']
        stats = channel.get('statistics', {})

        return {
            "channel_title": snippet.get("title"),
            "subscriber_count": int(stats.get("subscriberCount", 0)),
            "channel_country": snippet.get("country", None)
        }
    except Exception as e:
        print("Channel info error:", e)
        return {}

def get_video_data(video_id):
    response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    ).execute()

    if not response['items']:
        return None

    video = response['items'][0]
    snippet = video['snippet']
    stats = video.get('statistics', {})
    details = video['contentDetails']

    thumbnail_url = snippet['thumbnails']['high']['url']
    brightness = get_thumbnail_brightness(thumbnail_url)
    face_count = detect_faces_in_thumbnail(thumbnail_url)

    channel_id = snippet['channelId']
    channel_info = get_channel_info(channel_id)

    publish_date = datetime.datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    today = datetime.datetime.utcnow()
    days_since_upload = max((today - publish_date).days, 1)  # avoid division by zero

    view_count = int(stats.get('viewCount', 0))
    views_per_day = view_count / days_since_upload

    estimated_views_7d = int(views_per_day * min(7, days_since_upload))
    estimated_views_30d = int(views_per_day * min(30, days_since_upload))

    data = {
        "video_id": video_id,
        "title": snippet['title'],
        "description_length": len(snippet['description']),
        "publish_date": snippet['publishedAt'],
        "category_id": snippet.get('categoryId'),
        "tags_count": len(snippet.get('tags', [])),
        "view_count": view_count,
        "like_count": int(stats.get('likeCount', 0)),
        "comment_count": int(stats.get('commentCount', 0)),
        "duration_sec": parse_duration(details['duration']),
        "thumbnail_brightness": brightness,
        "face_count": face_count,
        "channel_title": channel_info.get("channel_title"),
        "subscriber_count": channel_info.get("subscriber_count"),
        "channel_country": channel_info.get("channel_country"),
        "upload_hour": publish_date.hour,
        "upload_day": publish_date.strftime('%A'),
        "days_since_upload": days_since_upload,
        "est_views_7d": estimated_views_7d,
        "est_views_30d": estimated_views_30d,
    }

    return data

# --- List of video IDs ---

video_ids = [
    "Ye8NxLnh8qE",
    "fGF10RLUm1U",
    "K_XcqhPtmzo",
    "M_AeBRELg4w",
    "FRled0BaA_Q",
    "i6bI8MRkxBc",
    "omp-XZ_X7wo",
    "nVJJ_ivgELA",
    "txmLqITl1h8",
    "y8himFW553M",
    "me8guS2gYyI",
    "Sc1OI1i-Kgs",
    "oGFn8MI3Bmo",
    "lsqbpw67hSs",
    "-JhZOeTXwrg",
    "UZqN1QT0ZXs",
    "XYMCRw_6PRA",
    "HVxeyJoY1lk",
    "kz6pELQncyw",
    "g6ygdCjHoak",
    "dYngnREoIEY",
    "-JhZOeTXwrg",
    "BcKBAl3dOGA",
    "Ju04VnTdkEA",
    "i4LKULh4wEw",
    "uXN6wT9Qz18",
    "RL7Y3wAMOlg",
    "NsCP-IdSW1k",
    "m4Tj1EfRKlg",
    "U5syMIJ5JRA",
    "ALtgiWtA_VM",
    "5yuuRveinFc",
    "K-w04FG6eyI",
    "7uOq9zWTC5g",
    "sggZZXZkaDc",
    "iTSmKz9EoYo",
    "KfIo1E5VFws",
    "9bd2nvAKyMc",
    "pYHGmfgNYAQ",
    "SAxf5p1bjPo",
    "QThx68A9LkU",
    "O5eePfGZWP8",
    "ImnlZsJNI-A",
    "jXz2YH06Epw",
    "_q09tp1-L5k",
    "vufspps4erY",
    "at93FMsH3fY",
    "_cap4oWCW-g",
    "UYclbkc2_Js",
    "-nnYpg0wY5o",
    "phSN6iciG94",
    "61TqN5amlzQ",
    "yu40vUYUjVo",
    "gebozQyu-pY",
    "S_ExfLW4mfM",
    "FLbE0IkHLkg",
    "QBeoEGW4aXg",
    "sCQDGs7W6mE",
    "RDtRITCl07eVQ",
    "RDbAInQtdFHlE",
    "Bm7EIuztc-g",
    "UqMTGW4tPP8",
    "UC3k11aJnnU",
    "4oR9hq7QQKU",
    "8FkLpm0txkk",
    "0nP9axR2mVU",
    "ok9MH86gRK4",
    "SC5c-AzmCbs",
    "y9YdkP-6d_E",
    "O3F4q8RkI68",
    "HyDNDgZjDws",
    "rpk_NmKt7FE",
    "L4XjEuCPOJY",
    "8vcdlGvBugo",
    "2m4gYL9jmJE",
    "7O8xMiTAmpQ",
    "UTeep0eR7_c",
    "mpuk6hpti34",
    "YTxo4ljQyE8",
    "gRTWJ2Jxg4w",
    "F4LdrfmbPC0",
    "dCbHta4Fz1g",
    "dCbHta4Fz1g",
    "RTqeFLPFp7U",
    "2C1uVB-n7jY",
    "1R3q507dzdY",
    "RM-sgtC9PPs",
    "n4TTwG_9Huw",
    "vNCeY6czwvI",
    "UL4-ZEQyRaY",
    "P5SblXMOols",
    "MDxcWFJIOTQ",
    "LDs26opO4yY",
    "SMPEq5r6fDY",
    "ikY7Avp_Sto",
    "-GfrnoqTopA",
    "buSeNrLsj2M",
    "P2R-wukVxOo",
    "OHAUJ70KnMg",
    "btOaIxwLJtk",
    "hLUTSqqHMxM",
    "1xuKAKJeQkk",
    "D6oDup51h3k",
    "u_IchGWYyWw",
    "GEcrXlV8INI",
    "euk8LLHitsI",
    "S-Kf6CnJC2w",
    "KNhO9qfZ2o0",
    "Ro2O69mM6dw",
    "AUWMxpDAFh4",
    "W-bBQD5pP7o",
    "1rTqcZXxYIk",
    "sjBMxI-R-8Y",
    "fYVphsLPCW8",
    "XssGcf9peFo",
    "WRPjhT-wfKM",
    "BOMebhx7kdk",
    "FPyGWhdPqzA",
    "4kQ09EfBi5s",
    "DaTdxmGK1yo",
    "zu6Tad3RSYI",
    "lSn1ytqcZjg",
    "2l8q2ZGNHjY",
    "--CfYt5bD-U",
    "ZrVfpp4Helw",
    "lVXyqE34InE",
    "CFJlK2Ycdf0",
    "I9GXzy2gsUM",
    "DWa_HLrAW64",
    "66cOP2bPVak",
    "WCfNkmMTWIE",
    "RxM4yCF4wQU",
    "BaMerY8rOrY",
    "5kG06KGLxsE",
    "lWcwudHPqXE",
    "BGCc4fDhj9A",
    "zq6g1xgCOTI",
    "mlbY_JRhFIM",
    "f4ek_hvtkeA",
    "F2Rz-sAxNYM",
    "01Ocf5GFijo",
]

# --- Collect Data ---

video_data_list = []
for vid in video_ids:
    print(f"Processing video ID: {vid}")
    d = get_video_data(vid)
    if d:
        video_data_list.append(d)

# --- Save to CSV ---

df = pd.DataFrame(video_data_list)
df.to_csv("youtube_video_data_full.csv", index=False)
print("✅ Dataset with brightness, face count, channel info, and estimated views created!")
