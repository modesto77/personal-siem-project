from datetime import datetime

failed_logins = {}
MAX_FAILURES = 5
TIME_WINDOW_SECONDS = 60

def analyze_log(log):
    if log.event == "ssh_login_failed" and log.src_ip:
        ip = log.src_ip
        now = datetime.now()

        if ip not in failed_logins:
            failed_logins[ip] = []

        failed_logins[ip].append(now)
        failed_logins[ip] = [t for t in failed_logins[ip] if (now - t).total_seconds() <= TIME_WINDOW_SECONDS]

        if len(failed_logins[ip]) >= MAX_FAILURES:
            # On prépare les données de l'alerte au lieu de juste renvoyer True
            alert_data = {
                "rule_name": "Brute Force SSH",
                "severity": "CRITICAL",
                "description": f"L'IP {ip} a échoué {len(failed_logins[ip])} fois en moins de {TIME_WINDOW_SECONDS}s.",
                "source_ip": ip
            }
            
            print(f"\n🚨 ALERTE : {alert_data['description']}\n")
            failed_logins[ip] = []
            
            return alert_data # On renvoie le dictionnaire
            
    return None # Aucune alerte