from pathlib import Path

import streamlit as st
import pandas as pd

st.title("PlatZHirsch at EBUCC 2025")
st.header(f"Total Player Stats")

script_dir = Path(__file__).parent.absolute()
data_path = script_dir / 'players.csv'

df = pd.read_csv(data_path)
df.set_index('Name', inplace=True)
st.dataframe(df, use_container_width=True)
