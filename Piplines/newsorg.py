import os
import requests
import mysql.connector
from mysql.connector import Error
import datetime
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
API_KEY = os.getenv("NEWSAPI_KEY")

NEWSAPI_URL = "https://newsapi.org/v2/everything"

def get_laptop_models():
    """Holt alle Laptop-Modellnummern aus der MySQL-Datenbank."""
    models = []
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT modell FROM Dim_Produkt")
        models = [row[0] for row in cursor.fetchall()]
    except Error as e:
        print(f"Fehler beim Abrufen der Modellnummern: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return models

def fetch_news(keyword):
    """Holt Nachrichten von NewsAPI für ein bestimmtes Laptop-Modell."""
    params = {
        "q": keyword,
        "apiKey": API_KEY,
        "language": "de",
        "sortBy": "publishedAt",
        "pageSize": 5 
    }
    
    response = requests.get(NEWSAPI_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print(f"Fehler beim Abruf von News für {keyword}: {response.status_code}")
        return []

def save_news_to_db(news_data):
    """Speichert Nachrichten in die MySQL-Datenbank."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO Dim_Nachrichten (produkt_id, datum_id, titel, quelle, url, inhalt)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for news in news_data:
            cursor.execute("SELECT produkt_id FROM Dim_Produkt WHERE modell = %s LIMIT 1", (news['produkt'],))
            result = cursor.fetchone()
            produkt_id = result[0] if result else None

            if not produkt_id:
                print(f"⚠️ Produkt nicht gefunden: {news['produkt']}")
                continue

            news_date = datetime.datetime.strptime(news["datum"], "%Y-%m-%dT%H:%M:%SZ").date()
            cursor.execute("SELECT datum_id FROM Dim_Datum WHERE datum = %s LIMIT 1", (news_date,))
            result = cursor.fetchone()
            if result:
                datum_id = result[0]
            else:
                cursor.execute("INSERT INTO Dim_Datum (datum, jahr, quartal, monat, woche, tag, wochentag) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                               (news_date, news_date.year, (news_date.month-1)//3 + 1, news_date.month, news_date.isocalendar()[1], news_date.day, news_date.strftime("%A")))
                conn.commit()
                datum_id = cursor.lastrowid

            cursor.execute(insert_query, (
                produkt_id, datum_id, news["titel"], news["quelle"], news["url"], news["inhalt"]
            ))
        
        conn.commit()
        print("Alle Nachrichten erfolgreich gespeichert!")

    except Error as e:
        print(f"Fehler beim Speichern in der Datenbank: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def main():
    """Hauptfunktion: Holt Modellnummern, ruft Nachrichten ab und speichert sie."""
    models = get_laptop_models()
    if not models:
        print("Keine Modellnummern gefunden.")
        return
    
    all_news = []
    
    for model in models:
        articles = fetch_news(model)
        for article in articles:
            news_entry = {
                "produkt": model,
                "datum": article["publishedAt"],
                "titel": article["title"],
                "quelle": article["source"]["name"],
                "url": article["url"],
                "inhalt": article["description"][:500] 
            }
            all_news.append(news_entry)
    
    if all_news:
        save_news_to_db(all_news)
    else:
        print("Keine neuen Nachrichten gefunden.")

if __name__ == "__main__":
    main()
