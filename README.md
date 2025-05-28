# LLM Paper Collector

一个自动收集和整理大模型相关高质量论文的程序，支持从多个知名网站抓取论文，按日期归类，并提供按名称/描述/摘要搜索的功能。

## 功能特点

- 自动从多个来源收集大模型相关论文（ArXiv, ACL Anthology, Papers With Code等）
- 智能过滤，专注于高质量论文（来自知名研究机构、引用量高的论文）
- 按日期归类存储，便于查询历史论文
- 支持按标题、摘要、作者等多维度搜索
- 支持中英文关键词搜索

## 安装

```bash
# 克隆仓库
git clone https://github.com/mouyaling99/devin-format.git
cd devin-format

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 收集最新论文

```bash
# 收集过去7天的高质量论文
python -m src.main

# 收集过去30天的高质量论文
python -m src.main --days 30
```

### 搜索已收集的论文

```bash
# 在所有字段中搜索关键词
python -m src.main --search "大模型"

# 在特定字段中搜索
python -m src.main --search "GPT-4" --field title
python -m src.main --search "OpenAI" --field authors
python -m src.main --search "benchmark" --field abstract
```

### 按日期查询

```bash
# 查看特定日期收集的论文
python -m src.main --date 2023-05-28

# 查看日期范围内的论文
python -m src.main --date-range 2023-05-01 2023-05-31
```

## 数据存储

所有收集的论文数据以JSON格式存储在`data`目录下，按日期命名。

## 项目结构

```
devin-format/
├── data/                  # 存储收集的论文数据
├── src/                   # 源代码
│   ├── models/            # 数据模型
│   ├── scrapers/          # 各网站爬虫
│   ├── utils/             # 工具函数
│   └── main.py            # 主程序
├── requirements.txt       # 项目依赖
└── README.md              # 项目说明
```
