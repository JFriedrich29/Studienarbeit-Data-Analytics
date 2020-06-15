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
# stations_BY = pd.read_excel(
#     "Stations_BY.xlsx", index_col=0)
# stations_BY
# %%
# stations_data_dict = dict()
# for id in stations_BY.index:
#     response = requests.get("https://www.umweltbundesamt.de/api/air_data/v2/measures/json", params={
#                             "date_from": "2016-01-01", "time_from": "1", "date_to": "2019-12-31", "time_to": "24", "station": str(id), "component": "5", "scope": "2"})
#     json_data = json.loads(response.text)
#     stations_data_dict[id] = json_data['data']
#     if(response.status_code==200):
#         print(str(id) + ": Abfrage fertig")
#     else:
#         break

# %%

#df_measurements = pd.DataFrame.from_dict(
#   stations_dict, orient="index", columns=["STATION_ID", "DT", "NO2"])
# list_to_create = []
# for station_id in stations_data_dict:
#     for station_data in stations_data_dict[station_id]:
#         measurements_for_id = stations_data_dict[station_id][station_data].values()
#         for data_point in measurements_for_id:
#             datetime = data_point[3]
#             no2_value = data_point[2]
#             list_to_create.append([station_id, datetime, no2_value])
# df_measurements = pd.DataFrame(list_to_create, columns=["STATION_ID", "DT", "NO2"])
# %%
# stations_data_dict
# df_measurements
# %%
# TODO Abspeichern in Chache entfernen
# df_measurements_write_1 = df_measurements[:802284]
# df_measurements_write_2 = df_measurements[802284:]
# with pd.ExcelWriter("NO2_Measurements.xlsx")as writer:
#     df_measurements_write_1.to_excel(writer, sheet_name="NO2_Measurements_1")
#     df_measurements_write_2.to_excel(writer, sheet_name="NO2_Measurements_2")
#%%
xls = pd.ExcelFile('path_to_file.xls') 
df1 = pd.read_excel(xls, 'Sheet1') 
df2 = pd.read_excel(xls, 'Sheet2')
df_measurements = df1.append(df2)
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
