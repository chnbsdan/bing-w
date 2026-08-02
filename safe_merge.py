# safe_merge.py
import pandas as pd
import os
import re

HISTORY_FILE = "source_list.csv"
NEW_FILE = "new_data.csv"

def extract_image_id(url):
    match = re.search(r'OHR\.([^_]+)', str(url))
    return match.group(1) if match else url

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

# 3. 合并（历史数据 + 新数据）
combined_df = pd.concat([history_df, new_df], ignore_index=True)
print(f"📊 合并后总数（去重前）: {len(combined_df)} 条")

# 4. 提取图片ID
combined_df['image_id'] = combined_df['url'].apply(extract_image_id)

# 5. ★★★ 核心：按 (date, image_id) 去重，保留第一条（历史优先）★★★
combined_df = combined_df.drop_duplicates(subset=['date', 'image_id'], keep='first')
print(f"📊 去重后总数: {len(combined_df)} 条")

# 6. 删除辅助列，排序
combined_df = combined_df.drop(columns=['image_id'])
combined_df = combined_df.sort_values('date', ascending=False).reset_index(drop=True)

# 7. ★★★ 直接覆盖写入 source_list.csv ★★★
combined_df.to_csv(HISTORY_FILE, index=False, encoding='utf-8')
print(f"✅ 已保存到 {HISTORY_FILE}，共 {len(combined_df)} 条记录")
print("=" * 60)
