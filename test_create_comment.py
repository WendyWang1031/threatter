import random
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

environment = os.getenv("ENVIRONMENT", "local")
base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

users = [
    {"account_id": "ygxje0062", "password": "ygxje0062"},
    {"account_id": "izxh728", "password": "izxh728"},
    {"account_id": "kwjq55064", "password": "kwjq55064"},
    {"account_id": "vqur22561", "password": "vqur22561"},
    {"account_id": "beezu249796", "password": "beezu249796"},
    {"account_id": "ydtif750948", "password": "ydtif750948"},
    {"account_id": "tslqd7005", "password": "tslqd7005"},
    {"account_id": "pepx035335", "password": "pepx035335"},
    {"account_id": "rclcg797595", "password": "rclcg797595"},
    {"account_id": "zblu786761", "password": "zblu786761"},
    {"account_id": "kloin3605", "password": "kloin3605"},
    {"account_id": "uaduq409439", "password": "uaduq409439"},
    {"account_id": "wngyp399142", "password": "wngyp399142"},
    {"account_id": "nkxbn80472", "password": "nkxbn80472"},
    {"account_id": "rjtu517640", "password": "rjtu517640"},
    {"account_id": "wzbp403928", "password": "wzbp403928"},
    {"account_id": "itqk0380", "password": "itqk0380"},
    {"account_id": "qxth827", "password": "qxth827"},
    {"account_id": "wvgk7478", "password": "wvgk7478"}
    
]

posts = [
    {"post_id": "P-e2903114", "account_id": "eijcp24502"},
    # {"post_id": "P-48f1be56", "account_id": "tmwg05163"},
    # {"post_id": "P-ed0b5001", "account_id": "jqdx54297"},
    # {"post_id": "P-1953689b", "account_id": "esxjg48232"},
    # {"post_id": "P-4ba53c05", "account_id": "poat450588"},
    # {"post_id": "P-92a09bc5", "account_id": "kptqu153"},
    # {"post_id": "P-1c39e68f", "account_id": "bxnpp095"},
    # {"post_id": "P-1ab5a502", "account_id": "zyny8104"},
    # {"post_id": "P-f3eecdd3", "account_id": "ydtif750948"},
    # {"post_id": "P-cca3731e", "account_id": "ikbig663"},
    # {"post_id": "P-5d626c32", "account_id": "yzmso6437"},
    # {"post_id": "P-3f44d874", "account_id": "gctab252906"},
    # {"post_id": "P-a663ec43", "account_id": "pudding"},
    # {"post_id": "P-c9965727", "account_id": "5566"}
    
]

comment_texts = [
    "咖啡、會議、加班",
    "陽光、放鬆、音樂",
    "挑戰、突破、成就",
    "混亂、意外、驚喜",
    "美食、朋友、歡笑",
    "運動、疲憊、滿足",
    "專注、學習、成長",
    "經痛、發瘋、躺平",
    "躺著、發呆、不說話",
    "看書、追劇、吃零食",
    "聽廣播、追串文、看廢文",
    "發瘋、發瘋、發瘋",
    "emo、emo、emo"

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

def comment_on_post(user, post, comment_text):
    url_reply = f"{base_url}/api/member/{post['account_id']}/post/{post['post_id']}/reply"
    headers = {"Authorization": f"Bearer {user['token']}"}
    payload = {
        "content": {
            "text": comment_text,
            "media": {
                "images": None,
                "videos": None,
                "audios": None
            }
        },
        "visibility": "public"
    }

    try:
        response = requests.post(url_reply, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"{user['account_id']} commented on post {post['post_id']} from {post['account_id']}")
        else:
            print(f"Failed to comment on post {post['post_id']} for {user['account_id']}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error commenting on post for {user['account_id']}: {e}")

def mass_comment_simulation(users, post, max_workers=5):
    
    for user in users:
        login(user)
    
    batch_size = 2  
    for i in range(0, len(users), batch_size):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for user in users[i:i + batch_size]:
                comment_text = random.choice(comment_texts)
                futures.append(executor.submit(comment_on_post, user, post, comment_text))

            for future in as_completed(futures):
                future.result()

        time.sleep(random.uniform(3, 5))  

specific_post = {"post_id": "P-e2903114", "account_id": "eijcp24502"}
mass_comment_simulation(users, specific_post, max_workers=5)


if __name__ == "__app__":
    mass_comment_simulation(users, posts, max_workers=10)