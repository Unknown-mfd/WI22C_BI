# app.py

import os
import streamlit as st
import pandas as pd

# Eigene Module importieren
from data_loader import get_engine, load_data
from charts import (
    plot_sales_chart,
    plot_price_chart,
    plot_trends_chart_by_product
)
from news import render_news  # optional

st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.image("../logo.png", use_container_width=True)
st.sidebar.header("Filter")

# -------------------------------------------------
# 1) Daten laden
# -------------------------------------------------
engine = get_engine()
produkte, verkaeufe, preise, suchtrends, nachrichten = load_data(engine)

# -------------------------------------------------
# 2) Sidebar-Filter
# -------------------------------------------------

# Kategorie-Filter
if 'kategorie' in produkte.columns:
    kategorien = produkte['kategorie'].dropna().unique().tolist()
    selected_kategorie = st.sidebar.selectbox("Kategorie auswählen", ["Alle"] + kategorien)
    if selected_kategorie != "Alle":
        cat_prod_ids = produkte.loc[produkte['kategorie'] == selected_kategorie, 'produkt_id'].unique()
        verkaeufe = verkaeufe[verkaeufe['produkt_id'].isin(cat_prod_ids)]
        preise = preise[preise['produkt_id'].isin(cat_prod_ids)]
        suchtrends = suchtrends[suchtrends['produkt_id'].isin(cat_prod_ids)]
        nachrichten = nachrichten[nachrichten['produkt_id'].isin(cat_prod_ids)]

# Produkt-Filter
produkt_liste = produkte['name'].unique().tolist()
selected_product = st.sidebar.selectbox("Produkt auswählen", ['Alle'] + produkt_liste)

# Datumsfilter (Verkäufe / Preise)
if not verkaeufe.empty:
    min_date = pd.to_datetime(verkaeufe['datum']).min()
    max_date = pd.to_datetime(verkaeufe['datum']).max()
else:
    min_date = pd.to_datetime("2020-01-01")
    max_date = pd.to_datetime("2030-01-01")

start_date, end_date = st.sidebar.date_input("Zeitraum auswählen", [min_date, max_date])

# Diagrammtyp für Verkäufe
chart_type = st.sidebar.radio(
    "Diagramm-Typ für Verkäufe",
    ("Liniendiagramm", "Balkendiagramm"),
    index=0
)

# Quelle-Filter (für Preis)
if 'quelle' in preise.columns and not preise.empty:
    quellen_liste = preise['quelle'].dropna().unique().tolist()
    selected_quellen = st.sidebar.multiselect("Quelle(n) auswählen", quellen_liste, default=quellen_liste)
else:
    selected_quellen = None

# Region-Filter (für Trends)
if 'region' in suchtrends.columns and not suchtrends.empty:
    regionen_liste = suchtrends['region'].dropna().unique().tolist()
    # "Weltweit" aus der Liste entfernen
    regionen_liste = [r for r in regionen_liste if r != 'Weltweit']
    
    selected_regionen = st.sidebar.multiselect(
        "Region(en) auswählen",
        regionen_liste,
        default=regionen_liste
    )
else:
    selected_regionen = None


# Trend-Score-Filter
if 'trend_score' in suchtrends.columns and not suchtrends.empty:
    min_score = float(suchtrends['trend_score'].min())
    max_score = float(suchtrends['trend_score'].max())
    trend_range = st.sidebar.slider("Trend-Score eingrenzen", min_value=min_score, max_value=max_score, value=(min_score, max_score))
else:
    trend_range = None

# -------------------------------------------------
# 3) Filter anwenden
# -------------------------------------------------
# Produktfilter
if selected_product != 'Alle':
    produkt_id = produkte.loc[produkte['name'] == selected_product, 'produkt_id'].values[0]
    verkaeufe = verkaeufe[verkaeufe['produkt_id'] == produkt_id]
    preise = preise[preise['produkt_id'] == produkt_id]
    suchtrends = suchtrends[suchtrends['produkt_id'] == produkt_id]
    nachrichten = nachrichten[nachrichten['produkt_id'] == produkt_id]

# Datumsfilter
if start_date and end_date:
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    verkaeufe = verkaeufe[
        (pd.to_datetime(verkaeufe['datum']) >= start_dt) &
        (pd.to_datetime(verkaeufe['datum']) <= end_dt)
    ]
    preise = preise[
        (pd.to_datetime(preise['datum']) >= start_dt) &
        (pd.to_datetime(preise['datum']) <= end_dt)
    ]

# Quelle
if selected_quellen is not None:
    preise = preise[preise['quelle'].isin(selected_quellen)]

# Region
if selected_regionen is not None:
    suchtrends = suchtrends[suchtrends['region'].isin(selected_regionen)]

# Trend-Score
if trend_range is not None:
    suchtrends = suchtrends[
        (suchtrends['trend_score'] >= trend_range[0]) &
        (suchtrends['trend_score'] <= trend_range[1])
    ]

# -------------------------------------------------
# 4) Key-Metriken berechnen
# -------------------------------------------------
if not verkaeufe.empty:
    total_sales = verkaeufe.shape[0]
else:
    total_sales = 0

if not preise.empty:
    average_price = preise['preis'].mean()
    min_price = preise['preis'].min()
    max_price = preise['preis'].max()
    price_range = max_price - min_price
else:
    average_price = 0
    min_price = 0
    price_range = 0

if not suchtrends.empty and 'region' in suchtrends.columns:
    region_trends = suchtrends.groupby('region')['trend_score'].mean().sort_values(ascending=False)
    top_region = region_trends.index[0]
    top_region_score = region_trends.iloc[0]
else:
    top_region = "Keine Daten"
    top_region_score = 0

# -------------------------------------------------
# 5) Layout (Container & Spalten)
# -------------------------------------------------
with st.container():
    st.subheader("Key Metrics")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Gesamtverkäufe", value=int(total_sales))
    col_m2.metric("Durchschnittspreis", value=round(average_price, 2))
    col_m3.metric("Top-Region", f"{top_region} ({top_region_score:.2f})" if top_region_score else "Keine Daten")

    col_m4, col_m5, col_m6 = st.columns(3)
    col_m4.metric("Niedrigster Preis", round(min_price, 2))
    col_m5.metric("Preisspanne", round(price_range, 2))
    col_m6.metric("Höchster Preis", round(max_price, 2))

st.markdown("---")

with st.container():
    st.subheader("Verkaufs- und Preisanalysen")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Verkäufe über die Zeit")
        fig_sales = plot_sales_chart(verkaeufe, chart_type)
        if fig_sales:
            st.plotly_chart(fig_sales, use_container_width=True)
        else:
            st.write("Keine Verkaufsdaten verfügbar.")

    with col2:
        st.markdown("#### Preisverlauf")
        fig_price = plot_price_chart(preise)
        if fig_price:
            st.plotly_chart(fig_price, use_container_width=True)
        else:
            st.write("Keine Preisdaten verfügbar.")

st.markdown("---")

with st.container():
    st.subheader("Suchtrends und Nachrichten")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Suchtrends")
        fig_trend = plot_trends_chart_by_product(suchtrends, produkte)
        if fig_trend:
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.write("Keine Suchtrend-Daten verfügbar oder Spalten fehlen.")

    with col4:
        st.markdown("#### Aktuelle Nachrichten")
        render_news(nachrichten)

st.sidebar.markdown("---")
st.sidebar.write("Datenquelle: " + os.getenv('DB_HOST'))
