# 🖼️ Bing Wallpaper Fetcher

> 自动抓取必应4K+壁纸 · 支持网页展示 & RESTful API

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-自动更新-2088FF?logo=github-actions&logoColor=white)](.github/workflows)
[![Cloudflare Pages](https://img.shields.io/badge/Cloudflare%20Pages-部署成功-F38020?logo=cloudflare&logoColor=white)](https://bing-wallpaper-fetcher.pages.dev/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**在线演示**：[https://bing.hangdn.com](https://bing.hangdn.com) | API文档：[https://bing-wallpaper-fetcher.pages.dev/api](https://bing-wallpaper-fetcher.pages.dev/api)

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


