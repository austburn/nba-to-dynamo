var AWS, dynamodb, request, format, nba;

AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-1'});
dynamodb = new AWS.DynamoDB.DocumentClient();

request = require('request');
format = require("string-template");

nba = {
  currentSeason: '2015-16',
  leagueId: '00',
  getPlayerId: function (firstName, lastName, actionCallback, responseCallback) {
    var params, filterExpression, expAttributeVals;
    params = {
      TableName: 'nba'
    };
    filterExpression = [];
    expAttributeVals = {};
    if (firstName) {
      filterExpression.push('first_name = :first_name');
      expAttributeVals[':first_name'] = firstName;
    }
    if (lastName) {
      filterExpression.push('last_name = :last_name');
      expAttributeVals[':last_name'] = lastName;
    }

    params['FilterExpression'] = filterExpression.join(' AND ');
    params['ExpressionAttributeValues'] = expAttributeVals;

    dynamodb.scan(params, function (err, data) {
      if (err) {
        console.log(err, err.stack);
        responseCallback('No player found with name.');
        return;
      } else if (data.Count == 0) {
        console.log('No player found with that name.');
        responseCallback('No player found with that name.');
        return;
      } else if (data.Count > 1) {
        var playerList, playerString;

        playerList = data['Items'].map(function (i) {
          return i['first_name'];
        });

        playerList.splice(playerList.length - 1, 0, 'and');
        playerString = playerList.join(', ');

        console.log('Too many players: ' + playerString + ' match your request.');
        responseCallback('I found these players: ' + playerString + ' with that last name.');
        return;
      } else {
        var id;

        id = data['Items'][0]['player_id'];

        actionCallback(id, responseCallback);
      }
    });
  },
  getGeneralPlayerInfo: function (id, responseCallback) {
    request({
      url: 'http://stats.nba.com/stats/commonplayerinfo',
      json: true,
      qs: {
        PlayerID: id
      }
    }, function (error, response, json) {
      if (!error && response.statusCode == 200) {
        var playerInfo, statement;
        playerInfo = json['resultSets'][1]['rowSet'][0];
        statement = format('{player} is averaging {points} points with {assists} assists and {rebounds} rebounds.', {
          player: playerInfo[1],
          points: playerInfo[3],
          assists: playerInfo[4],
          rebounds: playerInfo[5]
        });

        responseCallback(statement);
      }
    });
  }
};

module.exports = nba;
