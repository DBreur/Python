import os
import streamlit as st
from datetime import datetime  # datetime toegevoegd voor de tijd
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Database configuratie ophalen
load_dotenv()

# Database gegevens
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")

# SQL connectie
conn_string = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(conn_string)

# Data ophalen uit de database
query = "SELECT * FROM training"
df = pd.read_sql(query, con=engine)


@st.dialog("Nieuwe training")
def add_training_dialog():
    with st.form("training_form"):
        # We gebruiken nu datetime.now() om automatisch de huidige datum EN tijd te pakken
        huidige_tijd = datetime.now()

        st.write(
            f"📅 **Tijdstip log:** {huidige_tijd.strftime('%d-%m-%Y %H:%M')}")

        categorie = st.radio("Training", ["🏋️", "🥋"])

        # NIEUW: Bloedsuiker input (bijv. tussen 0.0 en 30.0 mmol/L)
        blood_sugar = st.number_input(
            "Bloedsuiker (mmol/L)", min_value=0.0, max_value=30.0, value=5.5, step=0.1)

        notitie = st.text_area("Notitie")

        submitted = st.form_submit_button("Opslaan")

        if submitted:
            # 1. De database-push (Inclusief blood_sugar!)
            insert_query = text("""
                INSERT INTO training (date, categorie, note, blood_sugar) 
                VALUES (:date, :categorie, :note, :blood_sugar)
            """)

            with engine.begin() as conn:
                conn.execute(insert_query, {
                    "date": huidige_tijd,  # Dit stuurt nu datum + tijd naar de DATETIME kolom
                    "categorie": categorie,
                    "note": notitie,
                    "blood_sugar": blood_sugar  # Push naar de nieuwe kolom
                })

            # 2. De app herstarten
            st.rerun()


# Nieuwe training knop
if st.button("➕ Add new training"):
    add_training_dialog()


st.title("📅 Trainingslogboek")

if not df.empty:

    # Zorg dat Pandas de DATETIME kolom goed begrijpt
    df['date'] = pd.to_datetime(df['date'])

    # Voor het filter-menu (selectbox) willen we nog wel filteren op DATUM (zonder tijd)
    df['just_date'] = df['date'].dt.date
    beschikbare_datums = sorted(df['just_date'].unique(), reverse=True)

    geselecteerde_datum = st.selectbox(
        "Selecteer datum",
        beschikbare_datums,
        format_func=lambda x: x.strftime("%d-%m-%Y")
    )

    st.divider()

    # Filter de DataFrame op de geselecteerde datum
    trainingen_van_datum = df[df['just_date'] == geselecteerde_datum]

    st.subheader(
        f"Trainingen op {geselecteerde_datum.strftime('%d-%m-%Y')}"
    )

    # Sorteer binnen die dag ook even van nieuw naar oud op basis van de exacte TIJD
    trainingen_van_datum = trainingen_van_datum.sort_values(
        by='date', ascending=False)

    # Loop door de rijen
    for index, row in trainingen_van_datum.iterrows():
        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(
                    f"### {row['categorie']}"
                )
                # Toon de bloedsuikerwaarde bij de training
                st.markdown(f"🩸 **Bloedsuiker:** {row['blood_sugar']} mmol/L")

            with col2:
                # Hier tonen we nu de exacte TIJD (%H:%M) in plaats van alleen de datum
                st.caption(
                    f"🕒 {row['date'].strftime('%H:%M')}"
                )

            st.write(row['note'])

else:
    st.info(
        "Nog geen trainingen gevonden in de database. Klik op 'Add new training'."
    )
