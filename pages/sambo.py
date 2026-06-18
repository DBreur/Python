import streamlit as st
from datetime import datetime
import functions

# Data opbalen uit de database
df = functions.get_data(table="training")

#! ----------------------------------------------------------
#! Alle functies die niet in het functie bestand gaan
#! ----------------------------------------------------------

# Functie voor het tonen van een dialog


@st.dialog("Nieuwe training")
def add_training_dialog():
    with st.form("training_form"):
        huidige_tijd = datetime.now()

        st.write(
            f"📅 **Tijdstip log:** {huidige_tijd.strftime('%d-%m-%Y %H:%M')}")

        categorie = st.radio("Training", ["🏋️", "🥋"])
        blood_sugar = st.number_input(
            "Bloedsuiker (mmol/L)", min_value=0.0, max_value=30.0, value=5.5, step=0.1)
        notitie = st.text_area("Notitie")

        submitted = st.form_submit_button("Opslaan")

        if submitted:
            functions.insert_training(
                huidige_tijd, categorie, notitie, blood_sugar)
            st.rerun()


# Functie voor het tonen van een delete dialog
@st.dialog("Delete training")
def delete_training_dialog(training_id):
    st.write("## Weet je zeker dat je deze training wilt verwijderen?")

    col_cancel, col_delete = st.columns([1, 1])

    with col_cancel:
        canceled = st.button("Cancel", use_container_width=True)

    with col_delete:
        deleted = st.button("Delete", type="primary", use_container_width=True)

    if canceled:
        st.rerun()

    if deleted:
        functions.delete_training(training_id)
        st.rerun()


# Nieuwe training knop
if st.button("➕ Add new training"):
    add_training_dialog()


st.title("📅 Trainingslogboek")

if not df.empty:
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
                st.markdown(f"🩸 **Bloedsuiker:** {row['blood_sugar']} mmol/L")

            with col2:
                st.caption(
                    f"🕒 {row['date'].strftime('%H:%M')}"
                )

                if st.button("🗑️ Delete", key=f"delete_{row['id']}"):
                    delete_training_dialog(row["id"])

            st.write(row['note'])

else:
    st.info(
        "Nog geen trainingen gevonden in de database. Klik op 'Add new training'."
    )
