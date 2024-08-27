import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

base_url = "http://127.0.0.1:8000"

users = [
    {"account_id": "a", "password": "a"},
    {"account_id": "c", "password": "c"},
    {"account_id": "b", "password": "b"},
    {"account_id": "d", "password": "d"},
    {"account_id": "f", "password": "f"},
    
]

posts = [
    {"post_id": "P-5f0db1bd", "account_id": "meow"},
    {"post_id": "P-b875bc07", "account_id": "44"},
    {"post_id": "P-ebde1059", "account_id": "p1"},
    {"post_id": "P-5a63c406", "account_id": "p1"}
    
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

        time.sleep(random.uniform(1, 3))


mass_like_simulation(users, posts, max_workers=5)


if __name__ == "__app__":
    mass_like_simulation(users, posts, max_workers=10)