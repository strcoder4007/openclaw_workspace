#!/usr/bin/env python3
"""
Topic Hunter - picks a random topic and finds learning resources
Runs at 11 PM daily via cron
Enriched with high-quality sources and better search strategies
"""

import os
import random
import subprocess
import json
from datetime import datetime

# Output settings
REPORTS_DIR = "/Users/str/.openclaw/workspace/outputs/reports"
REPORT_FILE = os.path.join(REPORTS_DIR, "topic-hunter.md")

# The topic list - expanded with high-value topics
TOPICS = [
    "Ambient Agents that keep running",
    "Agents with RL training", 
    "Make MCP Servers, NPM Packages & CLI Tools",
    "Agentic Graph RAG",
    "KV Cache",
    "VAE",
    "Speech to speech model",
    "RLHF, GRPO, PPO",
    "ASR and VAD",
    "Finetuning in 2026",
    "Transformer Architecture",
    "Self attention, cross attention, sparse attention",
    "Sebastian Raschka LLM Architecture",
    "Research Papers from Hugging Face daily papers best 3",
    "NVIDIA GPU architecture YouTube videos",
    "AI agent architecture 2026",
    "x86 processor architecture YouTube videos",
    "ARM processor architecture YouTube videos",
    "PC computer architecture YouTube videos",
    # New high-value topics
    "Graph RAG implementation guide",
    "Mixture of Experts MoE explained",
    "Speculative decoding LLM optimization",
    "Quantization techniques LLM GPTQ AWQ",
    "Function calling LLM agents",
    "Computer vision transformers ViT",
    "Retrieval augmented generation best practices",
    "Multi-agent systems architecture",
    "Vector database comparison 2026",
    "LoRA fine-tuning best practices",
]

# High-quality source domains to prioritize
QUALITY_BLOGS = [
    "jalammar.github.io",
    "sebastianraschka.com",
    "til.simonwillison.net",
    "magazine.sebastianraschka.com",
    "hwaseong.kr",
    "bdtechtalks.com",
    "gradientflow.com",
    "www.interconnects.ai",
    "www.latent.space",
    "newsletter.abacus.ai",
]

QUALITY_YOUTUBE_CHANNELS = [
    "Lex Fridman",
    "Andrej Karpathy",
    "Sebastian Raschka",
    "3Blue1Brown",
    "CodeEmporium",
    "Jay Anatar",
    "AI Explained",
    "Samuel Flender",
    "Dave Ebbelaar",
    "Weights & Biases",
]

QUALITY_PAPER_SOURCES = [
    "arxiv.org",
    "huggingface.co/papers",
    "paperswithcode.com",
    "semantic scholar",
]


def search_with_serper(query, num=5):
    """Search using Serper API"""
    serper_key = os.environ.get("SERPER_API_KEY")
    if not serper_key:
        return None
    
    cmd = [
        "curl", "-s", "-X", "POST", "https://google.serper.dev/search",
        "-H", f"X-API-KEY: {serper_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"q": query, "num": num})
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if proc.returncode == 0:
            return json.loads(proc.stdout)
    except Exception as e:
        print(f"Serper error: {e}")
    return None


def search_with_serpapi(query, num=5):
    """Search using SerpAPI as fallback"""
    serpapi_key = os.environ.get("SERP_API_KEY")
    if not serpapi_key:
        return None
    
    cmd = [
        "curl", "-s", 
        f"https://serpapi.com/search.json?q={query}&api_key={serpapi_key}&num={num}"
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if proc.returncode == 0:
            return json.loads(proc.stdout)
    except Exception as e:
        print(f"SerpAPI error: {e}")
    return None


def search_resources(topic):
    """Search for learning resources with quality focus"""
    
    results = {
        "blogs": [],
        "github": [],
        "youtube": [],
        "papers": [],
        "courses": [],
        "community": [],
    }
    
    # === BLOG SEARCHES (Quality-focused) ===
    blog_queries = [
        f"{topic} tutorial comprehensive guide",
        f"{topic} explained simply",
        f"{topic} implementation Python",
    ]
    
    for query in blog_queries[:2]:
        data = search_with_serper(query)
        if data:
            for item in data.get("organic", [])[:3]:
                domain = item.get("link", "")
                # Prioritize known quality blogs
                priority = any(q in domain for q in QUALITY_BLOGS)
                results["blogs"].append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")[:100],
                    "priority": priority
                })
    
    # Dedupe and sort by priority
    seen = set()
    blogs = []
    for b in results["blogs"]:
        if b["link"] not in seen:
            seen.add(b["link"])
            blogs.append(b)
    blogs.sort(key=lambda x: (-x["priority"], x["title"]))
    results["blogs"] = blogs[:4]
    
    # === GITHUB SEARCHES ===
    github_queries = [
        f"{topic} GitHub awesome list",
        f"{topic} GitHub trending 2026",
        f"{topic} implementation repository stars>500",
    ]
    
    for query in github_queries[:2]:
        data = search_with_serper(query)
        if data:
            for item in data.get("organic", [])[:3]:
                if "github.com" in item.get("link", "").lower():
                    results["github"].append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                    })
    
    # Dedupe
    seen = set()
    github = []
    for g in results["github"]:
        if g["link"] not in seen:
            seen.add(g["link"])
            github.append(g)
    results["github"] = github[:4]
    
    # === YOUTUBE SEARCHES (Channel-focused) ===
    yt_queries = [
        f"{topic} tutorial",
        f"{topic} explained",
        f"{topic} deep dive",
    ]
    
    for query in yt_queries[:2]:
        data = search_with_serper(query)
        if data:
            for item in data.get("organic", [])[:4]:
                link = item.get("link", "")
                title = item.get("title", "")
                # Check for YouTube
                if "youtube.com" in link.lower() or "youtu.be" in link.lower():
                    # Try to identify channel
                    channel_known = any(ch.lower() in title.lower() for ch in QUALITY_YOUTUBE_CHANNELS)
                    results["youtube"].append({
                        "title": title,
                        "link": link,
                        "channel_known": channel_known
                    })
    
    # Dedupe and prioritize known channels
    seen = set()
    youtube = []
    for yt in results["youtube"]:
        if yt["link"] not in seen:
            seen.add(yt["link"])
            youtube.append(yt)
    youtube.sort(key=lambda x: (-x["channel_known"], x["title"]))
    results["youtube"] = youtube[:4]
    
    # === PAPERS SEARCH ===
    paper_queries = [
        f"{topic} arxiv 2025 2026",
        f"{topic} paper research",
    ]
    
    for query in paper_queries[:1]:
        data = search_with_serper(query)
        if data:
            for item in data.get("organic", [])[:4]:
                link = item.get("link", "").lower()
                if any(src in link for src in QUALITY_PAPER_SOURCES) or "arxiv" in link:
                    results["papers"].append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                    })
    
    # Dedupe
    seen = set()
    papers = []
    for p in results["papers"]:
        if p["link"] not in seen:
            seen.add(p["link"])
            papers.append(p)
    results["papers"] = papers[:4]
    
    # === COURSES ===
    course_queries = [
        f"{topic} course online learning",
        f"{topic} free course MOOC",
    ]
    
    for query in course_queries[:1]:
        data = search_with_serper(query)
        if data:
            for item in data.get("organic", [])[:3]:
                link = item.get("link", "")
                title = item.get("title", "")
                # Filter for course platforms
                if any(p in link.lower() for p in ["coursera", "udemy", "edx", "fast.ai", "deeplearning.ai", "kaggle"]):
                    results["courses"].append({
                        "title": title,
                        "link": link,
                    })
    
    # Dedupe
    seen = set()
    courses = []
    for c in results["courses"]:
        if c["link"] not in seen:
            seen.add(c["link"])
            courses.append(c)
    results["courses"] = courses[:3]
    
    # === COMMUNITIES / NEWSLETTERS ===
    community_queries = [
        f"{topic} newsletter",
        f"{topic} Discord community",
        f"{topic} subreddit",
    ]
    
    for query in community_queries[:1]:
        data = search_with_serper(query)
        if data:
            for item in data.get("organic", [])[:2]:
                results["community"].append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                })
    
    # Dedupe
    seen = set()
    community = []
    for c in results["community"]:
        if c["link"] not in seen:
            seen.add(c["link"])
            community.append(c)
    results["community"] = community[:2]
    
    return results


def format_message(topic, results):
    """Format the results as a message with quality indicators"""
    msg = f"🎯 *Topic Hunter*\n\n*{topic}*"
    msg += "\n\n"
    
    if not results or all(not v for v in results.values()):
        return msg + "⚠️ No results found. Try a different topic."
    
    # Blogs - show priority indicator
    if results.get("blogs"):
        msg += "📝 *Blogs & Articles*\n"
        for b in results["blogs"]:
            indicator = "⭐" if b.get("priority") else "•"
            msg += f"{indicator} [{b['title']}]({b['link']})\n"
        msg += "\n"
    
    # GitHub
    if results.get("github"):
        msg += "🐙 *GitHub Repos*\n"
        for g in results["github"]:
            msg += f"• [{g['title']}]({g['link']})\n"
        msg += "\n"
    
    # YouTube - show channel quality
    if results.get("youtube"):
        msg += "🎬 *YouTube Videos*\n"
        for yt in results["youtube"]:
            indicator = "⭐" if yt.get("channel_known") else "•"
            msg += f"{indicator} [{yt['title']}]({yt['link']})\n"
        msg += "\n"
    
    # Papers
    if results.get("papers"):
        msg += "📄 *Papers & Research*\n"
        for p in results["papers"]:
            msg += f"• [{p['title']}]({p['link']})\n"
        msg += "\n"
    
    # Courses
    if results.get("courses"):
        msg += "🎓 *Courses*\n"
        for c in results["courses"]:
            msg += f"• [{c['title']}]({c['link']})\n"
        msg += "\n"
    
    # Community
    if results.get("community"):
        msg += "💬 *Communities*\n"
        for c in results["community"]:
            msg += f"• [{c['title']}]({c['link']})\n"
    
    return msg


def send_telegram(message):
    """Send message via Telegram bot"""
    
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Missing Telegram credentials")
        return False
    
    # Escape markdown
    message_escaped = message.replace("_", r"\_").replace("*", r"\*").replace("`", r"\`").replace("[", "[").replace("]", "]")
    
    cmd = [
        "curl", "-s", "-X", "POST",
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        "-d", f"chat_id={chat_id}",
        "-d", f"text={message_escaped}",
        "-d", "parse_mode=MarkdownV2"
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
    
    # Save to reports file
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(REPORT_FILE, "a") as f:
        f.write(f"\n---\n*Topic: {topic}*\n*Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        
        for cat in ["blogs", "github", "youtube", "papers", "courses", "community"]:
            if results.get(cat):
                f.write(f"*{cat.title()}*\n")
                for item in results[cat]:
                    f.write(f"• {item['title']} - {item['link']}\n")
                f.write("\n")
    
    # Send via Telegram
    if send_telegram(message):
        print("✅ Sent to Telegram")
    else:
        print("⚠️ Failed to send to Telegram, logged to file")


if __name__ == "__main__":
    main()
