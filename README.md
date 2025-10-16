# AttackerTool - Web Application Security Scanner

A Python-based security testing tool focused on detecting SQL injection vulnerabilities in web applications. This tool is designed specifically for testing AI-generated code for security flaws.

⚠️ **IMPORTANT**: This tool should ONLY be used on applications you own or have explicit permission to test. Unauthorized security testing is illegal.

## Features

### Phase 1 (Current)
- **Web Crawler**: Automatically discovers input points (forms and URL parameters)
- **SQL Injection Testing**:
  - Error-based SQLi detection
  - Boolean-based blind SQLi detection
- **Detailed Reporting**: CVSS scores, remediation steps, and evidence
- **REST API**: FastAPI-based backend for integration

## Project Structure

```
AttackerTool/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── scanner/
│   │   │   ├── __init__.py
│   │   │   └── crawler.py       # Web crawler
│   │   └── modules/
│   │       ├── __init__.py
│   │       └── sql_injection.py # SQL injection tester
│   ├── requirements.txt
│   └── tests/
├── docs/
│   ├── Initial Prompt
│   ├── Project_Recommendations.md
│   └── Phase1_SQL_Injection_Testing.md
├── README.md
└── LICENSE
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/wdrew31/AttackerTool.git
cd AttackerTool
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Running the Application

### Start the API Server

```bash
# From the backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API Base: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

## Usage

### Using the API

#### 1. Start a Scan

```bash
curl -X POST "http://localhost:8000/api/scans/start" \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "http://testsite.local",
    "max_depth": 2
  }'
```

Response:
```json
{
  "scan_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "queued",
  "message": "Scan started for http://testsite.local"
}
```

#### 2. Check Scan Status

```bash
curl "http://localhost:8000/api/scans/{scan_id}"
```

Response:
```json
{
  "scan_id": "123e4567-e89b-12d3-a456-426614174000",
  "target_url": "http://testsite.local",
  "status": "completed",
  "progress": 100,
  "pages_crawled": 5,
  "input_points_found": 3,
  "vulnerabilities_found": 2,
  "vulnerabilities": [
    {
      "type": "SQL Injection",
      "subtype": "Error-Based",
      "severity": "Critical",
      "url": "http://testsite.local/login",
      "parameter": "username",
      "payload": "' OR '1'='1",
      "cvss_score": 9.8
    }
  ],
  "summary": {
    "critical": 2,
    "high": 0,
    "medium": 0,
    "low": 0
  }
}
```

#### 3. List All Scans

```bash
curl "http://localhost:8000/api/scans"
```

### Using Python

```python
import requests

# Start a scan
response = requests.post(
    "http://localhost:8000/api/scans/start",
    json={
        "target_url": "http://testsite.local",
        "max_depth": 2
    }
)
scan_id = response.json()["scan_id"]

# Check status
status_response = requests.get(
    f"http://localhost:8000/api/scans/{scan_id}"
)
print(status_response.json())
```

## Testing

### Setting Up a Test Target

For testing purposes, we recommend using DVWA (Damn Vulnerable Web Application):

```bash
# Using Docker
docker run -d -p 80:80 vulnerables/web-dvwa

# Access at http://localhost
# Default credentials: admin/password
```

### Running Tests

```bash
# From the backend directory
pytest tests/
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/scans/start` | Start a new scan |
| GET | `/api/scans/{scan_id}` | Get scan results |
| GET | `/api/scans` | List all scans |
| DELETE | `/api/scans/{scan_id}` | Delete a scan |

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# Scanner Configuration
MAX_CRAWL_DEPTH=3
REQUEST_TIMEOUT=10
MAX_CONCURRENT_SCANS=5
```

## Security Considerations

### Legal and Ethical Use

- ✅ **DO**: Test your own applications
- ✅ **DO**: Get written permission before testing
- ✅ **DO**: Use on intentionally vulnerable apps (DVWA, WebGoat)
- ❌ **DON'T**: Test applications without permission
- ❌ **DON'T**: Use for malicious purposes
- ❌ **DON'T**: Run aggressive scans on production systems

### Rate Limiting

The scanner includes built-in rate limiting to prevent:
- Overloading target servers
- Triggering IDS/IPS systems
- Denial of Service

## Vulnerability Detection

### SQL Injection Types Detected

#### 1. Error-Based SQLi
- **Detection Method**: Looks for database error messages in responses
- **Severity**: Critical
- **CVSS Score**: 9.8
- **Example Payload**: `' OR '1'='1`

#### 2. Boolean-Based Blind SQLi
- **Detection Method**: Compares responses to TRUE/FALSE conditions
- **Severity**: High
- **CVSS Score**: 8.6
- **Example Payload**: `' AND '1'='1` vs `' AND '1'='2`

## Remediation Guidance

For each vulnerability found, AttackerTool provides:

1. **Severity Rating**: Critical, High, Medium, Low
2. **CVSS Score**: Industry-standard scoring
3. **CWE Mapping**: Common Weakness Enumeration
4. **OWASP Top 10**: Reference to OWASP category
5. **Remediation Steps**: Specific fix instructions
6. **Code Examples**: Secure coding patterns

### Example Remediation

**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**Secure Code:**
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

## Troubleshooting

### Common Issues

#### 1. Module Import Errors

```bash
# Make sure you're in the backend directory
cd backend
python -m uvicorn app.main:app --reload
```

#### 2. Connection Refused

```bash
# Check if the server is running
curl http://localhost:8000/health

# Check for port conflicts
lsof -i :8000
```

#### 3. Scan Not Completing

- Check target URL is accessible
- Verify no firewall blocking
- Check logs for errors

### Debugging

Enable debug logging:

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Run with debug output
python -m uvicorn app.main:app --reload --log-level debug
```

## Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Style

This project follows PEP 8 style guidelines:

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Roadmap

### Phase 1 ✅ (Current)
- [x] Web crawler
- [x] Error-based SQLi detection
- [x] Boolean-based SQLi detection
- [x] REST API
- [x] Basic reporting

### Phase 1.5 (Next)
- [ ] Time-based blind SQLi
- [ ] Union-based SQLi
- [ ] Web-based frontend dashboard
- [ ] Database storage (SQLite)
- [ ] Enhanced reporting (PDF export)

### Phase 2 (Future)
- [ ] XSS (Cross-Site Scripting) testing
- [ ] Authentication testing
- [ ] API security testing
- [ ] CSRF detection
- [ ] User authentication
- [ ] Multi-user support

### Phase 3 (Future)
- [ ] CI/CD integration
- [ ] Custom test profiles
- [ ] Scheduled scans
- [ ] Compliance reporting (OWASP Top 10, PCI DSS)
- [ ] Machine learning for anomaly detection

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Resources

### Learning SQL Injection
- [PortSwigger SQL Injection Labs](https://portswigger.net/web-security/sql-injection)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackTheBox Academy](https://academy.hackthebox.com/)

### Practice Platforms
- [DVWA](http://www.dvwa.co.uk/) - Damn Vulnerable Web Application
- [WebGoat](https://owasp.org/www-project-webgoat/) - OWASP learning platform
- [bWAPP](http://www.itsecgames.com/) - Buggy Web Application
- [Juice Shop](https://owasp.org/www-project-juice-shop/) - Modern vulnerable app

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is provided for educational and authorized testing purposes only. The developers assume no liability for misuse or damage caused by this tool. Always ensure you have explicit permission before testing any web application.

## Support

For issues, questions, or contributions:
- GitHub Issues: [https://github.com/wdrew31/AttackerTool/issues](https://github.com/wdrew31/AttackerTool/issues)
- Documentation: [docs/](docs/)

## Acknowledgments

- OWASP Foundation for security research and standards
- PortSwigger for SQL injection detection techniques
- FastAPI team for the excellent web framework

---

**Version**: 0.1.0  
**Last Updated**: October 2025  
**Status**: Phase 1 Complete
