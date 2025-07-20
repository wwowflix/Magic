# -*- coding: utf-8 -*-
import requests

API_KEY = "your_convertkit_api_key"
FORM_ID = "your_form_id"
EMAIL = "subscriber_email@example.com"

def subscribe(email):
    url = f"https://api.convertkit.com/v3/forms/{FORM_ID}/subscribe"
    data = {
        "api_key": API_KEY,
        "email": email
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Subscribed {email} successfully!")
    else:
        print(f"Failed to subscribe: {response.text}")

if __name__ == "__main__":
    subscribe(EMAIL)



