# HEARTBEAT.md

## Checks (run all each heartbeat)

Every heartbeat, check all of these:

### Email
- Run: `gog gmail search "is:unread" --max 5`
- Flag urgent emails
- **Auto-delete from these senders (move to trash):**
  - greater@berkeley.edu
  - info@digital.axisbankmail.bank.in
  - info@naukri.com
  - jobalert@naukri.com
  - jobalerts-noreply@linkedin.com
  - jobs-noreply@linkedin.com
  - messages-noreply@linkedin.com
  - no-reply@substack.com
  - recommendations@discover.pinterest.com
- For each match: `gog gmail move <thread-id> TRASH` or delete directly

### Teams
- Browser required (Chrome extension must be attached)
- Check Activity section for @mentions

### Calendar
- Run: `gog calendar events primary --upcoming 24h`
- Flag events in next 24h

### Weather
- Use Open-Meteo API (free, no key):
  `curl -s "https://api.open-meteo.com/v1/forecast?latitude=26.75&longitude=83.36&current_weather=true"`
- Gorakhpur, UP coordinates by default
- Skip if curl hangs

## When to Alert

- Important email arrived
- Calendar event in next 2 hours
- Teams @mentions
- Weather alert (if going out)

## Quiet Hours

00:00-06:00 — stay quiet unless urgent
