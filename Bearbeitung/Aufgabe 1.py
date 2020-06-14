# %%
import folium.plugins
import folium
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
                                              "Settings_Short", "Type", "Street_Name", "Street_Number", "x6"],
                                     )
df_stations.head(10)

# %%

df_stations.set_index('ID', inplace=True)
df_stations
# %%
# df_stations.shape
# df_stations[["Code"]]
# df_stations.head()

# %%
# Convert to numeric
conv_to_int_cols = ["Longtitude", "Latitude", "Network_ID", "Settings_ID",
                    "Type_ID"]
df_stations[conv_to_int_cols] = df_stations[conv_to_int_cols].apply(
    pd.to_numeric, errors='coerce', axis=1)

# Convert to datetime
conv_to_date_cols = ["Construction_Date", "Deconstruction_Date"]
df_stations[conv_to_date_cols] = df_stations[conv_to_date_cols].apply(
    pd.to_datetime, errors='coerce', axis=1)


df_stations.dtypes
# %% [markdown]
# ##### Export to excel
# df_stations.to_excel("stations_2020.csv") #TODO Auskommentieren für Abgabe
# df_stations.to_excel("stations.xlsx")  # TODO Delete line #TODO Auskommentieren für Abgabe

# %% [markdown]
# #### b) Wie viele Messstationen sind derzeit bundesweit in Betrieb?
# When Deconstruction_Date is null, then station is still active
len(df_stations.loc[df_stations["Deconstruction_Date"].isnull()])

# %% [markdown]
# #### c) Visualisieren Sie mit Hilfe eines Kreisdiagramms, wie sich die Stationen hinsichtlich ihresTyps zusammensetzen.
# %%
df_stations['Type'].value_counts().plot.pie(figsize=(
    6, 6), title="Station Types", legend=True)  # TODO Schöneres Diagramm verwenden

# %% [markdown]
# #### d)  Erstellen Sie mit folium eine interaktive Karte, auf der die einzelnen Messstationen als Kreise eingezeichnet sind. Industrienahe Stationen sollen gelb, verkehrsnahe rot und die Stationen mit Hintergrundbelastung grün eingezeichnet werden. Beim Klick auf die Kreisesollen die Namen der Stationen angezeigt werden.
# %%
colors = {"industry": "yellow", "traffic": "red", "background": "green"}

m = folium.Map(
    location=[50.86, 12.96],
    zoom_start=13,
)
# TODO Umlaute bei Namen werden nicht richtig gerendert
for i in range(len(df_stations)):
    folium.Circle(
        location=df_stations[['Latitude', 'Longtitude']].iloc[i],
        popup=df_stations['Name'].iloc[i],
        radius=30,
        color=colors[df_stations['Type'].iloc[i]]
    ).add_to(m)

m

# %% [markdown]
# #### e)  Erzeugen Sie durch Filterung des DataFramesstationseinen DataFramestations_BY, der die Informationen zu allen Messstationen in Bayern enthält.
# %%
# stations_BY = df_stations[df_stations['Network_ID'] == "2"]
stations_BY = df_stations[df_stations['Network_Name'] == "Bavaria"]
# stations_BY.to_excel("Stations_BY.xlsx") #TODO Auskommentieren für Abgabe
# %%
