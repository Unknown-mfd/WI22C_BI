# charts.py

import pandas as pd
import plotly.express as px

def plot_sales_chart(verkaeufe: pd.DataFrame, chart_type: str):
    """
    Erstellt ein Plotly-Diagramm (Linie oder Balken) über die Zeit.
    Gruppiert die Verkäufe nach Monat und zählt die Anzahl.
    Gibt None zurück, falls verkaeufe leer ist.
    """
    if verkaeufe.empty:
        return None
    
    verkaeufe['datum'] = pd.to_datetime(verkaeufe['datum'], errors='coerce')
    df_sales = (
        verkaeufe
        .groupby(verkaeufe['datum'].dt.to_period("M"))
        .size()
        .reset_index(name='anzahl_verkaeufe')
    )
    # Period -> Timestamp (1. Tag des Monats)
    df_sales['Monat'] = df_sales['datum'].dt.to_timestamp()
    df_sales = df_sales.sort_values('Monat')
    
    if chart_type == "Liniendiagramm":
        fig = px.line(
            df_sales, x='Monat', y='anzahl_verkaeufe',
            title='Verkäufe pro Monat', markers=True
        )
    else:  # Balkendiagramm
        fig = px.bar(
            df_sales, x='Monat', y='anzahl_verkaeufe',
            title='Verkäufe pro Monat'
        )

    fig.update_layout(xaxis_title="Monat", yaxis_title="Anzahl Verkäufe")
    return fig


def plot_price_chart(preise: pd.DataFrame):
    """
    Erstellt ein Plotly-Liniendiagramm für den Preisverlauf (ggf. mit Farbe nach 'quelle').
    Hebt den höchsten Preis per Annotation hervor.
    Gibt None zurück, falls preise leer ist.
    """
    if preise.empty:
        return None
    
    preise['datum'] = pd.to_datetime(preise['datum'], errors='coerce')
    preise = preise.sort_values('datum')

    if 'quelle' in preise.columns:
        fig = px.line(
            preise, x='datum', y='preis', color='quelle',
            title='Preisverlauf', markers=True
        )
    else:
        fig = px.line(
            preise, x='datum', y='preis',
            title='Preisverlauf', markers=True
        )

    if not preise.empty:
        max_price = preise['preis'].max()
        max_row = preise.loc[preise['preis'].idxmax()]
        fig.add_annotation(
            x=max_row['datum'],
            y=max_price,
            text="Höchster Preis",
            showarrow=True,
            arrowhead=1,
            ax=20,
            ay=-30,
            bgcolor="red",
            font=dict(color="white")
        )

    fig.update_layout(xaxis_title="Datum", yaxis_title="Preis")
    return fig


def plot_trends_chart_by_product(suchtrends: pd.DataFrame, produkte: pd.DataFrame):
    if suchtrends.empty:
        return None
    
    if 'produkt_id' not in suchtrends.columns or 'trend_score' not in suchtrends.columns:
        return None

    # Merge mit Produkten, um den Produktnamen zu bekommen
    merged = suchtrends.merge(produkte[['produkt_id', 'name']], on='produkt_id', how='left')
    
    # Gruppieren nach Produktname und durchschnittlichen trend_score bilden
    df_trends = (
        merged.groupby('name')['trend_score']
        .mean()
        .reset_index()
        .sort_values('trend_score', ascending=False)
    )
    
    # Balkendiagramm (horizontal)
    import plotly.express as px
    fig = px.bar(
        df_trends,
        x='trend_score',
        y='name',
        orientation='h',
        title='Durchschnittlicher Trendscore pro Produkt'
    )
    
    # Hier erzwingen wir den x-Bereich von 0 bis 100
    fig.update_layout(
        xaxis=dict(range=[0, 100]),
        xaxis_title="Trendscore",
        yaxis_title="Produkt"
    )
    return fig

