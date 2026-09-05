import requests
import time
import random
from datetime import datetime, timezone

# L'URL de l' API locale
API_URL = "http://127.0.0.1:8000/api/v1/logs"

# Listes de fausses données pour générer des logs réalistes
USERS = ["root", "admin", "modeste", "guest", "ubuntu"]
IPS = ["192.168.1.10", "192.168.1.50", "10.0.0.5", "203.0.113.42", "145.23.4.111"]

def generate_fake_log():
    """Génère un log aléatoire (simulation d'activité SSH)"""
    user = random.choice(USERS)
    ip = random.choice(IPS)
    
    # On simule un fort taux d'échec (80%) pour mimer une attaque Brute-Force
    if random.random() < 0.8:
        event = "ssh_login_failed"
        severity = "WARNING"
        raw_msg = f"Failed password for {user} from {ip} port {random.randint(10000, 65000)} ssh2"
    else:
        event = "ssh_login_success"
        severity = "INFO"
        raw_msg = f"Accepted password for {user} from {ip} port {random.randint(10000, 65000)} ssh2"

    # Construction du dictionnaire au format attendu par notre backend FastAPI
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_host": "server-linux-01",
        "log_type": "auth",
        "severity": severity,
        "event": event,
        "src_ip": ip,
        "user": user,
        "raw_message": raw_msg
    }

def run_agent():
    print("🚀 Démarrage de l'agent collecteur (Mode Simulation)...")
    print(f"📡 Envoi des logs vers {API_URL}")
    print("-" * 50)
    
    while True:
        log_data = generate_fake_log()
        
        try:
            # Envoi du log en POST au format JSON
            response = requests.post(API_URL, json=log_data)
            
            if response.status_code == 200:
                print(f"[+] Envoyé | {log_data['severity']} - {log_data['event']} (IP: {log_data['src_ip']})")
            else:
                print(f"[-] Erreur {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("[-] Impossible de joindre l'API. Le backend (FastAPI) est-il allumé ?")
            
        # Pause aléatoire entre 1 et 3 secondes pour ne pas surcharger instantanément
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    run_agent()
