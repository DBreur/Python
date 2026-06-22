import os
import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Connectie-engine
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# LET OP: We gebruiken nu postgresql+psycopg2 in plaats van mysql+pymysql
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Maak de engine aan
engine = create_engine(DATABASE_URL)


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
