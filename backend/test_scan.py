#!/usr/bin/env python3
"""
Simple test script to demonstrate AttackerTool usage
Run this after starting the API server
"""

import requests
import time
import json
from typing import Dict, Any


def print_banner():
    """Print a nice banner"""
    print("=" * 60)
    print("  AttackerTool - SQL Injection Scanner Test")
    print("=" * 60)
    print()


def check_api_health(base_url: str) -> bool:
    """Check if API is running"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✓ API is healthy and running")
            return True
        else:
            print("✗ API returned unexpected status code")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to API: {e}")
        print("\nMake sure the API is running:")
        print("  cd backend")
        print("  python -m uvicorn app.main:app --reload")
        return False


def start_scan(base_url: str, target_url: str, max_depth: int = 2) -> str:
    """Start a new scan"""
    print(f"\n🔍 Starting scan of: {target_url}")
    print(f"   Max crawl depth: {max_depth}")
    
    try:
        response = requests.post(
            f"{base_url}/api/scans/start",
            json={
                "target_url": target_url,
                "max_depth": max_depth
            },
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        scan_id = data["scan_id"]
        
        print(f"✓ Scan started successfully")
        print(f"  Scan ID: {scan_id}")
        return scan_id
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to start scan: {e}")
        return None


def monitor_scan(base_url: str, scan_id: str) -> Dict[str, Any]:
    """Monitor scan progress until completion"""
    print(f"\n⏳ Monitoring scan progress...")
    
    while True:
        try:
            response = requests.get(
                f"{base_url}/api/scans/{scan_id}",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            status = data["status"]
            progress = data["progress"]
            
            # Print progress
            bar_length = 40
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\r  [{bar}] {progress}% - {status}", end="", flush=True)
            
            # Check if complete
            if status in ["completed", "failed"]:
                print()  # New line after progress bar
                return data
            
            time.sleep(2)  # Wait before checking again
            
        except requests.exceptions.RequestException as e:
            print(f"\n✗ Error monitoring scan: {e}")
            return None


def print_results(results: Dict[str, Any]):
    """Print scan results in a nice format"""
    print("\n" + "=" * 60)
    print("  SCAN RESULTS")
    print("=" * 60)
    
    status = results.get("status")
    if status == "failed":
        print("✗ Scan failed")
        print(f"  Error: {results.get('error', 'Unknown error')}")
        return
    
    print(f"\n📊 Statistics:")
    print(f"  Target: {results.get('target_url')}")
    print(f"  Pages Crawled: {results.get('pages_crawled', 0)}")
    print(f"  Input Points Found: {results.get('input_points_found', 0)}")
    print(f"  Vulnerabilities Found: {results.get('vulnerabilities_found', 0)}")
    
    # Print summary
    summary = results.get('summary', {})
    if summary and any(summary.values()):
        print(f"\n🚨 Severity Breakdown:")
        if summary.get('critical', 0) > 0:
            print(f"  Critical: {summary['critical']} 🔴")
        if summary.get('high', 0) > 0:
            print(f"  High: {summary['high']} 🟠")
        if summary.get('medium', 0) > 0:
            print(f"  Medium: {summary['medium']} 🟡")
        if summary.get('low', 0) > 0:
            print(f"  Low: {summary['low']} 🟢")
    
    # Print vulnerabilities
    vulnerabilities = results.get('vulnerabilities', [])
    if vulnerabilities:
        print(f"\n🐛 Vulnerabilities Detected:")
        print("-" * 60)
        
        for i, vuln in enumerate(vulnerabilities, 1):
            print(f"\n[{i}] {vuln.get('type')} - {vuln.get('subtype')}")
            print(f"    Severity: {vuln.get('severity')} (CVSS: {vuln.get('cvss_score')})")
            print(f"    URL: {vuln.get('url')}")
            print(f"    Parameter: {vuln.get('parameter')}")
            print(f"    Payload: {vuln.get('payload')}")
            print(f"    CWE: {vuln.get('cwe')}")
            print(f"    OWASP: {vuln.get('owasp')}")
            
            # Print remediation summary
            remediation = vuln.get('remediation', {})
            if remediation:
                print(f"    Fix: {remediation.get('summary')}")
    else:
        print("\n✓ No vulnerabilities detected!")
        print("  The application appears to be secure against SQL injection.")
    
    print("\n" + "=" * 60)


def save_results(results: Dict[str, Any], filename: str = "scan_results.json"):
    """Save results to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {filename}")
    except Exception as e:
        print(f"\n✗ Failed to save results: {e}")


def main():
    """Main test function"""
    print_banner()
    
    # Configuration
    API_BASE_URL = "http://localhost:8000"
    
    # Example target URLs (replace with your test target)
    # For testing, use DVWA: docker run -d -p 80:80 vulnerables/web-dvwa
    TARGET_URL = input("Enter target URL (e.g., http://localhost:5000): ").strip()
    
    if not TARGET_URL:
        print("No target URL provided. Using example: http://localhost:5000")
        TARGET_URL = "http://localhost:5000"
    
    # Add http:// if missing
    if not TARGET_URL.startswith(('http://', 'https://')):
        print(f"⚠️  Adding http:// prefix to URL")
        TARGET_URL = f"http://{TARGET_URL}"
        print(f"   Using: {TARGET_URL}")
    
    # Confirm before scanning
    print(f"\n⚠️  WARNING: This will perform security testing on {TARGET_URL}")
    print("   Make sure you have permission to test this application.")
    confirm = input("   Continue? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("Scan cancelled.")
        return
    
    # Check API
    if not check_api_health(API_BASE_URL):
        return
    
    # Start scan
    scan_id = start_scan(API_BASE_URL, TARGET_URL, max_depth=2)
    if not scan_id:
        return
    
    # Monitor scan
    results = monitor_scan(API_BASE_URL, scan_id)
    if not results:
        return
    
    # Print results
    print_results(results)
    
    # Save results
    save_results(results, f"scan_{scan_id}.json")
    
    print("\n✓ Test complete!")
    print(f"  View detailed results at: {API_BASE_URL}/api/scans/{scan_id}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
