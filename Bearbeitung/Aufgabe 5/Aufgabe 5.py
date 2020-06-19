# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px

# %%
# TODO Import aus Datei bei zusammenfügen entfernen
xls = pd.ExcelFile("Temp_für_3.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1.append(df2)
# %%

fig = px.histogram(
    df_measurements["NO2"])
fig.show()
# %% [markdown]
# #### a) Erstellen Sie ein Histogramm über alle gemessenen NO2-Konzentrationen im Auswertungszeitraum 2016-2019.

trace = go.Histogram(
    x=df_measurements["NO2"],
    marker=dict(
        line=dict(
            width=1.5,
        )
    ),
    histnorm='density'
)

layout = go.Layout(
    title=go.layout.Title(
        text='NO2 Konzentration Häufigkeiten',
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Konzentration',
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Häufigkeit',
        )
    )
)

data = [trace]

fig = go.Figure(data=data, layout=layout)
fig.show()

# %% [markdown]
# #### b)  Stellen  Sie  den  jahreszeitlichen  Verlauf  der  gemessenen  NO2-Konzentrationen  in  einemgeeigneten Diagramm dar. Was ist zu beobachten und wie kann dies erkl ̈art werden?
# %%
SEASONS = np.array(['Winter', 'Spring', 'Summer', 'Autumn'])
month = np.arange(12) + 1
season = SEASONS[(month // 3) % 4]


def month_to_season(month_int):
    return season[month_int - 1]


# %%
df_measurements["Season"] = df_measurements["DT"].map(
    lambda dt: month_to_season(dt.month))

# %%
# df_measurements.groupby(month_to_season(df_measurements["DT"].dt.month)).mean()[["NO2"]]

df_mean_per_season = df_measurements.groupby(
    [
        df_measurements["DT"].dt.year,
        month_to_season(df_measurements["DT"].dt.month)
    ]
).mean()[["NO2"]]

# %%
# df_mean_per_season.unstack().plot(kind="line")
# df_mean_per_season.unstack().plot(kind="bar")
#df_mean_per_season.iloc[range(0, 16)]["NO2"]
#df_mean_per_season.loc[2016, "Spring"]
# df_mean_per_season.iloc[df_mean_per_season.index.isin(
#   ["Spring"], level=1)].index
#df_mean_per_season.unstack().loc[:, (slice(None), 'Spring')]
df_mean_per_season.index.get_level_values(level=0).unique()
# %%


# %% [markdown]
# #### c) Visualisieren Sie in einem geeigneten Diagramm den Zeitverlauf der Tagesmittel der ge-messenen NO2-Konzentrationen im Beobachtungszeitraum. Lassen sich Trends erkennen?
# %%
df_mean_per_day = df_measurements.groupby(
    df_measurements["DT"].dt.date).agg({"NO2": "mean"})
# %%
fig = px.line(
    df_mean_per_day,
    x=df_mean_per_day.index,
    y=df_mean_per_day["NO2"],
    title='Mean NO2 per day')
fig.show()


# %%
