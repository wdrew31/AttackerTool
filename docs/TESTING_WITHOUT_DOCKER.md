# Testing AttackerTool Without Docker

Since Docker Desktop requires macOS Ventura or newer, I've created a simple vulnerable Flask application you can run locally to test AttackerTool.

## Quick Test Setup (5 minutes)

### Step 1: Set Up the Vulnerable Test App

```bash
# From the AttackerTool root directory
cd test_app

# Install Flask
pip install -r requirements.txt

# Make the script executable
chmod +x vulnerable_app.py

# Run the vulnerable application
python vulnerable_app.py
```

You should see:
```
============================================================
  Vulnerable Test Application
  WARNING: For Testing Only!
============================================================

✓ Database initialized with test data

🚀 Starting server on http://localhost:5000
📝 Visit http://localhost:5000 for instructions

⚠️  Press Ctrl+C to stop
```

**Keep this terminal open** - the app needs to stay running.

### Step 2: Start AttackerTool API (New Terminal)

Open a **new terminal window** and run:

```bash
# Navigate to backend directory
cd AttackerTool/backend

# Activate virtual environment
source ../venv/bin/activate

# Start the API server
python -m uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this terminal open too** - the API needs to stay running.

### Step 3: Run a Scan (Third Terminal)

Open a **third terminal window**:

```bash
# Navigate to backend directory
cd AttackerTool/backend

# Activate virtual environment
source ../venv/bin/activate

# Run the test script
python test_scan.py
```

When prompted, enter: `http://localhost:5000`

When asked to confirm, type: `yes`

## What You'll See

### 1. Crawling Phase
```
🔍 Starting scan of: http://localhost:5000
   Max crawl depth: 2

✓ Scan started successfully
  Scan ID: 123e4567-e89b-12d3-a456-426614174000

⏳ Monitoring scan progress...
  [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 30% - crawling
```

### 2. Testing Phase
```
  [████████████████████████░░░░░░░░░░░░░░░░] 60% - testing
```

### 3. Results
```
============================================================
  SCAN RESULTS
============================================================

📊 Statistics:
  Target: http://localhost:5000
  Pages Crawled: 4
  Input Points Found: 5
  Vulnerabilities Found: 3

🚨 Severity Breakdown:
  Critical: 3 🔴

🐛 Vulnerabilities Detected:
------------------------------------------------------------

[1] SQL Injection - Error-Based
    Severity: Critical (CVSS: 9.8)
    URL: http://localhost:5000/login
    Parameter: username
    Payload: ' OR '1'='1
    CWE: CWE-89
    OWASP: A03:2021 - Injection
    Fix: Use parameterized queries (prepared statements)

[2] SQL Injection - Error-Based
    Severity: Critical (CVSS: 9.8)
    URL: http://localhost:5000/search
    Parameter: q
    Payload: '
    CWE: CWE-89
    OWASP: A03:2021 - Injection
    Fix: Use parameterized queries (prepared statements)

[3] SQL Injection - Error-Based
    Severity: Critical (CVSS: 9.8)
    URL: http://localhost:5000/profile
    Parameter: id
    Payload: '
    CWE: CWE-89
    OWASP: A03:2021 - Injection
    Fix: Use parameterized queries (prepared statements)

============================================================

💾 Results saved to: scan_123e4567-e89b-12d3-a456-426614174000.json

✓ Test complete!
  View detailed results at: http://localhost:8000/api/scans/123e4567-e89b-12d3-a456-426614174000
```

## Understanding the Vulnerabilities

The test app has **3 intentionally vulnerable endpoints**:

### 1. Login Form (`/login`)
**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)  # Vulnerable!
```

**Attack:** Try entering `admin' OR '1'='1` as username

### 2. Search Form (`/search`)
**Vulnerable Code:**
```python
sql = f"SELECT * FROM users WHERE username LIKE '%{query}%'"
cursor.execute(sql)  # Vulnerable!
```

**Attack:** Try entering `' OR '1'='1` in search

### 3. Profile Page (`/profile?id=1`)
**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)  # Vulnerable!
```

**Attack:** Try visiting `/profile?id=1 OR 1=1`

## Manual Testing (Optional)

You can also test manually to see the vulnerabilities in action:

### Test 1: Login Bypass
1. Visit http://localhost:5000/login
2. Enter username: `admin' OR '1'='1-- `
3. Enter any password
4. Click Login
5. You'll see "Login successful!" even with wrong password

### Test 2: Search Injection
1. Visit http://localhost:5000/search
2. Enter: `' OR '1'='1`
3. Click Search
4. You'll see all users or an error message

### Test 3: Profile Injection
1. Visit: `http://localhost:5000/profile?id=1 OR 1=1`
2. You'll see user data or an error message

## Using the API Directly

You can also test using curl:

```bash
# Start a scan
curl -X POST http://localhost:8000/api/scans/start \
  -H "Content-Type: application/json" \
  -d '{"target_url": "http://localhost:5000", "max_depth": 2}'

# Check results (replace {scan_id} with actual ID)
curl http://localhost:8000/api/scans/{scan_id}
```

## Using the Interactive API Docs

1. Visit http://localhost:8000/docs
2. Try the endpoints interactively
3. See real-time scan progress
4. Download results as JSON

## Cleanup

When you're done testing:

1. **Stop the test app** (Terminal 1): Press `Ctrl+C`
2. **Stop AttackerTool API** (Terminal 2): Press `Ctrl+C`
3. **Clean up test database** (optional):
   ```bash
   cd test_app
   rm test.db
   ```

## Troubleshooting

### Issue: "Address already in use"
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
python vulnerable_app.py  # Edit app.run(port=5001) in the file
```

### Issue: "Flask not installed"
```bash
cd test_app
pip install flask
```

### Issue: "Module 'app' not found"
```bash
# Make sure you're in the backend directory
cd backend
python -m uvicorn app.main:app --reload
```

## Next Steps

After confirming AttackerTool works:

1. ✅ **Study the results** - Review each vulnerability
2. ✅ **Read remediation guidance** - Learn how to fix SQLi
3. ✅ **Explore the code** - See how detection works
4. ✅ **Try different payloads** - Modify the test payloads
5. ✅ **Build your own tests** - Create new vulnerable endpoints

## Alternative: Docker on Different Machine

If you have access to a machine with macOS Ventura+ or Linux, you can use Docker:

```bash
# Install Docker Desktop on that machine
# Then run DVWA:
docker run -d -p 80:80 vulnerables/web-dvwa

# Access at http://localhost
# Default credentials: admin/password
```

## Resources

- **Test App Code**: `test_app/vulnerable_app.py`
- **AttackerTool Source**: `backend/app/`
- **Full Documentation**: `README.md`
- **Quick Start**: `docs/QUICK_START.md`

---

**You're all set to test!** The vulnerable app provides a safe, local environment to learn about SQL injection and security testing. 🔒
