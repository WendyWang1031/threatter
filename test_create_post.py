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
    {"account_id": "5566", "password": "5566"},
    {"account_id": "pudding", "password": "pudding"},
    {"account_id": "gctab252906", "password": "gctab252906"},
    {"account_id": "yzmso6437", "password": "yzmso6437"},
    {"account_id": "ikbig663", "password": "ikbig663"},
    {"account_id": "ydtif750948", "password": "ydtif750948"},
    {"account_id": "zyny8104", "password": "zyny8104"},
    {"account_id": "bxnpp095", "password": "bxnpp095"},
    {"account_id": "kptqu153", "password": "kptqu153"},
    {"account_id": "poat450588", "password": "poat450588"},
    {"account_id": "esxjg48232", "password": "esxjg48232"},
    {"account_id": "jqdx54297", "password": "jqdx54297"},
    {"account_id": "tmwg05163", "password": "tmwg05163"},
    {"account_id": "eijcp24502", "password": "eijcp24502"},
    {"account_id": "kaehu018", "password": "kaehu018"},
    {"account_id": "ghnto2993", "password": "ghnto2993"},
    {"account_id": "ozfqy0625", "password": "ozfqy0625"},
    {"account_id": "zzic319", "password": "zzic319"},
    {"account_id": "ioats200", "password": "ioats200"},
    
]

post_templates = [
    "你那裡的天氣如何呢？",
    "我想上來看看看有沒有新消息！",
    "一個字毀掉一部電影",
    "這裡講政治，會發生什麼事情？",
    "推薦一部你看過最喜歡的電影",
    "推薦一本你看過最喜歡的書",
    "一句話，遇到已讀不回怎麼辦？",
    "一句話，遇到不讀不回怎麼辦？",
    "不懂就問，後端工程師平常在幹嘛？",
    "不懂就問，前端工程師平常在幹嘛？",
    "不懂就問，nginx是什麼？",
    "不懂就問，cdn是什麼？",
    "麥當勞最好吃的是非薯餅、雞塊莫屬",
    "有誰沒被摩斯漢堡的雞塊燙過？",
    "這裡有誰是轉職成工程師的呢？",
    "真是太神奇了～傑克！",
    "據說這裡可以看人吵架",
    "聽說 ikea 甜甜圈燈很難買，有誰成功購買到？",
    "我也想去吃藏壽司，最近有吉伊卡哇的壽司扭蛋QQ",
    "近期最推薦的一本書？",
    "I人？E人？都幾？",
    "大家都聽誰的 Podcast ？",

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

daily_post_and_interact()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # 測試腳本的執行時間
    scheduler.add_job(daily_post_and_interact, 'cron', hour=23, minute=59)
    
    print("Starting scheduled tasks...")
    scheduler.start()