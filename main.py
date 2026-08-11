# main.py - 全球地区版

import os
import time
import argparse
import requests
import pandas as pd
import re
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

# ★★★ 全球所有地区列表 ★★★
REGIONS = [
    # 亚洲
    'zh-CN', 'zh-HK', 'zh-TW',  # 中国（简体/香港/台湾）
    'ja-JP', 'ko-KR',           # 日本、韩国
    'hi-IN', 'ta-IN', 'te-IN',  # 印度
    'id-ID', 'ms-MY',           # 印尼、马来西亚
    'th-TH', 'vi-VN',           # 泰国、越南
    'fil-PH',                   # 菲律宾
    'ar-SA', 'ar-AE',           # 沙特、阿联酋
    'he-IL', 'tr-TR',           # 以色列、土耳其
    
    # 欧洲
    'en-GB', 'en-US',           # 英国、美国
    'fr-FR', 'de-DE',           # 法国、德国
    'it-IT', 'es-ES',           # 意大利、西班牙
    'pt-PT', 'pt-BR',           # 葡萄牙、巴西
    'nl-NL', 'be-NL',           # 荷兰
    'sv-SE', 'da-DK',           # 瑞典、丹麦
    'no-NO', 'fi-FI',           # 挪威、芬兰
    'pl-PL', 'cs-CZ',           # 波兰、捷克
    'hu-HU', 'ro-RO',           # 匈牙利、罗马尼亚
    'bg-BG', 'el-GR',           # 保加利亚、希腊
    'hr-HR', 'sl-SI',           # 克罗地亚、斯洛文尼亚
    'et-EE', 'lv-LV',           # 爱沙尼亚、拉脱维亚
    'lt-LT', 'sk-SK',           # 立陶宛、斯洛伐克
    'uk-UA', 'ru-RU',           # 乌克兰、俄罗斯
    
    # 美洲
    'en-CA', 'fr-CA',           # 加拿大（英语/法语）
    'es-MX', 'es-AR',           # 墨西哥、阿根廷
    'es-CL', 'es-CO',           # 智利、哥伦比亚
    'es-PE', 'es-VE',           # 秘鲁、委内瑞拉
    
    # 大洋洲
    'en-AU', 'en-NZ',           # 澳大利亚、新西兰
    
    # 非洲
    'af-ZA', 'en-ZA',           # 南非（南非语/英语）
    'ar-EG', 'ar-MA',           # 埃及、摩洛哥
]

def get_current_time():
    return time.strftime('%H:%M:%S')

def notify(message):
    print(f'-> ({get_current_time()}) {message}')

def create_parser():
    parser = argparse.ArgumentParser(
        description='Bing Wallpaper Fetcher - Global Edition',
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
    parser.add_argument('--save-raw', type=str, help='Save raw data to a file without merging')
    # ★★★ 新增：只抓取指定地区 ★★★
    parser.add_argument('--regions', type=str, help='Comma-separated list of regions to fetch (e.g. "zh-CN,en-US,ja-JP")')
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
            if 'region' not in df.columns:
                df['region'] = 'zh-CN'
                notify("Added 'region' column with default value 'zh-CN'")
            return df
        except Exception as e:
            notify(f"Failed to load database: {str(e)}")
            return pd.DataFrame(columns=required_columns)
    
    if args.no_fetch:
        raise FileNotFoundError("No existing database found when --no-fetch is enabled")
    return pd.DataFrame(columns=required_columns)

def extract_image_id(url: str) -> str:
    """从URL中提取图片ID（如 OHR.HelsinkiBlue）"""
    match = re.search(r'OHR\.([^_]+)', str(url))
    return match.group(1) if match else url

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
        # 静默跳过失败的地区（有些地区可能不支持）
        # notify(f"⚠️ Region {region} failed: {str(e)}")
        return []

def update_database(existing_df: pd.DataFrame) -> pd.DataFrame:
    """安全合并：保留所有历史，只追加新数据，按图片ID去重"""
    
    if existing_df is None or len(existing_df) == 0:
        existing_df = pd.DataFrame(columns=['date', 'title', 'url', 'description', 'region'])
    
    if 'region' not in existing_df.columns:
        existing_df['region'] = 'zh-CN'
    
    # ★★★ 确定要抓取哪些地区 ★★★
    regions_to_fetch = REGIONS
    
    # 如果指定了 --regions，只抓取指定的地区
    if hasattr(args, 'regions') and args.regions:
        custom_regions = [r.strip() for r in args.regions.split(',')]
        regions_to_fetch = [r for r in REGIONS if r in custom_regions]
        if not regions_to_fetch:
            notify(f"⚠️ No valid regions found in: {args.regions}")
            regions_to_fetch = REGIONS
    
    all_new_records = []
    success_count = 0
    fail_count = 0
    
    total_regions = len(regions_to_fetch)
    notify(f"🌍 开始抓取 {total_regions} 个地区的壁纸...")
    
    for i, region in enumerate(regions_to_fetch, 1):
        # 显示进度
        print(f"   [{i}/{total_regions}] {region}...", end=' ')
        
        records = fetch_region(region)
        if records:
            all_new_records.extend(records)
            success_count += 1
            print(f"✅")
        else:
            fail_count += 1
            print(f"❌")
    
    notify(f"📊 成功: {success_count}，失败: {fail_count}，总计: {total_regions}")
    
    if not all_new_records:
        notify("⚠️ 没有抓取到任何新数据")
        return existing_df
    
    new_df = pd.DataFrame(all_new_records)
    
    # 合并新旧数据
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    
    # 按图片ID去重
    combined_df['image_id'] = combined_df['url'].apply(extract_image_id)
    combined_df = combined_df.drop_duplicates(subset=['date', 'image_id'], keep='first')
    combined_df = combined_df.drop(columns=['image_id'])
    
    # 按日期排序（最新的在前）
    combined_df = combined_df.sort_values('date', ascending=False).reset_index(drop=True)
    
    # 保存
    try:
        combined_df.to_csv(database, index=False, encoding='utf-8')
        new_count = len(combined_df) - len(existing_df)
        notify(f"✅ 新增 {new_count} 条，总计 {len(combined_df)} 条")
    except Exception as e:
        notify(f"Failed to save: {str(e)}")
    
    return combined_df

def download_images_task(src_df, img_dir, cache_dir, img_prefix, use_wget):
    downloaded_imgs = os.listdir(img_dir) if os.path.exists(img_dir) else []
    total = len(src_df)
    downloaded_count = 0
    
    for i, (date_str, url) in enumerate(zip(src_df['date'], src_df['url']), 1):
        try:
            target_file = f'{img_prefix}-{date_str[2:]}.jpg'
            if target_file in downloaded_imgs:
                downloaded_count += 1
                continue
            cache_file = f'{cache_dir}/img_cache'
            if use_wget:
                os.system(f'wget -q -O {cache_file} {url}')
            else:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                with open(cache_file, 'wb') as f:
                    f.write(response.content)
            file_op.move_files(cache_file, os.path.join(img_dir, target_file))
            notify(f'[{i}/{total}] {target_file} downloaded')
            downloaded_count += 1
        except Exception as e:
            notify(f'[{i}/{total}] Download failed: {str(e)}')
    
    notify(f"📥 下载完成: {downloaded_count}/{total} 张图片")

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
        notify(f'✅ 生成 wallpaper/index.html')
        notify(f'✅ 生成 {num} 个子页面到 {subpages_dir}/')
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
        notify(f"📂 加载了 {len(src)} 条历史记录")
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        exit(1)
    
    if not args.no_fetch:
        try:
            src = update_database(src)
        except Exception as e:
            notify(f"Update failed: {str(e)}")
    
    if hasattr(args, 'save_raw') and args.save_raw:
        src.to_csv(args.save_raw, index=False, encoding='utf-8')
        notify(f"✅ Raw data saved to {args.save_raw}")
        exit(0)
    
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
            notify("🧹 Cache files cleaned")
        except Exception as e:
            notify(f"Failed to clean cache: {str(e)}")
    else:
        notify("💾 Cache files retained")
    
    print('<' * MSG_LEN, end='\n\n')
    exit(0)
