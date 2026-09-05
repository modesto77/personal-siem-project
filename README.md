# 🛡️ SIEM Personnel - SOC Dashboard

Un projet éducatif de **Security Information and Event Management (SIEM)**, développé pour comprendre de l'intérieur le fonctionnement des solutions de supervision de sécurité (SOC).

Ce projet capture des événements de sécurité simulés ou réels, les analyse en temps réel pour détecter des comportements malveillants (comme les attaques par force brute), et remonte les alertes sur un tableau de bord moderne.

## 🚀 Fonctionnalités

* **Agent de Collecte (Python) :** Lit les fichiers de logs en temps réel (façon `tail -f`), parse les données avec des Regex et les transmet via HTTP.
* **Backend API (FastAPI) :** Reçoit, valide (Pydantic) et stocke les événements dans une base de données SQLite via SQLAlchemy.
* **Moteur de Corrélation :** Analyse les flux à la volée. Intègre une règle de détection temporelle (ex: 5 échecs d'authentification SSH en moins de 60 secondes = Alerte Brute Force).
* **Dashboard (React/Vite) :** Interface utilisateur sobre (Dark Mode) affichant les alertes critiques en temps réel.

## 🛠️ Stack Technique

* **Backend :** Python 3, FastAPI, Uvicorn, SQLAlchemy, SQLite
* **Frontend :** React, Vite, Axios, CSS pur
* **Collecteur :** Python (Requests, Regex)

## 📂 Structure du Projet

```text
my-personal-siem/
├── collector/          # Agent de collecte de logs en Python
├── backend/            # API FastAPI et Moteur de règles (Analyzer)
└── frontend/           # Interface utilisateur React (Vite)
```

## ⚙️ Installation et Lancement

### 1. Cloner le dépôt
```bash
git clone https://github.com/VOTRE_NOM/personal-siem-project.git
cd personal-siem-project
```

### 2. Lancer le Backend (API)
```bash
cd backend
python -m venv venv
# Activation sur Windows (PowerShell) :
venv\Scripts\activate
# Activation sur Linux/Mac :
# source venv/bin/activate

pip install fastapi uvicorn pydantic sqlalchemy
uvicorn main:app --reload
```
*L'API sera accessible sur `http://127.0.0.1:8000`*

### 3. Lancer le Frontend (Dashboard)
Ouvrez un nouveau terminal :
```bash
cd frontend
npm install
npm run dev
```
*Le tableau de bord sera accessible sur `http://localhost:5173`*

### 4. Lancer le Collecteur de Logs
Ouvrez un troisième terminal :
```bash
cd collector
python real_agent.py
```

## 🎯 Comment tester la détection de menaces ?

Une fois les trois services lancés, ouvrez le fichier `collector/app_securite.log` (créez-le s'il n'existe pas) et ajoutez rapidement 5 lignes consécutives pour simuler une attaque SSH (Brute Force) :

```text
[2026-08-31 10:45:00] WARNING ssh_login_failed IP:10.0.0.99 USER:hacker
[2026-08-31 10:45:01] WARNING ssh_login_failed IP:10.0.0.99 USER:hacker
[2026-08-31 10:45:02] WARNING ssh_login_failed IP:10.0.0.99 USER:hacker
[2026-08-31 10:45:03] WARNING ssh_login_failed IP:10.0.0.99 USER:hacker
[2026-08-31 10:45:04] WARNING ssh_login_failed IP:10.0.0.99 USER:hacker
```
Dès l'enregistrement du fichier, le collecteur enverra les logs au backend. Le moteur d'analyse va corréler ces 5 échecs en moins de 60 secondes et générer une alerte critique qui s'affichera instantanément sur votre tableau de bord React !

## 👨‍💻 Auteur
**Modeste Amessi** - Projet d'exploration et de démonstration technique en cybersécurité.
