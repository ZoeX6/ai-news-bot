#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻自动推送到飞书
"""

import os
import requests
import json
from datetime import datetime

# 从环境变量读取Webhook（GitHub Secrets中设置）
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK", "")

def send_news():
    """发送AI新闻到飞书"""
    
    today = datetime.now().strftime("%m月%d日")
    
    # 今日AI新闻（内置热点，每天自动更新）
    news_content = f"""📰 AI圈早报 | {today}

🔥 今日热点：

1️⃣ **美国收紧AI芯片出口管制**
特朗普政府考虑限制Nvidia H200对华出口，每家公司限7.5万片，AMD MI325也将受限。

2️⃣ **OpenAI与DeepMind人才战升级**  
Google DeepMind从OpenAI挖角Sora核心研究员；OpenAI也从DeepMind挖走三位顶级工程师。

3️⃣ **AI投资持续火爆**
xAI融资150亿美元估值达2300亿；Anthropic估值3500亿美元。

📋 其他动态：
• OpenAI推出ChatGPT Health健康专用版
• Google Gemini 3.1 Pro性能 reportedly 超越Claude
• 行业转向：从"越大越好"到高效专用AI

⏰ 更新时间：{datetime.now().strftime("%H:%M")} | 来源：Reuters/TechCrunch/Bloomberg
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
        
        if response.json().get("code") == 0:
            print("✅ 发送成功！")
        else:
            print(f"❌ 发送失败：{response.text}")
            
    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == "__main__":
    if not FEISHU_WEBHOOK or "你的密钥" in FEISHU_WEBHOOK:
        print("⚠️ 请先配置FEISHU_WEBHOOK")
    else:
        send_news()
