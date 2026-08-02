# safe_merge.py - 修正版

import pandas as pd
import os
import re

HISTORY_FILE = "source_list.csv"
NEW_FILE = "new_data.csv"

def extract_image_id(url):
    """提取图片ID：只提取 OHR. 后面的部分，去掉地区后缀"""
    match = re.search(r'OHR\.([A-Za-z0-9]+)', str(url))
    if match:
        return match.group(1)
    return url

print("=" * 60)
print("🔄 开始安全合并...")

# 1. 读取历史数据
if os.path.exists(HISTORY_FILE):
    history_df = pd.read_csv(HISTORY_FILE, encoding='utf-8')
    print(f"📚 历史数据: {len(history_df)} 条")
else:
    history_df = pd.DataFrame(columns=['date', 'title', 'url', 'description', 'region'])
    print("ℹ️ 没有找到历史数据，将创建新文件")

# 2. 读取新数据
if not os.path.exists(NEW_FILE):
    print("⚠️ 没有新数据需要合并")
    exit(0)

new_df = pd.read_csv(NEW_FILE, encoding='utf-8')
print(f"🆕 新数据: {len(new_df)} 条")

# 3. 合并
combined_df = pd.concat([history_df, new_df], ignore_index=True)

# ★★★ 关键修复：提取图片ID ★★★
combined_df['image_id'] = combined_df['url'].apply(extract_image_id)

print(f"📊 合并后总记录数: {len(combined_df)}")
print(f"📊 唯一 image_id: {combined_df['image_id'].nunique()} 个")

# ★★★ 按 (date, image_id) 去重 ★★★
combined_df = combined_df.drop_duplicates(subset=['date', 'image_id'], keep='first')

print(f"📊 去重后总记录数: {len(combined_df)}")

# 6. 删除辅助列
combined_df = combined_df.drop(columns=['image_id'])
combined_df = combined_df.sort_values('date', ascending=False).reset_index(drop=True)

# 7. 保存
combined_df.to_csv(HISTORY_FILE, index=False, encoding='utf-8')
print(f"✅ 已保存到 {HISTORY_FILE}，共 {len(combined_df)} 条记录")
print("=" * 60)
