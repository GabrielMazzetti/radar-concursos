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
from datetime import datetime
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
os.makedirs("logs", exist_ok=True)

# Custom logger to print and save to file
logger = logging.getLogger("ConcursoRadar")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%H:%M')

file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_step(msg, success=True):
    symbol = "✔" if success else "✖"
    logger.info(f"{symbol} {msg}")
    print(f"{symbol} {msg}")

def main():
    logger.info("--- INÍCIO DA EXECUÇÃO ---")
    
    db = Database()
    matcher = KeywordMatcher()
    notifier = EmailNotifier()
    
    scrapers = [
        (PCIScraper(), "PCI Concursos"),
        (FolhaScraper(), "Folha Dirigida"),
        (DOUScraper(), "DOU")
    ]
    
    all_contests = []
    
    for scraper_obj, name in scrapers:
        logger.info(f"{name} iniciado")
        try:
            found = scraper_obj.fetch_latest()
            log_step(f"{len(found)} concursos encontrados em {name}")
            all_contests.extend(found)
        except Exception as e:
            log_step(f"Erro no scraper {name}: {e}", success=False)

    logger.info("Parser iniciado")
    new_matches_list = []
    for contest in all_contests:
        score = matcher.calculate_score(contest)
        contest['score'] = score
        if score > 0:
            new_matches_list.append(contest)
    
    log_step(f"{len(new_matches_list)} concursos compatíveis encontrados pelo Parser")

    logger.info("Banco de dados atualizado")
    new_inserted = 0
    for contest in new_matches_list:
        if db.insert_concurso(contest):
            new_inserted += 1
    
    log_step(f"{new_inserted} novos concursos salvos no banco")

    unnotified = db.get_unnotified()
    if unnotified:
        logger.info("Email iniciado")
        for row in unnotified:
            contest_dict = dict(row)
            notifier.send_notification(contest_dict)
            db.mark_as_notified(contest_dict['id'])
        log_step(f"{len(unnotified)} e-mails de notificação processados")
    else:
        logger.info("Nenhuma nova notificação pendente")
            
    log_step("Fim da execução")
    logger.info("--- FIM ---")

if __name__ == "__main__":
    main()
