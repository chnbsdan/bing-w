# fetch_only.py - 修正版

import os
import time
import requests
import pandas as pd
import re
from datetime import datetime, timezone, timedelta

REGIONS = ['zh-CN', 'en-US', 'ja-JP', 'fr-FR', 'de-DE']
url_base = "https://cn.bing.com"

def fetch_region(region: str) -> list:
    try:
        api_url = f"https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt={region}&nc=1614319565639&pid=hp&FORM=BEHPTB&uhd=1"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        image_data = response.json()['images'][0]
        
        # ★★★ 只保留当天的数据 ★★★
        beijing_tz = timezone(timedelta(hours=8))
        today = datetime.now(beijing_tz).strftime('%Y%m%d')
        
        if image_data['enddate'] != today:
            print(f"⚠️ {region}: 日期 {image_data['enddate']} 不是今天 ({today})，跳过")
            return []
        
        return [{
            'date': image_data['enddate'],
            'title': image_data['title'],
            'url': f"{url_base}{image_data['urlbase']}_UHD.jpg",
            'description': image_data['copyright'],
            'region': region
        }]
    except Exception as e:
        print(f"Failed to fetch {region}: {str(e)}")
        return []

def main():
    all_records = []
    for region in REGIONS:
        print(f"Fetching {region}...")
        records = fetch_region(region)
        if records:
            all_records.extend(records)
    
    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv('new_data.csv', index=False, encoding='utf-8')
        print(f"✅ 已抓取 {len(all_records)} 条记录，保存到 new_data.csv")
    else:
        print("⚠️ 没有抓取到任何数据")

if __name__ == "__main__":
    main()
