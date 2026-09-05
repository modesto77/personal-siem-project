import time
import requests
import re
from datetime import datetime, timezone

API_URL = "http://127.0.0.1:8000/api/v1/logs"
LOG_FILE = "app_securite.log" # Le fichier réel que nous allons surveiller sur le PC

# Regex pour comprendre un format de log spécifique. 
# Exemple attendu : [2026-08-31 10:22:00] WARNING ssh_login_failed IP:192.168.1.50 USER:modeste
LOG_PATTERN = re.compile(r'\[(.*?)\]\s+(\w+)\s+(\w+)\s+IP:([\d\.]+)\s+USER:(\w+)')

def follow_file(filepath):
    """Surveille les ajouts dans un fichier en temps réel (façon 'tail -f')"""
    try:
        with open(filepath, 'r') as file:
            # Se place à la toute fin du fichier pour ne lire que les NOUVEAUX logs
            file.seek(0, 2)
            print(f" Surveillance active du fichier : {filepath}...")
            
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.5) # Pour Faire une pause s'il n'y a pas de nouvelle ligne
                    continue
                
                process_and_send(line.strip())
    except FileNotFoundError:
        print(f"[-] Fichier introuvable. Crée un fichier '{filepath}' dans ce dossier.")

def process_and_send(line):
    """Analyse la ligne avec la Regex et l'envoie au SIEM"""
    match = LOG_PATTERN.match(line)
    
    if match:
        date_str, severity, event, ip, user = match.groups()
        
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_host": "mon-pc-windows",
            "log_type": "auth",
            "severity": severity,
            "event": event,
            "src_ip": ip,
            "user": user,
            "raw_message": line
        }
        
        try:
            requests.post(API_URL, json=log_data)
            print(f"[+] Nouveau log ingéré : {user} depuis {ip}")
        except Exception:
            print("[-] API injoignable.")
    else:
        print(f"[?] Log ignoré (format non reconnu) : {line}")

if __name__ == "__main__":
    follow_file(LOG_FILE)
