# cautious-potato
Dark Web Monitoring OSINT

## Quick Start (5 minutes)

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/dark-web-osint-monitor.git
cd dark-web-osint-monitor
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Get Free API Keys (Parallel - 10 mins)

| API | Steps | Free Limit |
|-----|-------|-----------|
| **Mailgun** | 1. https://www.mailgun.com/signup<br/>2. Create verified sending domain<br/>3. Copy API key from Dashboard | 100/day first 12 months |
| **Shodan** | 1. https://shodan.io/register<br/>2. Account Settings → API Key<br/>3. Copy key | 1 query/month |
| **VirusTotal** | 1. https://www.virustotal.com/gui/sign-up<br/>2. API Docs → API Key<br/>3. Copy key | 4 requests/min |
| **Censys** | 1. https://censys.com/register<br/>2. Account → API Credentials<br/>3. Copy UID + Secret | 250/month |
| **SecurityTrails** | 1. https://securitytrails.com/app/register<br/>2. Account → API Token<br/>3. Copy token | 50/month |
| **AbuseIPDB** | 1. https://www.abuseipdb.com/register<br/>2. Account → API Key<br/>3. Copy key | 1000/day |

### 3. Configure Environment
```bash
cp .env.example .env

# Edit .env with your keys
nano .env
# Or on Windows:
notepad .env
```

### 4. Test Locally
```bash
python app.py
# Visit http://localhost:5000
```

---

## Deployment Options

### ✅ **Option 1: Heroku (Recommended - Free tier available)**

```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create your-osint-app
git push heroku main

# View logs
heroku logs --tail
```

**Procfile** (add to repo root):
```
web: gunicorn app:app
```

**runtime.txt** (add to repo root):
```
python-3.11.0
```

### ✅ **Option 2: PythonAnywhere (Free + Easy)**

1. Sign up: https://www.pythonanywhere.com/
2. Upload project via Git or ZIP
3. Create WSGI configuration:
```python
import sys
sys.path.insert(0, '/home/yourusername/dark-web-osint-monitor')
from app import app as application
```
4. Enable web app
5. Your app is live at: https://yourusername.pythonanywhere.com

### ✅ **Option 3: GitHub Actions + Render (Continuous Deployment)**

**`.github/workflows/deploy.yml`**:
```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: |
          curl https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }} -X POST
```

1. Create account at https://render.com
2. Create Web Service from GitHub
3. Set environment variables in dashboard
4. Auto-deploy on push!

### ✅ **Option 4: Docker + Cloud Run (Google Cloud Free Tier)**

**Dockerfile**:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

```bash
# Deploy to Google Cloud Run
gcloud run deploy osint-monitor \
  --source . \
  --platform managed \
  --region us-central1
```

---

## Module Details & API Integration

### 1. **Breach Finder** 🔐
```python
# No API key needed - uses public HaveIBeenPwned
# Example: Check if email was in breaches
results = breach_finder.search('victim@example.com', 'email')
# Returns: {
#   'breaches': [{'Name': 'Adobe', 'Date': '2013-10-04'}, ...],
#   'breach_count': 5,
#   'credentials_found': True
# }
```

### 2. **Dark Web Crawler** 🔗
```python
# Requires Tor installation
# Searches onion search engines and .onion mentions
results = dark_web_crawler.search('yourdomain.com')
# Returns: {
#   'mentions': [{'url': 'http://xxx.onion/leak', 'text': '...'}],
#   'threat_level': 'high',
#   'sources_checked': 3
# }
```

### 3. **Domain Intelligence** 🌐
```python
# Uses SecurityTrails API (50 free queries/month)
results = domain_intel.search('example.com')
# Returns: {
#   'dns_records': {'A': ['1.2.3.4'], 'MX': ['mail.example.com']},
#   'subdomains': ['mail.example.com', 'api.example.com'],
#   'ssl_certs': [{'issuer': 'Let\'s Encrypt', 'expiry': '2025-01-15'}]
# }
```

### 4. **Threat Intelligence** ⚠️
```python
# Uses VirusTotal, URLhaus, AbuseIPDB
results = threat_intel.search('malicious.com', 'domain')
# Returns: {
#   'threat_found': True,
#   'reputation_score': 85,
#   'detections': ['Trojan', 'Phishing'],
#   'last_analysis': {...}
# }
```

### 5. **TTP Mapper** 🎯
```python
# Maps to MITRE ATT&CK framework
results = ttp_mapper.analyze_results(all_results)
# Returns: {
#   'identified_ttps': [
#     {'tactic': 'Initial Access', 'technique': 'Phishing', 'confidence': 0.92},
#     {'tactic': 'Execution', 'technique': 'Malicious Script', 'confidence': 0.87}
#   ],
#   'threat_groups': ['APT28', 'Lazarus'],
#   'severity': 'CRITICAL'
# }
```

### 6. **Leak Detector** 💧
```python
# Searches Pastebin, leaks.sh, leaked sources
results = leak_detector.search('your-data')
# Returns: {
#   'leaks_found': True,
#   'leak_count': 3,
#   'leaked_data': [{
#     'source': 'Pastebin',
#     'date': '2024-01-15',
#     'content_preview': '...'
#   }]
# }
```

---

## Email Alert System

### Mailgun Integration
```python
# Automatically sends alerts when threats found
email_notifier.send_alert(
    to_email='security@company.com',
    search_input='company.com',
    results=all_results
)

# Email includes:
# ✓ Threat summary with severity
# ✓ Which modules found threats
# ✓ IOC details (breaches, malicious URLs, etc.)
# ✓ TTP classification with MITRE ATT&CK mapping
# ✓ Recommended actions
```

### Custom Alert Rules
```python
# In email_notifier.py, extend:
def should_alert(severity, threat_type):
    """Determine if email should be sent"""
    if severity == 'CRITICAL':
        return True
    if threat_type == 'active_malware':
        return True
    if threat_type == 'credential_leak':
        return True
    return False
```

---

## Performance & Scaling

### Single Instance (Local/Free Tier)
- **Concurrent searches**: 4 (configurable)
- **Response time**: 15-60 seconds
- **Rate limits**: Respected per API
- **Storage**: File-based results

### Scaling Options
1. **Add Redis caching** (for free tier: https://redis.cloud/try-free/)
2. **Increase workers** in ThreadPoolExecutor
3. **Use job queue** (Celery + message broker)
4. **Database** (PostgreSQL free tier via Heroku)

---

## Security Best Practices

### ✅ DO:
- Store API keys in `.env` (never commit)
- Validate all user inputs
- Use HTTPS for production
- Rotate API keys regularly
- Log all searches
- Implement rate limiting

### ❌ DON'T:
- Commit `.env` file to Git
- Use hardcoded credentials
- Expose raw API responses
- Store PII longer than needed
- Access without authorization

---

## Troubleshooting

### "API key is invalid"
```bash
# Check .env file exists and has correct key
cat .env

# Verify API key format (no extra spaces)
# Test API key directly:
curl -X GET "https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com" \
  -H "User-Agent: OSINT-Monitor"
```

### "Tor connection refused"
```bash
# Install Tor
# Ubuntu/Debian:
sudo apt-get install tor

# macOS:
brew install tor

# Start Tor:
sudo systemctl start tor

# Check it's running:
curl -x socks5://127.0.0.1:9050 -I https://www.torproject.org
```

### "Email not sending"
```bash
# Verify Mailgun sandbox domain setup
# Check spam folder
# Verify recipient email in Mailgun dashboard
# Test API directly:
curl -X POST "https://api.mailgun.net/v3/YOUR_DOMAIN/messages" \
  -u "api:YOUR_API_KEY" \
  -F from="Test <test@YOUR_DOMAIN>" \
  -F to="recipient@example.com" \
  -F subject="Test" \
  -F text="Test message"
```

### "Rate limit exceeded"
```python
# Implement exponential backoff in osint_modules/__init__.py
import time
from functools import wraps

def rate_limited(max_per_minute=4):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Implement backoff
            time.sleep(60/max_per_minute)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## File Structure Reference

```
dark-web-osint-monitor/
├── app.py                              # Flask application
├── config.py                           # Configuration
├── requirements.txt                    # Python dependencies
├── Procfile                           # For Heroku
├── runtime.txt                        # Python version
├── Dockerfile                         # For container deployment
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore rules
│
├── osint_modules/
│   ├── __init__.py                   # Core OSINT classes
│   ├── breach_finder.py              # (future: separate file)
│   ├── dark_web_crawler.py
│   ├── domain_intel.py
│   ├── threat_intel.py
│   ├── ttp_mapper.py
│   └── leak_detector.py
│
├── notifiers/
│   ├── __init__.py
│   └── email_notifier.py             # Mailgun integration
│
├── utils/
│   ├── __init__.py
│   ├── validators.py                 # Input validation
│   └── logger.py                     # Logging setup
│
├── templates/
│   ├── base.html                     # Base template
│   ├── index.html                    # Search form
│   └── results.html                  # Results display
│
├── static/
│   └── style.css                     # Styling
│
└── README.md                         # Documentation
```

---

## Next Steps

1. **Fork repository** on GitHub
2. **Get API keys** (parallel - takes 10 mins)
3. **Configure .env** file
4. **Test locally** (`python app.py`)
5. **Deploy** using Heroku/PythonAnywhere
6. **Create GitHub Actions** for auto-deployment
7. **Customize** for your use case

---

## Contributing Guidelines

Pull requests welcome! Areas to contribute:
- Additional OSINT APIs
- Better UI/UX
- Docker optimization
- CI/CD improvements
- Documentation
- Bug fixes

## License & Legal

- **License**: MIT
- **Legal**: Educational/authorized use only
- **Compliance**: Follow Computer Fraud & Abuse Act, local regulations
- **Responsibility**: User's responsibility for legal compliance

---

**Questions? Issues?** Open a GitHub issue with:
- Error message
- Steps to reproduce
- Python version
- OS information
