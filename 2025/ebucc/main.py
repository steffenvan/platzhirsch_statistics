import pandas as pd
import streamlit as st


st.title("PlatZHirsch at EBUCC 2025")

players = pd.read_csv('players.csv')
st.dataframe(players)