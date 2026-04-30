import requests
import os
import csv
import datetime

URL = "import requests
import time
import logging

# 配置日志
logging.basicConfig(filename='inventory_monitor.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# 商品URL
url = " https://www.kmonstar.com.tw/products/%E6%87%89%E5%8B%9F-260522-woodz-1st-full-album-archive-1-%E5%B0%88%E8%BC%AF%E7%99%BC%E8%A1%8C%E7%B4%80%E5%BF%B5%E7%B0%BD%E5%90%8D%E6%9C%83-in-taipei.json"

# 初始化上一次的库存数量
last_inventory_quantity =0

def get_inventory_quantity():
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        inventory_quantity = data['variants'][0]['inventory_quantity']
        return inventory_quantity
    except requests.exceptions.RequestException as e:
        logging.error(f"请求失败: {e}")
        return None

def monitor_inventory():
    global last_inventory_quantity
    while True:
        current_inventory_quantity = get_inventory_quantity()
        if current_inventory_quantity is not None:
            if current_inventory_quantity != last_inventory_quantity:
                change = current_inventory_quantity - last_inventory_quantity
                logging.info(f"库存变化: {last_inventory_quantity} -> {current_inventory_quantity}, 变化差值: {change}")
                last_inventory_quantity = current_inventory_quantity
        time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    monitor_inventory().json"
CSV_FILE = "inventory_history.csv"

def run_monitor():
    try:
        # 1. 抓取庫存 (模擬瀏覽器)
        res = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        current_qty = res.json()['variants'][0].get('inventory_quantity', 0)
        
        # 2. 檢查有沒有舊的 CSV 紀錄
        last_qty = None
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                lines = list(csv.reader(f))
                if len(lines) > 1:
                    last_qty = int(lines[-1][2]) # 抓取最後一行的「新庫存」那一欄

        # 3. 比對：如果庫存變了，或者還沒有紀錄過
        if last_qty is None or current_qty != last_qty:
            # 取得台北時間
            now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            diff = current_qty - last_qty if last_qty is not None else 0
            
            file_exists = os.path.isfile(CSV_FILE)
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["時間", "舊庫存", "新庫存", "變動量"])
                writer.writerow([now, last_qty if last_qty is not None else "N/A", current_qty, f"{diff:+=d}"])
            
            # 產生一個臨時文件，告訴 GitHub 說「真的有變動，請上傳」
            with open('changed.txt', 'w') as f: f.write('yes')
            print(f"發現變動！目前庫存：{current_qty}")
        else:
            print("庫存沒變，不執行存檔動作。")

    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    run_monitor()
