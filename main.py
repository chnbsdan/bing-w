# main.py - 完整修正版（支持多地区抓取 + 安全追加数据，绝不覆盖历史）

import os
import time
import argparse
import requests
import pandas as pd
import FileOperations as file_op
from HTMLGenerator import Generator

database = "./source_list.csv"
img_dir = "./wallpaper/images"
subpages_dir = "./wallpaper/subpages"
cache_dir = "./cache"
backup_dir = "./backup"
url_base = "https://cn.bing.com"
img_prefix = "BW"
MSG_LEN = 50

# ★★★ 定义要抓取的所有地区列表 ★★★
REGIONS = ['zh-CN', 'en-US', 'ja-JP', 'fr-FR', 'de-DE']

def get_current_time():
    return time.strftime('%H:%M:%S')

def notify(message):
    print(f'-> ({get_current_time()}) {message}')

def create_parser():
    parser = argparse.ArgumentParser(
        description='Bing Wallpaper Fetcher (Multi-Region)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--image-only', action='store_true', help='Download images only')
    group.add_argument('--html-only', action='store_true', help='Generate HTML only')
    parser.add_argument('--update', action='store_true', help='Update database only')
    parser.add_argument('--keep-cache', action='store_true', help='Keep temporary files')
    parser.add_argument('--no-image', action='store_true', help='Do not download images')
    parser.add_argument('--no-html', action='store_true', help='Do not generate HTML')
    parser.add_argument('--no-fetch', action='store_true', help='Do not update source_list')
    parser.add_argument('--no-history', action='store_true', help='Caution! Overwrite existing source list.')
    parser.add_argument('--column-number', type=int, default=3, help='Number of images per row in HTML')
    parser.add_argument('--use-wget', action='store_true', help='Use system wget to download data')
    return parser

def validate_arguments(args):
    if args.image_only and args.html_only:
        raise ValueError("--image-only and --html-only are mutually exclusive")
    if args.image_only:
        return (True, False)
    if args.html_only:
        return (False, True)
    download = not args.no_image
    generate = not args.no_html
    if args.update:
        return (False, False)
    return (download, generate)

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        notify(f"Created directory: {path}")

def load_database(database_path: str, no_history: bool) -> pd.DataFrame:
    required_columns = ['date', 'title', 'url', 'description', 'region']
    
    if os.path.exists(database_path) and not no_history:
        try:
            df = pd.read_csv(database_path, encoding='utf-8')
            # 如果缺少 region 列，自动添加并填充 'zh-CN'
            if 'region' not in df.columns:
                df['region'] = 'zh-CN'
                notify("Added 'region' column with default value 'zh-CN'")
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                notify(f"Database missing required fields: {', '.join(missing_cols)}")
                return pd.DataFrame(columns=required_columns)
            return df[required_columns].astype({'date': str, 'region': str})
        except Exception as e:
            notify(f"Failed to load database: {str(e)}")
            return pd.DataFrame(columns=required_columns)
    
    if args.no_fetch:
        raise FileNotFoundError("No existing database found when --no-fetch is enabled")
    return pd.DataFrame(columns=required_columns)

def fetch_region(region: str) -> list:
    """获取指定地区的壁纸数据（只抓取当天）"""
    try:
        # ★★★ 强制只抓取当天（idx=0）★★★
        api_url = f"https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt={region}&nc=1614319565639&pid=hp&FORM=BEHPTB&uhd=1"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        image_data = response.json()['images'][0]
        
        # ★★★ 获取当前日期（按北京时间）★★★
        from datetime import datetime, timezone, timedelta
        beijing_tz = timezone(timedelta(hours=8))
        today = datetime.now(beijing_tz).strftime('%Y%m%d')
        
        # ★★★ 如果抓到的日期不是今天，跳过 ★★★
        if image_data['enddate'] != today:
            notify(f"Region {region}: Skipping {image_data['enddate']} (not today)")
            return []
        
        return [{
            'date': image_data['enddate'],
            'title': image_data['title'],
            'url': f"{url_base}{image_data['urlbase']}_UHD.jpg",
            'description': image_data['copyright'],
            'region': region
        }]
    except Exception as e:
        notify(f"Failed to fetch region {region}: {str(e)}")
        return []

def update_database(existing_df: pd.DataFrame) -> pd.DataFrame:
    """更新数据库 - 安全地追加新数据，绝不覆盖历史记录"""
    all_new_records = []
    
    # 获取当前日期（北京时间）
    from datetime import datetime, timezone, timedelta
    beijing_tz = timezone(timedelta(hours=8))
    today = datetime.now(beijing_tz).strftime('%Y%m%d')
    notify(f"Today is: {today}")
    
    # 1. 抓取所有地区的新数据
    for region in REGIONS:
        notify(f'Requesting Bing API for region: {region}...')
        records = fetch_region(region)
        if records:
            all_new_records.extend(records)
            notify(f'Region {region} fetched successfully')
    
    if not all_new_records:
        notify("No new records fetched from any region")
        return existing_df
    
    new_df = pd.DataFrame(all_new_records).astype({'date': str, 'region': str})
    
    # 2. 确保现有数据有 region 列
    if 'region' not in existing_df.columns:
        existing_df['region'] = 'zh-CN'
        notify("Existing data missing 'region' column, set to 'zh-CN'")
    
    # ★★★ 3. 关键修复：合并数据，保留所有历史 ★★★
    # 创建一个包含所有现有记录唯一标识的集合 (date, region)
    existing_keys = set(zip(existing_df['date'], existing_df['region']))
    
    # 只选择新数据中 (date, region) 组合不存在于现有数据的记录
    new_records_to_add = []
    for _, row in new_df.iterrows():
        if (row['date'], row['region']) not in existing_keys:
            new_records_to_add.append(row)
    
    if new_records_to_add:
        # 将新记录追加到现有数据中
        new_df_to_add = pd.DataFrame(new_records_to_add)
        combined_df = pd.concat([existing_df, new_df_to_add], ignore_index=True)
        combined_df = combined_df.sort_values(['date', 'region'], ascending=[False, True]).reset_index(drop=True)
        notify(f"✅ 成功追加 {len(new_records_to_add)} 条新记录")
    else:
        combined_df = existing_df
        notify("ℹ️ 没有发现需要追加的新记录")
    
    # 4. 保存
    try:
        combined_df.to_csv(database, index=False, encoding='utf-8')
        notify(f"📊 数据库总记录数: {len(combined_df)}")
    except IOError as e:
        notify(f"❌ 保存数据库失败: {str(e)}")
    
    return combined_df

def download_images_task(src_df, img_dir, cache_dir, img_prefix, use_wget):
    downloaded_imgs = os.listdir(img_dir)
    for date_str, url in zip(src_df['date'], src_df['url']):
        try:
            target_file = f'{img_prefix}-{date_str[2:]}.jpg'
            if target_file in downloaded_imgs:
                continue
            cache_file = f'{cache_dir}/img_cache'
            if use_wget:
                os.system(f'wget -q -O {cache_file} {url}')
            else:
                response = requests.get(url)
                response.raise_for_status()
                with open(cache_file, 'wb') as f:
                    f.write(response.content)
            file_op.move_files(cache_file, os.path.join(img_dir, target_file))
            notify(f'{target_file} downloaded')
        except Exception as e:
            notify(f"Download failed for {target_file}: {str(e)}")

def generate_html_task(src_df, subpages_dir, column_number):
    try:
        hg = Generator(
            src_df['date'], 
            src_df['url'], 
            src_df['title'], 
            src_df['description'],
            col=column_number
        )
        num = hg.generate_all()
        with open(f'{cache_dir}/index.html', 'w', encoding='utf8') as f:
            f.write(hg.mainpage)
        for key in hg.subpages.keys():
            with open(f'{cache_dir}/page-{key}.html', 'w', encoding='utf8') as f:
                f.write(hg.subpages[key])
        if num > 0:
            file_op.copy_files(f'{cache_dir}/index.html', 'wallpaper/')
            file_op.copy_files(f'{cache_dir}/page-*.html', subpages_dir)
        notify(f'Successfully generated wallpaper/index.html')
        notify(f'Generated {num} subpages to {subpages_dir}/')
    except Exception as e:
        notify(f"HTML generation failed: {str(e)}")
        raise

if __name__ == "__main__":
    parser = create_parser()
    global args
    args = parser.parse_args()
    
    try:
        download_images, generate_html = validate_arguments(args)
    except ValueError as e:
        print(f"Argument error: {e}")
        parser.print_help()
        exit(1)
    
    required_dirs = [img_dir, subpages_dir, cache_dir, backup_dir]
    for directory in required_dirs:
        ensure_directory(directory)
    
    print('>' * MSG_LEN)
    print('\t', time.ctime())
    print('>' * MSG_LEN)
    
    try:
        src = load_database(database, args.no_history)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        exit(1)
    
    if not args.no_fetch:
        try:
            src = update_database(src)
        except requests.HTTPError:
            notify("Continuing with local database")
    
    if download_images:
        try:
            download_images_task(src, img_dir, cache_dir, img_prefix, args.use_wget)
        except Exception as e:
            print(f"Image download task failed: {str(e)}")
            exit(1)
    
    if generate_html:
        try:
            generate_html_task(src, subpages_dir, args.column_number)
        except Exception as e:
            print(f"HTML generation task failed: {str(e)}")
            exit(1)
    
    if not args.keep_cache:
        try:
            file_op.remove_files(f'{cache_dir}/img_cache')
            file_op.remove_files(f'{cache_dir}/*.html')
            notify("Cache files cleaned")
        except Exception as e:
            notify(f"Failed to clean cache: {str(e)}")
    else:
        notify("Cache files retained")
    
    print('<' * MSG_LEN, end='\n\n')
    exit(0)
