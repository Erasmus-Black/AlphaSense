import requests
import yaml
import logging

# Load credentials from config.yaml
def load_config(path="config.yaml"):
    with open(path, "r") as file:
        config = yaml.safe_load(file)
        return config["alphasense"]

creds = load_config()

API_KEY = creds["api_key"]
USERNAME = creds["username"]
PASSWORD = creds["password"]
CLIENT_ID = creds["client_id"]
CLIENT_SECRET = creds["client_secret"]

AUTH_URL = "http://localhost:5001/auth"
#AUTH_URL = "https://api.alpha-sense.com/auth"

# Shared token storage
access_token = None
refresh_token = None


def authenticate():
    global access_token, refresh_token
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    # Log the request (masking sensitive fields)
    logging.info("📤 Sending authentication request:")
    logging.info(f"URL: {AUTH_URL}")
    logging.info(f"Headers: {{'x-api-key': '{API_KEY[:4]}***', 'Content-Type': 'application/x-www-form-urlencoded'}}")
    logging.info(f"Data: {{'grant_type': 'password', 'username': '{USERNAME}'}}")

    res = requests.post(AUTH_URL, headers=headers, data=data)
    res.raise_for_status()
    tokens = res.json()
    access_token = tokens["access_token"]
    refresh_token = tokens.get("refresh_token")
    logging.info("Token successfully issued - Authentication passed.")

    return access_token, refresh_token

def refresh_access_token():
    global access_token, refresh_token
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token
    }
    res = requests.post(AUTH_URL, headers=headers, data=data)
    res.raise_for_status()
    tokens = res.json()
    access_token = tokens["access_token"]
    refresh_token = tokens.get("refresh_token")
    logging.info("Authentication token successfully refreshed.")