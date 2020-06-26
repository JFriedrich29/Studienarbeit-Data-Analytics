# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import plotly.graph_objs as go
import sklearn.linear_model as sk
import sklearn.model_selection as sm


# %% [markdown]
# ### Aufgabe 7

# %% [markdown]
# #### a) Laden Sie sich die Wetterdaten aus der Dateiwetterdaten.csvin einen DataFrame na-mensdf_weather. Dieser enth ̈alt historische Wetterdaten f ̈ur die Oberpfalz f ̈ur die Jah-re 2016-2019. F ̈ur unsere Analyse ist die SpaltetemperatureMaxrelevant, die die Ta-gesh ̈ochsttemperaturen in Grad Fahrenheit beinhaltet.
df_weather = pd.read_csv('wetterdaten.csv')
# %%
# Convert to datetime
df_weather['date'] = pd.to_datetime(df_weather['date'])

# %% [markdown]
# #### b) Wandeln Sie die Temperaturwerte in Grad Celsius um.
df_weather['temperatureMax'] = df_weather['temperatureMax'].apply(
    lambda x: ((x-32)*(5/9)))

# %% [markdown]
# #### c) Laden Sie ̈uber die Measurements-API f ̈ur die Station in der Nikolaistraße in Weiden dieEin-Stunden-Mittelwerte f ̈ur die Ozon-Konzentrationen f ̈ur den Zeitraum 01.01.2016 bis31.12.2019 herunter und ̈uberf ̈uhren Sie diese in einen DataFrame namensdata_o3. Diesersoll die SpaltenDTundO3besitzen, die das Messdatum mit Uhrzeit (Beginn der Stunde, ̈uber die gemittelt wird) und die gemessene O3-Konzentration enthalten.
# %%
# TODO Id wird in Aufgabe 3 berechnet
id_nikolaistraße = 509

# %%
response = requests.get('https://www.umweltbundesamt.de/api/air_data/v2/measures/json',
                        params={'use': 'measure', 'date_from': '2016-01-01', 'date_to': '2019-12-31', 'time_to': '24', 'time_from': '1', 'scope': '2', 'component': '3', 'station': id_nikolaistraße})
print(response.status_code)

json_data = json.loads(response.text)

# %%
data_o3_dict = dict(json_data['data']["509"])


# %%
data_o3_dict

# %%
data_o3 = pd.DataFrame.from_dict(
    data_o3_dict, orient="index", columns=["component id", "scope id", "O3", "date end", "index"])
# %%
data_o3 = data_o3.replace(to_replace='24:00:00', value="00:00:00", regex=True)
data_o3.head()

# %%
data_o3.index = pd.to_datetime(data_o3.index)

# %%
data_o3.drop(['component id', 'scope id', 'date end',
              'index'], inplace=True, axis=1)
# %%
data_o3.index.rename("DT")

# %%
data_o3.to_csv('data_o3.csv')

# %% [markdown]
# #### d) Aggregieren Sie die Messwerte, indem Sie die O3-Maximalkonzentrationen pro Tag ermit-teln und diese in einen DataFrame namenso3_data_maxspeichern.
o3_data_max = data_o3.groupby(data_o3.index.date).max()
# %% [markdown]
# #### e) Stellen Sie den zeitlichen Verlauf der aggregierten Tageswerte f ̈ur die Jahre 2016-2019 gra-fisch dar und beschreiben Sie die beobachteten Trends.
trace = go.Scattergl(
    x=o3_data_max.index,
    y=o3_data_max['O3'],
    mode='lines',
    text='Daily O3 Concentration'
)

layout = go.Layout(
    title=go.layout.Title(
        text='Daily chart of mean ozone measurements',
        font=dict(
            size=24,
            color='#4863c7'
        )
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Day',
            font=dict(
                size=18,
                color='green'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Ozone',
            font=dict(
                size=18,
                color='green'
            )
        ),
    ),
    hovermode='closest'
)

data = [trace]
fig = go.Figure(data=data, layout=layout)
fig.show()

# %%
df_weather.set_index('date', inplace=True)
# %% [markdown]
# #### f) Erstellen Sie ein Streudiagramm, in dem die Maximalkonzentration(y-Achse) und die Ma-ximaltemperatur(x-Achse) der einzelnen Tage f ̈ur die Jahre 2016-2019 gegeneinander auf-tragen sind. Beschreiben und erkl ̈aren Sie den beobachteten Zusammenhang
df_max_temp_o3 = o3_data_max.merge(
    df_weather['temperatureMax'],
    how='outer',
    left_index=True,
    right_index=True,
)

df_max_temp_o3


# %%

trace = go.Scattergl(
    x=df_max_temp_o3['temperatureMax'],
    y=df_max_temp_o3['O3'],
    mode='markers',
    marker=dict(
        size=6,
    ),
    text=df_max_temp_o3.index.date
)

layout = go.Layout(
    title=go.layout.Title(
        text='Daily maximum values of ozone and temperature',
        font=dict(
            size=22,
            color='#4863c7'
        )
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Temperature',
            font=dict(
                size=18,
                color='green'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Ozone',
            font=dict(
                size=18,
                color='green'
            )
        ),
    ),
    hovermode='closest'
)

data = [trace]
fig = go.Figure(data=data, layout=layout)
fig.show()

# %%


# Unter 12 Grad gibt es keinen Ozone Konzentration über 100
# Mit höheren Temperaturen ist der Ozone Wert höher (mehr radikale aus O2 durch höhere sonneneinstrahlung, dominiert durch neigung der erdachse bzgl der sonne [2])
# => Es lässt sich ein linearer Zusammenhang zwischen der Ozone Konzentration und der vorhandenen Temperatur vermuten

# %% [markdown]
# g) #### Ermitteln Sie anhand der Tageswerte den empirischen Korrelationskoeffizienten zwischender Maximalkonzentration und der Maximaltemperatur.
# %%
np.corrcoef(df_max_temp_o3["O3"], df_max_temp_o3['temperatureMax'])[0][1]

# %%
# corr_matrix = df_max_temp_o3.corr()
# trace = go.Heatmap(corr_matrix,
#                    colorscale='Viridis')
# data = [trace]
# fig = go.Figure(data=data)
# fig.show()


# %%
x = df_max_temp_o3['temperatureMax'].values
y = df_max_temp_o3['O3'].values
# %%
y.shape

# %%
model = sk.LinearRegression()
model.fit(x.reshape(-1, 1), y)

# %%
modelline = go.Scattergl(
    x=x,
    y=model.predict(x.reshape(-1, 1)),
    name="Linear Regression",
    line=dict(
        color="red"
    )
)

fig.add_trace(modelline)
fig.show()


# %%
