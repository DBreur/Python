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

# 1. Fetch raw data
data = client.graph(patient_identifier=patient)

# --- DEBUGGING SECTION ---
# This will show us exactly what the API structure looks like so we can target it
st.subheader("Raw Data Structure Debug")
st.write("Type of data:", type(data))
if isinstance(data, list) and len(data) > 0:
    st.write("Sample item from list:", data[0])
elif isinstance(data, dict):
    st.write("Keys in dict:", list(data.keys()))
# -------------------------

# 2. Convert to DataFrame cleanly
# If data is a dictionary containing a list under a key like 'connection' or 'data',
# we need to pass that specific key to pd.DataFrame().
# For now, let's try reading it directly but forcing column parsing.
try:
    df = pd.DataFrame(data)

    # If pandas created a transposed dataframe (where keys are rows instead of columns),
    # we flip it. If your debug section shows column 0 contains things like 'Timestamp', flip it:
    if df.shape[1] == 1 or (df.index.dtype == 'int64' and df.columns.tolist() == [0]):
        # Let's see if forcing standard list-of-dicts parsing helps:
        df = pd.DataFrame.from_records(data)

    # Let's inspect the actual columns available right now
    st.write("Actual Columns found:", df.columns.tolist())

    # 3. Clean up and Convert types safely
    # If the API returns 'timestamp' (lowercase) or similar, adjust here:
    target_col = None
    for col in df.columns:
        if str(col).lower() in ['timestamp', 'date', 'time']:
            target_col = col
            break

    if target_col:
        df[target_col] = pd.to_datetime(df[target_col], errors='coerce')
        # Rename it to standard Title Case for consistency
        df = df.rename(columns={target_col: "Timestamp"})

    if 'value' in df.columns:
        df = df.rename(columns={'value': 'Value'})

    # Show the cleaned dataframe
    st.subheader("Cleaned Dataframe")
    st.dataframe(df)

    # 4. Render the chart safely
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
            "Could not find 'Timestamp' and 'Value' columns to plot. Check the debug data above.")

except Exception as e:
    st.error(f"Error building DataFrame: {e}")
