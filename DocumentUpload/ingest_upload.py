import os
import requests
import yaml
import datetime
import json
import logging

from authenticate import authenticate, refresh_access_token, creds, load_config
from utils import is_valid_file, move_to_archive, build_metadata

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("upload.log"),
        logging.StreamHandler()
    ]
)

# Config
CLIENT_ID = creds["client_id"]
USERNAME = creds["username"]
UPLOAD_URL = "http://localhost:5001/ingestion/v1/documents/upload"
#UPLOAD_URL = "https://research.alpha-sense.com/services/i/ingestion-api/v1/upload-document"

# Load file paths from config
SOURCE_FOLDER = creds.get("source_folder", "./to_upload")
ARCHIVE_FOLDER = creds.get("archive_folder", "./processed")

access_token = None
refresh_token = None

def upload_document(file_path):
    global access_token, refresh_token

    filename = os.path.basename(file_path)
    metadata_dict = json.loads(build_metadata(filename, USERNAME))

    headers = {
        "Authorization": f"Bearer {access_token}",
        "ClientId": CLIENT_ID
    }

    with open(file_path, "rb") as file_data:
        files = {
            "file": (filename, file_data),
            "metadata(type:string)": (None, json.dumps(metadata_dict), "application/json")
        }

        response = requests.post(UPLOAD_URL, headers=headers, files=files)

    if response.status_code == 401:
        logging.info("Token expired. Refreshing...")
        access_token, refresh_token = refresh_access_token()
        return upload_document(file_path)

    if response.status_code in (200, 201, 202):
        logging.info(f"Succesfully uploaded: {filename}")
        return True
    else:
        logging.info(f"File failed to upload {filename}: {response.status_code} - {response.text}")
        return False

def process_files():
    for filename in os.listdir(SOURCE_FOLDER):
        file_path = os.path.join(SOURCE_FOLDER, filename)

        if not os.path.isfile(file_path):
            continue

        is_valid, reason = is_valid_file(file_path)
        if not is_valid:
            logging.info(f"Skipping and failing file: {filename} ({reason})")
            move_to_archive(file_path, ARCHIVE_FOLDER, failed=True)
            continue

        success = upload_document(file_path)
        move_to_archive(file_path, ARCHIVE_FOLDER, failed=not success)

if __name__ == "__main__":
    try:
        access_token, refresh_token = authenticate()
        process_files()
    except Exception as e:
        logging.info("❌ Error:", e)
