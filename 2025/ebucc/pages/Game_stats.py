from pathlib import Path

import pandas as pd
import streamlit as st

st.title("PlatZHirsch at EBUCC 2025")

script_dir = Path(__file__).parent.parent.absolute()
game_files = list(script_dir.glob("data/*.csv"))

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
