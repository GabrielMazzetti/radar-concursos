import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

class PCIScraper:
    def __init__(self):
        self.url = "https://www.pciconcursos.com.br/ultimas/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_latest(self):
        response = requests.get(self.url, headers=self.headers, timeout=15)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        contests = []
        
        # The structure is usually inside divs with class 'ca' or similar
        # Based on my analysis, they are inside #conteudo .ca
        items = soup.select('#conteudo .ca')
        
        for item in items:
            try:
                link_tag = item.find('a')
                if not link_tag:
                    continue
                
                link = link_tag['href']
                orgao = link_tag.text.strip()
                
                # Extracting details from the text inside the div
                text_content = item.get_text(separator='|').split('|')
                # Filter out empty or whitespace strings
                text_content = [t.strip() for t in text_content if t.strip()]
                
                # PCI structure: Orgao | State | Info (vagas, salario) | Cargo | Level | Date
                # This varies, so we'll store the whole text for later parsing
                full_text = " ".join(text_content)
                
                # Basic extraction
                salario = ""
                salario_match = re.search(r'R\$\s?[\d\.,]+', full_text)
                if salario_match:
                    salario = salario_match.group(0)
                
                cidade = ""
                # Often the state is in a span or specific part
                state_tag = item.find('span', title=True)
                if state_tag:
                    cidade = state_tag.text.strip()

                contests.append({
                    'orgao': orgao,
                    'link': link,
                    'texto': full_text,
                    'salario': salario,
                    'cidade': cidade,
                    'data': datetime.now().strftime('%Y-%m-%d')
                })
            except Exception as e:
                print(f"Error parsing PCI item: {e}")
                continue
                
        return contests
