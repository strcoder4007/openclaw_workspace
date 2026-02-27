---
name: scrapling
description: Adaptive web scraping framework with anti-bot bypass. Use for scraping websites.
metadata:
  {
    "openclaw": { "emoji": "🕷️" }
  }
---

# Scrapling Skill

Adaptive web scraping with anti-bot bypass and automatic element relocation.

## Quick Use

```bash
# Simple fetch
cd /Users/str/.openclaw/workspace && source .venv/bin/activate && python3 -c "
from scrapling import Fetcher
f = Fetcher()
p = f.get('URL', verify=False)
print(p.css('title::text').get())
print(p.css('h1::text').get())
"

# With CSS selector
cd /Users/str/.openclaw/workspace && source .venv/bin/activate && python3 -c "
from scrapling import Fetcher
f = Fetcher()
p = f.get('URL', verify=False)
items = p.css('.item::text').all()
for item in items:
    print(item)
"

# Adaptive scraping (survives website changes)
p.css('.product', adaptive=True).all()
```

## Key Classes

- `Fetcher` — HTTP requests ( Basicfast, stealthy)
- `StealthyFetcher` — Bypasses Cloudflare, anti-bot
- `DynamicFetcher` — JavaScript-rendered pages

## Notes

- Requires workspace venv: `source .venv/bin/activate`
- Use `verify=False` to avoid SSL errors
- Adaptive mode (`adaptive=True`) relocates elements if page changes
