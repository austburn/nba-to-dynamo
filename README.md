# NBA Stats to DynamoDB

I created this script to index all NBA players into an AWS DynamoDB table named "nba".

I did so because while the NBA's stats API is great, there is no easy way to search for a player via the API. You need access to a player's player_id in order to access interesting stats pertaining to that player.

## Requirements
* python
* pip
    * boto3
    * botocore (dep of boto3)
    * requests

## Usage

Creates a table called 'nba' and indexes the data:

```python nba_to_dynamo.py```

Scanning the database:

```bash
$ python fetch_player_id.py
usage: fetch_player_id.py [-h] [--last-name LAST_NAME]
                          [--first-name FIRST_NAME] [--team TEAM]

One of the following is required.

optional arguments:
  -h, --help            show this help message and exit
  --last-name LAST_NAME
                        Search by last name
  --first-name FIRST_NAME
                        Search by first name
  --team TEAM           Search by team abbreviation

```

```bash
$ python fetch_player_id.py --last-name Curry
[{u'first_name': u'Seth', u'last_name': u'Curry', u'games_played_flag': True, u'team_abbreviation': u'SAC', u'team_id': Decimal('1610612758'), u'to_year': u'2015', u'from_year': u'2013', u'roster_status': True, u'player_id': Decimal('203552'), u'team_name': u'Kings', u'team_code': u'kings', u'player_code': u'seth_curry', u'team_city': u'Sacramento'}, {u'first_name': u'Stephen', u'last_name': u'Curry', u'games_played_flag': True, u'team_abbreviation': u'GSW', u'team_id': Decimal('1610612744'), u'to_year': u'2015', u'from_year': u'2009', u'roster_status': True, u'player_id': Decimal('201939'), u'team_name': u'Warriors', u'team_code': u'warriors', u'player_code': u'stephen_curry', u'team_city': u'Golden State'}]

$ python fetch_player_id.py --first-name Ish
[{u'first_name': u'Ish', u'last_name': u'Smith', u'games_played_flag': True, u'team_abbreviation': u'PHI', u'team_id': Decimal('1610612755'), u'to_year': u'2015', u'from_year': u'2010', u'roster_status': True, u'player_id': Decimal('202397'), u'team_name': u'76ers', u'team_code': u'sixers', u'player_code': u'ish_smith', u'team_city': u'Philadelphia'}]

$ python fetch_player_id.py --team CLE
[{u'first_name': u'LeBron', u'last_name': u'James', u'games_played_flag': True, u'team_abbreviation': u'CLE', u'team_id': Decimal('1610612739'), u'to_year': u'2015', u'from_year': u'2003', u'roster_status': True, u'player_id': Decimal('2544'), u'team_name': u'Cavaliers', u'team_code': u'cavaliers', u'player_code': u'lebron_james', u'team_city': u'Cleveland'}, {u'first_name': u'Anderson', u'last_name': u'Varejao', u'games_played_flag': True, u'team_abbreviation': u'CLE', u'team_id': Decimal('1610612739'), u'to_year': u'2015', u'from_year': u'2004', u'roster_status': True, u'player_id': Decimal('2760'), u'team_name': u'Cavaliers', u'team_code': u'cavaliers', u'player_code': u'anderson_varejao', u'team_city': u'Cleveland'}, ... ]

# Combine flags
$ python fetch_player_id.py --last-name Curry --team GSW
[{u'first_name': u'Stephen', u'last_name': u'Curry', u'games_played_flag': True, u'team_abbreviation': u'GSW', u'team_id': Decimal('1610612744'), u'to_year': u'2015', u'from_year': u'2009', u'roster_status': True, u'player_id': Decimal('201939'), u'team_name': u'Warriors', u'team_code': u'warriors', u'player_code': u'stephen_curry', u'team_city': u'Golden State'}]
```
