var AWS, dynamodb, request, format, nba;

AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-1'});
dynamodb = new AWS.DynamoDB.DocumentClient();

// var params = {
//     TableName: 'nba',
//     FilterExpression: 'last_name = :last_name',
//     ExpressionAttributeValues : {':last_name' : 'Wall'}
// };

// dynamodb.scan(params, function(err, data) {
//   if (err) console.log(err, err.stack); // an error occurred
//   else     console.log(data);           // successful response
// });
request = require('request');
format = require("string-template");

nba = {
  statsRequest: request.defaults({
    baseUrl: 'http://stats.nba.com/stats/',
    json: true
  }),
  currentSeason: '2015-16',
  leagueId: '00',
  getPlayerId: function (firstName, lastName) {
    var params, filterExpression, expAttributeVals;
    params = {
      TableName: 'nba'
    };
    filterExpression = [];
    expAttributeVals = {};
    if (firstName) {
      filterExpression.append('first_name = :first_name');
      expAttributeVals[':first_name'] = firstName;
    }
    if (lastName) {
      filterExpression.append('last_name = :last_name');
      expAttributeVals[':last_name'] = lastName;
    }

    params['FilterExpression'] = filterExpression.join(' AND ');
    params['ExpressionAttributeValues'] = expAttributeVals;
  },
  getGeneralPlayerInfo: function (id, cb) {
    this.statsRequest({
      url: 'commonplayerinfo',
      qs: {
        PlayerID: id
      }
    }, function (error, response, json) {
      if (!error && response.statusCode == 200) {
        var playerInfo, statement;
        playerInfo = json['resultSets'][1]['rowSet'][0];
        statement = format('{player} is averaging {points} with {assists} assists and {rebounds} rebounds.', {
          player: playerInfo[1],
          points: playerInfo[3],
          assists: playerInfo[4],
          rebounds: playerInfo[5]
        });

        cb(statement);
      }
    });
  }
};

module.exports = nba;
if (process.argv.length == 2) {
  console.log('Last name required... Exiting...');
} else {
  var lastName, params;

  lastName = process.argv[2];
  params = {
    TableName: 'nba',
    FilterExpression: 'last_name = :last_name',
    ExpressionAttributeValues : {':last_name' : lastName}
  };

  dynamodb.scan(params, function (err, data) {
    if (err) {
      console.log(err, err.stack);
      return;
    } else if (data.Count == 0) {
      console.log('No player found with name.');
      return;
    } else {
      var id;

      id = data['Items'][0]['player_id'];

      var g = function (s) {
        console.log(s);
      }

      nba.getGeneralPlayerInfo(id, g);
    }
  });
};