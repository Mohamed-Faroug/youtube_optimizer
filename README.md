# YouTube Road Trip Optimizer 🚗💨

A production-grade Python automation tool that identifies videos with "raw" filenames (e.g., `IMG_1234.mp4`) and replaces them with SEO-friendly, road-trip-themed titles and metadata.

## ✨ Features
- **High Quota Efficiency:** Uses PlaylistItems instead of Search, saving 99 units per request.
- **Smart Filtering:** Uses regex to target only unedited filenames.
- **Auto-SEO:** Adds relevant tags, descriptions, and sets the category to 'Autos & Vehicles'.
- **Safe Resume:** Features a built-in delay and quota-exhaustion handling.

## 🛠️ Setup
1. **Google Cloud Console:**
   - Enable **YouTube Data API v3**.
   - Create **OAuth 2.0 Client IDs** (Desktop App).
   - Download the JSON and rename it to `client_secrets.json`.
2. **Install Dependencies:**
   ```bash
   pip install google-auth-oauthlib google-api-python-client

**Run:**
 ```bash
python youtube_optimizer.py
