# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import plotly.graph_objects as go
import requests

# %% [markdonw]
# #### Graphische Analyse der Daten
# 1. Diagramm Alle 5 Schadstoffe über Zeit (Täglich). Radoi Buttons für StationsTypen und Filter für Schadstoffstypen
# 2. Diagramm Vergleich des Schadstoffes mit dem Durchschnitt der Vorjahre (5. Vorjahre), Schadstoff über Radio Button änderbar
# #### Art der Daten
# Dataframe mit Allen Schadstoffstypen zu den entsprechenden Stationstypen und Zeitstempel, eventluell ein Binärencoding von dem Lockdownstatus

# #### Hypothesen
# 1.

# TODO Auslesen von Chache entfernen
stations_BY = pd.read_excel(
    "Stations_BY.xlsx", index_col=0)
# stations_BY
# %%
air_pollutants = {"1": "PM10", "2": "CO", "3": "O3", "4": "SO2", "5": "NO2"}
stations_data_dict = dict()
for station_id in stations_BY.index:
    for pollutant in air_pollutants:
        stations_data_dict[station_id]
    response = requests.get("https://www.umweltbundesamt.de/api/air_data/v2/measures/json",
                            params={
                                "date_from": "2016-01-01",
                                "time_from": "1",
                                "date_to": "2019-12-31",
                                "time_to": "24",
                                "station": str(station_id),
                                "component": "5",
                                "scope": "2"
                            }
                            )
    json_data = json.loads(response.text)
    stations_data_dict[station_id] = json_data['data']
    if(response.status_code == 200):
        print(str(station_id) + ": Abfrage fertig")
    else:
        break
