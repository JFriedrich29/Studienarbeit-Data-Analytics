#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

#%%
stations_BY = pd.read_excel("Stations_BY.xlsx", index_col=0)
stations_dict = dict()
for id in stations_BY.index:
    response = requests.get("https://www.umweltbundesamt.de/api/air_data/v2/measures/json", params={"date_from":"2016-01-01", "time_from":"1", "date_to":"2019-12-31", "time_to":"24", "station":str(id), "component":"5", "scope":"2"})
    json_data = json.loads(response.text)
    station_dict = json_data['data']
    stations_dict[id] = station_dict


df_stations = pd.DataFrame.from_dict(stations_dict,orient="index",columns=["STATION_ID", "DT", "NO2"],)


# %%
