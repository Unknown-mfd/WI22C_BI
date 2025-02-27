# news.py

import streamlit as st
import pandas as pd

def render_news(nachrichten: pd.DataFrame):
    """
    Gibt die Nachrichten in Textform aus, sortiert nach Datum absteigend.
    """
    if not nachrichten.empty:
        nachrichten['datum'] = pd.to_datetime(nachrichten['datum'], errors='coerce')
        nachrichten = nachrichten.sort_values(by='datum', ascending=False)
        for _, row in nachrichten.iterrows():
            st.write(f"##### {row['titel']}")
            st.write(f"Datum: {row['datum'].date()}")
            st.write(row['inhalt'])
            if row['url']:
                st.write(f"[Mehr dazu]({row['url']})")
            st.write("---")
    else:
        st.write("Keine News verfügbar.")
