import requests
from django.conf import settings

def send_push_notification(title , subtitle, message, event_id , notification_id, image_url = None):
    headers = {
        "Authorization": f"Basic {settings.ONESIGNAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "app_id": settings.ONESIGNAL_APP_ID,
        "headings": {"en": title},
        #"subtitle": { "en": subtitle if subtitle else None,},
        "contents": {"en": message},
        #"data": data or {},
        #"included_segments": f"event_segment_{event_id.toString()}",
        "filters": [
            {
                "field": "tag",
                "relation": "=",
                "key": f"event_{event_id}",
                "value": "registered" 
            }
        ],
        "big_picture": image_url if image_url else None,
        "ios_attachments": { "id": image_url if image_url else None, },
        "data": {
            "event_id": event_id , 
            "notification_id" : notification_id
            
        },
    }

    response = requests.post(settings.ONESIGNAL_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": response.status_code,
            "details": response.json()
        }
    



def create_user(external_id):

    url = "https://api.onesignal.com/apps/{app_id}/users"

    payload = {
        "properties": {
            "tags": {},
            "language": "en",
            "timezone_id": "America/Los_Angeles",
            "lat": 123,
            "long": 123,
            "country": "US",
            "first_active": 123,
            "last_active": 123,
            "ip": "<string>",
            "test_user_name": "<string>"
        },
        "identity": { "external_id": external_id.toString() },
        "subscriptions": [
            {
                "type": "Email",
                "token": "<string>",
                "enabled": True,
                "notification_types": 123,
                "session_time": 123,
                "session_count": 123,
                "app_version": "<string>",
                "device_model": "<string>",
                "device_os": "<string>",
                "test_type": 123,
                "sdk": "<string>",
                "rooted": True,
                "web_auth": "<string>",
                "web_p256": "<string>"
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def create_user(title, message, user_ids=None, data=None):
    url = "https://api.onesignal.com/apps/{app_id}/users/by/{alias_label}/{alias_id}"

    payload = {
        "properties": {
            "tags": {},
            "language": "en",
            "timezone_id": "America/Los_Angeles",
            "lat": 123,
            "long": 123,
            "country": "US",
            "first_active": 123,
            "last_active": 123,
            "ip": "<string>",
            "test_user_name": "<string>"
        },
        "deltas": {
            "session_time": 123,
            "session_count": 123,
            "purchases": [
                {
                    "sku": "<string>",
                    "iso": "USD",
                    "amount": "<string>",
                    "count": 123
                }
            ]
        }
    }
    headers = {
        "Authorization": "Key YOUR_APP_API_KEY",
        "Content-Type": "application/json"
    }

    response = requests.patch(url, json=payload, headers=headers)

    print(response.text)



def update_user(external_id , event_id):

    appid = settings.ONESIGNAL_APP_ID
    extIdStr = f"{external_id}"
    url = f"https://api.onesignal.com/apps/{appid}/users/by/external_id/{extIdStr}"

    payload = {
        "properties": {
            "tags": {f"event_{event_id}": "registered"},
        }
    }
    headers = {
        "Authorization": f"Key {settings.ONESIGNAL_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.patch(url, json=payload, headers=headers)

    print(response.text)

def create_segment(event_id):

    url = f"https://api.onesignal.com/apps/{settings.ONESIGNAL_API_ID}/segments"

    payload = {
        "name": f"event_segment_{event_id.toString()}",
        "filters": [
            {
                "field": "tag",
                "relation": "=",
                "key": f"event_{event_id}",
                "value": "registered"
            }
        ]#,
        #"id": event_id.toString()
    }
    headers = {
        "Authorization": f"Key {settings.ONESIGNAL_API_KEY}",
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def update_segment(event_id):

    url = f"https://api.onesignal.com/apps/{settings.ONESIGNAL_API_ID}/segments/{settings.ONESIGNAL_APP_SEGMENTID}"

    payload = {
        "filters": [
            {
                "field": "tag",
                "relation": "=",
                "key": f"event_{event_id}",
                "value": "registered"
            }
        ]
    }
    headers = {
        "Authorization": f"Key {settings.ONESIGNAL_API_KEY}",
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.patch(url, json=payload, headers=headers)

    print(response.text)