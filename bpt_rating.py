from beerpongscripts.elo.elo import new_Elo
import json
from beerpongscripts.airtable.airtable import BeerpongStats
from configparser import ConfigParser

import pandas as pd
import numpy as np

# Config Parser Setup
config = ConfigParser()
config.read("./beerpongscripts/ini/init.ini")

# Airtable Setup
api_key = config.get("AIRTABLE", "api_key")
base_id = config.get("AIRTABLE", "base_id")
bpt = BeerpongStats(api_key, base_id)
#Update Airtable
AIRTABLE = True

# Rating Setup
playerDict = {}
teamsDict = {}
DATA = []

i = 1
for player in bpt.getPlayer():
    player_id = player["id"]
    player_aktiv = player["fields"]["Aktiv"]
    player_name = player["fields"]["Name"]
    player_elo = int(player["fields"]["start_elo"])
    playerDict[player_id] = {"Name": player_name, "Elo" : [],"Max_Elo": 0, "Games":0, "Aktiv": player_aktiv}
    playerDict[player_id]["Elo"].append(player_elo)


for data_piece in bpt.getPlayedGames():
    DATA.append(data_piece)

for team in bpt.getTeams():
    team_id = team["id"]
    team_name = team["fields"]["Teamname"]
    spieler1 = team["fields"]["Spieler"][0]
    spieler2 = team["fields"]["Spieler"][1]
    spieler3 = ""
    if len(team["fields"]["Spieler"]) == 3:
        spieler3 = team["fields"]["Spieler"][2]
    teamsDict[team_id] = {"Teamname": team_name, "Spieler1": spieler1, "Spieler2": spieler2, "Spieler3": spieler3}

for game in DATA:
    Heim1 = {"ID": "", "Name": "", "Punkte": 0}
    Heim2 = {"ID": "", "Name": "", "Punkte": 0}
    Heim3 = {"ID": "", "Name": "", "Punkte": 0}
    Gast1 = {"ID": "", "Name": "", "Punkte": 0}
    Gast2 = {"ID": "", "Name": "", "Punkte": 0}
    Gast3 = {"ID": "", "Name": "", "Punkte": 0}

    game_Id = game["id"]
    game_Winner = game["fields"]["Winner"] # Heim oder Gast oder Unentschieden
    Heimteam_Player_Ids = teamsDict[game["fields"]["Heimteam"][0]]
    Gastteam_Players_Ids = teamsDict[game["fields"]["Gastteam"][0]]

    Heim1["Name"] = playerDict[Heimteam_Player_Ids["Spieler1"]]["Name"]
    Heim2["Name"] = playerDict[Heimteam_Player_Ids["Spieler2"]]["Name"]
    Gast1["Name"] = playerDict[Gastteam_Players_Ids["Spieler1"]]["Name"]
    Gast2["Name"] = playerDict[Gastteam_Players_Ids["Spieler2"]]["Name"]

    if len(Heimteam_Player_Ids) == 3:
        Heim3["Name"] = playerDict[Heimteam_Player_Ids["Spieler3"]]["Name"]
    if len(Gastteam_Players_Ids) == 3:
        Gast3["Name"] = playerDict[Gastteam_Players_Ids["Spieler3"]]["Name"]

    Heim1["ID"] = Heimteam_Player_Ids["Spieler1"]
    Heim2["ID"] = Heimteam_Player_Ids["Spieler2"]
    Gast1["ID"] = Gastteam_Players_Ids["Spieler1"]
    Gast2["ID"] = Gastteam_Players_Ids["Spieler2"]

    if len(Heimteam_Player_Ids) == 3:
        Heim3["ID"] = Heimteam_Player_Ids["Spieler3"]
    if len(Gastteam_Players_Ids) == 3:
        Gast3["ID"] = Gastteam_Players_Ids["Spieler3"]

    if game_Winner == "Heim":
        Heim1["Punkte"] = 1
        Heim2["Punkte"] = 1
        Heim3["Punkte"] = 1
    elif game_Winner == "Gast":
        Gast1["Punkte"] = 1
        Gast2["Punkte"] = 1
        Gast3["Punkte"] = 1
    elif game_Winner == "Unentschieden":
        Heim1["Punkte"] = 0.5
        Heim2["Punkte"] = 0.5
        Heim3["Punkte"] = 0.5
        Gast1["Punkte"] = 0.5
        Gast2["Punkte"] = 0.5
        Gast3["Punkte"] = 0.5
    else:
        print("ERROR: Ein Fehler bei der Punktevergabe ist aufgetreten!")

    # Neue Elo Heim1
    new_Elo_Heim1 = new_Elo(playerDict[Heim1["ID"]]["Elo"][-1], playerDict[Gast1["ID"]]["Elo"][-1], playerDict[Heim1["ID"]]["Games"], Heim1["Punkte"])
    playerDict[Heim1["ID"]]["Games"] = playerDict[Heim1["ID"]]["Games"] + 1

    playerDict[Heim1["ID"]]["Elo"].append(new_Elo_Heim1)

    new_Elo_Heim1 = new_Elo(playerDict[Heim1["ID"]]["Elo"][-1], playerDict[Gast2["ID"]]["Elo"][-1], playerDict[Heim1["ID"]]["Games"], Heim1["Punkte"])
    playerDict[Heim1["ID"]]["Games"] = playerDict[Heim1["ID"]]["Games"] + 1

    playerDict[Heim1["ID"]]["Elo"].append(new_Elo_Heim1)

    # Neue Elo Heim2
    new_Elo_Heim2 = new_Elo(playerDict[Heim2["ID"]]["Elo"][-1], playerDict[Gast1["ID"]]["Elo"][-1], playerDict[Heim2["ID"]]["Games"], Heim2["Punkte"])
    playerDict[Heim2["ID"]]["Games"] = playerDict[Heim2["ID"]]["Games"] + 1

    playerDict[Heim2["ID"]]["Elo"].append(new_Elo_Heim2)

    new_Elo_Heim2 = new_Elo(playerDict[Heim2["ID"]]["Elo"][-1], playerDict[Gast2["ID"]]["Elo"][-1], playerDict[Heim2["ID"]]["Games"], Heim2["Punkte"])
    playerDict[Heim2["ID"]]["Games"] = playerDict[Heim2["ID"]]["Games"] + 1

    playerDict[Heim2["ID"]]["Elo"].append(new_Elo_Heim2)

    # Neue Elo Gast1
    new_Elo_Gast1 = new_Elo(playerDict[Gast1["ID"]]["Elo"][-1], playerDict[Heim1["ID"]]["Elo"][-1], playerDict[Gast1["ID"]]["Games"], Gast1["Punkte"])
    playerDict[Gast1["ID"]]["Games"] = playerDict[Gast1["ID"]]["Games"] + 1

    playerDict[Gast1["ID"]]["Elo"].append(new_Elo_Gast1)

    new_Elo_Gast1 = new_Elo(playerDict[Gast1["ID"]]["Elo"][-1], playerDict[Heim2["ID"]]["Elo"][-1],playerDict[Gast1["ID"]]["Games"], Gast1["Punkte"])
    playerDict[Gast1["ID"]]["Games"] = playerDict[Gast1["ID"]]["Games"] + 1

    playerDict[Gast1["ID"]]["Elo"].append(new_Elo_Gast1)

    # Neue Elo Gast2
    new_Elo_Gast2 = new_Elo(playerDict[Gast2["ID"]]["Elo"][-1], playerDict[Heim1["ID"]]["Elo"][-1], playerDict[Gast2["ID"]]["Games"], Gast2["Punkte"])
    playerDict[Gast2["ID"]]["Games"] = playerDict[Gast2["ID"]]["Games"] + 1

    playerDict[Gast2["ID"]]["Elo"].append(new_Elo_Gast2)

    new_Elo_Gast2 = new_Elo(playerDict[Gast2["ID"]]["Elo"][-1], playerDict[Heim2["ID"]]["Elo"][-1], playerDict[Gast2["ID"]]["Games"], Gast2["Punkte"])
    playerDict[Gast2["ID"]]["Games"] = playerDict[Gast2["ID"]]["Games"] + 1

    playerDict[Gast2["ID"]]["Elo"].append(new_Elo_Gast2)

    if len(Heimteam_Player_Ids) == 3:
        new_Elo_Gast1 = new_Elo(playerDict[Gast1["ID"]]["Elo"][-1], playerDict[Heim3["ID"]]["Elo"][-1], playerDict[Gast1["ID"]]["Games"], Gast1["Punkte"])
        playerDict[Gast1["ID"]]["Games"] = playerDict[Gast1["ID"]]["Games"] + 1

        playerDict[Gast1["ID"]]["Elo"].append(new_Elo_Gast1)

        new_Elo_Gast2 = new_Elo(playerDict[Gast2["ID"]]["Elo"][-1], playerDict[Heim3["ID"]]["Elo"][-1], playerDict[Gast2["ID"]]["Games"], Gast2["Punkte"])
        playerDict[Gast2["ID"]]["Games"] = playerDict[Gast2["ID"]]["Games"] + 1

        playerDict[Gast2["ID"]]["Elo"].append(new_Elo_Gast2)

        new_Elo_Heim3 = new_Elo(playerDict[Heim3["ID"]]["Elo"][-1], playerDict[Gast1["ID"]]["Elo"][-1], playerDict[Heim3["ID"]]["Games"], Heim3["Punkte"])
        playerDict[Heim3["ID"]]["Games"] = playerDict[Heim3["ID"]]["Games"] + 1

        playerDict[Heim3["ID"]]["Elo"].append(new_Elo_Heim3)

        new_Elo_Heim3 = new_Elo(playerDict[Heim3["ID"]]["Elo"][-1], playerDict[Gast2["ID"]]["Elo"][-1], playerDict[Heim3["ID"]]["Games"], Heim3["Punkte"])
        playerDict[Heim3["ID"]]["Games"] = playerDict[Heim3["ID"]]["Games"] + 1

        playerDict[Heim3["ID"]]["Elo"].append(new_Elo_Heim3)

    if len(Gastteam_Players_Ids) == 3:
        new_Elo_Heim1 = new_Elo(playerDict[Heim1["ID"]]["Elo"][-1], playerDict[Gast3["ID"]]["Elo"][-1], playerDict[Heim1["ID"]]["Games"], Heim1["Punkte"])
        playerDict[Heim1["ID"]]["Games"] = playerDict[Heim1["ID"]]["Games"] + 1

        playerDict[Heim1["ID"]]["Elo"].append(new_Elo_Heim1)

        new_Elo_Heim2 = new_Elo(playerDict[Heim2["ID"]]["Elo"][-1], playerDict[Gast3["ID"]]["Elo"][-1], playerDict[Heim2["ID"]]["Games"], Heim2["Punkte"])
        playerDict[Heim2["ID"]]["Games"] = playerDict[Heim2["ID"]]["Games"] + 1

        playerDict[Heim2["ID"]]["Elo"].append(new_Elo_Heim2)

        new_Elo_Gast3 = new_Elo(playerDict[Gast3["ID"]]["Elo"][-1], playerDict[Heim1["ID"]]["Elo"][-1], playerDict[Gast3["ID"]]["Games"], Gast3["Punkte"])
        playerDict[Gast3["ID"]]["Games"] = playerDict[Gast3["ID"]]["Games"] + 1

        playerDict[Gast3["ID"]]["Elo"].append(new_Elo_Gast3)

        new_Elo_Gast2 = new_Elo(playerDict[Gast3["ID"]]["Elo"][-1], playerDict[Heim2["ID"]]["Elo"][-1], playerDict[Gast2["ID"]]["Games"], Gast2["Punkte"])
        playerDict[Gast3["ID"]]["Games"] = playerDict[Gast3["ID"]]["Games"] + 1

        playerDict[Gast3["ID"]]["Elo"].append(new_Elo_Gast3)

    if len(Heimteam_Player_Ids) == 3 and len(Gastteam_Players_Ids) == 3:
        new_Elo_Heim3 = new_Elo(playerDict[Heim3["ID"]]["Elo"][-1], playerDict[Gast3["ID"]]["Elo"][-1],playerDict[Heim3["ID"]]["Games"], Heim3["Punkte"])
        playerDict[Heim3["ID"]]["Games"] = playerDict[Heim3["ID"]]["Games"] + 1

        playerDict[Heim3["ID"]]["Elo"].append(new_Elo_Heim3)

        new_Elo_Gast3 = new_Elo(playerDict[Gast3["ID"]]["Elo"][-1], playerDict[Heim3["ID"]]["Elo"][-1], playerDict[Gast3["ID"]]["Games"], Gast3["Punkte"])
        playerDict[Gast3["ID"]]["Games"] = playerDict[Gast3["ID"]]["Games"] + 1

        playerDict[Gast3["ID"]]["Elo"].append(new_Elo_Gast3)

    print(i, Heim1["Name"], ":", new_Elo_Heim1, " ", Heim2["Name"], ":",new_Elo_Heim2 , " ",Gast1["Name"], ":",new_Elo_Gast1, " ",Gast2["Name"], ":",new_Elo_Gast2)
    i = i + 1

listElo = []

for p in playerDict:
    print(p)
    if playerDict[p]["Aktiv"] == "Nein":
        continue
    playerDict[p]["Max_Elo"] = max(playerDict[p]["Elo"])
    listElo.append({"Name": playerDict[p]["Name"], "Elo": playerDict[p]["Elo"][-1],"Max_Elo": max(playerDict[p]["Elo"]) , "Max_Elo_Game":  playerDict[p]["Elo"].index(max(playerDict[p]["Elo"])), "Games": playerDict[p]["Games"]})

listElo = sorted(listElo, key=lambda x: (x["Elo"], x["Games"]), reverse=True)

with open("./results/sorted_elo_final.json", "w") as jsonfile:
    jsonfile.write(json.dumps(listElo, ensure_ascii=False, indent=4))

with open("./results/elo_gesamt.json", "w") as jsonfile:
    jsonfile.write(json.dumps(playerDict, ensure_ascii=False, indent=4))

# Updating airtable
for p in playerDict:
    print(p)
    if AIRTABLE:
        bpt.setPlayerField(p, {"Elo": playerDict[p]["Elo"][-1]})
        bpt.setPlayerField(p, {"Max_Elo": playerDict[p]["Max_Elo"]})

# Excel, Numpy and Pandas
elo_array = []
max_colums = 0
colums_array = []
index_array = []

for p in playerDict:
    if playerDict[p]["Aktiv"] == "Nein":
        continue
    elo_array.append(playerDict[p]["Elo"])
    index_array.append(playerDict[p]["Name"])
    if len(playerDict[p]["Elo"]) > max_colums:
        colums_array = playerDict[p]["Elo"]

df = pd.DataFrame(elo_array, index=index_array)
df = df.sort_values(by=[0], ascending=False)
print(df)

df.to_excel("./results/test.xlsx")
