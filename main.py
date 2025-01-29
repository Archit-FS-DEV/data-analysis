import pandas as pd

# Load the data from the CSV file
df = pd.read_csv("/Users/archit/Downloads/data.csv")

# -----------------------------------------
# Data Cleaning
# -----------------------------------------
# Uncomment to inspect the dataset
# print(df.info())  # Check data types and null values
# print(df.isnull().sum())  # Count null values in each column

# Handle missing values
df['city'] = df['city'].fillna('No location')
df['winner'] = df['winner'].fillna('NO RESULT')
df['player_of_match'] = df['player_of_match'].fillna('Not disclosed')

# Drop unnecessary columns
df = df.drop(columns=['umpire3'], errors='ignore')

# Uncomment to verify changes
# print(df.isnull().sum())

# -----------------------------------------
# Analysis and Insights
# -----------------------------------------

# 1. City with the most wins
city_wins = df[df['winner'] != 'NO RESULT'].groupby('city')['winner'].count()
max_wins_city = city_wins.idxmax()
max_wins_count = city_wins.max()
print(f"City with the most wins: {max_wins_city} ({max_wins_count} wins)")

# 2. Stadium with the most wins
stadium_wins = df[df['winner'] != 'NO RESULT'].groupby('venue')['winner'].count()
max_wins_venue = stadium_wins.idxmax()
max_wins_count = stadium_wins.max()
print(f"Stadium with the most wins: {max_wins_venue} ({max_wins_count} wins)")

# 3. Player with the most Player of the Match awards
player_awards = df.groupby('player_of_match').size()
top_player = player_awards.idxmax()
top_player_count = player_awards.max()
print(f"{top_player} won the most Player of the Match awards ({top_player_count} awards)")

# 4. Team with the highest victory margin (runs)
max_runs_index = df['win_by_runs'].idxmax()
if not pd.isna(max_runs_index):
    max_run_details = df.loc[max_runs_index]
    print(f"Highest victory by runs: {max_run_details['winner']} "
          f"({max_run_details['win_by_runs']} runs) at {max_run_details['venue']}")

# 5. Team with the highest average margin of victory
df['margin_of_victory'] = df['win_by_runs']
avg_margin = df.groupby('winner')['margin_of_victory'].mean()
team_with_highest_margin = avg_margin.idxmax()
print(f"Team with the highest average victory margin: {team_with_highest_margin}")

# 6. Team that won by the most wickets
max_wickets_index = df['win_by_wickets'].idxmax()
if not pd.isna(max_wickets_index):
    max_wicket_details = df.loc[max_wickets_index]
    print(f"Highest victory by wickets: {max_wicket_details['winner']} "
          f"({max_wicket_details['win_by_wickets']} wickets)")

# -----------------------------------------
# Toss Decisions and Probabilities
# -----------------------------------------

# List of teams
teams = df['winner'].unique()

# Analyze toss decisions and their outcomes for each team
for team in teams:
    team_toss = df[df['toss_winner'] == team]

    # Calculate probabilities for batting and fielding decisions
    bat_total = team_toss[team_toss['toss_decision'] == 'bat'].shape[0]
    bat_wins = team_toss[(team_toss['toss_decision'] == 'bat') & (team_toss['winner'] == team)].shape[0]
    P_bat = bat_wins / bat_total if bat_total > 0 else 0

    field_total = team_toss[team_toss['toss_decision'] == 'field'].shape[0]
    field_wins = team_toss[(team_toss['toss_decision'] == 'field') & (team_toss['winner'] == team)].shape[0]
    P_field = field_wins / field_total if field_total > 0 else 0

    # Decide based on higher win probability
    recommended_decision = "bat" if P_bat > P_field else "field"

    # Print results for the team
    print(f"{team} Toss Decisions Analysis:")
    print(f"  Matches chosen to bat: {bat_total}, Wins: {bat_wins} (Win Probability: {P_bat:.2f})")
    print(f"  Matches chosen to field: {field_total}, Wins: {field_wins} (Win Probability: {P_field:.2f})")
    print(f"  Recommended decision: {recommended_decision}")
    print("-" * 50)

# -----------------------------------------
# Additional Analysis
# -----------------------------------------
# Example: Number of matches affected by Duckworth-Lewis (DL) method
dl_matches = df['dl_applied'].sum()
print(f"Total matches affected by Duckworth-Lewis method: {dl_matches}")
