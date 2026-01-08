"""
Job Description Scraper Module
Fetches and extracts job description content from URLs
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict
import re


class JDScraper:
    """Scrape job descriptions from URLs"""

    @staticmethod
    def fetch_job_description(url: str) -> Dict[str, any]:
        """
        Fetch and extract job description from a URL

        Args:
            url: URL of the job posting

        Returns:
            Dictionary containing job description text and metadata
        """
        try:
            # Set headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            # Extract text
            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            # Try to extract title
            title = None
            if soup.title:
                title = soup.title.string

            return {
                "success": True,
                "url": url,
                "title": title,
                "text": text,
                "length": len(text)
            }

        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Failed to fetch URL: {str(e)}",
                "text": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing content: {str(e)}",
                "text": None
            }

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format

        Args:
            url: URL string to validate

        Returns:
            True if valid, False otherwise
        """
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return url_pattern.match(url) is not None
