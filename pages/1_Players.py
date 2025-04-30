import pandas as pd
import streamlit as st

st.title("PlatZHirsch at Skybowl 2025")

df_players = pd.read_csv('2025/skybowl/players.csv')
df_games = pd.read_csv('2025/skybowl/games.csv')

def win_loss_color(df):
  def color(row):
      return ['background-color: green' if x == "Win" else 'background-color: red' for x in row] 
  
  return df.style.apply(color, subset=["Result"], axis=1)

df_players.rename(columns={"Assists": "A1", "Secondary assists": "A2"}, inplace=True)
df_players['+/-'] = df_players['A1'] + df_players['A2'] / 2 + df_players['Goals'] - df_players['Turnovers']
df_players.set_index('Player', inplace=True)
player_cols = ['Touches', 'Goals', 'A1', 'A2', 'Defensive blocks', 'Thrower errors', 'Receiver errors', 'Turnovers', '+/-', 'Offense points played', 'Defense points played', 'Points played total']
df_players = df_players[player_cols]

df_games.set_index("Opponent", inplace=True)
game_cols = ['Date', 'Time', 'Our score',
       'Opponent\'s score', 'Result', 'Won points started on offense (holds)',
       'Won points started on defense (breaks)', 'Possessions total',
       'Offense possessions', 'Defense possessions', 'Passes', 'Turnovers', 'Defensive blocks',
       'Opposition errors', 'Stall outs for', 'Stall outs against']

df_games = df_games[game_cols]
df_games = win_loss_color(df_games)


st.dataframe(df_players)
st.dataframe(df_games)