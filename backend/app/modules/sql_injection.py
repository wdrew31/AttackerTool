"""
SQL Injection Testing Module
Tests for SQL injection vulnerabilities using error-based and boolean-based detection
"""

import requests
import re
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLInjectionTester:
    """
    SQL Injection vulnerability tester
    Supports error-based and boolean-based blind SQLi detection
    """
    
    def __init__(self):
        """Initialize the SQL injection tester"""
        self.error_patterns = self._load_error_patterns()
        self.payloads = self._load_payloads()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AttackerTool/0.1.0 Security Scanner'
        })
    
    def _load_error_patterns(self) -> List[str]:
        """
        Load regex patterns for detecting SQL errors
        
        Returns:
            List of compiled regex patterns
        """
        return [
            # MySQL
            r"SQL syntax.*MySQL",
            r"Warning.*mysql_.*",
            r"MySQLSyntaxErrorException",
            r"valid MySQL result",
            r"check the manual that corresponds to your MySQL",
            
            # PostgreSQL
            r"PostgreSQL.*ERROR",
            r"Warning.*\Wpg_.*",
            r"valid PostgreSQL result",
            r"Npgsql\.",
            r"PG::SyntaxError",
            
            # SQL Server
            r"Driver.*SQL[\-\_\ ]*Server",
            r"OLE DB.*SQL Server",
            r"SQLServer JDBC Driver",
            r"SqlException",
            r"Unclosed quotation mark after the character string",
            r"Microsoft SQL Native Client error",
            
            # Oracle
            r"ORA-[0-9][0-9][0-9][0-9]",
            r"Oracle error",
            r"Warning.*\Woci_.*",
            r"Warning.*\Wora_.*",
            
            # Generic SQL errors
            r"SQL error",
            r"SQL syntax",
            r"syntax error",
            r"unexpected end of SQL command",
            r"Warning.*SQL.*",
            r"quoted string not properly terminated",
        ]
    
    def _load_payloads(self) -> Dict[str, List[str]]:
        """
        Load test payloads for different SQLi types
        
        Returns:
            Dictionary of payload lists by type
        """
        return {
            'error_based': [
                "'",
                "\"",
                "')",
                "';",
                "' OR '1'='1",
                "' OR '1'='1' --",
                "' OR '1'='1' #",
                "' OR '1'='1' /*",
                "admin'--",
                "admin' #",
                "admin'/*",
                "' OR 1=1--",
                "') OR ('1'='1",
                "1' OR '1'='1",
                "' OR 'x'='x",
                "1' AND '1'='2' UNION SELECT NULL--",
            ],
            'boolean_based': [
                # TRUE conditions
                "' AND '1'='1",
                "1' AND '1'='1",
                "' AND 1=1--",
                "1 AND 1=1",
                # FALSE conditions  
                "' AND '1'='2",
                "1' AND '1'='2",
                "' AND 1=2--",
                "1 AND 1=2",
            ]
        }
    
    def test_input_point(self, input_point: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Test a single input point for SQL injection vulnerabilities
        
        Args:
            input_point: Dictionary containing input point details
            
        Returns:
            List of discovered vulnerabilities
        """
        vulnerabilities = []
        
        logger.info(f"Testing {input_point['type']} at {input_point['url']}")
        
        # Get baseline response
        baseline_response = self._send_request(input_point, None)
        
        if not baseline_response:
            logger.warning(f"Failed to get baseline response for {input_point['url']}")
            return vulnerabilities
        
        # Test error-based SQLi
        error_vulns = self._test_error_based(input_point, baseline_response)
        vulnerabilities.extend(error_vulns)
        
        # If error-based found, skip boolean (already confirmed vulnerable)
        if error_vulns:
            logger.info(f"Error-based SQLi found, skipping boolean tests")
            return vulnerabilities
        
        # Test boolean-based SQLi
        boolean_vulns = self._test_boolean_based(input_point, baseline_response)
        vulnerabilities.extend(boolean_vulns)
        
        return vulnerabilities
    
    def _test_error_based(self, input_point: Dict[str, Any], 
                          baseline: requests.Response) -> List[Dict[str, Any]]:
        """
        Test for error-based SQL injection
        
        Args:
            input_point: Input point to test
            baseline: Baseline response for comparison
            
        Returns:
            List of vulnerabilities found
        """
        vulnerabilities = []
        
        for payload in self.payloads['error_based']:
            response = self._send_request(input_point, payload)
            
            if not response:
                continue
            
            # Check for SQL error messages
            for pattern in self.error_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    evidence = self._extract_evidence(response.text, pattern)
                    
                    vulnerability = {
                        'type': 'SQL Injection',
                        'subtype': 'Error-Based',
                        'severity': 'Critical',
                        'url': input_point['url'],
                        'method': input_point['method'],
                        'parameter': self._get_param_name(input_point),
                        'payload': payload,
                        'evidence': evidence,
                        'description': 'SQL error messages exposed, indicating SQL injection vulnerability',
                        'cvss_score': 9.8,
                        'cwe': 'CWE-89',
                        'owasp': 'A03:2021 - Injection',
                        'remediation': {
                            'summary': 'Use parameterized queries (prepared statements)',
                            'steps': [
                                'Replace string concatenation with parameterized queries',
                                'Use ORM frameworks that handle parameterization automatically',
                                'Validate and sanitize all user inputs',
                                'Apply principle of least privilege to database accounts',
                                'Implement proper error handling to avoid exposing database errors'
                            ]
                        }
                    }
                    
                    vulnerabilities.append(vulnerability)
                    logger.info(f"✓ Error-based SQLi found at {input_point['url']} with payload: {payload}")
                    # Found vulnerability, return immediately
                    return vulnerabilities
        
        return vulnerabilities
    
    def _test_boolean_based(self, input_point: Dict[str, Any],
                           baseline: requests.Response) -> List[Dict[str, Any]]:
        """
        Test for boolean-based blind SQL injection
        
        Args:
            input_point: Input point to test
            baseline: Baseline response for comparison
            
        Returns:
            List of vulnerabilities found
        """
        vulnerabilities = []
        
        # Get TRUE and FALSE payloads
        true_payloads = self.payloads['boolean_based'][0:4]
        false_payloads = self.payloads['boolean_based'][4:8]
        
        for true_payload, false_payload in zip(true_payloads, false_payloads):
            true_response = self._send_request(input_point, true_payload)
            false_response = self._send_request(input_point, false_payload)
            
            if not true_response or not false_response:
                continue
            
            # Compare responses
            if self._responses_differ_significantly(true_response, false_response, baseline):
                vulnerability = {
                    'type': 'SQL Injection',
                    'subtype': 'Boolean-Based Blind',
                    'severity': 'High',
                    'url': input_point['url'],
                    'method': input_point['method'],
                    'parameter': self._get_param_name(input_point),
                    'payload': f"TRUE: {true_payload}, FALSE: {false_payload}",
                    'evidence': f"Response differs between TRUE and FALSE conditions. TRUE length: {len(true_response.text)}, FALSE length: {len(false_response.text)}",
                    'description': 'Application behavior differs based on SQL condition truth value, indicating blind SQL injection',
                    'cvss_score': 8.6,
                    'cwe': 'CWE-89',
                    'owasp': 'A03:2021 - Injection',
                    'remediation': {
                        'summary': 'Use parameterized queries (prepared statements)',
                        'steps': [
                            'Replace string concatenation with parameterized queries',
                            'Use ORM frameworks that handle parameterization automatically',
                            'Validate and sanitize all user inputs',
                            'Apply principle of least privilege to database accounts',
                            'Implement consistent error handling'
                        ]
                    }
                }
                
                vulnerabilities.append(vulnerability)
                logger.info(f"✓ Boolean-based blind SQLi found at {input_point['url']}")
                return vulnerabilities
        
        return vulnerabilities
    
    def _send_request(self, input_point: Dict[str, Any], 
                     payload: Optional[str] = None) -> Optional[requests.Response]:
        """
        Send HTTP request with optional payload
        
        Args:
            input_point: Input point details
            payload: Test payload (None for baseline request)
            
        Returns:
            Response object or None if request failed
        """
        try:
            if input_point['type'] == 'form':
                data = {}
                for input_field in input_point['inputs']:
                    if payload and input_field['type'] not in ['submit', 'button', 'hidden']:
                        data[input_field['name']] = payload
                    else:
                        data[input_field['name']] = input_field.get('value', 'test')
                
                if input_point['method'] == 'POST':
                    return self.session.post(input_point['url'], data=data, timeout=10, allow_redirects=True)
                else:
                    return self.session.get(input_point['url'], params=data, timeout=10, allow_redirects=True)
            
            elif input_point['type'] == 'url_param':
                params = {input_point['param_name']: payload if payload else input_point['param_value']}
                return self.session.get(input_point['url'], params=params, timeout=10, allow_redirects=True)
        
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def _responses_differ_significantly(self, resp1: requests.Response, 
                                       resp2: requests.Response,
                                       baseline: requests.Response) -> bool:
        """
        Check if two responses differ significantly, indicating vulnerability
        
        Args:
            resp1: First response (TRUE condition)
            resp2: Second response (FALSE condition)
            baseline: Baseline response for reference
            
        Returns:
            True if responses differ significantly
        """
        # Check status codes
        if resp1.status_code != resp2.status_code:
            # Both should be similar to baseline
            if resp1.status_code == baseline.status_code and resp2.status_code != baseline.status_code:
                return True
        
        # Check content length difference (>10% change)
        len1, len2 = len(resp1.text), len(resp2.text)
        
        if len1 > 0 and len2 > 0:
            diff_percentage = abs(len1 - len2) / max(len1, len2)
            if diff_percentage > 0.1:  # More than 10% difference
                return True
        
        # Check if content is completely different
        if len1 > 0 and len2 > 0:
            # Simple similarity check - count common substrings
            words1 = set(resp1.text.split())
            words2 = set(resp2.text.split())
            if words1 and words2:
                similarity = len(words1 & words2) / len(words1 | words2)
                if similarity < 0.7:  # Less than 70% similar
                    return True
        
        return False
    
    def _get_param_name(self, input_point: Dict[str, Any]) -> str:
        """
        Extract parameter name from input point
        
        Args:
            input_point: Input point details
            
        Returns:
            Parameter name
        """
        if input_point['type'] == 'url_param':
            return input_point['param_name']
        elif input_point['type'] == 'form' and input_point['inputs']:
            # Return first non-hidden input name
            for inp in input_point['inputs']:
                if inp['type'] != 'hidden':
                    return inp['name']
            return input_point['inputs'][0]['name']
        return 'unknown'
    
    def _extract_evidence(self, text: str, pattern: str, context_chars: int = 200) -> str:
        """
        Extract relevant evidence from response
        
        Args:
            text: Response text
            pattern: Regex pattern that matched
            context_chars: Number of characters to include around match
            
        Returns:
            Evidence string with context
        """
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            evidence = text[start:end].strip()
            # Clean up evidence
            evidence = ' '.join(evidence.split())  # Normalize whitespace
            if len(evidence) > 500:
                evidence = evidence[:500] + '...'
            return evidence
        return "Error pattern detected in response"
    
    def close(self):
        """Close the requests session"""
        self.session.close()
