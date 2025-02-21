# E-Commerce Dashboard

## Beschreibung

Dieses Streamlit-Dashboard visualisiert Verkaufs-, Preis- und Suchtrend-Daten aus einer MariaDB-Datenbank. Zusätzlich können Produktnews abgerufen werden.

## Installation

1. **Abhängigkeiten installieren:**

   ```bash
   pip install -r requirements.txt
   ```

2. **.env-Datei erstellen** (im gleichen Verzeichnis wie das Skript) und mit den richtigen Datenbank-Zugangsdaten befüllen:

   ```
   DB_HOST=dein_host
   DB_USER=dein_benutzername
   DB_PASSWORD=dein_passwort
   DB_NAME=dein_datenbankname
   DB_PORT=3306
   ```

## Nutzung

Das Dashboard kann mit folgendem Befehl gestartet werden:

```bash
streamlit run dashboard.py
```

## Features

- Produktfilterung
- Verkaufsanalyse über die Zeit
- Preisverläufe von Produkten
- Suchtrends von Produkten
- Anzeige aktueller Produktnews

