"""
BIS LIMS Portal Scraper

Scrapes test parameter data from BIS LIMS portal to create datasets
similar to the cement dataset format.

Usage:
    python src/collectors/lims_scraper.py --start 1 --end 2000 --output food_standards.csv
    
IMPORTANT: 
- Use responsibly with reasonable delays
- Check BIS terms of service
- This scrapes publicly available data only
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import argparse
import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/lims_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LIMSScraper:
    """Scraper for BIS LIMS portal"""
    
    BASE_URL = "https://lims.bis.gov.in"
    SEARCH_URL = "https://lims.bis.gov.in/home/search_is_number/"
    
    def __init__(self, delay: int = 3):
        """
        Initialize scraper
        
        Args:
            delay: Delay between requests in seconds (be respectful!)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_standard(self, is_number: int) -> Optional[Dict]:
        """
        Search for a standard by IS number
        
        Args:
            is_number: IS standard number (e.g., 269 for IS 269)
            
        Returns:
            Dictionary with standard info or None if not found
        """
        try:
            url = f"{self.SEARCH_URL}?is_number__doc_no={is_number}"
            logger.info(f"Searching IS {is_number}...")
            
            # Be respectful - add delay
            time.sleep(self.delay)
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                logger.warning(f"IS {is_number}: HTTP {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check if standard exists
            if "No records found" in response.text or "not found" in response.text.lower():
                logger.info(f"IS {is_number}: Not found")
                return None
            
            # Extract standard information
            standard_info = self.extract_standard_info(soup, is_number)
            
            if standard_info:
                logger.info(f"IS {is_number}: Found - {standard_info.get('title', 'N/A')}")
            
            return standard_info
            
        except requests.exceptions.RequestException as e:
            logger.error(f"IS {is_number}: Request failed - {e}")
            return None
        except Exception as e:
            logger.error(f"IS {is_number}: Unexpected error - {e}")
            return None
    
    def extract_standard_info(self, soup: BeautifulSoup, is_number: int) -> Optional[Dict]:
        """
        Extract standard information from page
        
        Args:
            soup: BeautifulSoup object of the page
            is_number: IS standard number
            
        Returns:
            Dictionary with standard details and test parameters
        """
        try:
            records = []
            
            # Extract basic info (customize based on actual HTML structure)
            # This is a template - you'll need to inspect the actual page
            
            # Try to find standard title
            title_elem = soup.find('h2') or soup.find('h3') or soup.find('h4')
            title = title_elem.text.strip() if title_elem else f"IS {is_number}"
            
            # Extract standard number with year
            standard_number = f"IS {is_number}"
            year_match = re.search(r'(\d{4})', title)
            if year_match:
                standard_number = f"IS {is_number}:{year_match.group(1)}"
            
            # Find tables with test parameters
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows[1:]:  # Skip header
                    cols = row.find_all('td')
                    
                    if len(cols) >= 3:
                        # Extract data based on table structure
                        # Adjust indices based on actual table structure
                        
                        record = {
                            'standard_number': standard_number,
                            'title': title,
                            'is_number': is_number,
                            'content': cols[0].text.strip() if len(cols) > 0 else '',
                            'clause': cols[1].text.strip() if len(cols) > 1 else '',
                            'lab_name': cols[2].text.strip() if len(cols) > 2 else '',
                            'testing_charge_inr': cols[3].text.strip() if len(cols) > 3 else '',
                        }
                        
                        records.append(record)
            
            return {
                'standard_number': standard_number,
                'title': title,
                'is_number': is_number,
                'records': records
            }
            
        except Exception as e:
            logger.error(f"Extract error for IS {is_number}: {e}")
            return None
    
    def scrape_range(self, start: int, end: int, output_file: str):
        """
        Scrape a range of IS standards
        
        Args:
            start: Starting IS number
            end: Ending IS number
            output_file: Output CSV file path
        """
        logger.info(f"Starting scrape: IS {start} to IS {end}")
        logger.info(f"Output file: {output_file}")
        logger.info(f"Delay: {self.delay} seconds between requests")
        logger.info("-" * 60)
        
        all_records = []
        found_count = 0
        
        for is_num in range(start, end + 1):
            standard_info = self.search_standard(is_num)
            
            if standard_info and standard_info.get('records'):
                found_count += 1
                
                for record in standard_info['records']:
                    # Add record_id
                    record['record_id'] = f"IS_{is_num}_{len(all_records):05d}"
                    all_records.append(record)
            
            # Progress update
            if is_num % 50 == 0:
                logger.info(f"Progress: {is_num}/{end} - Found: {found_count} standards")
                self.save_records(all_records, output_file)
        
        # Final save
        self.save_records(all_records, output_file)
        
        logger.info("-" * 60)
        logger.info(f"Scraping complete!")
        logger.info(f"Total standards searched: {end - start + 1}")
        logger.info(f"Standards found: {found_count}")
        logger.info(f"Total records: {len(all_records)}")
        logger.info(f"Output file: {output_file}")
    
    def save_records(self, records: List[Dict], output_file: str):
        """
        Save records to CSV file
        
        Args:
            records: List of record dictionaries
            output_file: Output CSV file path
        """
        if not records:
            return
        
        # Define CSV columns (match cement dataset format)
        fieldnames = [
            'record_id',
            'document_id',
            'standard_number',
            'title',
            'revision',
            'section',
            'clause',
            'document_type',
            'industry',
            'source_url',
            'page',
            'language',
            'content',
            'lab_name',
            'osl_code',
            'testing_charge_inr',
            'validity_date',
            'remark'
        ]
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                
                for record in records:
                    # Fill in default values
                    record.setdefault('document_type', 'Indian Standard')
                    record.setdefault('language', 'English')
                    record.setdefault('source_url', self.SEARCH_URL)
                    record.setdefault('document_id', record.get('standard_number', '').replace(':', '_').replace(' ', '_'))
                    
                    writer.writerow(record)
            
            logger.info(f"Saved {len(records)} records to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Scrape BIS LIMS portal for standard data')
    parser.add_argument(
        '--start',
        type=int,
        default=1,
        help='Starting IS number (default: 1)'
    )
    parser.add_argument(
        '--end',
        type=int,
        default=100,
        help='Ending IS number (default: 100)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/scraped/lims_data.csv',
        help='Output CSV file path'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=3,
        help='Delay between requests in seconds (default: 3)'
    )
    
    args = parser.parse_args()
    
    # Create output directory if needed
    import os
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Initialize scraper
    scraper = LIMSScraper(delay=args.delay)
    
    # Start scraping
    try:
        scraper.scrape_range(args.start, args.end, args.output)
    except KeyboardInterrupt:
        logger.info("\nScraping interrupted by user")
        logger.info("Partial results saved")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()


"""
USAGE EXAMPLES:

# Test with small range first
python src/collectors/lims_scraper.py --start 269 --end 270 --output test.csv

# Scrape food standards (typical range: 1-1000)
python src/collectors/lims_scraper.py --start 1 --end 1000 --output data/food_standards.csv --delay 5

# Scrape electrical standards (typical range: 1000-5000)
python src/collectors/lims_scraper.py --start 1000 --end 5000 --output data/electrical_standards.csv --delay 3

# Large range (be patient!)
python src/collectors/lims_scraper.py --start 1 --end 10000 --output data/all_standards.csv --delay 5


NOTES:
1. This is a TEMPLATE - you need to inspect the actual LIMS portal HTML structure
2. Adjust the extract_standard_info() method based on actual page structure
3. Use --delay 3-5 to be respectful to the server
4. Test with small ranges first
5. Script saves progress every 50 standards
6. Check logs/lims_scraper.log for detailed progress

ETHICAL CONSIDERATIONS:
- This scrapes publicly available data only
- Uses reasonable delays to avoid server overload
- Check BIS terms of service before large-scale scraping
- Consider reaching out to BIS for official data access
"""
