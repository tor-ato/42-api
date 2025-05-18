from config import API_URL, CAMPUS_TOKYO
from auth_config import UID, SECRET
import requests

def get_token():
    token_url = f"{API_URL}/oauth/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': UID,
        'client_secret': SECRET
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        return access_token
    else:
        print(f"get token error : {response.status_code}")
        print(response.text)
        sys.exit(1)
