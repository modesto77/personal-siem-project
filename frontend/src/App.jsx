import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [alerts, setAlerts] = useState([])

  // Fonction pour récupérer les alertes depuis FastAPI
  const fetchAlerts = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/alerts')
      setAlerts(response.data)
    } catch (error) {
      console.error("Erreur de connexion à l'API SIEM", error)
    }
  }

  useEffect(() => {
    fetchAlerts() // Premier appel
    // On rafraîchit les données toutes les 5 secondes (Temps réel simulé)
    const interval = setInterval(fetchAlerts, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="dashboard">
      <header>
        <h1>🛡️ SIEM Personnel - SOC Dashboard</h1><br />
        <p>Surveillance des menaces en temps réel</p>
      </header>

      <main>
        <section className="alerts-section">
          <h2>Dernières Alertes ({alerts.length})</h2>
          {alerts.length === 0 ? (
            <p>Aucune alerte pour le moment. Le système est sécurisé. ✅</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Date et Heure</th>
                  <th>Règle déclenchée</th>
                  <th>Niveau</th>
                  <th>IP Source</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((alert) => (
                  <tr key={alert.id} className={alert.severity.toLowerCase()}>
                    <td>{new Date(alert.timestamp).toLocaleString()}</td>
                    <td>{alert.rule_name}</td>
                    <td><strong>{alert.severity}</strong></td>
                    <td><code>{alert.source_ip}</code></td>
                    <td>{alert.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </div>
  )
}

export default App