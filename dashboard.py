import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mariadb
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# .env-Datei laden
load_dotenv()

# Sicherstellen, dass der Port als Integer existiert
port = os.getenv('DB_PORT')
if port is None:
    port = 3306  # Standard MariaDB Port
else:
    port = int(port)

# SQLAlchemy Engine für MariaDB erstellen
engine = create_engine(f"mariadb+mariadbconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{port}/{os.getenv('DB_NAME')}")

# Laden der Daten
produkte = pd.read_sql("SELECT * FROM Dimension_Produkt", engine)
verkaeufe = pd.read_sql("SELECT * FROM Fakt_Verkauf", engine)
preise = pd.read_sql("SELECT * FROM Dimension_Preisverlauf", engine)
suchtrends = pd.read_sql("SELECT * FROM Dimension_Suchtrend", engine)
anbieter = pd.read_sql("SELECT * FROM Dimension_Anbieter", engine)
news = pd.read_sql("SELECT * FROM Dimension_News", engine)

# Streamlit-Layout mit Logo
st.image("logo.png", width=200)  # Logo hinzufügen, Datei 'logo.png' im selben Verzeichnis erforderlich
st.title("E-Commerce Dashboard")
st.sidebar.header("Filter")

# Produktfilter
produkt_liste = produkte['Name'].unique().tolist()
selected_product = st.sidebar.selectbox("Produkt auswählen", ['Alle'] + produkt_liste)

# Daten filtern, falls ein spezifisches Produkt ausgewählt wurde
if selected_product != 'Alle':
    produkt_id = produkte[produkte['Name'] == selected_product]['ProduktID'].values[0]
    verkaeufe = verkaeufe[verkaeufe['ProduktID'] == produkt_id]
    preise = preise[preise['ProduktID'] == produkt_id]
    suchtrends = suchtrends[suchtrends['ProduktID'] == produkt_id]
    news = news[news['ProductID'] == produkt_id]

# Verkaufsanalyse
st.subheader("Verkäufe über die Zeit")
if not verkaeufe.empty:
    verkaeufe['Verkaufsdatum'] = pd.to_datetime(verkaeufe['Verkaufsdatum'])
    verkauf_zeit = verkaeufe.groupby(verkaeufe['Verkaufsdatum'].dt.to_period("M")).size()
    fig, ax = plt.subplots()
    verkauf_zeit.plot(kind='line', ax=ax)
    ax.set_title("Verkäufe pro Monat")
    ax.set_xlabel("Monat")
    ax.set_ylabel("Anzahl Verkäufe")
    st.pyplot(fig)
else:
    st.write("Keine Verkaufsdaten verfügbar.")

# Preisentwicklung
st.subheader("Preisverlauf")
if not preise.empty:
    preise['Zeitpunkt'] = pd.to_datetime(preise['Zeitpunkt'])
    fig, ax = plt.subplots()
    for q in preise['Quelle'].unique():
        data = preise[preise['Quelle'] == q]
        ax.plot(data['Zeitpunkt'], data['Preis'], label=q)
    ax.set_title("Preisverlauf nach Quelle")
    ax.set_xlabel("Datum")
    ax.set_ylabel("Preis")
    ax.legend()
    st.pyplot(fig)
else:
    st.write("Keine Preisdaten verfügbar.")

# Suchtrend-Analyse
st.subheader("Suchtrends über die Zeit")
if not suchtrends.empty:
    suchtrends['Zeitraum'] = pd.to_datetime(suchtrends['Zeitraum'], errors='coerce')
    fig, ax = plt.subplots()
    ax.plot(suchtrends['Zeitraum'], suchtrends['Suchvolumen'], label="Suchvolumen")
    ax.set_title("Suchvolumen über die Zeit")
    ax.set_xlabel("Zeitraum")
    ax.set_ylabel("Suchvolumen")
    st.pyplot(fig)
else:
    st.write("Keine Suchtrend-Daten verfügbar.")

# Produktnews anzeigen
st.subheader("Aktuelle Produktnews")
if not news.empty:
    for index, row in news.iterrows():
        st.write(f"### {row['Headline']}")
        st.write(f"{row['Content']}")
        st.write(f"[Mehr dazu]({row['URL']})")
        st.write("---")
else:
    st.write("Keine News verfügbar.")

st.sidebar.write("Datenquelle: E-Commerce-Datenbank")
