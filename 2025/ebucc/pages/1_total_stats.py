import streamlit as st
import pandas as pd

st.title("PlatZHirsch at EBUCC 2025")
st.header(f"Total Player Stats")
df = pd.read_csv('players.csv')
df.set_index('Name', inplace=True)
st.dataframe(df, use_container_width=True)
