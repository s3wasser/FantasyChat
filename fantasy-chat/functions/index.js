'use strict';

process.env.DEBUG = 'actions-on-google:*';
const App = require('actions-on-google').ApiAiApp;
const functions = require('firebase-functions');
const firebaseAdmin = require('firebase-admin');
firebaseAdmin.initializeApp(functions.config().firebase);

// Action Names API.AI intent
const GET_STATS_CURRENT_SEASON_ACTION = 'get_stats_current_season';

// Parameters parsed from the intent
const PLAYER_FIRST_ARG = 'given-name';
const PLAYER_LAST_ARG = 'last-name';
const STATS_ARG = 'stats';

exports.fantasyChat = functions.https.onRequest((request, response) => {
  const app = new App({request, response});
  console.log('Request headers: ' + JSON.stringify(request.headers));
  console.log('Request body: ' + JSON.stringify(request.body));

  
	function getStatsFromPython (first, last, stat, app) {
		// Making API call through Python script
		 var statsResponseFromPy = '';
		 var data = '';
		 var spawn = require('child_process').spawn;
     	 var py = spawn('python', ['fantasy_stats.py', first, last, stat]);

		  py.stdout.on('data', function (data){
		  	app.tell(data.toString());
		  });
	}

	function getPlayerStat (app) {
		let playerFirstName = app.getArgument(PLAYER_FIRST_ARG);
		let playerLastName = app.getArgument(PLAYER_LAST_ARG);
		let stat = app.getArgument(STATS_ARG);

		getStatsFromPython(playerFirstName, playerLastName, stat, app);
	}

	const actionMap = new Map();
	actionMap.set(GET_STATS_CURRENT_SEASON_ACTION, getPlayerStat);

	app.handleRequest(actionMap);
});
