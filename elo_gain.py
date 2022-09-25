import json
from pyairtable import Api, Base, Table
from pyairtable.formulas import match
from configparser import ConfigParser

# Config Parser Setup
config = ConfigParser()
config.read("./beerpongscripts/ini/init.ini")

# Airtable Setup
api_key = config.get("AIRTABLE", "api_key")
base_id = config.get("AIRTABLE", "base_id")

playerTable = Table(api_key, base_id, "Gespielte Spiele", timeout=(2, 5))

AKTUELLES_TURNIER = "BPT XVIII"

# Zeigt alle Spiele außer die des aktuellen Turniers an
print(playerTable.all(formula="NOT({Turnier}=" + f"'{AKTUELLES_TURNIER}')", sort=["Numbering"]))