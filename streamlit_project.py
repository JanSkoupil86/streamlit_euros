import json
import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch

st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player/position to see all of their shots taken!")

df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

# Selection filters
team = st.selectbox('Select a team', df['team'].sort_values().unique(), index=None)
player = st.selectbox('Select a player', df[df['team'] == team]['player'].sort_values().unique(), index=None)
play_pattern = st.selectbox('Select a play pattern', df['play_pattern'].sort_values().unique(), index=None)
body_part = st.selectbox('Select a body part', df['shot_body_part'].sort_values().unique(), index=None)
position = st.selectbox('Select a position', df['position'].sort_values().unique(), index=None)
shot_outcome = st.selectbox('Select a shot outcome', df['shot_outcome'].sort_values().unique(), index=None)

def filter_data(df, team, player, play_pattern, body_part, position, shot_outcome):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    if play_pattern:
        df = df[df['play_pattern'] == play_pattern]
    if body_part:
        df = df[df['shot_body_part'] == body_part]
    if position:
        df = df[df['position'] == position]
    if shot_outcome:
        df = df[df['shot_outcome'] == shot_outcome]
    return df

filtered_df = filter_data(df, team, player, play_pattern, body_part, position, shot_outcome)

# Count Outcomes
outcome_counts = filtered_df['shot_outcome'].value_counts()

# Display Outcome Counts
st.subheader("Outcome Counts:")
if not outcome_counts.empty:
    st.write(outcome_counts)
else:
    st.write("No shots match the selected filters.")

# Draw pitch
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
            zorder=2 if x['shot_outcome'] == 'Goal' else 1,
        )

plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)
