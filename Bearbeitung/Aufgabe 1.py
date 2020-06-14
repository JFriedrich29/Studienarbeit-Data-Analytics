# %%
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import json

# %% [markdown]
# ### Aufgabe 1 (Messstationen, Datenakquise, Semistrukturierte Daten, Geovisualisierung)
# %% [markdown]
# #### a)
# %%
response = requests.get('https://www.umweltbundesamt.de/api/air_data/v2/meta/json',
                        params={'use': 'measure', 'date_from': '2020-01-01'})
print(response.status_code)

json_data = json.loads(response.text)


# %%

def printjson(json):
    print(json.dumps(json, indent=3))


# %% [markdown]
# ##### Meta Data in Python Object (dictionary) format since 01.01.2020
# %%
stations_dict = json_data['stations']
components_dict = json_data['components']
scopes_dict = json_data['scopes']
xref_dict = json_data['xref']
networks_dict = json_data['networks']
networks_dict = json_data['networks']
limits_dict = json_data['limits']

# %% [markdown]
# ##### Parse into custom column names
# %%
df_stations = pd.DataFrame.from_dict(stations_dict,
                                     orient="index",
                                     columns=["ID", "Code", "Name", "Location", "x2", "Construction_Date", "Deconstruction_Date", "Longtitude", "Latitude",
                                              "Network_ID", "Settings_ID", "Type_ID", "Network_Code", "Network_Name", "Settings_Long",
                                              "Seeings_Short", "Type", "Street_Name", "Street_Number", "x6"],
                                     )
df_stations.head(10)

# %%

df_stations.set_index('ID', inplace=True)
df_stations
# %%
# df_stations.shape
# df_stations[["Code"]]
# df_stations.head()
# %% [markdown]
# ##### Export to excel
df_stations.to_excel("Stations.xlsx")



# %%
stations_BY = df_stations[df_stations['Network_ID'] == "2"]
stations_BY.to_excel("Stations_BY.xlsx")
# %%
