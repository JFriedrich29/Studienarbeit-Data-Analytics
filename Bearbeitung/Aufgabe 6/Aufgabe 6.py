# %%
from ipywidgets import widgets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
# %%
# TODO Import aus Datei bei zusammenfügen entfernen
xls = pd.ExcelFile("Temp_für_3.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
# df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1  # .append(df2)
df_stations = pd.read_excel("Stations_BY.xlsx", index_col="ID")

# %% [markdown]
# ### Aufgabe 6  (Interaktives Diagramm)
# %% [markdown]
# #### a)  Erzeugen Sie ein interaktives S ̈aulendiagramm inPlotly, in welchem die Mittelwerte derNO2-Konzentrationen im Tagesverlauf ̈uber die (vollen) Stunden aufgetragen werden. Ver-wenden Sie als Datengrundlage die Messwerte der bayerischen Stationen aus dem DataFra-meno2_data. Das Diagramm soll zwei Radio-Buttons enthalten. ̈Uber den ersten Radio-Button kann der Stations-Typ gefiltert werden (Auswahlm ̈oglichkeitenall,backgroundundtraffic), ̈uber den zweiten Radio-Button kann der Wochentag eingeschr ̈ankt werden(Auswahlm ̈oglichkeitenAll,Monday, ...,Sunday)
# %% [markdown]
# TODO Diagramm für 4 Informationen finden, Säule oder Scatter mit Farbe? (Tabelle vom Prof nachschauen)
# Datenpunkte:
# - Tagesstunde (0:00, 1:00, ..., 23:00 Uhr)
# - NO2 Stunden-Mittelwerte
# Filter
# - Wochentag (All, Montag - Sonntag)
# - Typ (all, background, traffic)
# %%
df_merge = df_measurements.merge(
    df_stations[["Type"]], how="left", left_on="STATION_ID", right_index=True)
# %%
df_measurements.groupby(
    [
        df_measurements["Type"],
        df_measurements["DT"].dt.weekday,
        df_measurements["DT"].dt.hour,
    ]
).mean()

# %%
# Todo Vorlage anpassen, zweiten Radio-Button einfügen
df = pd.read_csv("fifa2019_transformed.csv").sample(5000)
df['Dribbling'] = df['Dribbling'].fillna('unbekannt')
trace = go.Scattergl(
    x=df['Dribbling'],
    y=df['Height'],
    mode='markers',
    marker=dict(
        size=10,
        color="grey"
    ),
    text=df["Name"]
)

data = [trace]
layout = go.Layout(
    title=go.layout.Title(
        text='Antrag Körpergröße zur Dribblingstärke',
        font=dict(
            size=24,
            color="#4863c7"
        )
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Dribblingstärke',
            font=dict(
                size=18,
                color='green'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Körpergröße',
            font=dict(
                size=18,
                color='green'
            )
        )
    ),
    hovermode='closest'
)

fig = go.FigureWidget(data=data, layout=layout)

radio = widgets.RadioButtons(options=list(
    df['Position'].unique())+['All'], description='Position')


def update_graph(change):
        if radio.value == 'All':
            df_filtered = df
        else:
            df_filtered = df[df['Position'] == radio.value]

        with fig.batch_update():
            fig.layout.xaxis.autorange = False
            fig.layout.yaxis.autorange = False
            fig.data[0].x = df_filtered['Dribbling']
            fig.data[0].y = df_filtered['Height']
            fig.data[0].text = df_filtered['Name']
            # fig.data[0].marker =


#Verknüpfung der Callback-Funktion mit dem Widget
radio.observe(update_graph, names="value")


final_fig = widgets.HBox([radio, fig])

final_fig

# %%
