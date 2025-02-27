# data_loader.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# Einmal .env laden (falls nicht schon in app.py)
load_dotenv()

def get_engine():
    """Erstellt und gibt eine SQLAlchemy-Engine für MariaDB zurück."""
    port = os.getenv('DB_PORT')
    if port is None:
        port = 3306
    else:
        port = int(port)

    engine = create_engine(
        f"mariadb+mariadbconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{port}/{os.getenv('DB_NAME')}"
    )
    return engine


def load_data(engine):
    """
    Lädt alle benötigten Tabellen/DataFrames aus der DB.
    Gibt sie in der Reihenfolge (produkte, verkaeufe, preise, suchtrends, nachrichten) zurück.
    """
    produkte = pd.read_sql("SELECT * FROM Dim_Produkt", engine)

    verkaeufe = pd.read_sql("""
        SELECT fv.*, dd.datum
        FROM Fakt_Verkauf fv
        JOIN Dim_Datum dd ON fv.datum_id = dd.datum_id
    """, engine)

    preise = pd.read_sql("""
        SELECT dp.*, dd.datum
        FROM Dim_Preisentwicklung dp
        JOIN Dim_Datum dd ON dp.datum_id = dd.datum_id
    """, engine)

    suchtrends = pd.read_sql("SELECT * FROM Dim_Trend", engine)

    nachrichten = pd.read_sql("""
        SELECT dn.*, dd.datum
        FROM Dim_Nachrichten dn
        JOIN Dim_Datum dd ON dn.datum_id = dd.datum_id
    """, engine)

    return produkte, verkaeufe, preise, suchtrends, nachrichten
