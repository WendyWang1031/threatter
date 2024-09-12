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

post_templates = [
    "為什麼沒有披薩香水？",
    "今天本來打算去健身房，但最後發現沙發的引力太強，實在無法抗拒……所以，選擇躺著，順便給自己下了一個健身延期的通知",
    "如果今天你只能用反邏輯的方式來做事情，你會怎麼做？🤔 例如，用筷子喝湯",
    "你們有沒有一些聽起來很奇怪但會偷偷遵守的小迷信？比如我媽媽總說，晚上不能剪指甲，不然會倒霉。但我從來沒試過，因為有點怕驗證結果。",
    "如果你可以擁有一個完全沒什麼用但超搞笑的超能力，你會選什麼？我會選擇瞬間長出一頭完美髮型，每當有人想拍照時，我的頭髮立刻變得像剛出沙龍一樣完美無瑕！",
    "每如果食物有星座，你覺得不同的食物會屬於哪個星座？🍔🍕比如，披薩應該是射手座，因為它總是變幻莫測、讓人驚喜，而咖啡應該是摩羯座，穩重、可靠且讓人精神百倍",
    "如果你只能用一隻手來做家務，你會怎麼做？",
    "如果你能開一家完全沒人想去但你超愛的商店，你會賣什麼？我想開一家專門賣只剩單隻的襪子商店，專門給那些失去另一隻襪子的靈魂找到安慰。",
    "來個謎語挑戰！我來出題，你們來解答：'什麼東西越分享越多，卻不會變少？",
    "如果你可以穿越到一個歷史上完全奇怪又搞笑的時代，你會去哪裡？我會選擇穿越到法國大革命的時候，但不是參加革命，而是賣法式馬卡龍，因為那個時候大家肯定需要甜點安慰自己。",
    "大家有沒有學過一些奇怪但毫無實際用途的知識？我發現，鴨子的呱呱聲不會產生回音",
    "如果你可以選擇擁有一個來自奇幻世界的魔法物品，你會選什麼？我會選擇一個可以瞬間召喚任何食物的魔法盤子",
    "如果今天你必須把生活中所有事都反過來做，你會怎麼做？比如倒著走路、反著穿衣服，或者用左手寫字！",
    "如果外星人有自己的社交媒體平台，你覺得他們會發什麼內容？",
    "如果你可以發明一種超古怪但你超愛的零食，它會是什麼？我想發明一款薯條口味的棒棒糖，這樣吃起來既有鹹味又有甜味，而且永遠不會掉在地上",
    "如果學校裡有一門搞笑課程，你覺得它會教什麼？📚😂比如'沙發學入門'，教你如何以最舒適的姿勢躺在沙發上看電視，或者'薯片哲學'，探討為什麼每袋薯片裡空氣總是比薯片多。",
    "如果家裡的物品突然有了人格並且會說話，你覺得它們會說什麼？我的沙發應該會說：'夠了，別再坐我身上了！我快要被壓扁了",
    "如果你今天只能說一個字，你會選什麼字？我應該會選'吃'",
    "如果你的寵物突然擁有了魔法能力，你覺得牠會做什麼？我的貓肯定會用魔法每天自動開罐頭",
    "如果你能發明一樣完全沒什麼用但超搞笑的東西，你會發明什麼？💡我會發明一個自動翻頁器，專門幫我在床上看書時翻頁，這樣我就可以繼續躺著不動",
    "你有沒有什麼超無用但你特別得意的技能？我會用筷子把一粒米精確夾到特定的地方，雖然完全沒用，但每次都讓我覺得自己是筷子界的神！",
    "如果你能預言未來，但只能預測一些完全沒用的事情，你會預言什麼？",
    "假如你今天發現你有超能力，但只能用一次，你會怎麼做？我可能會選擇瞬間移動到世界上最棒的餐廳，然後點滿所有的甜點！",
    "如果你這輩子只能吃一種食物，你會選什麼？",
    "如果動物能打工，你覺得牠們會做什麼職業？",
    "我有一次夢到自己變成了一隻會飛的漢堡，還參加了一場美食大賽，結果贏得了一座'番茄醬獎杯'！",
    "如果未來的科技讓你可以選擇變成半機器人，你會選擇哪個身體部位進行改造？我會選擇改造我的大腦，這樣我再也不用擔心忘記重要的事情了！",
    "假如你可以回到過去，但只能做一件超級無聊的事，你會選什麼？我會回到石器時代，給原始人表演用火柴生火，然後拍拍屁股走人",
    "如果未來10年裡有一個生活習慣變得超級奇怪，你覺得會是什麼？我猜可能大家會每天背著飛行背包上班，順便在空中喝咖啡，一邊飛一邊開會",
    "如果你能擁有一個隨時可以從口袋裡取出的無限道具，你會選什麼？",
    "假如生活中突然多了一條奇怪規則，你覺得會是什麼？也許所有人出門都必須穿兩頂帽子",
    "假如你喝的飲料突然有了奇怪的額外效果，你會希望是什麼？我希望每次喝咖啡都能瞬間變得超清醒，而且能自動完成工作，這樣我就能躺著等結果了",
    "假如天氣預報突然變得超級奇怪，你覺得會預報什麼樣的天氣？可能會有天氣預報說：'今天會下爆米花雨，記得帶上你的鍋子接住美味",
    "假如所有日常物品突然顛覆了使用方式，你覺得會怎麼樣？也許你得用電視遙控器煮飯，或者用牙刷開門……",
    "如果你擁有一個隨時可以變出任何東西的魔法袋，你會每天變出什麼？我會變出無限數量的暖暖包",


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