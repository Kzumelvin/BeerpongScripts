from pyairtable import Api, Base, Table

class BeerpongStats:
    def __init__(self, api_key, base_id):
        self.teams = Table(api_key, base_id, "Teams", timeout=(2, 5))
        self.matches = Table(api_key, base_id, "Gespielte Spiele", timeout=(2, 5))
        self.tournament = Table(api_key, base_id, "Turniere", timeout=(2, 5))
        self.player = Table(api_key, base_id, "Spieler", timeout=(2, 5))
        self.beer = Table(api_key, base_id, "Bierspender", timeout=(2, 5))

    # Teams
    def getTeams(self):
        return self.teams.all()

    def getTeamName(self, team_id):
        return self.teams.get(team_id)["fields"]["Teamname"]

    def getTeamPower(self, team_id, decimal=2):
        return round(float(self.teams.get(team_id)["fields"]["Teamstärke"]), decimal)

    def getTeamMembers(self, team_id):
        return self.teams.get(team_id)["fields"]["Spieler"]

    def getTeamSNRate(self, team_id, decimal=2):
        return round(float(self.teams.get(team_id)["fields"]["SN Rate Teams"]), decimal)

    def getTeamMatches(self, team_id):
        return self.teams.get(team_id)["fields"]["Spiele"]

    def checkTeamChamps(self, team_id):
        if self.teams.get(team_id)["fields"]["Champs"] == "Ja":
            return True
        else:
            return False

    def getTeamPlacement(self, team_id, place):
        return self.teams.get(team_id)["fields"][f"P{place}"]

    def getTeamParticipation(self, team_id):
        return self.teams.get(team_id)["fields"]["Teilnahmen"]

    def getTeamWins(self, team_id):
        return self.teams.get(team_id)["fields"]["Siege"]

    def getTeamLoses(self, team_id):
        return self.teams.get(team_id)["fields"]["Niederlagen"]

    def getTeamDraws(self, team_id):
        return self.teams.get(team_id)["fields"]["Unentschieden"]

    def getTeamHomeMatches(self, team_id):
        return self.teams.get(team_id)["fields"]["Gespielte Spiele Heim"]

    def getTeamAwayMatches(self, team_id):
        return self.teams.get(team_id)["fields"]["Gespielte Spiele Gast"]

    # Spieler

    def getPlayer(self):
        return self.player.all()

    def setPlayerField(self, player_id, field_dict):
        return self.player.update(player_id, field_dict)

    def getPlayerName(self, player_id):
        return self.player.get(player_id)["fields"]["Name"]

    def getPlayerPower(self, player_id):
        return self.player.get(player_id)["fields"]["Spielstärke"]

    def getPlayerWins(self, player_id):
        return self.player.get(player_id)["fields"]["Siege"]

    def getPlayerLoses(self, player_id):
        return self.player.get(player_id)["fields"]["Niederlagen"]

    def getPlayerDraws(self, player_id):
        return self.player.get(player_id)["fields"]["Unentschieden"]

    def getPlayerSNRate(self, player_id, decimal=2):
        return round(float(self.player.get(player_id)["fields"]["SN Rate"]), decimal)

    def getPlayerPlayedGames(self, player_id):
        return self.player.get(player_id)["fields"]["Spiele"]

    def getPlayerDitchedCups(self, player_id):
        return self.player.get(player_id)["fields"]["Ditched Cups"]

    def getPlayerTournamentWins(self, player_id):
        return self.player.get(player_id)["fields"]["Turniersiege"]

    def getPlayerTournamentPoints(self, player_id):
        return self.player.get(player_id)["fields"]["Turnierpunkte"]

    def getPlayerParticipations(self, player_id):
        return self.player.get(player_id)["fields"]["Teilnahmen"]

    def getPlayerTournamentWinQuote(self, player_id, decimal=2):
        return round(float(self.player.get(player_id)["fields"]["Turniersiegquote"]), decimal)

    def getPlayerMatchWinRate(self, player_id, decimal=2):
        return round(float(self.player.get(player_id)["fields"]["Game Win Rate"]), decimal)

    def getPlayerPlacement(self, player_id, place):
        return self.player.get(player_id)["fields"][f"Platz {place}"]

    def getPlayerAvgTournamentPoints(self, player_id):
        return self.player.get(player_id)["fields"]["Durch. Turnierpunkte"]

    def getPlayerAvgTournamentSeeding(self, player_id):
        return self.player.get(player_id)["fields"]["Durch. Turnierplatzierung"]

    def getPlayerDitchedCupsPerGame(self, player_id):
        return self.player.get(player_id)["fields"]["DC pro Spiele"]

    def getPlayerMembership(self, player_id):
        return self.player.get(player_id)["fields"]["Teams"]

    def getPlayerBeerDonations(self, player_id, decimal=2):
        return round(float(self.player.get(player_id)["fields"]["Bierspenden"]), decimal)

    def checkPlayerStatus(self, player_id):
        if self.player.get(player_id)["fields"]["Aktiv"] == "Ja":
            return True
        else:
            return False

    # gespielte Spiele

    def getPlayedGames(self):
        return self.matches.all(sort=["Numbering"])

    def getPlayedGameInTournament(self, tournament):
        return self.matches.all(sort=["Numbering"], formula="({Turnier}=" + f"'{tournament}')")

    def getMatch(self, match_id):
        return self.matches.get(match_id)["fields"]["Begegnung"]

    def getMatchGameMode(self, match_id):
        return self.player.get(match_id)["fields"]["Spielart"]

    def getMatchGroup(self, match_id):
        return self.player.get(match_id)["fields"]["Spielart"]

    def getMatchHomeTeam(self, match_id):
        return self.player.get(match_id)["fields"]["Heimteam"]

    def getMatchAwayTeam(self, match_id):
        return self.player.get(match_id)["fields"]["Gastteam"]

    def getMatchResult(self, match_id):
        return self.player.get(match_id)["fields"]["Ergebnis"]

    def getMatchCupsHome(self, match_id):
        return self.player.get(match_id)["fields"]["Heimbecher"]

    def getMatchCupsAway(self, match_id):
        return self.player.get(match_id)["fields"]["Gastbecher"]

    def getMatchWinRateHome(self, match_id, decimal=2):
        return round(float(self.player.get(match_id)["fields"]["Siegquote Heim"]), decimal)

    def getMatchWinRateAway(self, match_id, decimal=2):
        return round(float(self.player.get(match_id)["fields"]["Siegquote Gast"]), decimal)

    def getMatchWinner(self, match_id):
        return self.player.get(match_id)["fields"]["Winner"]

    # Turniere

    def getTournaments(self):
        return self.tournament.all(sort=["-Turniernummer"])

    def getTournamentId(self, tournament_name):
        for records in self.tournament.iterate(page_size=100, max_records=1000):
            print(records)

    def getTournament(self, tournament_id):
        return self.player.get(tournament_id)["fields"]["Turniername"]

    def getTournamentNumber(self, tournament_id):
        return self.player.get(tournament_id)["fields"]["Turniernummer"]

    def getTournamentPlacement(self, tournament_id, place):
        try:
            return self.player.get(tournament_id)["fields"][f"Platz {place}"]
        except KeyError:
            return None

    def getTournamentParticipations(self, tournament_id):
        return self.player.get(tournament_id)["fields"]["Teilnehmerzahl"]

    def getTournamentBeerDontaions(self, tournament_id):
        return self.player.get(tournament_id)["fields"]["Bierspenden"]