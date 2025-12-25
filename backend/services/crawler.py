import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set
import asyncio
from collections import deque
import re
import time


class DocumentationCrawler:
    """
    Crawls documentation websites and extracts clean text content.
    Handles internal links, removes navigation/scripts, and limits crawl depth.
    Optimized for speed and reliability with timeouts and retries.
    """
    
    def __init__(
        self,
        max_pages: int = 20,
        max_depth: int = 2,
        max_content_length: int = 40000,
        page_timeout: int = 8,
        max_total_time: int = 60
    ):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.max_content_length = max_content_length
        self.page_timeout = page_timeout
        self.max_total_time = max_total_time
        self.visited: Set[str] = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ModuleExtractor/1.0)'
        })
        self.start_time = None
    
    def _is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL is valid and within the same domain."""
        try:
            parsed = urlparse(url)
            base_parsed = urlparse(base_domain)
            
            # Must be http or https
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Should be same domain or subdomain
            if parsed.netloc != base_parsed.netloc:
                return False
            
            # Skip common non-content paths
            skip_patterns = [
                r'/api/',
                r'/download',
                r'/login',
                r'/signup',
                r'\.(pdf|zip|exe|dmg|jpg|png|gif|svg)$',
                r'#',
            ]
            
            for pattern in skip_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return False
            
            return True
        except:
            return False
    
    def _clean_text(self, soup: BeautifulSoup) -> str:
        """Extract and clean text content from HTML."""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Remove common navigation/UI classes
        for element in soup.find_all(class_=re.compile(
            r'nav|menu|sidebar|footer|header|breadcrumb|pagination|social|share',
            re.IGNORECASE
        )):
            element.decompose()
        
        # Get text and clean it
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    async def _fetch_page(self, url: str, retries: int = 2) -> tuple[str, str]:
        """Fetch a single page with retries and timeout."""
        url_result, content, _ = await self._fetch_page_with_soup(url, retries)
        return url_result, content
    
    async def _fetch_page_with_soup(self, url: str, retries: int = 2) -> tuple[str, str, BeautifulSoup]:
        """Fetch a single page with retries and timeout, returning content and soup."""
        for attempt in range(retries + 1):
            try:
                # Check overall timeout
                if self.start_time and (time.time() - self.start_time) > self.max_total_time:
                    return url, "", None
                
                # Run blocking request in thread pool with timeout
                loop = asyncio.get_event_loop()
                response = await asyncio.wait_for(
                    loop.run_in_executor(
                        None,
                        lambda: self.session.get(url, timeout=self.page_timeout)
                    ),
                    timeout=self.page_timeout + 2
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                text = self._clean_text(soup)
                
                # Limit individual page content
                if len(text) > 5000:
                    text = text[:5000] + "... [truncated]"
                
                return url, text, soup
            except asyncio.TimeoutError:
                if attempt < retries:
                    await asyncio.sleep(0.5)
                    continue
                print(f"Timeout fetching {url} (attempt {attempt + 1})")
                return url, "", None
            except Exception as e:
                if attempt < retries:
                    await asyncio.sleep(0.5)
                    continue
                print(f"Error fetching {url}: {str(e)}")
                return url, "", None
        
        return url, "", None
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str, base_domain: str) -> List[str]:
        """Extract valid internal links from a page."""
        links = []
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            absolute_url = urljoin(base_url, href)
            
            if self._is_valid_url(absolute_url, base_domain):
                links.append(absolute_url)
        
        return links
    
    async def crawl_documentation(self, start_url: str) -> str:
        """
        Crawl documentation starting from a URL.
        Returns concatenated clean text from all crawled pages.
        Optimized for speed with concurrent fetching and early stopping.
        """
        self.start_time = time.time()
        parsed_start = urlparse(start_url)
        base_domain = f"{parsed_start.scheme}://{parsed_start.netloc}"
        
        self.visited.clear()
        queue = deque([(start_url, 0)])  # (url, depth)
        all_content = []
        total_length = 0
        
        # Prioritize main page and immediate children
        priority_urls = {start_url}
        
        while queue and len(self.visited) < self.max_pages and total_length < self.max_content_length:
            # Check overall timeout
            if (time.time() - self.start_time) > self.max_total_time:
                print(f"Reached max time limit ({self.max_total_time}s), stopping crawl")
                break
            
            current_url, depth = queue.popleft()
            
            if current_url in self.visited or depth > self.max_depth:
                continue
            
            self.visited.add(current_url)
            
            # Fetch page and get both content and HTML for link extraction
            url, content, soup = await self._fetch_page_with_soup(current_url)
            
            if content:
                # Truncate if needed
                remaining = self.max_content_length - total_length
                if remaining <= 0:
                    break
                    
                if len(content) > remaining:
                    content = content[:remaining]
                
                all_content.append(f"\n\n--- Content from {url} ---\n\n{content}")
                total_length += len(content)
                
                # Extract links from the soup we already have (no double fetch)
                if soup and depth < self.max_depth and len(self.visited) < self.max_pages:
                    try:
                        links = self._extract_links(soup, current_url, base_domain)
                        
                        # Limit number of links to avoid explosion
                        links = links[:10]  # Max 10 links per page
                        
                        for link in links:
                            if link not in self.visited and link not in [q[0] for q in queue]:
                                # Prioritize links from main page
                                if link in priority_urls or depth == 0:
                                    queue.appendleft((link, depth + 1))
                                else:
                                    queue.append((link, depth + 1))
                    except:
                        pass
            
            # Reduced delay for faster crawling
            if len(self.visited) % 3 == 0:  # Only delay every 3rd page
                await asyncio.sleep(0.2)
        
        if not all_content:
            # If we got nothing, try just the main page
            url, content, _ = await self._fetch_page_with_soup(start_url)
            if content:
                all_content.append(f"Content from {start_url}:\n{content}")
        
        return "\n".join(all_content) if all_content else ""

