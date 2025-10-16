# AttackerTool - Quick Start Guide

Get up and running with AttackerTool in 5 minutes!

## Prerequisites

- Python 3.10+
- pip
- Git

## Quick Setup

### 1. Clone and Setup (2 minutes)

```bash
# Clone repository
git clone https://github.com/wdrew31/AttackerTool.git
cd AttackerTool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### 2. Start the Server (30 seconds)

```bash
# From the backend directory
python -m uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 3. Verify Installation (30 seconds)

Open another terminal and test:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","timestamp":"2025-10-16T14:30:00.000000"}
```

### 4. Set Up Test Target (2 minutes)

Use DVWA (Damn Vulnerable Web Application):

```bash
# Pull and run DVWA with Docker
docker run -d -p 80:80 vulnerables/web-dvwa

# Access at http://localhost
# Default login: admin/password
```

After logging in:
1. Click "Create / Reset Database"
2. Login again
3. Set security level to "Low" (DVWA Security button)

### 5. Run Your First Scan (1 minute)

#### Option A: Using the Test Script

```bash
# From the backend directory
python test_scan.py
```

When prompted, enter: `http://localhost`

#### Option B: Using curl

```bash
# Start a scan
curl -X POST http://localhost:8000/api/scans/start \
  -H "Content-Type: application/json" \
  -d '{"target_url": "http://localhost", "max_depth": 2}'

# Get the scan_id from response, then check status
curl http://localhost:8000/api/scans/{scan_id}
```

#### Option C: Using the Interactive API Docs

1. Open http://localhost:8000/docs in your browser
2. Click on `POST /api/scans/start`
3. Click "Try it out"
4. Enter request body:
   ```json
   {
     "target_url": "http://localhost",
     "max_depth": 2
   }
   ```
5. Click "Execute"
6. Copy the `scan_id` from the response
7. Use `GET /api/scans/{scan_id}` to check results

## What to Expect

### Scan Process

1. **Crawling** (10-20 seconds)
   - Discovers pages and forms
   - Finds input points

2. **Testing** (30-60 seconds)
   - Tests each input for SQL injection
   - Both error-based and blind SQLi

3. **Results** (immediate)
   - Detailed vulnerability report
   - Remediation guidance
   - JSON export

### Sample Output

```
🔍 Starting scan of: http://localhost
   Max crawl depth: 2

✓ Scan started successfully
  Scan ID: 123e4567-e89b-12d3-a456-426614174000

⏳ Monitoring scan progress...
  [████████████████████████████████████████] 100% - completed

============================================================
  SCAN RESULTS
============================================================

📊 Statistics:
  Target: http://localhost
  Pages Crawled: 15
  Input Points Found: 8
  Vulnerabilities Found: 3

🚨 Severity Breakdown:
  Critical: 2 🔴
  High: 1 🟠

🐛 Vulnerabilities Detected:
------------------------------------------------------------

[1] SQL Injection - Error-Based
    Severity: Critical (CVSS: 9.8)
    URL: http://localhost/vulnerabilities/sqli/
    Parameter: id
    Payload: ' OR '1'='1
    CWE: CWE-89
    OWASP: A03:2021 - Injection
    Fix: Use parameterized queries (prepared statements)
```

## Common Issues

### Issue: "Cannot connect to API"
```bash
# Make sure you're in the backend directory
cd backend

# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start the server
python -m uvicorn app.main:app --reload
```

### Issue: "Target not responding"
```bash
# Check if DVWA is running
docker ps

# If not running, start it
docker run -d -p 80:80 vulnerables/web-dvwa

# Test accessibility
curl http://localhost
```

### Issue: "No vulnerabilities found"
- Make sure DVWA security level is set to "Low"
- Try scanning specific vulnerable pages:
  - `http://localhost/vulnerabilities/sqli/`
  - `http://localhost/vulnerabilities/sqli_blind/`

## Next Steps

### Explore the API
- Visit http://localhost:8000/docs for interactive API documentation
- Try different scan configurations
- Experiment with max_depth parameter

### Test Different Applications
1. **DVWA** (easiest) - SQL injection vulnerabilities
2. **WebGoat** - OWASP training application
3. **Juice Shop** - Modern vulnerable web app
4. **Your own test application** (with permission!)

### Understand the Results
1. Review vulnerability details
2. Study the payloads used
3. Read the remediation guidance
4. Learn about CVSS scores and CWE mappings

### Customize and Extend
1. Modify payloads in `modules/sql_injection.py`
2. Adjust crawler depth and timeout
3. Add custom error patterns
4. Create your own testing modules

## Learning Path

### Beginner (Week 1)
- [x] Set up and run first scan
- [ ] Understand SQL injection basics
- [ ] Review PortSwigger SQL injection labs
- [ ] Practice on DVWA at different security levels

### Intermediate (Week 2-3)
- [ ] Study the crawler code
- [ ] Understand error-based vs blind SQLi
- [ ] Modify payloads and test
- [ ] Read OWASP Testing Guide

### Advanced (Week 4+)
- [ ] Add time-based SQLi detection
- [ ] Create custom testing modules
- [ ] Build a simple frontend
- [ ] Integrate with CI/CD pipeline

## Resources

- **Documentation**: See `/docs` folder
- **API Docs**: http://localhost:8000/docs
- **Phase 1 Checklist**: `docs/Phase1_SQL_Injection_Testing.md`
- **Project Plan**: `docs/Project_Recommendations.md`

## Getting Help

1. Check the README.md for detailed documentation
2. Review the code comments
3. Test with known vulnerable applications
4. Open an issue on GitHub

## Security Reminders

⚠️ **ALWAYS**:
- Get written permission before testing
- Only test applications you own
- Use on intentionally vulnerable apps for learning
- Never use on production systems without authorization

✅ **GOOD PRACTICES**:
- Test in isolated environments
- Document your findings
- Learn from the remediation guidance
- Share knowledge responsibly

---

**You're all set!** Start scanning and happy learning! 🚀

For detailed documentation, see the main [README.md](../README.md)
