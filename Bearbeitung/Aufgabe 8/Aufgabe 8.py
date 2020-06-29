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
# 1. Diagramme für Alle 5 Schadstoffe über Zeit (Täglich), im Vergleich zum 4 Jahres Druchschnitt der einzelnen Schadstoffe.
# #### Art der Daten
# Dataframe mit Allen Schadstoffstypen zu den entsprechenden Stationstypen und Zeitstempel.

# #### Hypothesen
# 1.

# #### Beobachtungen
# 1. Keine CO Daten für den Zeitraum 2015-2020
# 2. PM10 Daten erste ab Ende März 2019
# 3. SO2 Daten nur bis Juni 2018
# 4. NO2 2020 ist niedriger als die Druchschnittskurve der letzten 4 Jahre
# 5. Groß Abfall der NO2 Kurve von 2020 sind mit Ausgansprerre und großen Infektionsevents scheinbar korreliert


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

df_all_components.count()
df_all_components_by.count()
# Wie man sieht sind für CO deutschlandweit keine Daten vorhanden. Ebenfalls zu erkennen ist der unvollständige Datensatz von PM10 und SO2 in Bayer über den Erhebungszeitraum.
# %%
# df_all_components_by.to_csv('all_components_by.csv')
# df_all_components.to_csv('SO2_CO.csv')
# %%
df_all_components_by = pd.read_csv('all_components_by.csv', parse_dates=[1])
df_all_components_by.set_index(['STATION_ID', 'DT'], inplace=True)
# %%
# df_all_components = pd.read_csv('SO2_CO.csv', parse_dates=[1])
# df_all_components.set_index(['STATION_ID', 'DT'], inplace=True)
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
    stations_BY["Type"], how="left", left_on="STATION_ID", right_index=True)
# %%
# df_all_components_by.set_index('Type',append=True, inplace=True)
df_all_components_by['Type'] = df_all_components_by['Type'].astype(str)
df_all_components_by.dtypes

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
df_all_components_by[["PM10", "CO", "O3", "SO2", "NO2"]] = df_all_components_by[["PM10", "CO", "O3", "SO2", "NO2"]].groupby(
    level="DT", by=[lambda dt: dt.year, lambda dt: dt.month, lambda dt: dt.day]).mean()
# df_plot_data.rename_axis(['Year', 'Month', 'Day'], inplace=True)

# df_all_components_by["Type"].mean(numeric_only = False)

# df_plot_data
# %%
df_all_components_by.groupby(level="DT", by=[
                             lambda dt: dt.year, lambda dt: dt.month, lambda dt: dt.day]).mean()
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
fig = make_subplots(rows=4, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.05,
                    subplot_titles=("Particulate matter",
                                    "Ozone", "Sulphur dioxide", "Nitrogen dioxide")
                    )

# DATA
# 1. plot PM10
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["PM10"],
        name="Year 2020",
        line=dict(color='orange'),
        legendgroup="Year 2020",

    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day["PM10"],
        legendgroup="Mean of years 2016-2019",
        name="Mean of years 2016-2019",
        line=dict(color='cyan')

    ),
    row=1, col=1
)

# # 2. plot CO
# fig.add_trace(
#     go.Scatter(
#         x=x_axis_data,
#         y=df_halfyears_2020["CO"],
#         name="Year 2020",
#         line=dict(color='orange'),
#         legendgroup="Year 2020",
#         showlegend=False
#     ),
#     row=2, col=1
# )
# fig.add_trace(
#     go.Scatter(
#         x=x_axis_data,
#         y=df_halfyears_before_2020_mean_per_day["CO"],
#         legendgroup="Mean of years 2016-2019",
#         name="Mean of years 2016-2019",
#         line=dict(color='cyan'),
#         showlegend=False
#     ),
#     row=2, col=1
# )

# 3. plot O3
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["O3"],
        name="Year 2020",
        line=dict(color='orange'),
        legendgroup="Year 2020",
        showlegend=False
    ),
    row=2, col=1
)
# 3. plot O3
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day["O3"],
        legendgroup="Mean of years 2016-2019",
        name="Mean of years 2016-2019",
        line=dict(color='cyan'),
        showlegend=False

    ),
    row=2, col=1
)

# 4. plot SO2
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["SO2"],
        name="Year 2020",
        line=dict(color='orange'),
        legendgroup="Year 2020",
        showlegend=False

    ),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day["SO2"],
        legendgroup="Mean of years 2016-2019",
        name="Mean of years 2016-2019",
        line=dict(color='cyan'),
        showlegend=False
    ),
    row=3, col=1
)

# 5. plot NO2
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_2020["NO2"],
        name="Year 2020",
        line=dict(color='orange'),
        legendgroup="Year 2020",
        showlegend=False
    ),
    row=4, col=1
)
fig.add_trace(
    go.Scatter(
        x=x_axis_data,
        y=df_halfyears_before_2020_mean_per_day['NO2'],
        legendgroup="Mean of years 2016-2019",
        name="Mean of years 2016-2019",
        line=dict(color='cyan'),
        showlegend=False
    ),
    row=4, col=1
)


fig.update_xaxes(title_text="Time", tickangle=45, row=5, col=1)

# Update yaxis properties
# range=[40, 80] is a usable attribute
fig.update_yaxes(title_text="PM10 [µg/m³]", row=1, col=1)
fig.update_yaxes(title_text="O3 [µg/m³]", row=2, col=1)
fig.update_yaxes(title_text="SO2 [µg/m³]", row=3, col=1)
fig.update_yaxes(title_text="NO2 [µg/m³]", range=[0, 55], row=4, col=1)

fig.update_layout(
    title_text="Component measurements of fist halfyears",
    template="plotly_dark",
    width=800,
    height=800
    # legend_orientation="h",
    # margin=dict(r=0, t=0, b=40, l=0)
    # annotations=[
    #     go.layout.Annotation(
    #         text="Source: NOAA",
    #         showarrow=False,
    #         xref="paper",
    #         yref="paper",
    #         x=0,
    #         y=0)
    # ]
    # legend=dict(
    #     x=0,
    #     y=1,
    #     traceorder="normal",
    #     font=dict(
    #         family="sans-serif",
    #         size=12,
    #         color="white"
    #     )
    # )
)
fig.show()


# %%
