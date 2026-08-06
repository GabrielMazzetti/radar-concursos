from scrapers.diario_oficial import DOUScraper
import requests

print("Testing DOUScraper...")
scraper = DOUScraper()
try:
    results = scraper.fetch_latest()
    print(f"Success! Found {len(results)} items.")
    for r in results[:3]:
        print(f"- {r['orgao']}")
except Exception as e:
    print(f"Error: {e}")
