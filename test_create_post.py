import random
import time
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os

environment = os.getenv("ENVIRONMENT", "local")
base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

print(f"Running in {environment} environment with base URL: {base_url}")

users = [
    {"account_id": "p1", "password": "p1"},
    {"account_id": "1031", "password": "1031"},
    {"account_id": "44", "password": "44"},
    {"account_id": "meow", "password": "meow"},
    {"account_id": "a", "password": "a"},
    {"account_id": "c", "password": "c"},
    {"account_id": "b", "password": "b"},
    
]

post_templates = [
    "1你那裡的天氣如何呢？",
    "2我想上來看看看有沒有新消息！",
    "3一個字毀掉一部電影",
    "4這裡講政治，會發生什麼事情？",
    "5推薦一部你看過最喜歡的電影",
    "6推薦一本你看過最喜歡的書",
    "7一句話，遇到已讀不回怎麼辦？",
    "8一句話，遇到不讀不回怎麼辦？",
    "9不懂就問，後端工程師平常在幹嘛？",
    "10不懂就問，前端工程師平常在幹嘛？",
    "11不懂就問，nginx是什麼？",
    "12麥當勞最好吃的是非薯餅、雞塊莫屬",
    "13有誰沒被摩絲漢堡的雞塊燙過？",
    "14這裡有誰是轉職成工程師的呢？",
    "15真是太神奇了～傑克！",
    "16據說這裡可以看人吵架，我要的血流成河在哪",
    "17聽說ikea甜甜圈燈很難買，有誰成功購買到？",
    "18江蕙復出！？",
    "19I人？E人？都幾？",
    "20有推薦的 Podcast 嗎？",

]

def login(user):
    url = f"{base_url}/api/user/auth"
    data = {
        "account_id": user["account_id"],
        "password": user["password"]
    }
    
    response = requests.put(url, json=data)
    if response.status_code == 200:
        user["token"] = response.json().get("token")
        print(f"{user['account_id']} logged in successfully.")
    else:
        print(f"Failed to log in for {user['account_id']}")

def post_content(user, used_templates):
    url = f"{base_url}/api/post"
    headers = {"Authorization": f"Bearer {user['token']}"}
    
    # 確保貼文內容不重複
    content = None
    while content is None or content in used_templates:
        content = random.choice(post_templates)
    used_templates.add(content)
    
    data = {
        "post_parent_id": None,
        "content_type": "Post",
        "content": {
            "text": content,
            "media": {
            "images": None,
            "videos": None,
            "audios": None
            }
        },
        "visibility": "Public" if random.random() > 0.5 else "Private",
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("success"):
            print(f"{user['account_id']} successfully posted: {content}")
            return response_data.get('post_id'), user['account_id']  
        else:
            print(f"Post failed for {user['account_id']}, success=False returned.")
            return None, None
    else:
        print(f"Failed to post for {user['account_id']}, status code: {response.status_code}")
        return None
    

def like_and_post(user, post_id, account_id):
    if user["account_id"] == account_id:
        return
    
    url_like = f"{base_url}/api/member/{account_id}/post/{post_id}/like"
    headers = {"Authorization": f"Bearer {user['token']}"}
    payload = {"like": True}
    
    
    if random.random() > 0.5:
        response = requests.post(url_like, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"{user['account_id']} liked post {post_id}")
        else:
            print(f"Failed to like post {post_id} for {user['account_id']}")
    

def daily_post_and_interact():
    post_ids = []
    used_templates = set()

    # 登入每個用戶
    for user in users:
        login(user)

    # 每個用戶發文
    for user in users:
        post_id = post_content(user , used_templates)
        if post_id:
            post_ids.append(post_id)
        time.sleep(random.randint(1, 5))  # 發文間隔

    # 互動
    for user in users:
        for post_id , post_account_id in post_ids:
            if post_id:  
                like_and_post(user, post_id, post_account_id)
                time.sleep(random.randint(1, 3))  # 按讚間隔

# daily_post_and_interact()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # 測試腳本的執行時間
    scheduler.add_job(daily_post_and_interact, 'cron', hour=23, minute=59)
    
    print("Starting scheduled tasks...")
    scheduler.start()