#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻自动抓取（GNews API）+ 推送到飞书
"""

import os
import requests
import json
from datetime import datetime, timedelta

# 从环境变量读取
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK", "")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")

def fetch_ai_news():
    """从GNews获取AI相关新闻"""
    if not GNEWS_API_KEY:
        print("⚠️ 未设置GNEWS_API_KEY")
        return None
    
    try:
        # 查询AI相关新闻，中文，最近24小时
        url = "https://gnews.io/api/v4/search"
        params = {
            "q": "人工智能 OR AI OR OpenAI OR ChatGPT OR 大模型",
            "lang": "zh",
            "country": "cn",
            "max": 5,  # 取5条
            "from": (datetime.now() - timedelta(days=1)).isoformat(),
            "to": datetime.now().isoformat(),
            "token": GNEWS_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "articles" in data:
            return data["articles"]
        else:
            print(f"API返回错误: {data}")
            return None
            
    except Exception as e:
        print(f"获取新闻失败: {e}")
        return None

def send_news():
    """发送AI新闻到飞书"""
    
    today = datetime.now().strftime("%m月%d日")
    
    # 获取实时新闻
    articles = fetch_ai_news()
    
    if articles and len(articles) >= 3:
        # 使用API新闻
        hot_news = ""
        for i, article in enumerate(articles[:3], 1):
            title = article.get("title", "无标题")
            desc = article.get("description", "")[:60] + "..."
            source = article.get("source", {}).get("name", "未知来源")
            
            hot_news += f"{i}️⃣ **{title}**\n   {desc}（{source}）\n\n"
        
        news_content = f"""📰 AI圈早报 | {today} | 实时版

🔥 今日热点：

{hot_news}
📋 快速一览：
• 全球AI动态持续更新
• 投资、技术、产品全覆盖
• 来源：GNews专业媒体聚合

⏰ 更新时间：{datetime.now().strftime("%H:%M")} | 来源：GNews API
"""
    else:
        # 备用新闻
        news_content = f"""📰 AI圈早报 | {today}

🔥 今日热点：

1️⃣ **美国收紧AI芯片出口管制**
特朗普政府考虑限制Nvidia H200对华出口，每家公司限7.5万片。

2️⃣ **OpenAI与DeepMind人才战升级**
Google DeepMind从OpenAI挖角Sora核心研究员。

3️⃣ **AI投资持续火爆**
xAI融资150亿美元估值达2300亿；Anthropic估值3500亿美元。

📋 其他动态：
• OpenAI推出ChatGPT Health健康专用版
• Google Gemini性能 reportedly 超越Claude
• 行业转向高效专用AI

⚠️ 注：实时新闻获取失败，显示备用内容
⏰ 更新时间：{datetime.now().strftime("%H:%M")}
"""
    
    # 发送到飞书
    payload = {
        "msg_type": "text",
        "content": {
            "text": news_content
        }
    }
    
    try:
        response = requests.post(
            FEISHU_WEBHOOK,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload, ensure_ascii=False)
        )
        
        result = response.json()
        if result.get("code") == 0:
            print("✅ 发送成功！")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

if __name__ == "__main__":
    # 检查配置
    if not FEISHU_WEBHOOK or "你的密钥" in FEISHU_WEBHOOK:
        print("⚠️ 请先配置FEISHU_WEBHOOK")
    elif not GNEWS_API_KEY:
        print("⚠️ 请先配置GNEWS_API_KEY")
    else:
        send_news()
