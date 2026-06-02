

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt
import math

USER = "root"
PASSWORD = ""
HOST = "localhost"
PORT = 3306
DB_NAME = "sambo"

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

query = "SELECT * FROM log"

df = pd.read_sql(query, con=engine)

df.sort_values(by="datum", ascending=True)

df.style.hide(axis="index")

st.line_chart(df)

color = st.color_picker("Pick A Color", "#00f900")
st.write("The current color is", color)

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
