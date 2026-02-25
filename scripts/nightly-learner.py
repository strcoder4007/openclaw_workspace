#!/usr/bin/env python3
"""
Nightly topic learner - picks a random topic and finds learning resources
Runs at 11 PM daily via cron
"""

import os
import random
import subprocess
import json
from datetime import datetime

# The topic list
TOPICS = [
    "Ambient Agents that keep running",
    "Agents with RL training", 
    "Make MCP Servers, NPM Packages & CLI Tools",
    "Agentic Graph RAG",
    "KV Cache",
    "Speech to speech model"
    "RLHF, GRPO, PPO",
    "ASR and VAD",
    "Finetuning in 2026",
    "Transformer Architecture",
    "Self attention, cross attention, sparse attention",
    "Sabastian Raschka LLM Architecture"
    "Research Papers (from daily papers on hugging face look for the best 3 in the week)"
]

def search_resources(topic):
    """Search for learning resources on a topic using curl"""
    
    serper_key = os.environ.get("SERPER_API_KEY")
    if not serper_key:
        return "⚠️ No SERPER_API_KEY set"
    
    queries = {
        "blogs": f"{topic} tutorial blog post",
        "github": f"{topic} GitHub awesome",
        "youtube": f"{topic} tutorial video YouTube",
        "papers": f"{topic} research paper arxiv"
    }
    
    results = {}
    
    for category, query in queries.items():
        cmd = [
            "curl", "-s", "-X", "POST", "https://google.serper.dev/search",
            "-H", f"X-API-KEY: {serper_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"q": query, "num": 5})
        ]
        
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if proc.returncode == 0:
                data = json.loads(proc.stdout)
                items = []
                for item in data.get("organic", [])[:3]:
                    items.append(f"• {item['title']}\n  {item['link']}")
                results[category] = "\n".join(items) if items else "No results"
            else:
                results[category] = "Search failed"
        except Exception as e:
            results[category] = f"Error: {e}"
    
    return results

def format_message(topic, results):
    """Format the results as a message"""
    msg = f"📚 *Tonight's Learning Topic*\n\n*{topic}*\n\n"
    
    if isinstance(results, str):
        return msg + results
    
    if results.get("blogs"):
        msg += f"📝 *Blogs*\n{results['blogs']}\n\n"
    if results.get("github"):
        msg += f"🐙 *GitHub*\n{results['github']}\n\n"
    if results.get("youtube"):
        msg += f"🎬 *YouTube*\n{results['youtube']}\n\n"
    if results.get("papers"):
        msg += f"📄 *Papers*\n{results['papers']}\n"
    
    return msg

def send_telegram(message):
    """Send message via Telegram bot"""
    
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Missing Telegram credentials")
        return False
    
    # Escape markdown special chars
    message_escaped = message.replace("_", r"\_").replace("*", r"\*").replace("`", r"\`")
    
    cmd = [
        "curl", "-s", "-X", "POST",
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        "-d", f"chat_id={chat_id}",
        "-d", f"text={message_escaped}",
        "-d", "parse_mode=Markdown"
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return proc.returncode == 0
    except Exception as e:
        print(f"Error sending: {e}")
        return False

def main():
    # Pick random topic
    topic = random.choice(TOPICS)
    
    print(f"[{datetime.now()}] Selected topic: {topic}")
    
    # Search for resources
    results = search_resources(topic)
    
    # Format and send
    message = format_message(topic, results)
    print(message)
    
    # Also log to file
    log_path = os.path.expanduser("~/scripts/nightly-learner.log")
    with open(log_path, "a") as f:
        f.write(f"\n--- {datetime.now()} ---\n{topic}\n{results}\n")
    
    # Send via Telegram
    if send_telegram(message):
        print("✅ Sent to Telegram")
    else:
        print("⚠️ Failed to send to Telegram, logged to file")

if __name__ == "__main__":
    main()
