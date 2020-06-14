# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
# %% [markdown]
# ### Aufgabe 2 (NO2-Daten, Datenvorbereitung, Datenqualität)

# %% [markdown]
# #### a) Laden Sie über die Measurements-API für alle bayerischen Stationen (wie oben ermittelt) die Ein-Stunden-Mittelwerte für die NO2-Konzentrationen für den Zeitraum 01.01.2016 bis 31.12.2019 herunter und überführen Sie diese in einen DataFrame namens data_no2. Dieser soll die Spalten STATION_ID, DT und NO2 besitzen, die die Stations-ID, das Messdatum mit Uhrzeit sowie die gemessene NO2-Konzentration enthalten.
# %%
stations_BY = pd.read_excel("Stations_BY.xlsx", index_col=0)
stations_dict = dict()
for id in stations_BY.index:
    response = requests.get("https://www.umweltbundesamt.de/api/air_data/v2/measures/json", params={
                            "date_from": "2016-01-01", "time_from": "1", "date_to": "2019-12-31", "time_to": "24", "station": str(id), "component": "5", "scope": "2"})
    json_data = json.loads(response.text)
    station_dict = json_data['data']
    stations_dict[id] = station_dict


df_measurements = pd.DataFrame.from_dict(
    stations_dict, orient="index", columns=["STATION_ID", "DT", "NO2"],)

# %%
