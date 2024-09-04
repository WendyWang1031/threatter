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
    "我一定要把餐具按顏色或大小排好才開始吃，不然就會覺得不舒服",
    "我喜歡把爆米花按口味分好，再按順序吃，吃到最後感覺像在開美食會",
    "吃披薩一定要從邊緣開始吃，看能不能先吃掉所有餅邊再吃中心。",
    "我吃巧克力時一定要一小塊一小塊地慢慢吃，不能一次咬太大口",
    "我不管是什麼食物，都喜歡全部混在一起，這樣可以省事",
    "吃餅乾時，我一定要先把餅乾咬成完美的圓形！",
    "我吃三明治一定要先把麵包邊剝掉，最後才吃中間部分，因為這樣吃起來才有層次感",
    "我喝果汁前一定要先搖一搖，幻想自己像在調製一杯超高級雞尾酒",
    "直接用手抓",
    "喝咖啡時一定要先聞一聞香氣，閉上眼感受一下",
    "我喜歡一邊吃東西一邊思考人生的意義",
    "我吃餅乾前，先會把它掰成兩半，然後看哪邊的餡最多，再先吃餡少的那邊，讓最美味的留在最後 ",
    "吃冰淇淋的時候一定要先舔一圈邊緣，確保它不會融化滴下來",
    "我吃什麼都要跟家裡的貓分享一點",
    "每次吃蛋糕都要把外面的奶油先刮掉，因為我懷疑它們在圖謀不軌，糖分太高",
    "我每次吃飯都會看著手錶，確保吃飯的時間在20分鐘內結束",
    "我吃薯條的時候，總會偷偷留幾根，因為不想一次吃完",
    "我吃壽司一定要先把上面的魚片吃掉，再吃下面的米飯",
    "我吃三明治總是從中間咬下去，這樣可以省下兩邊的時間，直接進入核心",
    "我吃洋芋片時喜歡閉著眼睛隨便抓一片",
    "吃披薩時一定要把料全部挑出來吃，最後才吃餅皮",
    "我喝飲料時會先用吸管吸一口，然後再觀察杯子裡的水位，推算我還能喝幾口",
    "吃泡麵前一定要先把所有調味包按順序排列好，然後像在進行一場神聖儀式一樣倒進去",
    "我吃水果沙拉時，一定要把所有水果按顏色分類",
    "吃披薩時一定要把所有的餡料都撥到每一口都一樣多",
    "吃炸雞時一定要先把骨頭周圍的肉精確地啃乾淨",
    "吃漢堡時，總會先從一邊開始咬，然後轉著吃，最後變成一個奇怪的形狀",
    "吃壽司時，喜歡一口吞掉，因為感覺自己像忍者一樣迅速解決敵人",
    "吃甜點時總要先摸摸它，確認它沒有'偷偷'加太多糖，才敢下口",
    "我每次吃麥片，都會先把裡面的果乾撿出來",
    "我吃披薩時從餅皮開始",
    "吃零食時總會先留下最後一片",
    "我吃餅乾一定要先踩在地上",

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

specific_post = {"post_id": "P-1ab5a502", "account_id": "zyny8104"}
mass_comment_simulation(users, specific_post, max_workers=5)


if __name__ == "__app__":
    mass_comment_simulation(users, posts, max_workers=10)