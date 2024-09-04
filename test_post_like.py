import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

base_url = "http://127.0.0.1:8000"

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
    {"account_id": "ioats200", "password": "ioats200"}
    
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