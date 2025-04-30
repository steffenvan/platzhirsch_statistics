import pandas as pd
import streamlit as st

st.title("PlatZHirsch at Skybowl 2025")

df_players = pd.read_csv('2025/skybowl/players.csv')
df_players.rename(columns={"Assists": "A1", "Secondary assists": "A2"}, inplace=True)
df_players['+/-'] = df_players['A1'] + df_players['A2'] / 2 + df_players['Goals'] - df_players['Turnovers']
df_players = df_players.set_index('Player')
df_players = df_players[['Touches', 'Goals', 'A1', 'A2', 'Defensive blocks', 'Thrower errors', 'Receiver errors', 'Turnovers', '+/-', 'Offense points played', 'Defense points played', 'Points played total']]
df_games = pd.read_csv('2025/skybowl/games.csv')

st.dataframe(df_players)
st.dataframe(df_games)
