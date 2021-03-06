# from ipywidgets import widgets
# %%
import ipywidgets as widgets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
# %%
# # TODO Import aus Datei bei zusammenfügen entfernen
# xls = pd.ExcelFile("Temp_für_3.xlsx")
# df1 = pd.read_excel(xls, 'NO2_Measurements_1', index_col='dp_id')
# # df2 = pd.read_excel(xls, 'NO2_Measurements_2', index_col='dp_id')
# df_measurements = df1  # .append(df2)
# df_stations = pd.read_excel("Stations_BY.xlsx", index_col='ID')

# %% [markdown]
# ### Aufgabe 6  (Interaktives Diagramm)
# %% [markdown]
# #### a)  Erzeugen Sie ein interaktives Säulendiagramm inPlotly, in welchem die Mittelwerte derNO2-Konzentrationen im Tagesverlauf ̈uber die (vollen) Stunden aufgetragen werden. Ver-wenden Sie als Datengrundlage die Messwerte der bayerischen Stationen aus dem DataFra-meno2_data. Das Diagramm soll zwei Radio-Buttons enthalten. ̈Uber den ersten Radio-Button kann der Stations-Typ gefiltert werden (Auswahlm ̈oglichkeitenall,backgroundundtraffic), ̈uber den zweiten Radio-Button kann der Wochentag eingeschr ̈ankt werden(Auswahlm ̈oglichkeitenAll,Monday, ...,Sunday)
# %% [markdown]

# %%
df_merge = df_measurements.merge(
    df_stations[['Type']], how='left', left_on='STATION_ID', right_index=True)
# %%
df_data = df_merge.groupby(
    [
        df_merge['Type'],
        df_merge['DT'].dt.strftime('%A'),
        df_merge['DT'].dt.strftime('%X'),
    ]
).mean()[['NO2']]


df_data.rename_axis(['Type', 'Weekday', 'Hour'], inplace=True)
df_data

# %%
# Todo Stunde 24 ist nicht Stunde 0, Evtl auf 24 manuell mappen

data = [go.Bar(
    x=df_data.index.get_level_values('Hour').unique(),
    y=df_data['NO2'],
)]

layout = go.Layout(
    title=go.layout.Title(
        text='Daily chart of mean NO2 measurements of bavarian stations',
        font=dict(
            size=24,
            color='#4863c7'
        )
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Hour',
            font=dict(
                size=18,
                color='green'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='NO2',
            font=dict(
                size=18,
                color='green'
            )
        ),
        range=[0, 45]
    ),
    hovermode='closest'
)

fig = go.FigureWidget(data=data, layout=layout)

radio_type = widgets.RadioButtons(
    options=list(df_data.index.get_level_values('Type').unique()) + ['all'],
    description='Type of Stations'
)
radio_day = widgets.RadioButtons(
    options=list(df_data.index.get_level_values('Weekday').unique()) + ['All'],
    description='Days of Weeks'
)


def update_graph(change):
    chosen_type = radio_type.value
    chosen_day = radio_day.value
    if chosen_type == 'all' and chosen_day == 'All':
        df_diagramm = df_data.unstack().mean()
    elif chosen_type == 'all':
        df_diagramm = df_data.iloc[df_data.index.isin(
            [chosen_day], level='Weekday')].unstack().mean()
    elif chosen_day == 'All':
        df_diagramm = df_data.loc[chosen_type]
    else:
        df_diagramm = df_data.loc[chosen_type, chosen_day]

    with fig.batch_update():
        fig.layout.xaxis.autorange = False
        fig.layout.yaxis.autorange = False
        fig.data[0].y = df_diagramm['NO2']
        fig.data[0].text = df_diagramm['NO2']

# TODO Cleanup Text


# Verknüpfung der Callback-Funktion mit dem Widget
radio_type.observe(update_graph, names='value')
radio_day.observe(update_graph, names='value')

radio_buttons = widgets.HBox([radio_type, radio_day])
final_fig = widgets.VBox([fig, radio_buttons])

final_fig

# %% [markdown]
# #### b)
# Theorien:
# 1. Freitag abends und Montag morgens bei allen Typen höherer Ausstoß
# 2. Jeden Wochentag zwischen 6 und 9 und 17 - 21 Uhr
# 3. Traffic Stationen haben einen grundsätzlich einen höheren Durchschnittswert als Background Stationen
#
# Fakten:
# 1. Montag morgen ist kein erhöhter Ausstoß zu erkennen
# 2. Theorie 2 stimmt: Arbeitsverkehr ist bei allen Typen zu erkennen/Rush-Hour
# 3. Theorie 3 stimmt: Dies ist deutlich zu erkennen -> erhöhter Verkehr in städtischen Regionen

# 4. Freitag auffällig erhöhte Messwerte in den Abendstunden
# 5. Von Montag bis Freitag steigen kontinuierlich die gemessenen NO2-Mittelwerte in den Abendstunden

# -> Allein anhand den visualisierten Daten ist, kann man stark von einem Zusammenhang des Verkehrsaufkommens und der gemessenen NO2-Konzentration ausgehen.
# In der Tat ist das NO2 Vorkommen fast vollständig auf anthropogenen Quellen in Form von Verbrennungsemissionen zurückzuführen.
# Ein großteil davon ist dem Straßenverkehr zuzuschreiben (vgl. [1]).
