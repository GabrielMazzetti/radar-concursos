import requests
from bs4 import BeautifulSoup
from datetime import datetime

class DOUScraper:
    def __init__(self):
        self.url = "https://www.in.gov.br/web/guest/acesso-a-informacao/institucional/concursos-e-selecoes"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_latest(self):
        response = requests.get(self.url, headers=self.headers, timeout=15)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        contests = []
        
        # DOU structure: each entry has a title and a link
        # Based on analysis, they are in specific div structures
        items = soup.select('.journal-content-article')
        
        # Actually, the markdown showed a simpler structure with links
        links = soup.find_all('a', href=True)
        for a in links:
            href = a['href']
            if '/web/dou/-/' in href:
                title = a.get_text().strip()
                if not title:
                    continue
                
                # The parent or surrounding text might have the date
                # For now, let's just take the link and title
                contests.append({
                    'orgao': "DOU - " + title[:50],
                    'link': href if href.startswith('http') else "https://www.in.gov.br" + href,
                    'texto': title,
                    'salario': "",
                    'cidade': "Brasil",
                    'data': datetime.now().strftime('%Y-%m-%d')
                })
        
        return contests
