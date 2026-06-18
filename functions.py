import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

# Connectie-engine
db_user = st.secrets["mysql"]["username"]
db_password = st.secrets["mysql"]["password"]
db_host = st.secrets["mysql"]["host"]
db_port = st.secrets["mysql"]["port"]
db_name = st.secrets["mysql"]["database"]

conn_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(conn_string)


# Data ophalen uit de database
def get_data(selector="*", table="", conditions=None, orderby=None):

    # SQL Query
    query = f"SELECT {selector} FROM `{table}`"

    # Parameters
    params = {}

    # Condities toevoegen
    if conditions:
        query += " WHERE "
        where_parts = []
        for column, value in conditions.items():
            where_parts.append(f"`{column}` = :{column}")
            params[column] = value
        query += " AND ".join(where_parts)

    if orderby:
        query += f" ORDER BY {orderby}"

    executable_query = text(query)

    df = pd.read_sql(executable_query, con=engine, params=params)

    if not df.empty and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['just_date'] = df['date'].dt.date

    return df


# Training toevoegen en opslaan in de database
def insert_training(training_date, categorie, note, blood_sugar):
    query = text("""
        INSERT INTO training (date, categorie, note, blood_sugar) 
        VALUES (:date, :categorie, :note, :blood_sugar)
    """)

    # Query uitvoeren met de engine
    with engine.begin() as conn:
        conn.execute(query, {
            "date": training_date,
            "categorie": categorie,
            "note": note,
            "blood_sugar": blood_sugar
        })


def delete_training(training_id):
    query = text("DELETE FROM training WHERE id = :id")

    with engine.begin() as conn:
        conn.execute(query, {"id": training_id})
