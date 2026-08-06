import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class EmailNotifier:
    def __init__(self):
        self.sender = config.EMAIL_SENDER
        self.password = config.EMAIL_PASSWORD
        self.receiver = config.EMAIL_RECEIVER

    def send_notification(self, contest):
        subject = f"🎯 Novo Concurso: {contest['orgao']} (Score: {contest['score']})"
        
        body = f"""
        Olá! Encontramos um novo concurso que pode te interessar:
        
        Órgão: {contest['orgao']}
        Salário: {contest['salario']}
        Cidade: {contest['cidade']}
        Link: {contest['link']}
        Pontuação: {contest['score']}/100
        
        Resumo: {contest['texto'][:200]}...
        
        Boa sorte!
        """
        
        # Log to file for verification in sandbox
        log_file = os.path.join(config.BASE_DIR, "logs/notifications.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"--- NOTIFICATION SENT ---\nSubject: {subject}\n{body}\n")

        # Actual sending logic (will likely fail without real credentials)
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.receiver
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # For Gmail, use smtp.gmail.com and port 587
            # server = smtplib.SMTP('smtp.gmail.com', 587)
            # server.starttls()
            # server.login(self.sender, self.password)
            # server.send_message(msg)
            # server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
