import csv
import pickle

team_file = open('Group Project Dataset-20231209/Team.csv', 'r+')
team_dataset = csv.DictReader(team_file)

team_attribute_file = open('Group Project Dataset-20231209/TeamAttributes.csv', 'r+')
team_attribute_dataset = csv.DictReader(team_attribute_file)

match_file = open('Group Project Dataset-20231209/Match.csv', 'r+')
match_dataset = csv.DictReader(match_file)

league_file = open('Group Project Dataset-20231209/League.csv', 'r+')
league_dataset = csv.DictReader(league_file)


team_attributes = {attrib['team_api_id']: attrib for attrib in team_attribute_dataset}
team_attribute_file.close()

# assuming the attributes are ordered from oldest to newest, the dictionary will always have the latest attributes

leagues = {
  # league_id: number_of_fast_blps_teams
}

for match in match_dataset:
  home_id = match['home_team_api_id']
  away_id = match['away_team_api_id']
  league_id = match['league_id']

  if league_id not in leagues:
    leagues[league_id] = []
  
  if home_id in team_attributes and home_id not in leagues[league_id] and team_attributes[home_id]['buildUpPlaySpeedClass'] == 'Fast':
    leagues[league_id].append(home_id)
  if away_id in team_attributes and away_id not in leagues[league_id] and team_attributes[away_id]['buildUpPlaySpeedClass'] == 'Fast':
    leagues[league_id].append(away_id)

match_file.close()

result = list(max(leagues.items(), key = lambda x : len(x[1])))

for league in league_dataset:
  if league['id'] == result[0]:
    result[0] = league['name']

league_file.close()

# Create a dictionary mapping team_api_id to team_long_name
team_names = {team['team_api_id']: team['team_long_name'] for team in team_dataset}


result[1] = [team_names.get(team_id, team_id) for team_id in result[1]]

result = {result[0]: result[1]}
print(result)
with open('./query2.pkl', 'w+b') as result_file:
    pickle.dump(result, result_file)

#this is to see which teams have build up play speed class
#  this line of code is updating the second element of the result list (result[1]) by replacing each team id with its corresponding long name from the team names dictionary. if its not found it keeps the original team id