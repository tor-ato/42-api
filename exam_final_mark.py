import requests
import json
from requests.auth import HTTPBasicAuth
from pprint import pprint
import sys
from config import API_URL, CAMPUS_TOKYO
from auth_config import UID, SECRET
from get_token import get_token
from datetime import datetime

def get_data(access_token, user_id):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f"{API_URL}/v2/users/{user_id}/projects_users"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        exams_data = response.json()
        return response.status_code, exams_data
    else:
        print(f"API request error: {response.status_code}")
        print(response.text)
        return response.status_code, None

if __name__ == "__main__":
    # トークンを取得
    token = get_token()
    if not token:
        sys.exit(1)
    
    # ID-名前のマッピング
    id_to_name = {
        1320: "Exam Rank 02",
        1321: "Exam Rank 03",
        1322: "Exam Rank 04",
        1323: "Exam Rank 05",
        1324: "Exam Rank 06"
    }
    
    target_ids = [1320, 1321, 1322, 1323, 1324]
    
    # コマンドライン引数をチェック
    if len(sys.argv) < 2:
        print("使用方法: python3 exploit.py <user_id1> <user_id2> ...")
        print("例: python3 exploit.py yohatana yooshima")
        sys.exit(1)
    
    # コマンドライン引数からuser_idsを取得（最初の引数はスクリプト名なので除外）
    user_ids = sys.argv[1:]
    
    # hard codingも可能
    # user_ids = ["tkitahar, yohatana"]
    # 各ユーザーのデータを取得・表示
    for user_id in user_ids:
        status, data = get_data(token, user_id)
        
        if not data:
            print(f"ユーザー {user_id} のデータが空です。API リクエストに問題がある可能性があります。")
            continue
        
        print(f"user_id: {user_id}")
        found_exams = False
        
        for item in data:
            # project.idをチェック（JSONの構造に基づく）
            if "project" in item and item["project"]["id"] in target_ids:
                project_id = item["project"]["id"]
                project_name = id_to_name.get(project_id, "Unknown")
                final_mark = item["final_mark"]
                print(f"  {project_name}: final_mark = {final_mark}")
                found_exams = True
        
        if not found_exams:
            print(f"  対象の試験データが見つかりませんでした")
        
        print("")  # 空行を追加
