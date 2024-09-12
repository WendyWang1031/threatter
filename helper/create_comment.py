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
    "巧克力淋在炸雞上",
    "喝咖啡的時候配薯條",
    "吃披薩一定要從邊緣開始吃，看能不能先吃掉所有餅邊再吃中心。",
    "酸黃瓜加上巧克力醬",
    "超愛把蘋果切片加上醬油",
    "把薯條沾冰淇淋吃",
    "我超愛把可樂加牛奶喝，感覺像是在喝一杯特別的'奶昔'",
    "我喜歡在草莓上撒點鹽",
    "用起司配蘋果",
    "喜歡把泡麵加進牛奶裡煮，感覺就像在吃一碗豪華的牛奶拉麵",
    "把胡蘿蔔片配上花生醬",
    "我喜歡把果汁加進麵條湯裡，讓湯有點果味 ",
    "我喜歡把炸雞配棉花糖，外脆內軟的對比口感",
    "我會把熱湯裡加冰塊",
    "把鹹魚乾配上巧克力醬",
    "吃餅乾喜歡先泡水再吃",
    "在咖啡裡加番茄醬",
    "意大利麵條和酸乳酪拌在一起，口感軟滑順口",
    "把洋芋片放進奶昔裡",
    "會把花生醬塗在洋芋片上",
    "喜歡把西瓜撒上胡椒粉",
    "我會把醬油加進奶茶裡，因為這樣喝起來有點鹹鹹的，感覺特別'厚'",
    "我會把甜甜圈配上黃瓜吃",
    "我喜歡把辣椒粉撒在冰淇淋上",
    "我會把熱狗裡加草莓醬",
    "皮蛋搭豆腐",
    "漢堡搭黑醋",
    "陽春麵搭紅油抄手醬",
    "麻辣鍋配冰淇淋",
    "棉花糖泡水喝",
    "仙貝拌牛奶當麥片吃",
    "花生配美乃滋",
    "生魚片配攪爛的布丁",

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

specific_post = {"post_id": "P-a663ec43", "account_id": "pudding"}
mass_comment_simulation(users, specific_post, max_workers=5)


if __name__ == "__app__":
    mass_comment_simulation(users, posts, max_workers=10)