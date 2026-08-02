# fetch_only.py
import os
import time
import requests
import pandas as pd
import re

REGIONS = ['zh-CN', 'en-US', 'ja-JP', 'fr-FR', 'de-DE']
url_base = "https://cn.bing.com"

def fetch_region(region: str) -> list:
    try:
        api_url = f"https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt={region}&nc=1614319565639&pid=hp&FORM=BEHPTB&uhd=1"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        image_data = response.json()['images'][0]
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
