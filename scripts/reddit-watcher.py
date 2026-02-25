#!/usr/bin/env python3
"""
Weekly subreddit watcher - fetches top/new posts from AI/agent subreddits
Runs Monday 9 PM and Friday 9 PM via cron
"""

import os
import json
import subprocess
from datetime import datetime

SUBREDDITS = [
    "openclaw",
    "ChatGPT",
    "LocalLLaMA",
    "LLMs",
    "ArtificialIntelligence",
    "MachineLearning",
    "langchain",
    "langgraph"
]

OUTPUT_DIR = "/Users/str/.openclaw/workspace/outputs/reports"

def fetch_reddit_json(subreddit, sort="new", limit=10):
    """Fetch posts from subreddit using Reddit's JSON API"""
    import urllib.request
    import ssl
    
    # Skip SSL verification issues
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching r/{subreddit}: {e}")
        return None

def parse_posts(data, subreddit):
    """Parse Reddit JSON response into clean post list"""
    posts = []
    try:
        children = data.get("data", {}).get("children", [])
        for child in children:
            post = child.get("data", {})
            posts.append({
                "subreddit": subreddit,
                "title": post.get("title", ""),
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "author": post.get("author", ""),
                "created_utc": post.get("created_utc", 0)
            })
    except Exception as e:
        print(f"Error parsing r/{subreddit}: {e}")
    return posts

def format_report(all_posts, day_name):
    """Format posts as a readable report"""
    from datetime import datetime
    
    # Sort by score
    all_posts.sort(key=lambda x: x["score"], reverse=True)
    
    report = f"# 📊 Reddit Watch Report - {day_name}\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Group by subreddit
    by_subreddit = {}
    for post in all_posts:
        sr = post["subreddit"]
        if sr not in by_subreddit:
            by_subreddit[sr] = []
        by_subreddit[sr].append(post)
    
    # Write by subreddit
    for sr in SUBREDDITS:
        if sr in by_subreddit:
            report += f"## r/{sr}\n"
            for post in by_subreddit[sr][:5]:  # Top 5 per subreddit
                report += f"- [{post['title']}]({post['url']})\n"
                report += f"  ⬆️ {post['score']} 💬 {post['num_comments']} | by {post['author']}\n"
            report += "\n"
    
    # Top 10 overall
    report += "## 🔥 Top 10 Overall\n"
    for i, post in enumerate(all_posts[:10], 1):
        report += f"{i}. [{post['title']}]({post['url']}) (r/{post['subreddit']})\n"
        report += f"   ⬆️ {post['score']} 💬 {post['num_comments']}\n"
    
    return report

def main():
    day_name = datetime.now().strftime("%A")
    all_posts = []
    
    print(f"[{datetime.now()}] Fetching posts from {len(SUBREDDITS)} subreddits...")
    
    for sr in SUBREDDITS:
        data = fetch_reddit_json(sr, sort="new", limit=15)
        if data:
            posts = parse_posts(data, sr)
            all_posts.extend(posts)
            print(f"  r/{sr}: {len(posts)} posts")
    
    # Generate report
    report = format_report(all_posts, day_name)
    
    # Save markdown
    date_str = datetime.now().strftime("%Y-%m-%d")
    md_path = f"{OUTPUT_DIR}/reddit-watch-{date_str}.md"
    with open(md_path, "w") as f:
        f.write(report)
    
    # Save JSON for programmatic use
    json_path = f"{OUTPUT_DIR}/reddit-watch-{date_str}.json"
    with open(json_path, "w") as f:
        json.dump(all_posts, f, indent=2)
    
    print(f"\n✅ Saved:")
    print(f"  {md_path}")
    print(f"  {json_path}")
    print(f"\nTotal posts: {len(all_posts)}")

if __name__ == "__main__":
    main()
