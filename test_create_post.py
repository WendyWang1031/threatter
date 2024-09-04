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
    "你們覺得未來 10 年，AI 和機器人會取代哪些工作？",
    "如果只能選一個，寧願永遠不用手機還是永遠不能旅行？📱✈️ 選哪個會最難受？",
    "社交媒體的出現讓我們更接近還是更疏遠了？",
    "如果你今天只能用三個詞來形容自己的一天，你會選哪三個詞？",
    "如果動物可以說話，你最想和哪種動物聊天？🐶🦁 我個人很想知道貓每天都在想什麼！",
    "每個人都有些奇怪的小習慣，比如我喜歡把薯條一根根排整齊再吃 大家有沒有類似的小習慣",
    "你有沒有做過非常奇怪的夢？",
    "你今天遇到的最開心的事是什麼？",
    "來個謎語挑戰！我來出題，你們來解答：'什麼東西越分享越多，卻不會變少？",
    "如果今天你只能選一首歌來代表你的心情，你會選哪首？🎶",
    "你有沒有什麼讓人覺得奇怪但你超愛的食物搭配？",
    "你們有沒有在日常生活中遇到一些小困惑，卻又無法解釋？比如：為什麼襪子總是只會少一隻？😂 還有，為什麼手上的咖啡總是在走路時溢出來？",
    "如果不考慮時間和金錢，你最想去哪裡度假？",
    "大家小時候最喜歡的動畫是什麼？📺 我記得我每天都盯著電視看《神奇寶貝》，甚至想像自己也能當個訓練師！",


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