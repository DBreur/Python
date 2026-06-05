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
    # 2. Build initial dataframe
    df = pd.DataFrame(data)

    # 3. IF PANDAS STUCK EVERYTHING IN COLUMN 0 (Fixing the core issue):
    # This unpacks a list of dicts/tuples trapped inside a single column
    if 0 in df.columns or "0" in df.columns:
        col_key = 0 if 0 in df.columns else "0"
        # Extract the inner dictionaries safely
        inner_data = df[col_key].tolist()
        df = pd.DataFrame.from_records(inner_data)

    # 4. Handle Case Sensitivity and Column Mapping
    # Standardize names regardless of how the API returned them
    df.columns = [str(c).lower() for c in df.columns]

    if "timestamp" in df.columns:
        df = df.rename(columns={"timestamp": "Timestamp"})
    if "value" in df.columns:
        df = df.rename(columns={"value": "Value"})

    # --- EMERGENCY FALLBACK ---
    # If the API used completely different names, let's auto-map them by position
    if "Timestamp" not in df.columns and df.shape[1] >= 2:
        # Assuming typical setup: Col 0 is Time, Col 1 is Value
        df.columns = ["Timestamp", "Value"] + list(df.columns[2:])
    # ---------------------------

    # 5. Clean & Convert Timestamps safely
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    # 6. Render the Plotly chart
    if "Timestamp" in df.columns and "Value" in df.columns:
        fig = px.line(
            df,
            x="Timestamp",
            y="Value",
            title="Glucosewaarden"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(
            f"Could not map columns. Available columns are: {df.columns.tolist()}")

    # 7. Safe Display for the Dataframe (No raw object columns allowed!)
    st.subheader("Glucose Data Summary")

    df_display = df.copy()
    if "Timestamp" in df_display.columns:
        df_display["Timestamp"] = df_display["Timestamp"].dt.strftime(
            '%Y-%m-%d %H:%M:%S')

    # Drop any remaining columns that are pure unparsed 'object' types to ensure Arrow stays happy
    df_display = df_display.select_dtypes(exclude=['object'])

    st.dataframe(df_display)

except Exception as e:
    st.error(f"Error structuring dashboard layout: {e}")
