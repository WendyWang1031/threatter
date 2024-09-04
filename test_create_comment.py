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
    {"account_id": "wvgk7478", "password": "wvgk7478"},
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

posts = [
    {"post_id": "P-e2903114", "account_id": "eijcp24502"},
    {"post_id": "P-48f1be56", "account_id": "tmwg05163"},
    {"post_id": "P-ed0b5001", "account_id": "jqdx54297"},
    {"post_id": "P-1953689b", "account_id": "esxjg48232"},
    {"post_id": "P-4ba53c05", "account_id": "poat450588"},
    {"post_id": "P-92a09bc5", "account_id": "kptqu153"},
    {"post_id": "P-1c39e68f", "account_id": "bxnpp095"},
    {"post_id": "P-1ab5a502", "account_id": "zyny8104"},
    {"post_id": "P-f3eecdd3", "account_id": "ydtif750948"},
    {"post_id": "P-cca3731e", "account_id": "ikbig663"},
    {"post_id": "P-5d626c32", "account_id": "yzmso6437"},
    {"post_id": "P-3f44d874", "account_id": "gctab252906"},
    {"post_id": "P-a663ec43", "account_id": "pudding"},
    {"post_id": "P-c9965727", "account_id": "5566"}
    
]

comment_texts = [
    "馬爾地夫吧！不過我得確保有Wi-Fi，不然我就沒法在沙灘上懶散地刷手機了。",
    "我想去哈利波特的魔法學校！學個咒語，然後瞬間移動回家就不怕錯過任何假期了！",
    "我想去南極！看看企鵝怎麼滑冰，然後和牠們一起來個冰上派對。",
    "我選加勒比海，躺在吊床上喝椰子汁，看著海盜船從遠處漂過。",
    "我想去月球，順便幫NASA測試下新的月球漫步姿勢",
    "我想去日本，吃遍所有的拉麵和壽司",
    "我想去環球影城",
    "我想去火星，然後成為第一個在外星拍Vlog的地球人",
    "我想去北極，和北極熊一起冰上散步",
    "我要去埃及，看金字塔和木乃伊，然後說服自己其實只是去曬太陽的",
    "我想去亞馬遜叢林",
    "我想去環遊世界，一邊打卡一邊拍美照，然後告訴朋友我只是'出去散散步",
    "我想去韓國追星",
    "我想去海王星，聽說那裡的風速超快，順便試試風速滑翔傘"

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

specific_post = {"post_id": "P-ed0b5001", "account_id": "jqdx54297"}
mass_comment_simulation(users, specific_post, max_workers=5)


if __name__ == "__app__":
    mass_comment_simulation(users, posts, max_workers=10)