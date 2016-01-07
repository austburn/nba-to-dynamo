import requests
import json
import glob
import os
from subprocess import call

# Make request
req = requests.get('http://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2015-16&IsOnlyCurrentSeason=1')
data = json.loads(req.content)

#["PERSON_ID","DISPLAY_LAST_COMMA_FIRST","ROSTERSTATUS","FROM_YEAR","TO_YEAR","PLAYERCODE","TEAM_ID","TEAM_CITY"  ,"TEAM_NAME","TEAM_ABBREVIATION","TEAM_CODE","GAMES_PLAYED_FLAG"]
#[203112     ,'Acy, Quincy'             ,1             ,'2012'     ,'2015'   ,'quincy_acy',1610612758,'Sacramento','Kings'    ,'SAC'              ,'kings'    ,'Y']
player_data = data['resultSets'][0]['rowSet']

number_of_players = len(player_data)
# Dynamo only let's you make 25 requests at a time
aws_batch_upload_limit = 25
r = range(0, number_of_players, aws_batch_upload_limit)

# For each set of requests, structure the NBA data so that it can be indexed into Dynamo
for limit in r:
    # This 'nba' key is the name of your table
    dynamo_data = {'nba' : []}
    for player in player_data[limit:limit+aws_batch_upload_limit]:
        player_name = player[1].split(',')
        item = {
            'player_id': {'N': str(player[0])},
            'last_name': {'S': player_name[0].strip()},
            'roster_status': {'BOOL': bool(player[2])},
            'from_year': {'N': player[3]},
            'to_year': {'N': player[4]},
            'player_code': {'S': player[5]},
            'team_id': {'N': str(player[6])},
            'team_city': {'S': player[7]},
            'team_name': {'S': player[8]},
            'team_abbreviation': {'S': player[9]},
            'team_code': {'S': player[10]},
            'games_played_flag': {'BOOL': player[11] == 'Y'}
        }
        # Players like 'Nene' don't have a first name listed
        if len(player_name) > 1:
            item['first_name'] = {'S': player_name[1].strip()}

        # We can't leave these fields empty, so if the player does not have a team, mark as NA
        if item['team_id']['N'] == '0':
            item['team_city']['S'] = 'NA'
            item['team_name']['S'] = 'NA'
            item['team_abbreviation']['S'] = 'NA'
            item['team_code']['S'] = 'NA'

        dynamo_data['nba'].append({
            'PutRequest': {
               'Item': item
            }
        })

    dynamo_file = open('to_dynamo_{start}_{finish}.json'.format(start=limit, finish=limit+aws_batch_upload_limit), 'w')
    json.dump(dynamo_data, dynamo_file)
    dynamo_file.close()

# Get all the JSON files we dumped to
dynamo_files = glob.glob('to_dynamo_[0-9]*_[0-9]*.json')
for df in dynamo_files:
    # Upload the JSON
    call(['aws', 'dynamodb', 'batch-write-item', '--request-items', 'file://{filename}'.format(filename=df)])
    # Remove the file
    os.remove(df)
