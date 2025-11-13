import csv
import pickle

match_file = open('Group Project Dataset-20231209/Match.csv', 'r+')
match_dataset = csv.DictReader(match_file)

player_attributes_file = open('Group Project Dataset-20231209/PlayerAttributes.csv')
player_attributes_dataset = csv.DictReader(player_attributes_file)
player_attributes = {}

league_file = open('Group Project Dataset-20231209/League.csv')
league_dataset = csv.DictReader(league_file)

for player in player_attributes_dataset:
  player_attributes[player['player_api_id']] = player

player_attributes_file.close()

players_accuracy = {}
for match in match_dataset:
  league_id = match['league_id']
  
  if league_id not in players_accuracy:
    players_accuracy[league_id] = {}

  league_accuracy = players_accuracy[league_id]

  for i in range(0, 11):
    home_player = match[f'home_player_{i+1}'][1:-2]
    away_player = match[f'away_player_{i+1}'][1:-2]

    if home_player != '' and home_player not in league_accuracy and home_player in player_attributes and player_attributes[home_player]['free_kick_accuracy'] != '':
      league_accuracy[home_player] = int(player_attributes[home_player]['free_kick_accuracy'])
    if away_player != '' and away_player not in league_accuracy and away_player in player_attributes and player_attributes[away_player]['free_kick_accuracy'] != '':
      league_accuracy[away_player] = int(player_attributes[away_player]['free_kick_accuracy'])

match_file.close()

best_acc = [(-1, 0, 0)]
for (league_id, league) in players_accuracy.items():
  for (player, accuracy) in league.items():
    if accuracy > best_acc[0][2]:
      best_acc = [(league_id, player, accuracy)]
    elif accuracy == best_acc == best_acc[0][2]:
      best_acc.append((league_id, player, accuracy))

result = {}
for (league, player, accuracy) in best_acc:
  result[league] = result.get(league, 0) + 1

best_league = list(max(result.items(), key = lambda x : x[1]))

for league in league_dataset:
  if league['id'] == best_league[0]:
    best_league[0] = league['name']
print(result)
with open('./query3.pkl', 'w+b') as result_file:
  pickle.dump(best_league, result_file)
