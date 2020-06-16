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
# list_to_create = []
# for station_id in stations_data_dict:
#     for station_data in stations_data_dict[station_id]:
#         measurements_for_id = stations_data_dict[station_id][station_data].values()
#         for data_point in measurements_for_id:
#             datetime = data_point[3]
#             no2_value = data_point[2]
#             list_to_create.append([station_id, datetime, no2_value])
# df_measurements = pd.DataFrame(list_to_create,columns=["STATION_ID", "DT", "NO2"])
# df_measurements.index.name='dp_id'
# df_measurements = df_measurements.replace(to_replace='24:00:00', value="00:00:00", regex=True)

# # %%
# # TODO Abspeichern in Chache entfernen
# df_measurements_write_1 = df_measurements[:802284]
# df_measurements_write_2 = df_measurements[802284:]
# with pd.ExcelWriter("NO2_Measurements.xlsx")as writer:
#     df_measurements_write_1.to_excel(writer, sheet_name="NO2_Measurements_1")
#     df_measurements_write_2.to_excel(writer, sheet_name="NO2_Measurements_2")
# %%
xls = pd.ExcelFile("NO2_Measurements.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1.append(df2)
df_measurements = df_measurements.replace(
    to_replace='24:00:00', value="00:00:00", regex=True)

# %%
# Backup in memory
df_backup = df_measurements.copy(deep=True)
# %% [markdown]
# #### b) Setzen Sie den dtype der Spalte NO2 auf float und wandeln Sie die Spalte DT in ein DateTime-Format um.
# %%
# Convert to numeric
# df_measurements["NO2"] = df_measurements["NO2"].apply(
#     pd.to_numeric, errors='coerce', axis=1)
df_measurements["NO2"] = pd.to_numeric(df_measurements["NO2"], errors="coerce")

# Convert to datetime
# df_measurements["DT"] = df_measurements["DT"].apply(
#     pd.to_datetime, errors='coerce', axis=1)
df_measurements = df_measurements.replace(to_replace='24:00:00', value="00:00:00", regex=True)
df_measurements["DT"] = pd.to_datetime(df_measurements["DT"], errors="coerce")
# %% [markdown]
# #### c) Entfernen Sie alle Zeilen, bei denen der Wert in der Spalte NO2 fehlt. Geben Sie an, wieviele Zeilen dadurch entfernt wurden.
# %%
df_measurements_nanCleaned = df_measurements.dropna(
    axis=0, how="any", subset=["NO2"])
difCount = df_measurements.shape[0] - df_measurements_nanCleaned.shape[0]
print("Deleted " + str(difCount) + " rows that had a missing NO2 value")
# df_measurements = df_measurements_nanCleaned # Todo einkommentieren überschreibt das orginale dataframe, müssen wir Hr. Brunner fragen ob wir das weiter verwenden dürfen

# %%
# Todo Remove shape testing
df_measurements.isnull().sum()
df_measurements_nanCleaned.isnull().sum()

# %%
df_measurements.shape
df_measurements_nanCleaned.shape

# %% [markdown]
# #### d)  Entfernen Sie die Daten zu allen Stationen, die nicht für mindestens 95% der Messzeitpunkte im Auswertezeitraum einen gültigen Messwert enthalten

# %%
# Todo remove group filtering testing
# df_measurements_nanCleaned.groupby("STATION_ID").apply(lambda grp: grp["NO2"].isnull().sum())
# df_measurements_grouped = df_measurements.groupby("STATION_ID")
# df_measurements.groupby("STATION_ID").apply(
#     lambda grp: print("Station: " + str(grp.name) +
#     ": Count Nan: " + str(grp["NO2"].isnull().sum()) +
#     " --- Count all vals: " + str(grp["NO2"].count()))
#     )

# %%
#
df_tresholdFilter = df_measurements.groupby("STATION_ID").filter(
    lambda grp: grp["NO2"].isnull().sum() / grp["NO2"].count() > 0.05
)
df_tresholdCleaned = df_measurements.drop(df_tresholdFilter.index)
df_tresholdCleaned.shape


# %% [markdown]
# #### d)  LÖSUNG JAN: Entfernen Sie die Daten zu allen Stationen, die nicht für mindestens 95% der Messzeitpunkute im Auswertezeitraum einen gültigen Messwert enthielten
#%%
symbols_original = df_measurements.groupby("STATION_ID")

df_measurements.groupby("STATION_ID").apply(lambda x: print(
    "NO2 isnull count :" + str(symbols_original.get_group(x)["NO2"].isnull().count()) + " NO2 Count: " + str(x["NO2"].count())))

#df_measurements.groupby("STATION_ID").apply(lambda x: print("NO2 isnull count :" + str(x["NO2"].isnull()).sum() + " NO2 Count: " + str(x["NO2"].count())))
#%%
# symbols_original = df_measurements.groupby("STATION_ID")
# symbols_new = df_RemovedMeasurements.groupby("STATION_ID")
# for id in symbols_original.groups:
#     print(str(id))
#     amount_of_data_points = symbols_original.get_group(id)['STATION_ID'].count()
#     try:
#         amount_of_missing_no2_datapoints = symbols_new.get_group(id)['NO2'].count()
#     except KeyError:
#         print("deleted " + str(amount_of_data_points) + " in " + str(id))
#         df_measurements=df_measurements.drop(df_measurements[df_measurements["STATION_ID"]==id].index)
#     if((amount_of_missing_no2_datapoints/amount_of_data_points)<0.95):
#         print("Removed " + str(amount_of_missing_no2_datapoints) +" from station " + str(id) +". Original data points: " + str(amount_of_data_points))
#         df_measurements=df_measurements.drop(df_measurements[df_measurements["STATION_ID"]==id].index)
#df_measurements.drop(symbols_original.get_group(id).index, inplace=True)


# %% [markdown]
# #### e)  Für wie viele Stationen enthält der DataFrame data_no2 nun noch Daten?
# %%
len(df_tresholdCleaned["STATION_ID"].unique())
# %% [markdown]
# #### f)  Zu welchen der bayerischen Stationen enthält er keine Daten (mehr)? Geben Sie deren IDs und Namen aus.
# %%
stations_BY.loc[df_tresholdFilter["STATION_ID"].unique()][["Name"]]
# Todo e) und f) funktionieren nur so, wenn man df_tresholdFilter verwenden date_from


#%% 
#TODO Schreibt Daten in temp für aufgabe 3

df_measurements_write_1 = df_measurements[:802284]
df_measurements_write_2 = df_measurements[802284:]
with pd.ExcelWriter("Temp_für_3.xlsx")as writer:
    df_measurements_write_1.to_excel(writer, sheet_name="NO2_Measurements_1")
    df_measurements_write_2.to_excel(writer, sheet_name="NO2_Measurements_2")
