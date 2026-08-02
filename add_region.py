import pandas as pd

# 读取现有的 CSV
df = pd.read_csv('source_list.csv', encoding='utf-8')

# 添加 region 列，所有值设为 'zh-CN'
df['region'] = 'zh-CN'

# 保存为新文件
df.to_csv('source_list_with_region.csv', index=False, encoding='utf-8')

print(f"✅ 已生成 source_list_with_region.csv，共 {len(df)} 条记录")
