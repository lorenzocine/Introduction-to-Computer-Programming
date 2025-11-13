import csv
import pickle

match_file = open(r'Python\ University\ GroupProject\ Match.csv', 'r')
match_dataset = csv.DictReader(match_file)

league_file = open(r'Python\ University\ GroupProject\ League.csv', 'r')
league_dataset = csv.DictReader(league_file)
leagueGoals = {}

for match in match_dataset:
  league_id = match['league_id']
  # convert to int as every element from csv is reported as a string
  goals_scored = int(match['home_team_goal']) + int(match['away_team_goal'])

  if league_id not in leagueGoals: #Checking if league is present in leagueGoals Dictionary
    leagueGoals[league_id] = [0, 0] # [goals scored, games played]

  leagueGoals[league_id][0] += goals_scored #Adding the amount of goals scored per match
  leagueGoals[league_id][1] += 1 # adding the amount of games played

match_file.close()


result = {}

for l in leagueGoals:
  result[l] = leagueGoals[l][0] / leagueGoals[l][1] # Dictionary consisting of league ---> id : average amount of goals per game

max_scoring_league = max(result.items(), key = lambda x : x[1])  # Getting the tuple who has the maximum goals scored per game

for league in league_dataset:
  if league['id'] == max_scoring_league[0]: # Checking which league is the league with most goals score per game
    top_league = league['name']
    break

league_file.close()

result_file = open('Python\\University\\GroupProject\\query1.pkl', 'w+b')
pickle.dump([top_league, max_scoring_league[1]], result_file)
result_file.close()
