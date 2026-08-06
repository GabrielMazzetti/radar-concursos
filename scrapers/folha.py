import requests
from bs4 import BeautifulSoup
from datetime import datetime

class FolhaScraper:
    def __init__(self):
        self.url = "https://folha.qconcursos.com/e/concursos-abertos"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_latest(self):
        response = requests.get(self.url, headers=self.headers, timeout=15)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        contests = []
        
        # Folha Dirigida structure: news articles
        # Based on analysis, articles are usually in 'article' or specific classes
        # Let's look for links that start with /n/
        items = soup.find_all('a', href=True)
        
        for item in items:
            href = item['href']
            if href.startswith('/n/'):
                link = "https://folha.qconcursos.com" + href
                title = item.get_text().strip()
                
                if not title or len(title) < 10:
                    continue
                
                # For the MVP, we take the title as the 'orgao' or summary
                contests.append({
                    'orgao': title,
                    'link': link,
                    'texto': title,
                    'salario': "",
                    'cidade': "",
                    'data': datetime.now().strftime('%Y-%m-%d')
                })
                
        # Deduplicate by link
        unique_contests = {c['link']: c for c in contests}.values()
        return list(unique_contests)
