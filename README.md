# NBA Stats to DynamoDB

I created this script to index all NBA players into an AWS DynamoDB table named "nba".

I did so because while the NBA's stats API is great, there is no easy way to search for a player via the API. You need access to a player's player_id in order to access interesting stats pertaining to that player.

## Requirements
* python
* pip
    * awscli
    * requests
* DynamoDB table named 'nba'

## Usage
```python nba_to_dynamo.py```

```bash
$ aws dynamodb scan --table-name nba --filter-expression "last_name = :ln" --projection-expression "#pi, #fn" --expression-attribute-names file://expression-attribute-names.json --expression-attribute-values file://expression-attribute-values.json
{
    "Count": 1,
    "Items": [
        {
            "player_id": {
                "N": "202322"
            },
            "first_name": {
                "S": "John"
            }
        }
    ],
    "ScannedCount": 454,
    "ConsumedCapacity": null
}
```
