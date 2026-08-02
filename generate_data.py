import pandas as pd
import json
import os
from datetime import datetime

# 读取CSV
df = pd.read_csv('source_list.csv')

# 字段映射：CSV列名 → 模板需要的字段名
records = []
for _, row in df.iterrows():
    date_str = str(row['date']).strip()
    # 格式化日期为 YYYY-MM-DD
    if len(date_str) == 8:
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    else:
        formatted_date = date_str
    
    # 获取图片URL（必应UHD原图）
    img_url = row['url']
    if pd.isna(img_url) or not img_url:
        continue
    
    # 确保URL是完整的
    if not img_url.startswith('http'):
        img_url = 'https://cn.bing.com' + img_url
    
    record = {
        'date': formatted_date,
        'copyright': str(row['title']) if pd.notna(row['title']) else '',
        'description': str(row['description']) if pd.notna(row['description']) else '',
        'jpg': img_url,
        'webp': img_url,  # 如果有webp版本可以换，这里先用jpg
        'thumb': img_url.replace('_UHD.jpg', '_400x240.jpg')  # 生成缩略图URL
    }
    records.append(record)

# 按日期降序排列（最新的在前）
records.sort(key=lambda x: x['date'], reverse=True)

# 创建 data 目录（如果不存在）
os.makedirs('data', exist_ok=True)

# 保存为JSON文件（供HTML加载）
with open('data/wallpapers.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f'✅ 已生成 data/wallpapers.json，共 {len(records)} 张壁纸')

# 同时生成一个示例HTML（可选）
# 如果你想把数据直接嵌到HTML里而不是通过fetch加载，可以在这里生成
