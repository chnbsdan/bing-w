# 🖼️ Bing Wallpaper Fetcher

> 自动抓取必应4K+壁纸 · 支持网页展示 & RESTful API

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-自动更新-2088FF?logo=github-actions&logoColor=white)](.github/workflows)
[![Cloudflare Pages](https://img.shields.io/badge/Cloudflare%20Pages-部署成功-F38020?logo=cloudflare&logoColor=white)](https://bing-wallpaper-fetcher.pages.dev/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**在线演示**：[https://bing.+++.com](https://bing.+++.com) | API文档：[https://bing-wallpaper-fetcher.pages.dev/api](https://bing-wallpaper-fetcher.pages.dev/api)

---

## ✨ 功能特性

- 📥 **自动抓取**：每日获取必应4K+高清壁纸（部分为1080p）
- 🌐 **网页展示**：精美的瀑布流画廊，支持暗色/亮色模式
- 🔌 **RESTful API**：提供 `/daily`、`/random`、`/image`、`/list` 接口
- 🤖 **全自动运行**：通过 GitHub Actions 每日定时更新数据
- 📱 **响应式设计**：完美适配桌面、平板、手机
- 💬 **评论系统**：集成 Twikoo，支持访客留言互动

---

## 🚀 快速开始

### 方式一：本地运行（仅下载壁纸）

```bash
# 克隆项目
git clone https://github.com/chnbsdan/bing-wallpaper-fetcher.git
cd bing-wallpaper-fetcher

# 安装依赖
pip install requests pandas

# 下载壁纸（同时生成HTML相册）
python main.py

# 仅下载图片，不生成HTML
python main.py --no-html
```

| 参数 | 说明 |
|------|------|
| `--no-html` / `--image-only` | 跳过HTML生成 |
| `--update` | 仅更新数据库，不下载 |
| `--use-wget` | 使用系统 `wget` 下载 |
| `--no-cache` | ⚠️ 重置数据库（会丢失历史） |

### 方式二：GitHub Actions 自动运行（推荐）

项目已配置 GitHub Actions 工作流，每日自动：
1. 拉取最新壁纸数据
2. 更新 `source_list.csv`
3. 生成 `data/wallpapers.json`
4. 部署到 Cloudflare Pages

**查看**：`.github/workflows/generate-data.yml`

---

## 📁 项目结构

```
├── .github/workflows/       # GitHub Actions 自动化
│   └── generate-data.yml    # 每日更新数据
├── functions/api/           # Cloudflare Pages 函数 (API)
│   ├── index.js             # API 文档入口
│   ├── daily.js             # 今日壁纸
│   ├── random.js            # 随机壁纸
│   ├── image.js             # 指定日期壁纸
│   └── list.js              # 分页列表
├── data/                    # 数据文件
│   └── wallpapers.json      # 前端数据源
├── index.html               # 主页面（瀑布流画廊）
├── source_list.csv          # 壁纸元数据
├── generate_data.py         # CSV → JSON 转换脚本
├── main.py                  # 原始下载脚本
└── CNAME                    # 自定义域名配置
```

---

## 🌐 API 接口

所有接口托管在 Cloudflare Pages，基础地址：`https://bing-wallpaper-fetcher.pages.dev/api`

| 接口 | 说明 | 示例 |
|------|------|------|
| `/daily` | 获取今日壁纸 | `GET /daily?format=webp` |
| `/random` | 随机壁纸 | `GET /random?redirect=true` |
| `/image` | 指定日期壁纸 | `GET /image?date=20260802` |
| `/list` | 分页列表 | `GET /list?page=1&size=30` |

**参数说明**：

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `format` | 图片格式 | `webp` / `jpeg` / `original` |
| `redirect` | 是否重定向 | `true` / `false` |
| `date` | 日期 (YYYYMMDD) | 如 `20260802` |
| `page` | 页码 | 默认 `1` |
| `size` | 每页数量 | 默认 `30`，最大 `100` |

---

## 🛠️ 部署到 Cloudflare Pages

1. Fork 本仓库
2. 登录 [Cloudflare Pages](https://pages.cloudflare.com/)，连接你的 GitHub 仓库
3. 构建配置：
   - **构建命令**：留空
   - **输出目录**：`/`
4. 保存部署，自动识别 `functions/api/` 目录

**自定义域名**：在 Cloudflare Pages 设置中绑定你的域名（如 `bing.hangdn.com`）

---

## 🧩 依赖说明

| 依赖 | 用途 |
|------|------|
| `requests` | HTTP 请求（Python） |
| `pandas` | CSV 数据处理（Python） |
| `Twikoo` | 评论系统（前端） |
| `Font Awesome` | 图标库（前端） |

---

## 📜 更新日志

- **2026-08-02**：完成 API 重构，全面支持 Cloudflare Pages Functions
- **2026-08-01**：上线 GitHub Actions 自动化，每日定时更新
- **2026-07-20**：部署到 Cloudflare Pages，支持自定义域名

---

## 📄 开源协议

本项目遵循 [MIT License](LICENSE)

---

## 🙏 致谢

- 壁纸数据来源于 [Bing](https://cn.bing.com/)
- 项目思路参考 [ddddavid-he/bing-wallpaper-fetcher](https://github.com/ddddavid-he/bing-wallpaper-fetcher)

---

**如果这个项目对你有帮助，欢迎 ⭐ Star 支持！**





<details>
<summary>原项目readme（点击展开）</summary>

# Bing Wallpaper Fetcher

<p align="center">
    <a href="README_ZH.md">中文文档</a>
</p>

A tool to automatically download Bing wallpapers in 4K+ resolution.

> **Note:** Some images may only be available in 1080p due to Bing's limitations.

---

## Requirements
- Python 3
- Python packages: `requests`, `argparse`, `pandas`

## Usage
- Run `python3 main.py` to download images and generate the HTML gallery.
- To skip HTML generation, add `--no-html` or `--image-only`.
- To only update the `source_list.csv` database without downloading images or generating HTML, use both `--no-image` and `--no-html`.
- The `--update` option updates `source_list.csv` and creates a backup without downloading images or generating HTML.
- **Warning:** Using `--no-cache` will **delete** and rebuild the `source_list.csv` database, resulting in loss of history. Use with caution!
- The `--use-wget` option uses the system's `wget` tool instead of Python's `requests` package for downloading.
- The `--no-fetch` option prevents updating `source_list.csv` and uses the existing file.
- Other parameters are self-explanatory based on their names.
</details>



<details>
<summary>🔧 系统工作原理（点击展开）</summary>



### 1️⃣ 数据获取层（每日自动）

**触发方式**：GitHub Actions 定时任务（每天 UTC 0:00，即北京时间 8:00）

**执行流程**：
1. GitHub Actions 启动一个 Ubuntu 虚拟机
2. 拉取仓库最新代码
3. 安装 Python 依赖（`requests`、`pandas`）
4. 运行 `python main.py --no-html`
   - 向必应官方 API 请求壁纸数据
   - 下载新壁纸图片到 `wallpaper/images/`
   - 更新 `source_list.csv` 记录（日期、标题、图片URL、描述）
5. 运行 `python generate_data.py`
   - 读取 `source_list.csv`
   - 转换为 `data/wallpapers.json`
   - 添加缩略图字段（`thumb`）
6. 提交并推送变更到仓库
   - 提交 `source_list.csv` 和 `data/wallpapers.json`
   - **图片本身不提交**（由 `.gitignore` 忽略，避免仓库过大）

---

### 2️⃣ 数据存储层（GitHub 仓库）

**核心文件**：

| 文件 | 内容 | 更新方式 |
|------|------|---------|
| `source_list.csv` | 壁纸元数据（日期、标题、URL、描述） | 每日自动更新 |
| `data/wallpapers.json` | 同上，JSON 格式（供前端和 API 使用） | 每日自动生成 |
| `wallpaper/images/` | 实际图片文件 | 临时下载，不提交 |

**数据流**：
```
必应 API → main.py → source_list.csv → generate_data.py → wallpapers.json
```

---

### 3️⃣ 服务层（Cloudflare Pages）

**托管内容**：
- 静态文件：`index.html`、`favicon.ico`
- 数据文件：`data/wallpapers.json`
- API 函数：`functions/api/*.js`

**API 工作流程**（以 `/api/daily` 为例）：
1. 用户请求 `https://bing-wallpaper-fetcher.pages.dev/api/daily`
2. Cloudflare Pages 路由到 `functions/api/daily.js`
3. `daily.js` 从同域的 `/data/wallpapers.json` 获取数据
4. 按日期排序，取最新一条
5. 根据 `format` 参数返回对应格式的图片（webp/jpeg）
6. 直接代理必应 CDN 图片，返回给用户

---

### 4️⃣ 展示层（前端页面）

**页面加载流程**：
1. 用户访问 `https://bing.hangdn.com`（或 `*.pages.dev`）
2. 浏览器加载 `index.html`（包含 CSS + JavaScript）
3. JavaScript 执行 `fetch('/data/wallpapers.json')`
4. 获取壁纸列表数据
5. 动态生成卡片网格（瀑布流布局）
6. 支持无限滚动、搜索、主题切换

**交互功能**：
- 点击卡片 → 大图预览（支持缩放、左右切换）
- 下载按钮 → 选择分辨率下载（4K/FHD/手机竖屏）
- 搜索框 → 按标题/日期筛选壁纸
- 留言按钮 → 打开 Twikoo 评论弹窗

---

### 📊 完整数据流图

```
┌─────────────────────────────────────────────────────────────────────┐
│                          1. 数据获取层                              │
│  GitHub Actions (每天 8:00)                                        │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────────┐   │
│  │  必应 API   │ → │  main.py     │ → │ source_list.csv      │   │
│  │  (壁纸数据)  │    │  (下载+解析)  │    │ (日期/标题/URL/描述) │   │
│  └─────────────┘    └──────────────┘    └──────────┬──────────┘   │
│                                                      ↓              │
│                                          ┌─────────────────────┐   │
│                                          │ generate_data.py    │   │
│                                          │ (CSV → JSON)        │   │
│                                          └──────────┬──────────┘   │
│                                                     ↓              │
│                                          ┌─────────────────────┐   │
│                                          │ wallpapers.json     │   │
│                                          │ (前端数据源)         │   │
│                                          └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              │ git push
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          2. 数据存储层                              │
│  GitHub 仓库                                                       │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐   │
│  │ source_list.csv     │    │ data/wallpapers.json           │   │
│  │ (原始数据)           │    │ (供前端/API使用)               │   │
│  └─────────────────────┘    └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              │ Cloudflare Pages 自动部署
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          3. 服务层                                  │
│  Cloudflare Pages                                                  │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐   │
│  │ 静态资源             │    │ API 函数                        │   │
│  │ index.html           │    │ /api/daily    → daily.js       │   │
│  │ data/wallpapers.json │    │ /api/random   → random.js      │   │
│  │ favicon.ico          │    │ /api/image    → image.js       │   │
│  │                      │    │ /api/list     → list.js        │   │
│  │                      │    │ /api/         → index.js       │   │
│  └─────────────────────┘    └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              │ 用户访问
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          4. 展示层                                  │
│  用户浏览器                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │  https://bing.+++.com                                       ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐││
│  │  │ 瀑布流画廊   │  │ 大图预览    │  │ API 文档页面            ││
│  │  │ (卡片网格)   │  │ (缩放/切换) │  │ (/api 接口说明)         ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐││
│  │  │ 搜索功能     │  │ 主题切换    │  │ 评论区 (Twikoo)         ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```


### 🎯 核心亮点

| 特性 | 实现方式 |
|------|---------|
| **全自动** | GitHub Actions 定时触发，无需人工干预 |
| **零服务器成本** | GitHub + Cloudflare 免费额度 |
| **数据与展示分离** | CSV 存元数据，JSON 供前端，API 动态返回 |
| **图片按需加载** | 不存储图片到仓库，每次运行时临时下载 |
| **多端适配** | 响应式设计 + 大图预览支持触屏操作 |

---

</details>
