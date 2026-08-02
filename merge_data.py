# merge_data.py - 独立合并脚本

import pandas as pd
import os
import re

HISTORY_FILE = "source_list.csv"
NEW_FILE = "new_data.csv"

def extract_image_id(url):
    match = re.search(r'OHR\.([^_]+)', str(url))
    return match.group(1) if match else url

print("=" * 50)
print("🔄 开始合并数据...")

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
print(f"🆕 新抓取数据: {len(new_df)} 条")

# 3. 合并
combined_df = pd.concat([history_df, new_df], ignore_index=True)

# 4. 提取图片ID
combined_df['image_id'] = combined_df['url'].apply(extract_image_id)

# 5. 按 (date, image_id) 去重，保留历史优先
before_count = len(combined_df)
combined_df = combined_df.drop_duplicates(subset=['date', 'image_id'], keep='first')
after_count = len(combined_df)

# 6. 删除辅助列，排序
combined_df = combined_df.drop(columns=['image_id'])
combined_df = combined_df.sort_values('date', ascending=False).reset_index(drop=True)

# 7. 保存
combined_df.to_csv(HISTORY_FILE, index=False, encoding='utf-8')
print(f"✅ 合并完成！去重前: {before_count} 条，去重后: {after_count} 条")
print(f"📊 总记录数: {len(combined_df)}")
print("=" * 50)
