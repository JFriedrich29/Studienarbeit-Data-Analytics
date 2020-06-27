# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import plotly.graph_objects as go
import requests
import importlib
import API_Access as api

# %%
importlib.reload(api)

# %% [markdonw]
# #### Graphische Analyse der Daten
# 1. Diagramm Alle 5 Schadstoffe über Zeit (Täglich). Radoi Buttons für StationsTypen und Filter für Schadstoffstypen
# 2. Diagramm Vergleich des Schadstoffes mit dem Durchschnitt der Vorjahre (5. Vorjahre), Schadstoff über Radio Button änderbar
# #### Art der Daten
# Dataframe mit Allen Schadstoffstypen zu den entsprechenden Stationstypen und Zeitstempel, eventluell ein Binärencoding von dem Lockdownstatus

# #### Hypothesen
# 1.

# %%
# TODO Auslesen von Chache entfernen
stations_BY = pd.read_excel(
    "Stations_BY.xlsx", index_col=0)

# %%
date_from = "2020-01-01"
date_to = "2020-01-01"

df_all_components = pd.DataFrame()
for station_id in stations_BY.index:
    station_data = api.GetMeasurements_MeanPerHour_MultiComponents(
        station_id=str(station_id),
        components=["PM10", "CO", "O3", "SO2", "NO2"],
        date_from=date_from,
        date_to=date_to)
    station_data["STATION_ID"] = station_id
    station_data = station_data.set_index("STATION_ID", append=True).swaplevel()

    df_all_components = pd.concat([df_all_components, station_data])

df_all_components.count()
# %%
# TODO Use Get data for single component in earlier tasks
station_data = api.GetMeasurements_MeanPerHour_MultiComponents(
    station_id="509",
    components=["PM10", "CO", "O3", "SO2", "NO2"],
    date_from="2016-01-01",
    date_to="2016-01-03")

station_data
# %%
