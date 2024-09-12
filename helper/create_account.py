import random
import string
import requests
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

environment = os.getenv("ENVIRONMENT", "local")
base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

def generate_account_password():
    letters = random.choices(string.ascii_lowercase, k=random.randint(4, 5))  # 隨機選取 4-5 個英文字母
    numbers = random.choices(string.digits, k=random.randint(3, 6))           # 隨機選取 3-6 個數字
    return ''.join(letters + numbers)

def register(account_id, password):
    url = f"{base_url}/api/user"
    data = {
        "name": account_id ,
        "account_id": account_id,
        "email": f"{account_id}@example.com",
        "password": password
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Account {account_id} registered successfully.")
    else:
        print(f"Failed to register account {account_id}. Status code: {response.status_code}")



print(f"Running in {environment} environment with base URL: {base_url}")

# 生成 20 組帳號和密碼
accounts = [(generate_account_password(),) * 2 for _ in range(20)]

# 註冊新的帳號
for account_id, password in accounts:
    register(account_id, password)