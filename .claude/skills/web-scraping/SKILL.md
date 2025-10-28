---
name: web-scraping
description: Web scraping with anti-bot bypass, content extraction, undocumented APIs and poison pill detection. Use when extracting content from websites, handling paywalls, implementing scraping cascades or processing social media. Covers requests, trafilatura, Playwright with stealth mode, yt-dlp and instaloader patterns.
---

# Web scraping methodology

Patterns for reliable, ethical web scraping with fallback strategies and anti-bot handling.

## Scraping cascade architecture

Implement multiple extraction strategies with automatic fallback:

```python
from abc import ABC, abstractmethod
from typing import Optional
import requests
from bs4 import BeautifulSoup
import trafilatura

#for .py files
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

#for .ipynb files
import asyncio
from playwright.async_api import async_playwright

class ScrapingResult:
    def __init__(self, content: str, title: str, method: str):
        self.content = content
        self.title = title
        self.method = method  # Track which method succeeded

class Scraper(ABC):
    @abstractmethod
    def fetch(self, url: str) -> Optional[ScrapingResult]: ...

class TrafilaturaСscraper(Scraper):
    """Fast, lightweight extraction for standard articles."""

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return None

            content = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=True,
                favor_recall=True
            )

            if not content or len(content) < 100:
                return None

            # Extract title separately
            soup = BeautifulSoup(downloaded, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text() if title else ''

            return ScrapingResult(content, title_text, 'trafilatura')
        except Exception:
            return None

class RequestsScraper(Scraper):
    """HTTP requests with rotating user agents."""

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    ]

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        import random

        headers = {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script/style elements
            for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
                element.decompose()

            # Find main content
            main = soup.find('main') or soup.find('article') or soup.find('body')
            content = main.get_text(separator='\n', strip=True) if main else ''

            title = soup.find('title')
            title_text = title.get_text() if title else ''

            if len(content) < 100:
                return None

            return ScrapingResult(content, title_text, 'requests')
        except Exception:
            return None

class PlaywrightScraper(Scraper):
    """Heavy JavaScript rendering with stealth mode for anti-bot bypass."""

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()

                # Apply stealth to avoid detection
                stealth_sync(page)

                page.goto(url, wait_until='networkidle', timeout=60000)

                # Wait for content to load
                page.wait_for_timeout(2000)

                # Extract content
                content = page.evaluate('''() => {
                    const article = document.querySelector('article, main, .content, #content');
                    return article ? article.innerText : document.body.innerText;
                }''')

                title = page.title()

                browser.close()

                if len(content) < 100:
                    return None

                return ScrapingResult(content, title, 'playwright')
        except Exception:
            return None

class PlaywrightScraperAsync:
    """Async Playwright scraper for Jupyter notebooks (.ipynb files).
    
    Jupyter notebooks run their own event loop, so sync Playwright won't work.
    Use this async version with `await` in notebook cells.
    """

    async def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()

                # Note: playwright-stealth async version
                # from playwright_stealth import stealth_async
                # await stealth_async(page)

                await page.goto(url, wait_until='networkidle', timeout=60000)

                # Wait for content to load
                await page.wait_for_timeout(2000)

                # Extract content
                content = await page.evaluate('''() => {
                    const article = document.querySelector('article, main, .content, #content');
                    return article ? article.innerText : document.body.innerText;
                }''')

                title = await page.title()

                await browser.close()

                if len(content) < 100:
                    return None

                return ScrapingResult(content, title, 'playwright_async')
        except Exception:
            return None

# Usage in Jupyter notebook cells:
# scraper = PlaywrightScraperAsync()
# result = await scraper.fetch('https://example.com')

class ScrapingCascade:
    """Try multiple scrapers in order until one succeeds."""

    def __init__(self):
        self.scrapers = [
            TrafilaturaСscraper(),
            RequestsScraper(),
            PlaywrightScraper(),
        ]

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        for scraper in self.scrapers:
            result = scraper.fetch(url)
            if result:
                return result
        return None
```

## Undocumented APIs

### Finding undocumented APIs

Use browser developer tools to discover APIs:

1. **Open developer tools** (right-click → Inspect, or F12)
2. **Go to the Network tab** to monitor all requests
3. **Filter by Fetch/XHR** to show only API calls
4. **Trigger the action** you want to capture (search, scroll, click)
5. **Analyze the response** — usually JSON with key-value pairs
6. **Copy as cURL** (right-click the request)
7. **Convert to code** using [curlconverter.com](https://curlconverter.com/)

### Stripping down API requests

When you copy a cURL from dev tools, it includes many parameters. Strip it down by:

1. **Remove unnecessary cookies** — test without them first
2. **Keep authentication tokens** if required
3. **Identify the input parameters** you can modify (like `prefix` for search terms)
4. **Test parameter values** — some expire, so periodically verify

### Example: Reverse-engineering an autocomplete API

```python
import requests
import time

def search_suggestions(keyword: str) -> dict:
    """
    Get autocompleted search suggestions from an undocumented API.
    Stripped down from browser dev tools capture.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    params = {
        'prefix': keyword,
        'suggestion-type': ['WIDGET', 'KEYWORD'],
        'alias': 'aps',
        'plain-mid': '1',
    }

    response = requests.get(
        'https://completion.amazon.com/api/2017/suggestions',
        params=params,
        headers=headers
    )
    return response.json()

# Collect suggestions for multiple keywords
keywords = ['a', 'b', 'cookie', 'sock']
data = []

for keyword in keywords:
    suggestions = search_suggestions(keyword)
    suggestions['search_word'] = keyword  # track seed keyword
    time.sleep(1)  # rate limit yourself
    data.extend(suggestions.get('suggestions', []))
```
*Source: [Leon Yin, "Finding Undocumented APIs," Inspect Element](https://inspectelement.org/apis.html), 2023*

## Poison pill detection

Detect paywalls, anti-bot pages, and other failures:

```python
from dataclasses import dataclass
from enum import Enum
import re

class PoisonPillType(Enum):
    PAYWALL = 'paywall'
    CAPTCHA = 'captcha'
    RATE_LIMIT = 'rate_limit'
    CLOUDFLARE = 'cloudflare'
    LOGIN_REQUIRED = 'login_required'
    NOT_FOUND = 'not_found'
    NONE = 'none'

@dataclass
class PoisonPillResult:
    detected: bool
    type: PoisonPillType
    confidence: float
    details: str

class PoisonPillDetector:
    PATTERNS = {
        PoisonPillType.PAYWALL: [
            r'subscribe to continue',
            r'subscription required',
            r'become a member',
            r'sign up to read',
            r'you\'ve reached your limit',
