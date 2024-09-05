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
    {"post_id": "P-7f0733a3", "account_id": "ghnto2993"},
    {"post_id": "P-0f439702", "account_id": "kaehu018"},
    {"post_id": "P-6a45994b", "account_id": "eijcp24502"},
    {"post_id": "P-bd5ba466", "account_id": "tmwg05163"},
    {"post_id": "P-ce719820", "account_id": "jqdx54297"},
    {"post_id": "P-b2a23eb6", "account_id": "esxjg48232"},
    {"post_id": "P-03d3c282", "account_id": "poat450588"},
    {"post_id": "P-90ffbbf7", "account_id": "kptqu153"},
    {"post_id": "P-ac6231bd", "account_id": "bxnpp095"},
    {"post_id": "P-43237e38", "account_id": "zyny8104"},
    {"post_id": "P-9d081fcc", "account_id": "ydtif750948"},
    {"post_id": "P-2e9ef73c", "account_id": "ikbig663"},
    {"post_id": "P-ac3b9b0f", "account_id": "yzmso6437"},
    {"post_id": "P-749469ab", "account_id": "gctab252906"},
    {"post_id": "P-10f2807c", "account_id": "pudding"},
    {"post_id": "P-cbad07dd", "account_id": "5566"},
    {"post_id": "P-c758bab5", "account_id": "wvgk7478"},
    {"post_id": "P-3075cc64", "account_id": "qxth827"},
    {"post_id": "P-babfd7de", "account_id": "itqk0380"},
    {"post_id": "P-80e1efbc", "account_id": "wzbp403928"},
    {"post_id": "P-f55a7241", "account_id": "rjtu517640"},
    {"post_id": "P-1a873d0e", "account_id": "nkxbn80472"},
    {"post_id": "P-1cbbc51f", "account_id": "wngyp399142"},
    {"post_id": "P-5cd274fc", "account_id": "uaduq409439"},
    {"post_id": "P-5a4fc0f1", "account_id": "kloin3605"},
    {"post_id": "P-08b1b45f", "account_id": "zblu786761"},
    {"post_id": "P-db2be9ed", "account_id": "rclcg797595"},
    {"post_id": "P-09c0dca1", "account_id": "pepx035335"},
    {"post_id": "P-4054a9e3", "account_id": "tslqd7005"},
    {"post_id": "P-792a72c5", "account_id": "ydtif750948"},
    {"post_id": "P-d7d33194", "account_id": "beezu249796"},
    {"post_id": "P-1dbaef4a", "account_id": "vqur22561"},
    {"post_id": "P-a7b6eb1d", "account_id": "kwjq55064"},
    {"post_id": "P-39621649", "account_id": "izxh728"},
    {"post_id": "P-1a56e733", "account_id": "ygxje0062"}
    
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

def like_post(user, post):
    url_like = f"{base_url}/api/member/{post['account_id']}/post/{post['post_id']}/like"
    headers = {"Authorization": f"Bearer {user['token']}"}
    payload = {"like": True}

    try:
        response = requests.post(url_like, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"{user['account_id']} liked post {post['post_id']} from {post['account_id']}")
        else:
            print(f"Failed to like post {post['post_id']} for {user['account_id']}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error liking post for {user['account_id']}: {e}")

def mass_like_simulation(users, posts, max_workers=5):
    
    for user in users:
        login(user)
    
    batch_size = 2  
    for i in range(0, len(users), batch_size):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for user in users[i:i + batch_size]:
                post = random.choice(posts)  
                futures.append(executor.submit(like_post, user, post))

            for future in as_completed(futures):
                future.result()

        time.sleep(random.uniform(3, 3))


mass_like_simulation(users, posts, max_workers=5)


if __name__ == "__app__":
    mass_like_simulation(users, posts, max_workers=10)