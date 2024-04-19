import pandas as pd

import streamlit as st


def wide_space_default():
  st.set_page_config(layout="wide")

wide_space_default()

pd.set_option('display.max_rows', 100)
games = pd.read_csv("skybowl_games.csv")
games.set_index("Opponent", inplace=True)
players = pd.read_csv("skybowl_players.csv")
players = players.round(2)
players.set_index("Player", inplace=True)

def win_loss_color(df):
  def color(row):
      return ['background-color: green' if x == "Win" else 'background-color: red' for x in row] 
  
  return df.style.apply(color, subset=["Result"], axis=1)

def position_color(df):
    def color(row):
        return ['background-color: #90EE90' if x == 'D' else 'background-color: #ADD8E6' for x in row]
    
    return df.style.apply(color, subset=["Category"], axis=1)

cols = ['Category', 'Points played total','Touches', 'A1', 'A2', 'Goals','Defensive blocks', 'Thrower errors', 'Receiver errors', 'Turnovers', 'Offense points played', 'Defense points played', 'Offense points won', 'Defense points won', 'Points played with touches', 'Throws', 'Catches', 'Possessions initiated']
player_stats_columns = players.columns[:-10].tolist()
player_stats = players[cols].copy()

player_stats = position_color(player_stats)

# Add category to the distances columns
distance_columns = players.columns[-8:].tolist()
distances = players[distance_columns].copy()
distances.insert(0, 'Category', players['Category'])  # Insert 'Category' at the first position

player_distances = position_color(distances)


st.header("Team highlights")
st.markdown(
"""
- **Total scoring efficiency:** 43%
- **Offensive scoring efficiency:** 40%
- **Defensive scoring efficiency:** 49%
- **Defensive turnover efficiency:** 61%
- **Point recovery:** 30%
- **Pass completion:** 92%
""")

st.header("Individual highlights")
st.markdown(
    """
    - **Top scorer:** Max (12 goals) 
    - **Top assists:** Osci (11 assists)
    - **Most blocks:** Valentin (8 blocks)
    - **No turnovers:** Chrigu (0 turnovers) :)) 
    - Mo with second most goals and second most assists despite only playing 1 day. 
    """
)

st.header("Player stats")
st.dataframe(player_stats)

st.header("Distances")
st.dataframe(player_distances)

styled_games = win_loss_color(games)
st.header("Games")
st.dataframe(games)
