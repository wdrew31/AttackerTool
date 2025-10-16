"""
Web Crawler Module
Discovers input points (forms and URL parameters) on target websites
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from typing import List, Dict, Any, Set
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebCrawler:
    """
    Web crawler that discovers input points for security testing
    """
    
    def __init__(self, base_url: str, max_depth: int = 3, timeout: int = 10):
        """
        Initialize the web crawler
        
        Args:
            base_url: The starting URL to crawl
            max_depth: Maximum depth to crawl (default: 3)
            timeout: Request timeout in seconds (default: 10)
        """
        self.base_url = base_url
        self.max_depth = max_depth
        self.timeout = timeout
        self.visited_urls: Set[str] = set()
        self.input_points: List[Dict[str, Any]] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AttackerTool/0.1.0 Security Scanner'
        })
    
    def crawl(self) -> List[Dict[str, Any]]:
        """
        Start crawling from the base URL
        
        Returns:
            List of discovered input points
        """
        logger.info(f"Starting crawl of {self.base_url}")
        self._crawl_recursive(self.base_url, 0)
        logger.info(f"Crawl complete. Found {len(self.input_points)} input points across {len(self.visited_urls)} pages")
        return self.input_points
    
    def _crawl_recursive(self, url: str, depth: int):
        """
        Recursively crawl pages up to max_depth
        
        Args:
            url: Current URL to crawl
            depth: Current depth level
        """
        # Check stopping conditions
        if depth > self.max_depth:
            logger.debug(f"Max depth reached at {url}")
            return
        
        if url in self.visited_urls:
            logger.debug(f"Already visited {url}")
            return
        
        # Check if URL is from same domain
        if not self._is_same_domain(url):
            logger.debug(f"Skipping external URL {url}")
            return
        
        self.visited_urls.add(url)
        logger.info(f"Crawling: {url} (depth: {depth})")
        
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract forms
            forms = soup.find_all('form')
            for form in forms:
                self._extract_form_inputs(form, url)
            
            # Extract URL parameters from current page
            self._extract_url_parameters(url)
            
            # Follow links if we haven't reached max depth
            if depth < self.max_depth:
                links = soup.find_all('a', href=True)
                for link in links:
                    next_url = urljoin(url, link['href'])
                    # Remove fragment identifier
                    next_url = next_url.split('#')[0]
                    self._crawl_recursive(next_url, depth + 1)
        
        except requests.RequestException as e:
            logger.error(f"Error crawling {url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error crawling {url}: {e}")
    
    def _extract_form_inputs(self, form, page_url: str):
        """
        Extract input fields from an HTML form
        
        Args:
            form: BeautifulSoup form element
            page_url: URL of the page containing the form
        """
        action = form.get('action', '')
        method = form.get('method', 'get').upper()
        form_url = urljoin(page_url, action) if action else page_url
        
        inputs = []
        for input_tag in form.find_all(['input', 'textarea', 'select']):
            input_name = input_tag.get('name')
            input_type = input_tag.get('type', 'text')
            
            # Skip buttons and submits (we don't test these)
            if input_type in ['submit', 'button', 'image', 'reset']:
                continue
            
            if input_name:
                inputs.append({
                    'name': input_name,
                    'type': input_type,
                    'value': input_tag.get('value', '')
                })
        
        if inputs:
            input_point = {
                'type': 'form',
                'url': form_url,
                'method': method,
                'inputs': inputs,
                'page_url': page_url
            }
            self.input_points.append(input_point)
            logger.info(f"Found form with {len(inputs)} inputs at {page_url}")
    
    def _extract_url_parameters(self, url: str):
        """
        Extract URL query parameters
        
        Args:
            url: URL to extract parameters from
        """
        parsed = urlparse(url)
        if parsed.query:
            params = parse_qs(parsed.query)
            for param_name, param_values in params.items():
                # Use first value if multiple values exist
                param_value = param_values[0] if param_values else ''
                
                input_point = {
                    'type': 'url_param',
                    'url': f"{parsed.scheme}://{parsed.netloc}{parsed.path}",
                    'method': 'GET',
                    'param_name': param_name,
                    'param_value': param_value
                }
                self.input_points.append(input_point)
                logger.info(f"Found URL parameter '{param_name}' at {url}")
    
    def _is_same_domain(self, url: str) -> bool:
        """
        Check if URL belongs to the same domain as base_url
        
        Args:
            url: URL to check
            
        Returns:
            True if same domain, False otherwise
        """
        base_domain = urlparse(self.base_url).netloc
        url_domain = urlparse(url).netloc
        return base_domain == url_domain
    
    def close(self):
        """Close the requests session"""
        self.session.close()
