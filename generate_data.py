# generate_data.py - 修改后的完整版本

import pandas as pd
import json
import os
from collections import defaultdict

# 读取CSV
df = pd.read_csv('source_list.csv')

# ★★★ 按日期分组，每个日期下包含所有地区 ★★★
records = []
date_groups = defaultdict(dict)

for _, row in df.iterrows():
    date_str = str(row['date']).strip()
    if len(date_str) == 8:
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    else:
        formatted_date = date_str
    
    img_url = row['url']
    if pd.isna(img_url) or not img_url:
        continue
    if not img_url.startswith('http'):
        img_url = 'https://cn.bing.com' + img_url
    
    region = row.get('region', 'zh-CN')
    
    # 按日期分组，每个日期下存储所有地区的数据
    date_groups[formatted_date][region] = {
        'title': str(row['title']) if pd.notna(row['title']) else '',
        'description': str(row['description']) if pd.notna(row['description']) else '',
        'jpg': img_url,
        'webp': img_url,
        'thumb': img_url.replace('_UHD.jpg', '_400x240.jpg')
    }

# ★★★ 构建新的 JSON 结构 ★★★
for date, regions in date_groups.items():
    records.append({
        'date': date,
        'regions': regions,
        # 保留第一个地区作为默认显示（用于兼容旧版前端）
        'copyright': list(regions.values())[0]['title'],
        'description': list(regions.values())[0]['description'],
        'jpg': list(regions.values())[0]['jpg'],
        'webp': list(regions.values())[0]['webp'],
        'thumb': list(regions.values())[0]['thumb']
    })

records.sort(key=lambda x: x['date'], reverse=True)

os.makedirs('data', exist_ok=True)

# ★★★ 同时保存两种格式 ★★★
# 1. 完整版：供新版前端使用（含所有地区）
with open('data/wallpapers_full.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

# 2. 兼容版：仅包含默认地区（zh-CN），供现有前端使用
compatible_records = []
for item in records:
    default_region = 'zh-CN'
    if default_region in item['regions']:
        r = item['regions'][default_region]
        compatible_records.append({
            'date': item['date'],
            'copyright': r['title'],
            'description': r['description'],
            'jpg': r['jpg'],
            'webp': r['webp'],
            'thumb': r['thumb']
        })
    else:
        # 如果没有 zh-CN，用第一个地区
        first_region = list(item['regions'].values())[0]
        compatible_records.append({
            'date': item['date'],
            'copyright': first_region['title'],
            'description': first_region['description'],
            'jpg': first_region['jpg'],
            'webp': first_region['webp'],
            'thumb': first_region['thumb']
        })

with open('data/wallpapers.json', 'w', encoding='utf-8') as f:
    json.dump(compatible_records, f, ensure_ascii=False, indent=2)

print(f'✅ 已生成 data/wallpapers.json，共 {len(compatible_records)} 张壁纸（默认地区）')
print(f'✅ 已生成 data/wallpapers_full.json，共 {len(records)} 张壁纸（含多地区）')
