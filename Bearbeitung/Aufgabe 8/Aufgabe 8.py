# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# #### Beobachtungen
# 1. Keine CO Daten für den Zeitraum 2015-2020
# 2. PM10 Daten erste ab Ende März 2019
# 3. SO2 Daten nur bis Juni 2018
# 4. NO2 2020 ist niedriger als die Druchschnittskurve der letzten 4 Jahre
# 5. Groß Abfall der NO2 Kurve von 2020 sind mit Ausgansprerre und großen Infektionsevents scheinbar korreliert


# #### Hypothesen
# 1.

# %%
# TODO Auslesen von Chache entfernen
stations_BY = pd.read_excel(
    "Stations_BY.xlsx", index_col=0)
# %%
stations_ALL = pd.read_excel(
    "Stations.xlsx", index_col=0)

# %%
date_from = "2016-01-01"
# TODO Auf 30.06 setzen und nochmal abfragen (ganzer monat)
date_to = "2020-06-28"

# Deutsche Stationen
df_all_components = pd.DataFrame()
for station_id in stations_ALL.index:
    station_data = api.GetMeasurements_MeanPerHour_MultiComponents(
        station_id=str(station_id),
        components=["CO", "SO2"],
        date_from=date_from,
        date_to=date_to)
    station_data["STATION_ID"] = station_id
    station_data = station_data.set_index(
        "STATION_ID", append=True).swaplevel()
    print("Station " + str(station_id) + " done")

    df_all_components = pd.concat([df_all_components, station_data])

df_all_components.count()

# %%
# bayrische Stationen
df_all_components_by = pd.DataFrame()
for station_id in stations_BY.index:
    station_data = api.GetMeasurements_MeanPerHour_MultiComponents(
        station_id=str(station_id),
        components=["CO", "SO2"],
        date_from=date_from,
        date_to=date_to)
    station_data["STATION_ID"] = station_id
    station_data = station_data.set_index(
        "STATION_ID", append=True).swaplevel()
    print("Station " + str(station_id) + " done")

    df_all_components_by = pd.concat([df_all_components_by, station_data])

df_all_components_by.count()
# %%
df_all_components_by.to_csv('all_components_by.csv')
df_all_components.to_csv('SO2_CO.csv')
# %%
df_all_components_by = pd.read_csv('all_components_by.csv', parse_dates=[1])
df_all_components_by.set_index(['STATION_ID', 'DT'], inplace=True)

df_all_components = pd.read_csv('SO2_CO.csv', parse_dates=[1])
df_all_components.set_index(['STATION_ID', 'DT'], inplace=True)
# %%
# TODO Use Get data for single component in earlier tasks
station_data = api.GetMeasurements_MeanPerHour_SingleComponent(
    station_id="509",
    component="NO2",
    date_from="2016-01-01",
    date_to="2016-01-03")

station_data
# %%
# Add Type of station
df_all_components_by = df_all_components_by.merge(
    stations_BY[["Type"]], how="left", left_on="STATION_ID", right_index=True)

# %%
# df_all_components_by.groupby(
#     level="DT"
#     df_all_components_by.index.get_level_values('DT').dt.date
#     df_all_components_by["DT"].date
# ).mean()
# %%
# df_plot_data = df_all_components_by.groupby(
#     [
#         df_all_components["DT"].dt.month,
#         df_all_components["DT"].dt.date
#     ]
# ).mean()

# %%
df_plot_data = df_all_components_by.groupby(
    level="DT", by=[lambda dt: dt.year, lambda dt: dt.month, lambda dt: dt.day]).mean()
df_plot_data.rename_axis(['Year', 'Month', 'Day'], inplace=True)
df_plot_data
# %%
# Only select values of the first half year of each year
df_halfyears = df_plot_data.loc[(
    df_plot_data.index.get_level_values(level='Month') <= 6)]
df_halfyears
# %%
# Get data
df_halfyears_before_2020_mean_per_day = df_halfyears.loc[
    (df_halfyears.index.get_level_values(level='Year') <= 2019) &
    (df_halfyears.index.get_level_values(level='Year') >= 2016)
].groupby(["Month", "Day"]).mean()

df_halfyears_2020 = df_halfyears.loc[df_halfyears.index.get_level_values(
    level='Year') == 2020]

# %%
# Calculate x axes value
start_time = pd.to_datetime("2020-01-01",
                            infer_datetime_format=True)
end_time = pd.to_datetime("2020-06-28",
                          infer_datetime_format=True)
x_axis_data = pd.date_range(start_time, end_time, freq='d').to_list()
# %%
fig = make_subplots(rows=5, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.05,
                    subplot_titles=("Particulate matter", "Carbon monoxide",
                                    "Ozone", "Sulphur dioxide", "Nitrogen dioxide")
                    )

# x_axis_data = df_plot_data.index.get_level_values(
#     'DT').tolist()

# DATA
# 1. plot PM10
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["PM10"],
        name="PM10 2020",
        color=orange
    ),
    row=1, col=1
)

# 2. plot CO
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["CO"],
        name="CO 2020",
        color=cyan
    ),
    row=2, col=1
)

# 3. plot O3
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["O3"],
        name="O3 2020",
        color=orange
    ),
    row=3, col=1
)

# 4. plot SO2
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["SO2"],
        name="SO2 2020",
        color=cyan
    ),
    row=4, col=1
)

# 5. plot NO2
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["NO2"],
        name="NO2 2020",
        color=orange
    ),
    row=5, col=1
)

# 1. plot PM10
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day["PM10"],
        name="PM10 Average",
        color=cyan
    ),
    row=1, col=1
)

# 2. plot CO
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day["CO"],
        name="CO Average",
        color=orange
    ),
    row=2, col=1
)

# 3. plot O3
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day["O3"],
        name="O3 Average",
        color=cyan
    ),
    row=3, col=1
)

# 4. plot SO2
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day["SO2"],
        name="SO2 Average",
        color=orange
    ),
    row=4, col=1
)

# 5. plot NO2
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day["NO2"],
        name="NO2 Average",
        color=cyan
    ),
    row=5, col=1
)


fig.update_layout(
    title_text="Component measurements since start of year 2020",
    height=1000,
    width=800
)

# LAYOUT
# x_layout = go.Layout(
#     xaxis=go.layout.XAxis(
#         title=go.layout.xaxis.Title(
#             text='Time in Hours',
#             font=dict(
#                 size=18,
#                 color='green'
#             )
#         )
#     )
# )


fig.update_xaxes(title_text="Time", tickangle=45, row=5, col=1)

# Update yaxis properties
# range=[40, 80] is a usable attribute
fig.update_yaxes(title_text="PM10 [µg/m³]", row=1, col=1)
fig.update_yaxes(title_text="CO [mg/m³]", row=2, col=1)
fig.update_yaxes(title_text="O3 [µg/m³]", row=3, col=1)
fig.update_yaxes(title_text="SO2 [µg/m³]", row=4, col=1)
fig.update_yaxes(title_text="NO2 [µg/m³]", row=5, col=1)

fig.update_layout(
    template="plotly_dark"
    # margin=dict(r=10, t=50, b=40, l=60)
    # annotations=[
    #     go.layout.Annotation(
    #         text="Source: NOAA",
    #         showarrow=False,
    #         xref="paper",
    #         yref="paper",
    #         x=0,
    #         y=0)
    # ]
)

fig.show()


# %%
