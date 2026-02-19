---
name: linkedin-crawler
description: |
  Crawl LinkedIn for user profile information using browser automation. Use when you need to:
  (1) Find and extract LinkedIn profile data (names, titles, companies, locations, connections)
  (2) Search for people by name, company, title, or skills
  (3) Build prospect lists or lead databases
  (4) Research companies for hiring or partnership
  Requires authenticated LinkedIn session (user must be logged in).
---

# LinkedIn Crawler

This skill crawls LinkedIn for profile data. LinkedIn has anti-scraping measures - be polite and use proper search strategies.

## Prerequisites

- LinkedIn must be logged in (use browser to navigate to linkedin.com and log in first)
- Browser automation via `browser` tool with profile="chrome"

## Search Strategy

**DO NOT** stuff keywords. LinkedIn search is powerful but specific.

### Good Searches
```
"Software Engineer at Google" (exact title + company)
"VP of Engineering" "San Francisco" (title + location)
"AI Researcher" "Stanford" (title + school)
python developer (skills-based)
"Tech Lead" "Series B" (title + funding stage)
```

### Bad Searches (will return no results)
```
software engineer google facebook apple (too many keywords)
best developer (vague)
AI ML Data Science (all caps, too broad)
```

### Search Tips
- Start broad, then filter: search for "Software Engineer" then filter by company in results
- Use quotes for exact phrases: "Machine Learning Engineer"
- Location + title works well: "Product Manager" "Seattle"
- Company growth stage: "VP Engineering" "Y Combinator"

## Crawl Workflow

1. **Navigate to LinkedIn search**: `https://www.linkedin.com/search/results/people/?`
2. **Build search URL** with parameters:
   - `keywords=` - search terms
   - `geoUrn=` - location filter
   - `companyUrn=` - company filter
   - `titleUrn=` - title filter
3. **Extract profile cards** from search results (each result is a `li` with data-test-id)
4. **Click each profile** to open and extract full details
5. **Paginate** via "Next" button or scroll loading

## Profile Data to Extract

For each profile, extract:
- Name (from h3)
- Headline (title + company)
- Location
- Connection degree (1st, 2nd, 3rd)
- Profile URL
- About/Summary (if available)
- Experience (current + past)
- Education

## Rate Limiting

- Wait 2-3 seconds between actions
- Don't crawl more than 50 profiles per session
- Stop if LinkedIn shows captcha or rate limit message
- Use delays: `browser action=act request={"kind": "wait", "timeMs": 2000}`

## Example: Search for AI Engineers at Google

```bash
# Step 1: Navigate to search
browser action=open targetUrl="https://www.linkedin.com/search/results/people/?keywords=AI%20Engineer&companyUrn=li:817169"

# Step 2: Wait for results, take snapshot
browser action=snapshot

# Step 3: Extract first page of results (up to 10)
# Parse the HTML for profile cards

# Step 4: Click first result to view full profile
browser action=act request={"kind": "click", "ref": "result-1"}

# Step 5: Extract profile details from expanded view
browser action=snapshot
```

## Output Format

Return data as structured JSON:

```json
{
  "profiles": [
    {
      "name": "John Doe",
      "headline": "Senior AI Engineer at Google",
      "location": "San Francisco Bay Area",
      "connections": "500+",
      "url": "https://www.linkedin.com/in/johndoe",
      "about": "...",
      "experience": [...],
      "education": [...]
    }
  ],
  "metadata": {
    "searchQuery": "AI Engineer at Google",
    "totalResults": 234,
    "crawledAt": "2026-02-18T13:45:00Z"
  }
}
```

## Common Issues

- **No results**: Check search query syntax, try simpler terms
- **Login required**: User must authenticate first
- **Rate limited**: Stop crawling, wait 15 min before retry
- **Profile unavailable**: Some profiles are private/limited

## Notes

- Always respect LinkedIn's terms of service
- Don't store or share extracted data without consent
- Use for legitimate purposes (hiring, networking, research)
