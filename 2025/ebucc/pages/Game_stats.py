import pandas as pd
import streamlit as st
from pathlib import Path

st.title("PlatZHirsch at EBUCC 2025")

game_files = list(Path.cwd().glob("data/*.csv"))

game_names = [Path(f).stem.capitalize() for f in game_files]

tabs = st.tabs(game_names)

for tab, game_file in zip(tabs, game_files):
    df = pd.read_csv(game_file)
    df.set_index("Name", inplace=True)
    with tab:
        game_name = game_file.stem.capitalize()
        st.header(f"{game_name} Player Stats")
        st.subheader("Player Statistics")
        st.dataframe(df, use_container_width=True)
