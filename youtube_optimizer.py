---

### 🚀 Production-Ready Script (`youtube_optimizer.py`)



```python
import os
import re
import random
import time
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# --- CONFIGURATION ---
SCOPES = ["https://www.googleapis.com/auth/youtube"]
RAW_PATTERNS = r'(video|output|pxl|img|vid|mov|_|\.mp4|untitled)'
CATEGORY_ID = "2"  # Autos & Vehicles

def get_youtube_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def generate_metadata(filename):
    """Creates shuffled road-trip titles based on date extraction."""
    name = os.path.splitext(filename)[0]
    date_match = re.search(r'(\d{4})(\d{2})(\d{2})', name)
    
    if date_match:
        try:
            year, month, day = date_match.groups()
            date_str = datetime(int(year), int(month), int(day)).strftime("%B %d, %Y")
        except:
            date_str = datetime.now().strftime("%B %d, %Y")
    else:
        date_str = datetime.now().strftime("%B %d, %Y")

    titles = [
        f"Highway Chronicles - {date_str}", f"Open Road Adventure - {date_str}",
        f"Scenic Route Highlights - {date_str}", f"The Ultimate Drive - {date_str}",
        f"Miles & Memories - {date_str}", f"Asphalt Adventures - {date_str}",
        f"رحلة طريق ملحمية - {date_str}", f"أجواء قيادة مثالية - {date_str}",
        f"سحر الطريق السريع - {date_str}", f"مغامرة الأسفلت - {date_str}"
    ]
    return random.choice(titles)

def update_videos():
    youtube = get_youtube_service()
    
    try:
        # 1. Get the 'Uploads' playlist ID (Cheaper than search)
        channels_response = youtube.channels().list(mine=True, part="contentDetails").execute()
        uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        print(f"✅ Connected. Accessing uploads...")

        next_page_token = None
        while True:
            # Fetch playlist items (1 quota unit)
            playlist_request = youtube.playlistItems().list(
                playlistId=uploads_playlist_id,
                part="snippet,contentDetails",
                maxResults=50,
                pageToken=next_page_token
            )
            playlist_response = playlist_request.execute()

            for item in playlist_response["items"]:
                video_id = item["contentDetails"]["videoId"]
                current_title = item["snippet"]["title"]

                # 2. Check if the title needs fixing
                if re.search(RAW_PATTERNS, current_title.lower()):
                    new_title = generate_metadata(current_title)
                    
                    # 3. Update metadata (50 quota units)
                    try:
                        update_body = {
                            "id": video_id,
                            "snippet": {
                                "title": new_title,
                                "description": f"{new_title}\n\nCruising through the scenic routes. #RoadTrip #POV #Driving",
                                "categoryId": CATEGORY_ID,
                                "tags": ["Road Trip", "Driving", "POV", "Travel", "Vlog"]
                            }
                        }
                        youtube.videos().update(part="snippet", body=update_body).execute()
                        print(f"🚀 FIXED: {current_title} -> {new_title}")
                        time.sleep(1) # Safety buffer
                    except HttpError as e:
                        if e.resp.status == 403:
                            print("\n🛑 Quota limit reached. Restart tomorrow!")
                            return
                        print(f"⚠️ Error updating {video_id}: {e}")

            next_page_token = playlist_response.get("nextPageToken")
            if not next_page_token:
                break

        print("\n✨ All videos processed!")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    update_videos()