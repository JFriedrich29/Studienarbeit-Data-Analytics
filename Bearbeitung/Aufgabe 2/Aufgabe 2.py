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
# TODO Auslesen von Chache entfernen
stations_BY = pd.read_excel(
    "Stations_BY.xlsx", index_col=0)
stations_BY
# %%
stations_dict = dict()
for id in stations_BY.index:
    response = requests.get("https://www.umweltbundesamt.de/api/air_data/v2/measures/json", params={
                            "date_from": "2016-01-01", "time_from": "1", "date_to": "2019-12-31", "time_to": "24", "station": str(id), "component": "5", "scope": "2"})
    json_data = json.loads(response.text)
    station_dict = json_data['data']
    stations_dict[id] = station_dict

# %%
# TODO Der Wert stations_dict[id] ist nochmal ein dictionary das wiederum eine Liste als Wert enthält (siehe Postman Data für eine Station)
# TODO Muss richtig umgewandelt werden
df_measurements = pd.DataFrame.from_dict(
    stations_dict, orient="index", columns=["STATION_ID", "DT", "NO2"])
# %%
stations_dict
# %%
# TODO Abspeichern in Chache entfernen
df_measurements.to_excel("NO2_Measurements.xlsx")

# %% [markdown]
# #### b) Setzen Sie den dtype der Spalte NO2 auf float und wandeln Sie die Spalte DT in ein DateTime-Format um.
# %%
# Convert to numeric
df_measurements["NO2"] = df_measurements["NO2"].apply(
    pd.to_numeric, errors='coerce', axis=1)

# Convert to datetime
df_measurements["DT"] = df_measurements["DT"].apply(
    pd.to_datetime, errors='coerce', axis=1)

# %% [markdown]
# #### c) Entfernen Sie alle Zeilen, bei denen der Wert in der Spalte NO2 fehlt. Geben Sie an, wieviele Zeilen dadurch entfernt wurden.
# %%
dfMod = df_measurements.dropna(axis=0, how="any", subset=["NO2"])
difCount = df_measurements.shape[0] - dfMod.shape[0]
print("Deletet " + str(difCount) + " rows that had a missing NO2 value")
df = dfMod
df

# %% [markdown]
# #### d)  Entfernen Sie die Daten zu allen Stationen, die nicht für mindestens 95% der Messzeitpunkute im Auswertezeitraum einen gültigen Messwert enth
# %%
