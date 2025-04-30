import streamlit as st
import json
from dataclasses import dataclass
from collections import defaultdict

METRICS = [
    "Total Scoring Efficiency",
    "Offensive Scoring Efficiency",
    "Defensive Scoring Efficiency",
    "Defensive Turnovers Efficiency",
    "Point Recovery",
    "Pass Completion"
]

STAT_CATEGORIES = ["Per Point", "Per Possession", "First Possession"]

def read_stats(filename: str):
    with open(filename) as f:
        return json.load(f)

data = read_stats('games.json')

def aggregate_stats(selected_games):
    """
    Aggregates statistics from a list of game data objects.
    Sums the numerators and denominators for each metric's ratio,
    then recalculates the percentage.
    """
    if not selected_games:
        return None

    aggregated_sums = defaultdict(lambda: defaultdict())
    for category in STAT_CATEGORIES:
        for metric in METRICS:
            aggregated_sums[category][metric] = {"numerator": 0, "denominator": 0}

    for game_data in selected_games:
        for category in STAT_CATEGORIES:
            for metric in METRICS:
                metric_stats = game_data["stats"][category].get(metric)
                ratio_str = metric_stats["ratio"]
                numerator, denominator = map(int, ratio_str.split('/'))
                aggregated_sums[category][metric]["numerator"] += numerator
                aggregated_sums[category][metric]["denominator"] += denominator


    opponent = ""
    names = [game.get("opponent", "Unknown") for game in selected_games]
    opponent = f"{', '.join(names)}"

    # Prepare the final aggregated data structure with calculated percentages and new ratios
    final_aggregated_data = {
        "opponent": opponent,
        "stats": {}
    }
    for category in STAT_CATEGORIES:
        final_aggregated_data["stats"][category] = defaultdict(lambda: defaultdict)
        for metric in METRICS:
            num_sum = aggregated_sums[category][metric]["numerator"]
            den_sum = aggregated_sums[category][metric]["denominator"]

            if den_sum > 0:
                percentage_val = round((num_sum / den_sum) * 100)
                percentage = f"{percentage_val}%"
                ratio = f"{num_sum}/{den_sum}"
            else:
                percentage = "0%" if num_sum == 0 else "N/A"
                ratio = f"{num_sum}/0"
            
            final_aggregated_data["stats"][category][metric] = {
                "percentage": percentage,
                "ratio": ratio
            }
            
    return final_aggregated_data

st.set_page_config(layout="wide", page_title="Game Statistics Viewer")

st.title("📊 Game Statistics Viewer")
st.markdown("Select one or more games from the list below to view individual or aggregated statistics.")
st.markdown("---")

opponents = [game["opponent"] for game in data["games"]]
default_selection = opponents[0] if opponents else []

selected_opponents = st.multiselect(
    "Select one or more options:", opponents, key="select_opponents"
)

def _select_all():
    st.session_state.select_opponents = opponents

def _clear_all():
    st.session_state.select_opponents = []

select_all, clear_all, _ = st.columns([1, 1, 18])
select_all.button("Select all", on_click=_select_all)
clear_all.button("Clear all", on_click=_clear_all)

if selected_opponents:
    games_to_process_data = [game for game in data["games"] if game["opponent"] in selected_opponents]

    # Aggregate the stats for the selected games
    display_data = aggregate_stats(games_to_process_data)
    st.header(f"Statistics for: {display_data['opponent']}")
    tabs = st.tabs(STAT_CATEGORIES)

    for i, category_name in enumerate(STAT_CATEGORIES):
        with tabs[i]:
            st.subheader(f"{category_name} Stats")
            category_stats_data = display_data["stats"][category_name]
            cols = st.columns(3)
            
            for metric_idx, metric_key in enumerate(METRICS):
                if metric_key in category_stats_data:
                    stat_value = category_stats_data[metric_key]
                    percentage = stat_value["percentage"]
                    ratio = stat_value["ratio"]
                    
                    # Determine which column to place the metric in
                    current_col = cols[metric_idx % 3]
                    
                    with current_col:
                        with st.container(border=True):
                            st.markdown(f"**{metric_key}**")
                            st.markdown(f"<h2 style='text-align: center; color: #2a9d8f;'>{percentage}</h2>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align: center;'>{ratio}</p>", unsafe_allow_html=True)
else:
    st.info("Please select at least one game from the list to view statistics.")


st.subheader("Glossary")

st.markdown("""
* **Total Scoring Efficiency:** Percentage of points/possessions/first possessions scored.
* **Offensive Scoring Efficiency:** Percentage of points/possessions/first possessions that we scored when the team started on offense.
* **Defensive Scoring Efficiency:** Percentage of points/possessions/first possessions that we scored when the team started on defense.
* **Defensive Turnover Efficiency:** Percentage of defense points where the opposition turned the disc over.
* **Pass Completion:** Percentage of passes that reached their target and were caught.

For instance, the offensive scoring efficiency for first possessions corresponds to 'clean holds'.
""")

st.sidebar.info(
    "This page shows game specific statistics. "
    "You can select individual or multiple games to see their respective individual or aggregated stats (probably mostly relevant is all). "
    "The ratios (e.g., 5/10) are summed up, and percentages are recalculated based on the summed totals."
)
