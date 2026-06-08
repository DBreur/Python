import pandas as pd
import plotly.express as px
import streamlit as st
from pylibrelinkup import PyLibreLinkUp
import requests

url = "https://my.lyfta.app/api/v1/workouts"
headers = {
    "Authorization": "Bearer 0e2d9dfda1ef46ab786492443ec4266292e220a559146840ae5edc91c909a0c0"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    workouts_list = data.get("workouts", [])

    # Direct in Pandas laden!
    df_workouts = pd.DataFrame(workouts_list)
    # st.write(df_workouts.head())

    workout_names = df_workouts["title"] + \
        " - " + df_workouts["workout_perform_date"]
    selected_workout = st.selectbox("Kies een workout", workout_names)
    selected_index = workout_names[workout_names == selected_workout].index[0]
    workout = workouts_list[selected_index]

    eerste_workout = workouts_list[0]
    oefeningen = eerste_workout["exercises"]
    df_oefeningen = pd.DataFrame(oefeningen)
    df_oefeningen_display = df_oefeningen.drop(
        columns=['sets', 'exercise_image', 'is_completed'], errors='ignore')

    st.subheader("Oefeningen")
    st.write(df_oefeningen_display)

    # Selecteer een oefening
    oefeningen_namen = [ex["excercise_name"] for ex in oefeningen]
    selected_oefening_naam = st.selectbox(
        "Kies een oefening voor details:", oefeningen_namen)
    selected_oefening_index = oefeningen_namen.index(selected_oefening_naam)
    selected_oefening = oefeningen[selected_oefening_index]

    st.subheader(selected_oefening["excercise_name"])

    sets = selected_oefening["sets"]
    df_sets = pd.DataFrame(sets)
    df_sets_display = df_sets.drop(
        columns=['id', 'rir', 'duration', 'distance', 'set_type_id',
                 'is_completed', 'record_type', 'record_level', 'record_value']
    )
    df_sets_display.index = df_sets_display.index + 1

    # Rond gewicht af op geen decimalen
    df_sets_display.index.name = "Sets"
    st.write(df_sets_display)
else:
    st.write(f"Foutmelding: {response.status_code}")
