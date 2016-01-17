import sys
import argparse

import boto3
from boto3.dynamodb.conditions import Attr


dynamo = boto3.resource('dynamodb')
nba_table = dynamo.Table('nba')

parser = argparse.ArgumentParser(description='One of the following is required.')
parser.add_argument('--last-name', help='Search by last name')
parser.add_argument('--first-name', help='Search by first name')
parser.add_argument('--team', help='Search by team abbreviation')
args = parser.parse_args()

if args.last_name is None and args.first_name is None and args.team is None:
    sys.exit(parser.print_help())

expressions = []
if args.last_name:
    expressions.append(Attr('last_name').eq(args.last_name.lower()))
if args.first_name:
    expressions.append(Attr('first_name').eq(args.first_name.lower()))
if args.team:
    expressions.append(Attr('team_abbreviation').eq(args.team.lower()))

filter_expression = expressions.pop()
for expression in expressions:
    filter_expression = filter_expression & expression

response = nba_table.scan(FilterExpression=filter_expression)
items = response['Items']
print(items)
