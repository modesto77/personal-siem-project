from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import engine, Base, get_db
import models
from engine.analyzer import analyze_log
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware # <-- Important
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIEM Personnel API", version="1.0.0")

# --- CONFIGURATION  ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------------

# Mettre à jour la base de données (crée la table 'alerts')
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIEM Personnel API", version="1.0.0")

@app.post("/api/v1/logs")
def receive_log(log: models.LogCreate, db: Session = Depends(get_db)):
    # 1. Sauvegarde du log
    db_log = models.LogEvent(
        timestamp=log.timestamp, source_host=log.source_host, log_type=log.log_type,
        severity=log.severity, event=log.event, src_ip=log.src_ip,
        user=log.user, raw_message=log.raw_message
    )
    db.add(db_log)
    db.commit()
    
    # 2. Analyse et sauvegarde de l'alerte 
    alert_data = analyze_log(log)
    
    if alert_data:
        db_alert = models.AlertEvent(
            timestamp=datetime.now(),
            rule_name=alert_data["rule_name"],
            severity=alert_data["severity"],
            description=alert_data["description"],
            source_ip=alert_data["source_ip"]
        )
        db.add(db_alert)
        db.commit()
        print("💾 Alerte enregistrée en base de données !")
        
    return {"status": "success"}

# --- NOUVELLE ROUTE POUR REACT ---
@app.get("/api/v1/alerts")
def get_alerts(db: Session = Depends(get_db)):
    # Récupérer les 50 dernières alertes de la base de données
    alerts = db.query(models.AlertEvent).order_by(models.AlertEvent.timestamp.desc()).limit(50).all()
    return alerts
