import requests
import json
from requests.auth import HTTPBasicAuth
from pprint import pprint
import sys
from config import API_URL, CAMPUS_TOKYO
from auth_config import UID, SECRET
from get_token import get_token
from datetime import datetime

def get_data_with_filter(access_token, verified_ids, target_ids):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f"{API_URL}/v2/projects_users"
    params = {}
    # 'filter[user_id]': "12345,67890,98765"
    params['filter[user_id]'] = ','.join(map(str, verified_ids))
    params['filter[project_id]'] = ','.join(map(str, target_ids))
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        exams_data = response.json()
        return exams_data
    else:
        print(f"API request error: {response.status_code}")
        print(response.text)
        return None

def verifi_user(access_token, login):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f"{API_URL}/v2/users/{login}"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('id')
    else:
        print(f"ユーザー {login} の取得に失敗: {response.status_code}")
        return None

def check_argc(argc):
    if len(sys.argv) < 2:
        print("使用方法: python3 exploit.py <user_login1> <user_login2> ...")
        print("例: python3 exploit.py yohatana yooshima")
        sys.exit(2)

def verifi_users(access_token, user_logins):
    verified_ids = []
    login_to_id = {}
    
    for login in user_logins:
        user_id = verifi_user(access_token, login)
        if user_id:
            verified_ids.append(user_id)
            login_to_id[user_id] = login
        else:
            print(f"ユーザー {login} のIDを取得できませんでした")
    
    if not verified_ids:
        print("有効なユーザーIDが見つかりませんでした")
        sys.exit(3)
    
    return verified_ids, login_to_id

def print_data(data):
    if not data:
        print("no data")
        sys.exit(2)
    user_data = {}
    for item in data:
        user_id = item.get('user', {}).get('id')
        if user_id not in user_data:
            user_data[user_id] = []
        user_data[user_id].append(item)
    
    for user_id, items in user_data.items():
        login = login_to_id.get(user_id, f"user_id:{user_id}")
        print(f"\nuser_login: {login}")
        
        for item in items:
            project_id = item["project"]["id"]
            project_name = id_to_name.get(project_id, "Unknown")
            final_mark = item["final_mark"]
            print(f"  {project_name}: final_mark = {final_mark}")

if __name__ == "__main__":
    token = get_token()
    id_to_name = {
        1320: "Exam Rank 02",
        1321: "Exam Rank 03",
        1322: "Exam Rank 04",
        1323: "Exam Rank 05",
        1324: "Exam Rank 06"
    }
    target_ids = [1320, 1321, 1322, 1323, 1324]
    check_argc(sys.argv)
    verified_ids, login_to_id = verifi_users(token, sys.argv[1:])
    data = get_data_with_filter(token, verified_ids, target_ids)
    print_data(data)
