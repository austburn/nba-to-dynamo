import requests
import json
import glob
import os

import boto3
import botocore


dynamo = boto3.resource('dynamodb')
nba_table = dynamo.Table('nba')

try:
    nba_table.creation_date_time
except botocore.exceptions.ClientError:
    nba_table = dynamo.create_table(
        TableName='nba',
        KeySchema=[
            {
                'AttributeName': 'player_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'player_id',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    nba_table.meta.client.get_waiter('table_exists').wait(TableName='nba')

    # Make request
    req = requests.get('http://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2015-16&IsOnlyCurrentSeason=1')
    data = json.loads(req.content)

    #["PERSON_ID","DISPLAY_LAST_COMMA_FIRST","ROSTERSTATUS","FROM_YEAR","TO_YEAR","PLAYERCODE","TEAM_ID","TEAM_CITY"  ,"TEAM_NAME","TEAM_ABBREVIATION","TEAM_CODE","GAMES_PLAYED_FLAG"]
    #[203112     ,'Acy, Quincy'             ,1             ,'2012'     ,'2015'   ,'quincy_acy',1610612758,'Sacramento','Kings'    ,'SAC'              ,'kings'    ,'Y']
    player_data = data['resultSets'][0]['rowSet']

    for player in player_data:
        player_name = player[1].split(',')
        item = {
            'player_id': player[0],
            'last_name': player_name[0].strip(),
            'roster_status': bool(player[2]),
            'from_year': player[3],
            'to_year': player[4],
            'player_code': player[5],
            'team_id': player[6],
            'team_city': player[7],
            'team_name': player[8],
            'team_abbreviation': player[9],
            'team_code': player[10],
            'games_played_flag': player[11] == 'Y'
        }
        # Players like 'Nene' don't have a first name listed
        if len(player_name) > 1:
            item['first_name'] = player_name[1].strip()

        # We can't leave these fields empty, so if the player does not have a team, mark as NA
        if item['team_id'] == 0:
            item['team_city'] = 'NA'
            item['team_name'] = 'NA'
            item['team_abbreviation'] = 'NA'
            item['team_code'] = 'NA'

        nba_table.put_item(Item=item)
