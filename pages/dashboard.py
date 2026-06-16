import pandas as pd
import plotly.express as px
import streamlit as st
from pylibrelinkup import PyLibreLinkUp

st.title("Libre 3 Dashboard")

client = PyLibreLinkUp(
    email=st.secrets["LIBRE_EMAIL"],
    password=st.secrets["LIBRE_PASSWORD"],
)

try:
    client.authenticate()
    patients = client.get_patients()

    if not patients:
        st.error("Geen LibreLinkUp patienten gevonden voor dit account.")
        st.stop()

    patient_options = {
        f"{patient.first_name} {patient.last_name}": patient for patient in patients
    }
    selected_patient_name = st.selectbox("Patient", patient_options.keys())
    patient = patient_options[selected_patient_name]

    measurements = client.graph(patient_identifier=patient)
except Exception as exc:
    st.error(f"LibreLinkUp kon niet worden geladen: {exc}")
    st.stop()

if not measurements:
    st.warning("Er zijn nog geen glucosemetingen beschikbaar.")
    st.stop()

df = pd.DataFrame(
    [
        {
            "Tijdstip": measurement.timestamp,
            "Glucose": measurement.value,
            "Glucose mg/dL": measurement.value_in_mg_per_dl,
            "Hoog": measurement.is_high,
            "Laag": measurement.is_low,
        }
        for measurement in measurements
    ]
)

df["Tijdstip"] = pd.to_datetime(df["Tijdstip"], errors="coerce")
df["Glucose"] = pd.to_numeric(df["Glucose"], errors="coerce")
df = df.dropna(subset=["Tijdstip", "Glucose"]).sort_values("Tijdstip")

if df.empty:
    st.error("De LibreLinkUp-data kon niet worden omgezet naar een grafiek.")
    st.stop()

latest = df.iloc[-1]

st.metric(
    label="Laatste glucosewaarde",
    value=f"{latest['Glucose']:.1f}",
    delta=latest["Tijdstip"].strftime("%d-%m %H:%M"),
)

fig = px.line(
    df,
    x="Tijdstip",
    y="Glucose",
    title="Glucosewaarden over tijd",
    labels={"Glucose": "Glucose", "Tijdstip": "Tijdstip"},
)
fig.update_traces(mode="lines+markers")
st.plotly_chart(fig, use_container_width=True)
