"""
# My first app
Here's our first attempt at using data to create a table:
"""

import pandas as pd

import streamlit as st


def wide_space_default():
  st.set_page_config(layout="wide")

wide_space_default()

def clean_numbers(x):
    if isinstance(x, str) and x.isnumeric():
        return round(x, 2)
    return x


games = pd.read_csv("skybowl_games.csv")
players = pd.read_csv("skybowl_players.csv")
players = players.round(2)

def category(row):
    # Checks if the 'Category' column in the row is 'D', applies a green background; otherwise, blue.
    return ['background-color: #90EE90' if row['Category'] == 'D' else 'background-color: #ADD8E6' for _ in row]

# players.style.apply(alternate_row_color, axis=0)
def comprehensive_style(df):
    return (df.style
            .apply(category, axis=1)
            # .bar(subset=['Points played total', 'Touches'], color='lightblue')
            # .set_properties(**{'background-color': '#f4f4f4', 'font-size': '12pt'})
            .set_table_styles([
                {'selector': 'th', 'props': [('text-align', 'center'), ('font-size', '12pt')]},
                {'selector': 'td', 'props': [('text-align', 'center')]}
            ]))

styled_df = comprehensive_style(players)
# styled_df = pd.DataFrame(styled_df).iloc[:,:-10]
styled_df

relevant = players.iloc[:,:-10]
relevant

distances = players.iloc[:,-8:]
distances = pd.concat([players[['Player']], players.iloc[:, -8:]], axis=1)
distances = distances.round(2)
distances





