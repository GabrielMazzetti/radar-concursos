import time
from scrapers.pci import PCIScraper
from scrapers.folha import FolhaScraper
from scrapers.diario_oficial import DOUScraper
from parser.keyword_search import KeywordMatcher
from database import Database
from notifier.email_notifier import EmailNotifier
import logging
import os

# Setup Logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("🚀 Iniciando Concurso Radar...")
    logging.info("Iniciando execução do Concurso Radar")
    
    db = Database()
    matcher = KeywordMatcher()
    notifier = EmailNotifier()
    
    scrapers = [
        PCIScraper(),
        FolhaScraper(),
        DOUScraper()
    ]
    
    all_contests = []
    
    for scraper in scrapers:
        name = scraper.__class__.__name__
        print(f"🔍 Buscando em {name}...")
        try:
            found = scraper.fetch_latest()
            print(f"✅ Encontrados {len(found)} itens em {name}")
            all_contests.extend(found)
        except Exception as e:
            print(f"❌ Erro em {name}: {e}")
            logging.error(f"Erro no scraper {name}: {e}")

    new_matches = 0
    for contest in all_contests:
        # Calculate score
        score = matcher.calculate_score(contest)
        contest['score'] = score
        
        if score > 0:
            # Try to insert into DB (link is unique)
            is_new = db.insert_concurso(contest)
            if is_new:
                new_matches += 1
                print(f"✨ Novo match! {contest['orgao']} - Score: {score}")
                logging.info(f"Novo match: {contest['orgao']} - Link: {contest['link']}")

    # Notify about new matches
    unnotified = db.get_unnotified()
    if unnotified:
        print(f"📧 Enviando {len(unnotified)} notificações...")
        for row in unnotified:
            contest_dict = dict(row)
            success = notifier.send_notification(contest_dict)
            # Even if email fails (due to credentials), we mark as notified in this MVP 
            # to avoid spamming the logs, but the user can check the logs.
            db.mark_as_notified(contest_dict['id'])
            
    print(f"🏁 Fim da execução. {new_matches} novos concursos encontrados.")
    logging.info(f"Execução finalizada. Novos matches: {new_matches}")

if __name__ == "__main__":
    main()
