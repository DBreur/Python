import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

st.title("Dashboard")

USER = "root"
PASSWORD = ""
HOST = "localhost"
PORT = 3306
DB_NAME = "full_dia_app"

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

query = "SELECT * FROM glucose_metingen ORDER BY meetmoment"

df = pd.read_sql(query, con=engine)
df["meetmoment"] = pd.to_datetime(df["meetmoment"])
df["meetdatum"] = df["meetmoment"].dt.date
df["meettijd"] = df["meetmoment"].dt.strftime("%H:%M")

gekozen_dag = st.selectbox(
    "Kies een dag",
    sorted(df["meetdatum"].unique(), reverse=True)
)

dag_df = df[df["meetdatum"] == gekozen_dag].sort_values("meetmoment")

fig = px.line(
    df,
    x="meetmoment",
    y="glucose_waarde",
    color="meetdatum",
    markers=True,
    title="Glucosemetingen per dag",
    labels={
        "meetmoment": "Datum en tijd",
        "glucose_waarde": "Glucose (mmol/L)",
        "meetdatum": "Datum",
    },
    hover_data=["moment", "eenheid"],
)

fig.update_traces(
    marker=dict(size=8),
    line=dict(width=3)
)

fig.update_layout(
    xaxis_title="Datum en tijd",
    yaxis_title="Glucose (mmol/L)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader(f"Metingen op {gekozen_dag}")
st.dataframe(
    dag_df[["meettijd", "glucose_waarde", "eenheid", "moment"]],
    use_container_width=True
)
