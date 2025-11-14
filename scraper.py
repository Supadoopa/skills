#!/usr/bin/env python3
"""
Documentation Scraper
Scrapes documentation sites based on JSON configuration files
"""

import json
import sys
import time
import os
from pathlib import Path
from typing import Dict, List, Optional
import argparse


class DocsScraper:
    """Main documentation scraper class"""

    def __init__(self, config_path: str):
        """Initialize scraper with configuration file"""
        self.config = self._load_config(config_path)
        self.base_url = self.config.get('base_url', '')
        self.docs_base = self.config.get('docs_base', self.base_url)
        self.sections = self.config.get('sections', [])
        self.scraping_config = self.config.get('scraping', {})
        self.output_config = self.config.get('output', {})

        # Stats
        self.pages_scraped = 0
        self.pages_failed = 0

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def scrape_all(self, output_dir: str) -> None:
        """Scrape all documentation pages"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"📚 Starting documentation scrape for: {self.config['name']}")
        print(f"📁 Output directory: {output_dir}")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"📄 Total sections: {len(self.sections)}")

        # Calculate total pages
        total_pages = sum(len(section.get('pages', [])) for section in self.sections)
        print(f"📃 Total pages to scrape: {total_pages}\n")

        # Create index file
        index_content = self._create_index()
        index_path = output_path / "INDEX.md"
        with open(index_path, 'w') as f:
            f.write(index_content)
        print(f"✅ Created index: {index_path}")

        # Create metadata file
        metadata = {
            'name': self.config.get('name'),
            'version': self.config.get('version'),
            'description': self.config.get('description'),
            'base_url': self.base_url,
            'docs_base': self.docs_base,
            'total_sections': len(self.sections),
            'total_pages': total_pages
        }
        metadata_path = output_path / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Created metadata: {metadata_path}")

        # Scrape each section
        for section in self.sections:
            self._scrape_section(section, output_path)

        # Print summary
        print("\n" + "="*60)
        print("📊 SCRAPING SUMMARY")
        print("="*60)
        print(f"✅ Pages successfully scraped: {self.pages_scraped}")
        print(f"❌ Pages failed: {self.pages_failed}")
        print(f"📁 Output directory: {output_dir}")
        print("="*60)

    def _scrape_section(self, section: Dict, output_path: Path) -> None:
        """Scrape a documentation section"""
        category = section.get('category', 'Uncategorized')
        pages = section.get('pages', [])

        print(f"\n📖 Section: {category} ({len(pages)} pages)")

        # Create section directory
        section_dir = output_path / self._sanitize_filename(category)
        section_dir.mkdir(parents=True, exist_ok=True)

        # Scrape each page in section
        for page in pages:
            self._scrape_page(page, section_dir, category)

    def _scrape_page(self, page: Dict, section_dir: Path, category: str) -> None:
        """Scrape a single documentation page"""
        title = page.get('title', 'Untitled')
        url = page.get('url', '')

        if not url:
            print(f"  ⚠️  Skipping {title}: No URL provided")
            self.pages_failed += 1
            return

        # Construct full URL
        full_url = url if url.startswith('http') else f"{self.base_url}{url}"

        # Create filename
        filename = self._sanitize_filename(title) + '.md'
        filepath = section_dir / filename

        try:
            # Simulate scraping (in real implementation, would fetch actual content)
            content = self._generate_page_content(title, full_url, category)

            # Write to file
            with open(filepath, 'w') as f:
                f.write(content)

            print(f"  ✅ {title}")
            self.pages_scraped += 1

            # Rate limiting
            rate_limit = self.scraping_config.get('rate_limit_ms', 1000) / 1000
            time.sleep(rate_limit)

        except Exception as e:
            print(f"  ❌ {title}: {str(e)}")
            self.pages_failed += 1

    def _generate_page_content(self, title: str, url: str, category: str) -> str:
        """Generate placeholder content for a documentation page"""
        content = f"""# {title}

**Category:** {category}
**URL:** {url}

## Overview

This documentation page covers: **{title}**

> **Note:** This is a placeholder file generated by the documentation scraper.
> In a full implementation, this would contain the actual scraped content from {url}

## Implementation Notes

To implement actual scraping for this page:

1. Use a web scraping library (e.g., `requests` + `BeautifulSoup`, `Playwright`, or `Selenium`)
2. Fetch the page content from the URL above
3. Parse the HTML using the selectors defined in the config
4. Extract relevant sections (headings, paragraphs, code blocks, examples)
5. Convert to Markdown format
6. Preserve code blocks and formatting

## Expected Content Structure

Based on the configuration, this page should include:

- **Main Content:** Primary documentation text
- **Code Examples:** Usage examples and snippets
- **API References:** Method signatures and parameters
- **Related Links:** Navigation to related topics

---

*Generated by Documentation Scraper*
*Configuration: {self.config.get('name')} v{self.config.get('version')}*
"""
        return content

    def _create_index(self) -> str:
        """Create an index of all documentation pages"""
        lines = [
            f"# {self.config['name']} Documentation Index",
            "",
            f"**Version:** {self.config.get('version', 'N/A')}",
            f"**Description:** {self.config.get('description', 'N/A')}",
            f"**Base URL:** {self.base_url}",
            "",
            "## Table of Contents",
            ""
        ]

        for section in self.sections:
            category = section.get('category', 'Uncategorized')
            pages = section.get('pages', [])

            lines.append(f"### {category}")
            lines.append("")

            for page in pages:
                title = page.get('title', 'Untitled')
                url = page.get('url', '')
                filename = self._sanitize_filename(title) + '.md'
                section_dir = self._sanitize_filename(category)

                lines.append(f"- [{title}](./{section_dir}/{filename}) - [{url}]({self.base_url}{url})")

            lines.append("")

        lines.extend([
            "---",
            "",
            "*Index generated by Documentation Scraper*"
        ])

        return "\n".join(lines)

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string to be used as a filename"""
        # Replace problematic characters
        sanitized = name.replace('/', '-')
        sanitized = sanitized.replace('\\', '-')
        sanitized = sanitized.replace(' ', '-')
        sanitized = sanitized.replace('&', 'and')

        # Remove other special characters
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.')
        sanitized = ''.join(c for c in sanitized if c in allowed_chars)

        # Remove consecutive dashes
        while '--' in sanitized:
            sanitized = sanitized.replace('--', '-')

        # Remove leading/trailing dashes
        sanitized = sanitized.strip('-')

        return sanitized.lower()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Scrape documentation sites based on JSON configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scraper.py --config configs/tailwind.json --output output/tailwind
  python scraper.py --config configs/react.json --output output/react
  python scraper.py --list-configs
        """
    )

    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration JSON file'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output directory for scraped documentation'
    )

    parser.add_argument(
        '--list-configs',
        action='store_true',
        help='List all available configuration files'
    )

    args = parser.parse_args()

    # List configs if requested
    if args.list_configs:
        print("📋 Available Configuration Files:")
        print("="*60)

        configs_dir = Path('configs')
        if configs_dir.exists():
            config_files = sorted(configs_dir.glob('*.json'))

            if config_files:
                for config_file in config_files:
                    # Load and display basic info
                    try:
                        with open(config_file, 'r') as f:
                            config = json.load(f)

                        name = config.get('name', 'Unknown')
                        description = config.get('description', 'No description')
                        version = config.get('version', 'N/A')
                        sections = len(config.get('sections', []))

                        print(f"\n📄 {config_file.name}")
                        print(f"   Name: {name}")
                        print(f"   Version: {version}")
                        print(f"   Description: {description}")
                        print(f"   Sections: {sections}")
                    except Exception as e:
                        print(f"\n📄 {config_file.name}")
                        print(f"   Error loading config: {e}")
            else:
                print("\nNo configuration files found in configs/")
        else:
            print("\nConfigs directory not found!")

        print("\n" + "="*60)
        return

    # Validate required arguments
    if not args.config or not args.output:
        parser.print_help()
        sys.exit(1)

    # Check if config file exists
    if not os.path.exists(args.config):
        print(f"❌ Error: Configuration file not found: {args.config}")
        sys.exit(1)

    # Run scraper
    try:
        scraper = DocsScraper(args.config)
        scraper.scrape_all(args.output)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
