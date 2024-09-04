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
    "《Happy》 by Pharrell Williams",
    "《Eye of the Tiger》！今天真的是戰鬥模式，挑戰滿滿的一天！",
    "《Banana Pancakes》 by Jack Johnson，今天的節奏就是慢悠悠的。",
    "《Someone Like You》 by Adele，今天的心情有點低落，這首歌陪我度過。",
    "《Can’t Stop the Feeling》 by Justin Timberlake！今天感覺超High，根本停不下來",
    "《Let It Go》 from Frozen！因為今天工作太多，我選擇'放下，隨它去～'！",
    "《I’m So Tired》 by Lauv & Troye Sivan，今天真的累到不行，只想睡一整天",
    "慢慢喜歡你—莫文蔚",
    "累—張惠妹，今天真的累爆了",
    "《On Top of the World》 by Imagine Dragons",
    "《Dancing Queen》 by ABBA",
    "落日飛車 Young Man ",
    "Back In Love - Leisure",
    "'Good as Hell' by Lizzo",
    "'Work Hard, Play Hard' by Wiz Khalifa",
    "'Sunday Morning' by Maroon 5",
    "Fix You' by Coldplay",
    "落日飛車 金牛座的牢騷",
    "Uptown Funk' by Mark Ronson ft. Bruno Mars",
    "The Lazy Song' by Bruno Mars",
    "Somewhere Only We Know' by Keane",
    "Stayin' Alive' by Bee Gees",
    "Don't Stop Me Now' by Queen",
    "Yesterday' by The Beatles",
    "I Will Survive' by Gloria Gaynor",

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

specific_post = {"post_id": "P-1953689b", "account_id": "esxjg48232"}
mass_comment_simulation(users, specific_post, max_workers=5)


if __name__ == "__app__":
    mass_comment_simulation(users, posts, max_workers=10)