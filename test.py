import streamlit as st
import pandas as pd
import plotly.express as px
from pylibrelinkup import PyLibreLinkUp

client = PyLibreLinkUp(
    email=st.secrets["LIBRE_EMAIL"],
    password=st.secrets["LIBRE_PASSWORD"]
)

client.authenticate()
patient = client.get_patients()[0]

st.title("Libre 3 Dashboard")

# 1. Grab raw data from API
data = client.graph(patient_identifier=patient)

try:
    # 1. Bouw de dataframe
    df = pd.DataFrame(data)

    # Unpacken als het in één kolom gepropt zit
    if len(df.columns) == 1 and (0 in df.columns or "0" in df.columns):
        col_key = 0 if 0 in df.columns else "0"
        df = pd.DataFrame(df[col_key].tolist())

    # 2. SLIMME DETECTIE VAN KOLOMMEN (Op basis van inhoud)
    timestamp_col = None
    value_col = None

    for col in df.columns:
        # Check of de kolom tekst/datums bevat (zoals '2026-06-04' of '+00:00')
        sample_val = str(df[col].iloc[0]) if not df[col].empty else ""

        if "-" in sample_val and ":" in sample_val:
            timestamp_col = col
        # Als het puur een getal is (of makkelijk converteerbaar naar een getal)
        elif pd.to_numeric(df[col], errors='coerce').notna().any():
            value_col = col

    # Fallback: als de automatische detectie niets vindt, pakken we de oude namen/posities
    if timestamp_col is None or value_col is None:
        st.warning(
            "Automatische kolomdetectie mislukt, we proberen de standaardindeling...")
        timestamp_col = df.columns[0]
        value_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]

    # Hernoem de kolommen naar wat we nodig hebben
    df = df.rename(columns={timestamp_col: "Timestamp", value_col: "Value"})

    # 3. VEILIGE DATA CONVERSIE
    # Forceer Timestamp naar datetime en strip de tijdzone (+00:00) voor Plotly
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    if df["Timestamp"].dt.tz is not None:
        df["Timestamp"] = df["Timestamp"].dt.tz_localize(None)

    # Forceer Value naar een echt getal
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # Verwijder regels die écht leeg zijn
    df = df.dropna(subset=["Timestamp", "Value"])

    # Sorteer chronologisch
    df = df.sort_values("Timestamp")

    # 4. De Grafiek Tekenen
    if not df.empty:
        fig = px.line(
            df,
            x="Timestamp",
            y="Value",
            title="Glucosewaarden over tijd",
            labels={"Value": "Glucose (mg/dL)", "Timestamp": "Tijdstip"}
        )
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig, use_container_width=True)

        # 5. Tabel Weergave
        st.subheader("Glucose Data Overzicht")
        df_display = df.copy()
        df_display["Timestamp"] = df_display["Timestamp"].dt.strftime(
            '%d-%m %H:%M')
        st.dataframe(df_display)
    else:
        st.error(
            "De dataset is nog steeds leeg. Dit is de ruwe structuur die we proberen te lezen:")
        st.write(df.head())

except Exception as e:
    st.error(f"Fout bij het verwerken van de data: {e}")
