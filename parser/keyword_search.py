import re
import sys
import os

# Add parent dir to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class KeywordMatcher:
    def __init__(self):
        self.keywords = config.KEYWORDS
        self.scores = config.SCORES
        self.priorities = config.PRIORITIES

    def calculate_score(self, contest_data):
        score = 0
        text = contest_data.get('texto', '').lower()
        orgao = contest_data.get('orgao', '').upper()
        cidade = contest_data.get('cidade', '').lower()
        salario_text = contest_data.get('salario', '')

        # 1. Main Keywords (Estatística)
        found_main = False
        for kw in self.keywords.get('estatistica', []):
            if kw.lower() in text:
                score += self.scores.get('keyword_match', 50)
                found_main = True
                break
        
        if not found_main:
            return 0 # If it doesn't mention statistics, it's probably not relevant for the MVP

        # 2. Bonus Keywords (Python, R, etc.)
        for kw in self.keywords.get('bonus', []):
            if kw.lower() in text:
                score += self.scores.get('bonus_match', 10)

        # 3. Salary Score
        # Extract numeric value from salary string like "R$ 10.685,44"
        try:
            salary_num = re.sub(r'[^\d,]', '', salario_text).replace(',', '.')
            if salary_num and float(salary_num) > 10000:
                score += self.scores.get('salary_high', 20)
        except:
            pass

        # 4. City Priority
        for city in self.priorities.get('cities', []):
            if city.lower() in cidade or city.lower() in text:
                score += self.scores.get('city_priority', 5)
                break

        # 5. Org Priority
        for org in self.priorities.get('orgs', []):
            if org.upper() in orgao:
                score += self.scores.get('org_priority', 20)
                break

        return score
