
import requests
import os


def sms_api_router(phone_number,message):
    print(message)
    pass
    # send_geez_sms(phone_number,message)

def send_geez_sms(phone_number,message):
    print(phone_number)
    print(message)
    try:
        url = "https://api.geezsms.com/api/v1/sms/send"

        payload={
        'token': os.getenv("GEEZ_ACCESS_KEY"),
        'phone': phone_number,
        'msg': message,
        }
        files=[

        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response)
        return response
    except Exception as e:
        return e
