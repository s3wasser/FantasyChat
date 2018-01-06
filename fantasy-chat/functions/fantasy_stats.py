import urllib2
import sys
import json
import requests

source = 'https://api.mysportsfeeds.com/v1.1/pull/nhl/2017-2018-regular/cumulative_player_stats.json?playerstats='

# ******* REPLACE WITH YOUR OWN MY SPORTSFEED ACCOUNT CREDENTIALS *******
username = ''
password = ''

# 1st tuple value is param for the API get request,
# 2nd tuple value is a key within the returned JSON blob

#getting arguments from index.js
playerFirstName = sys.argv[1].lower()
playerLastName = sys.argv[2].lower()
requestedStat = sys.argv[3]. lower()

statsDictionary = {
  'points': ("Pts", "Points"),
  'goals': ("G", "Goals"),
  'assists': ("A", "Assists"),
  'hat tricks': ("Hat", "HatTricks"),
  'game tying goals': ("GTG", "GameTyingGoals"),
  'powerplay assists': ("PPA", "PowerplayAssists"),
  'shorthanded assists': ("SHA", "ShorthandedAssists"),
  'powerplay points': ("PPPts", "PowerplayPoints"),
  'powerplay goals': ("PPG", "PowerplayGoals"),
  'penalty minutes': ("PIM", "PenaltyMinutes"),
  'shorthanded goals': ("SHG", "ShorthandedGoals"),
  'overtime wins': ("OTW", "OvertimeWins"),
  'shots against': ("SA", "ShotsAgainst"),
  'wins': ("W", "Wins"),
  'losses': ("L", "Losses"),
  'shutouts': ("SO", "Shutouts"),
  'goals against': ("GA", "GoalsAgainst"),
  'overtime loses': ("OTL", "OvertimeLosses"),
  'penalties': ("Pn", "Penalties"),
  'saves': ("Sv", "Saves"),
  'shorthanded points': ("SHPts", "ShorthandedPoints"),
  'game winning goals': ("GWG", "GameWinningGoals")

}

def getPlayerListFromNetwork(stat, name):
  sys.stdout.flush()
  url = source + stat[0] + '&player='+name

  urlib2.timeout = 1
  passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passwordManager.add_password(None, url, username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(passwordManager)
  opener = urllib2.build_opener(authhandler)
  urllib2.install_opener(opener)
  response = urllib2.urlopen(url)

  # Getting player JSON and unwrapping
  playerInfo = response.read()
  player = json.loads(playerInfo)

  # Unwrapping JSON blob
  try:
    cumStats = player["cumulativeplayerstats"]
    statsentry = cumStats["playerstatsentry"]
    return statsentry

  except:
    return

def getFirstSearchPlayerStatsJSON(stat, name):
  try: 
    playerList = getPlayerListFromNetwork(stat, name)
    firstPlayer = playerList[0]
    playerStatsWrapper = firstPlayer["stats"]
    playerStats = playerStatsWrapper["stats"]
    textVal = playerStats[stat[1]]
    value = textVal["#text"]
    print(value)
    sys.stdout.flush()

  except:
    print("Sorry, I couldn't find what you were looking for.")
    sys.stdout.flush()
 
def startQueryForPlayer():
  apiSearchQuery = playerFirstName + "-" + playerLastName
  getFirstSearchPlayerStatsJSON(statsDictionary[statRequested], apiSearchQuery)

startQueryForPlayer()

