from configparser import ConfigParser
import json
from pyairtable import Api, Base, Table
from beerpongscripts.elo.elo import new_Elo

# Config Parser Setup
config = ConfigParser()
config.read("./beerpongscripts/ini/init.ini")

# Airtable Setup
api_key = config.get("AIRTABLE", "api_key")
base_id = config.get("AIRTABLE", "base_id")

matches = Table(api_key, base_id, "Gespielte Spiele", timeout=(2, 5))
spieler = Table(api_key, base_id, "Spieler", timeout=(2, 5))

# Rating Setup
playerDict = {}
matchesArray = []
tournament = "" #berechnet aktuelles Turnier und die aktuelle differenz.
AIRTABLE = True # erechnet aktuelle Elo und trägt diese in Tabelle ein.
i = 1

# Download Player Data
for player in spieler.all():
    print(player)
    player_id = player["id"]
    player_aktiv = player["fields"]["Aktiv"]
    player_name = player["fields"]["Name"] 
    player_elo = player["fields"]["Elo_old"]
    player_games = player["fields"]["Spiele"]
    player_max_elo = player["fields"]["All Time High Elo"]
    playerDict[player_id] = {
        "Name": player_name,
        "Elo": [],
        "Max_Elo": player_max_elo,
        "Games": player_games,
        "Aktiv": player_aktiv
    }
    playerDict[player_id]["Elo"].append(player_elo) 

if tournament:
    for match in matches.all(sort=["Numbering"], formula="({Turnier}=" + f"'{tournament}')"):
        matchesArray.append(match)
else:
    for match in matches.all(sort=["Numbering"]):
        matchesArray.append(match)

for match in matchesArray:
    heimspieler = match["fields"]["Heimspieler"][0]
    gastspieler = match["fields"]["Gastspieler"][0]
    elo_heim = playerDict[heimspieler]["Elo"][-1]
    elo_gast = playerDict[gastspieler]["Elo"][-1]
    games_heim = playerDict[heimspieler]["Games"]
    games_gast = playerDict[gastspieler]["Games"]
    
    if match["fields"]["Winner"] == "Heim":
        punkte_heim = 1
        punkte_gast = 0
    elif match["fields"]["Winner"] == "Gast":
        punkte_heim = 0
        punkte_gast = 1
    else:
        punkte_heim = 0.5
        punkte_gast = 0.5

    new_Elo_Heim = new_Elo(elo_heim, elo_gast, games_heim, punkte_heim) 
    new_Elo_Gast = new_Elo(elo_gast, elo_heim, games_gast, punkte_gast)

    print(heimspieler, elo_heim, punkte_heim, new_Elo_Heim)
    print(gastspieler, elo_gast, punkte_gast, new_Elo_Gast)

    playerDict[heimspieler]["Elo"].append(new_Elo_Heim)
    playerDict[gastspieler]["Elo"].append(new_Elo_Gast)

# Max Elo Berechnung
for p in playerDict:
    if max(playerDict[p]["Elo"]) > playerDict[p]["Max_Elo"]:
        playerDict[p]["Max_Elo"] = max(playerDict[p]["Elo"])
    else:
        continue

# Json Liste
rangliste = []
for p in playerDict:
    if playerDict[p]["Aktiv"] == "Nein":
        continue
    rangliste.append({
                         "Name": playerDict[p]["Name"],
                         "Elo": playerDict[p]["Elo"][-1],
                         "Max_Elo": playerDict[p]["Max_Elo"],
                         "Games": playerDict[p]["Games"],
                         "Diff": playerDict[p]["Elo"][-1] - playerDict[p]["Elo"][0] 
                     }) 
rangliste = sorted(rangliste, key=lambda x: (x["Elo"], x["Games"]), reverse=True)

with open("singplayer_elo_ranking.json", "w") as jsonfile:
    jsonfile.write(json.dumps(rangliste, indent=4, ensure_ascii=False))

# Airtable

if tournament == "" and AIRTABLE:
    for p in playerDict:
        spieler.update(p, {"Elo": playerDict[p]["Elo"][-1]})
        spieler.update(p, {"All Time High Elo": playerDict[p]["Max_Elo"]})
