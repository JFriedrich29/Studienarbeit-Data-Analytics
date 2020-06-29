# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium.plugins
import folium
import requests
import json
import datetime
import plotly.graph_objs as go
import plotly.express as px
import ipywidgets as widgets
import sklearn.linear_model as sk
import sklearn.model_selection as sm
import API_Access as api

# %%
import importlib
importlib.reload(api)

# %% [markdown]
# ### Aufgabe 1 (Messstationen, Datenakquise, Semistrukturierte Daten, Geovisualisierung)
# region
# %% [markdown]
# #### a) Beziehen Sie ̈uber die Metadaten-API des Umweltbundesamts die Daten zu den Messstatio-nen zum Stand 01.01.2020, indem Sie, z.B. unter Verwendung der Bibliothekrequests,einen geeigneten HTTP-Request absetzen. ̈Uberf ̈uhren Sie die erhaltenen (semistrukturier-ten) Daten in einen DataFrame namensstations, der f ̈ur jede Station eine Zeile mit denverf ̈ugbaren Informationen enth ̈alt (z.B. Name, Adresse, Geokoordinaten, Bundesland etc.).Speichern Sie den DataFrame in eine CSV-Datei namensstations_2020.csvund ladenSie diese mit Ihrer Einreichung auf Moodle hoch.
# %% [markdown]
# Zu Beginn wird sich ein Überblick über die API des Umweltbudesamtes verschaffen.
# Die API bietet eine Schnittstelle an, um Meta-Daten aller bundesweiten Messtationen zu erhalten.
# %%
df_stations = api.GetMetaData_Stations_All(date_from="2020-01-01", date_to="2020-01-01")
df_stations

# %% [markdown]
# ##### Export to excel
# df_stations.to_csv("stations_2020.csv") #TODO NOTWENDIG für Abgabe

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
# endregion
# %% [markdown]
# ### Aufgabe 2 (NO2-Daten, Datenvorbereitung, Datenqualität)
# region
# %% [markdown]
# #### a) Laden Sie über die Measurements-API für alle bayerischen Stationen (wie oben ermittelt) die Ein-Stunden-Mittelwerte für die NO2-Konzentrationen für den Zeitraum 01.01.2016 bis 31.12.2019 herunter und überführen Sie diese in einen DataFrame namens data_no2. Dieser soll die Spalten STATION_ID, DT und NO2 besitzen, die die Stations-ID, das Messdatum mit Uhrzeit sowie die gemessene NO2-Konzentration enthalten.
# %%
# TODO Auslesen von Chache entfernen
stations_BY = pd.read_excel(
    "Stations_BY.xlsx", index_col=0)
# stations_BY
# %%
# stations_data_dict = dict()
# for id in stations_BY.index:
#     response = requests.get("https://www.umweltbundesamt.de/api/air_data/v2/measures/json", params={
#                             "date_from": "2016-01-01", "time_from": "1", "date_to": "2019-12-31", "time_to": "24", "station": str(id), "component": "5", "scope": "2"})
#     json_data = json.loads(response.text)
#     stations_data_dict[id] = json_data['data']
#     if(response.status_code==200):
#         print(str(id) + ": Abfrage fertig")
#     else:
#         break

# %% # TODO evtl einfachere Methode finden
# list_to_create = []
# for station_id in stations_data_dict:
#     for station_data in stations_data_dict[station_id]:
#         measurements_for_id = stations_data_dict[station_id][station_data].values()
#         for data_point in measurements_for_id:
#             datetime = data_point[3]
#             no2_value = data_point[2]
#             list_to_create.append([station_id, datetime, no2_value])
# df_measurements = pd.DataFrame(list_to_create,columns=["STATION_ID", "DT", "NO2"])
# df_measurements.index.name='dp_id'
# df_measurements = df_measurements.replace(to_replace='24:00:00', value="00:00:00", regex=True)

# %%
df_data_no2 = pd.DataFrame()
for station_id in stations_BY.index:

    station_data = api.GetMeasurements_MeanPerHour_SingleComponent(
        station_id=str(station_id),
        component=api.ComponentEnum.NO2,
        date_from="2016-01-01",
        date_to="2019-12-31")


    # Add the station id as first index for a unique multiindex
    station_data["STATION_ID"] = station_id
    station_data = station_data.set_index(
        "STATION_ID", append=True).swaplevel()

    # Append to final df
    df_data_no2 = pd.concat([df_data_no2, station_data])

df_data_no2

# %%
# # TODO Chache entfernen
# data_no2.to_csv("data_no2.csv")
# data_no2 = pd.read_csv("data_no2.csv")

# %% [markdown]
# #### b) Setzen Sie den dtype der Spalte NO2 auf float und wandeln Sie die Spalte DT in ein DateTime-Format um.
# %%
# Convert to numeric
# df_measurements["NO2"] = df_measurements["NO2"].apply(
#     pd.to_numeric, errors='coerce', axis=1)
df_measurements["NO2"] = pd.to_numeric(df_measurements["NO2"], errors="coerce")

# Convert to datetime
# df_measurements["DT"] = df_measurements["DT"].apply(
#     pd.to_datetime, errors='coerce', axis=1)
df_measurements = df_measurements.replace(
    to_replace='24:00:00', value="00:00:00", regex=True)
df_measurements["DT"] = pd.to_datetime(df_measurements["DT"], errors="coerce")
# %% [markdown]
# #### c) Entfernen Sie alle Zeilen, bei denen der Wert in der Spalte NO2 fehlt. Geben Sie an, wieviele Zeilen dadurch entfernt wurden.
# %%
df_measurements_nanCleaned = df_measurements.dropna(
    axis=0, how="any", subset=["NO2"])
difCount = df_measurements.shape[0] - df_measurements_nanCleaned.shape[0]
print("Deleted " + str(difCount) + " rows that had a missing NO2 value")
# df_measurements = df_measurements_nanCleaned # Todo einkommentieren überschreibt das orginale dataframe, müssen wir Hr. Brunner fragen ob wir das weiter verwenden dürfen

# %%
# Todo Remove shape testing
df_measurements.isnull().sum()
df_measurements_nanCleaned.isnull().sum()

# %%
df_measurements.shape
df_measurements_nanCleaned.shape

# %% [markdown]
# #### d)  Entfernen Sie die Daten zu allen Stationen, die nicht für mindestens 95% der Messzeitpunkte im Auswertezeitraum einen gültigen Messwert enthalten

# %%
# Todo remove group filtering testing
# df_measurements_nanCleaned.groupby("STATION_ID").apply(lambda grp: grp["NO2"].isnull().sum())
# df_measurements_grouped = df_measurements.groupby("STATION_ID")
# df_measurements.groupby("STATION_ID").apply(
#     lambda grp: print("Station: " + str(grp.name) +
#     ": Count Nan: " + str(grp["NO2"].isnull().sum()) +
#     " --- Count all vals: " + str(grp["NO2"].count()))
#     )

# %%
#
df_tresholdFilter = df_measurements.groupby("STATION_ID").filter(
    lambda grp: grp["NO2"].isnull().sum() / grp["NO2"].count() > 0.05
)
df_tresholdCleaned = df_measurements.drop(df_tresholdFilter.index)
df_tresholdCleaned.shape


# %% [markdown]
# #### d)  LÖSUNG JAN: Entfernen Sie die Daten zu allen Stationen, die nicht für mindestens 95% der Messzeitpunkute im Auswertezeitraum einen gültigen Messwert enthielten
# %%
symbols_original = df_measurements.groupby("STATION_ID")

df_measurements.groupby("STATION_ID").apply(lambda x: print(
    "NO2 isnull count :" + str(symbols_original.get_group(x)["NO2"].isnull().count()) + " NO2 Count: " + str(x["NO2"].count())))

#df_measurements.groupby("STATION_ID").apply(lambda x: print("NO2 isnull count :" + str(x["NO2"].isnull()).sum() + " NO2 Count: " + str(x["NO2"].count())))
# %%
# symbols_original = df_measurements.groupby("STATION_ID")
# symbols_new = df_RemovedMeasurements.groupby("STATION_ID")
# for id in symbols_original.groups:
#     print(str(id))
#     amount_of_data_points = symbols_original.get_group(id)['STATION_ID'].count()
#     try:
#         amount_of_missing_no2_datapoints = symbols_new.get_group(id)['NO2'].count()
#     except KeyError:
#         print("deleted " + str(amount_of_data_points) + " in " + str(id))
#         df_measurements=df_measurements.drop(df_measurements[df_measurements["STATION_ID"]==id].index)
#     if((amount_of_missing_no2_datapoints/amount_of_data_points)<0.95):
#         print("Removed " + str(amount_of_missing_no2_datapoints) +" from station " + str(id) +". Original data points: " + str(amount_of_data_points))
#         df_measurements=df_measurements.drop(df_measurements[df_measurements["STATION_ID"]==id].index)
#df_measurements.drop(symbols_original.get_group(id).index, inplace=True)


# %% [markdown]
# #### e)  Für wie viele Stationen enthält der DataFrame data_no2 nun noch Daten?
# %%
len(df_tresholdCleaned["STATION_ID"].unique())
# %% [markdown]
# #### f)  Zu welchen der bayerischen Stationen enthält er keine Daten (mehr)? Geben Sie deren IDs und Namen aus.
# %%
stations_BY.loc[df_tresholdFilter["STATION_ID"].unique()][["Name"]]
# Todo e) und f) funktionieren nur so, wenn man df_tresholdFilter verwenden date_from


# %%
# TODO Schreibt Daten in temp für aufgabe 3

df_measurements_write_1 = df_measurements[:802284]
df_measurements_write_2 = df_measurements[802284:]
with pd.ExcelWriter("Temp_für_3.xlsx")as writer:
    df_measurements_write_1.to_excel(writer, sheet_name="NO2_Measurements_1")
    df_measurements_write_2.to_excel(writer, sheet_name="NO2_Measurements_2")
# endregion

# %%
# TODO Import aus Datei bei zusammenfügen entfernen
# TODO Import aus Datei bei zusammenfügen entfernen
xls = pd.ExcelFile("Temp_für_3.xlsx")
xls = pd.ExcelFile("Temp_für_3.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
# df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
# df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1  # .append(df2)
df_measurements = df1  # .append(df2)
df_stations = pd.read_excel("Stations_BY.xlsx", index_col="ID")
df_stations = pd.read_excel("Stations_BY.xlsx", index_col="ID")

# %% [markdown]
# ### Aufgabe 3 (Explorative Datenanalyse)
# region
# %% [markdown]
# #### a) Welches ist der in den Jahren 2016-2019 höchste gemessene Ein-Stunden-Mittelwert für NO2? Wann und an welcher Station wurde er gemessen?

# %%
MaxRow_ID, MaxRow_DT, MaxRow_NO2 = df_measurements.iloc[df_measurements["NO2"].idxmax(
)]
print("Der höchste NO2 Ein-Stunden-Mittelwert betrug " + str(MaxRow_NO2) + "."
      "\nEr wurde an Station " + str(MaxRow_ID) + " '" + df_stations.loc[MaxRow_ID]["Name"] + "' am " + str(MaxRow_DT) + " gemessen.")

# %% [markdown]
# #### b) An welchem Tag im Auswertezeitraum war die durchschnittliche NO2-Konzentration ̈uberalle bayerischen Stationen am höchsten und welchen Wert hatte sie?
# %%
df_measurements["Year"] = pd.to_datetime(df_measurements["DT"]).dt.year
df_measurements["Date"] = pd.to_datetime(df_measurements["DT"]).dt.date
df_measurements["Time"] = pd.to_datetime(df_measurements["DT"]).dt.time
# %%
daily_averages_no2 = []
days = df_measurements.groupby("Date")
for day in days.groups:
    daily_averages_no2.append((days.get_group(day)["NO2"].mean(), day))
print(max(daily_averages_no2, key=lambda element: element[0]))

# %%
#df_measurements[['Date', "NO2"]].groupby("Date").mean().max()

# %%
df_measurements[['Date', "NO2"]].groupby("Date").mean(
).sort_values(by="NO2", ascending=False).head(1)

# %% [markdown]
# #### c) Ermitteln Sie die 10 höchsten Messwerte und die zugehörigen Messzeitpunkte für die Station in der Nikolaistraße in Weiden.

# %%
id = df_stations.loc[df_stations["Name"] ==
                     "Weiden i.d.OPf./Nikolaistraße"].index[0]
df_measurements_nico = df_measurements.loc[df_measurements["STATION_ID"] == id]
df_measurements_nico.sort_values(by="NO2", ascending=False, inplace=True)
print(df_measurements_nico.iloc[: 10].to_string(
    index=False, columns=["DT", "NO2"]))
# %%

# #### d)  Berechnen Sie die Mittelwerte der gemessenen NO2-Konzentrationen über die einzelnen Jahre. Wie haben sich diese zeitlich entwickelt? Unterscheiden Sie dabei auch nach demStations-Typ.
# %%
# %%
# TODO @Jan Wie verstehst du Angabe: Ist das so gemeint, dass man erst nur nach Jahren gruppieren soll und dann nochmal nach Jahren und Typ?
# Gruppierung nur nach Year
df_yearMean = df_measurements.groupby(["Year"]).mean()
df_yearMean

# Gruppierung nur nach Year und Type, dazu ist merge notwendig
# %%
df_merge = df_measurements.merge(
    df_stations[["Type"]], how="left", left_on="STATION_ID", right_index=True)

df_YearTypeMean = df_merge.groupby(["Year", "Type"]).mean()[["NO2"]]
# %%
# Diagramm zeigt Mittelwert über Jahre gruppiert nach Typ
# TODO Diagramm schöner machen
df_YearTypeMean.unstack().plot(kind="bar")

# x = np.array([2, 4, 6, 8, 10])

# plt.bar(x-0.25, , width=0.5, label='Year')
# plt.bar(x+0.25, df_YearTypeMean.loc["Type"], width=0.5, label='Type')

# plt.xticks(x, df_YearTypeMean.index)
# plt.xlabel('Year')
# plt.ylabel('NO2')
# plt.legend()
# endregion
# %%
# %%
# TODO Import aus Datei bei zusammenfügen entfernen
xls = pd.ExcelFile("Temp_für_3.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1.append(df2)

# %% [markdown]
# ### Aufgabe 4 (Verletzung der zul ̈assigen NO2-Grenzwerte)
# region
# %% [markdown]
# #### a)  Ermitteln Sie, an welchen bayerischen Stationen jeweils in den Jahren 2016-2019 ̈Uberschrei-tungen des Stundengrenzwerts(d.h. der Ein-Stunden-Mittelwert ̈uberschreitet 200μg/m3)gemessen wurden, und geben Sie an wie viele ̈Uberschreitungen es jeweils waren. Dieserdarf innerhalb eines Jahres h ̈ochstens 18-Mal pro Station ̈uberschritten werden. Welche Sta-tionen haben dieses Kriterium verletzt?
# %%
# Alle Überschreitungen holen
violating_datapoints = df_measurements[df_measurements["NO2"] > 200]

# Die Anzahl pro Station auswerten
violations_per_station = violating_datapoints.groupby("STATION_ID").count()[
    ["NO2"]].rename(columns={"NO2": "NO2_limit_violations"})

violations_per_station

# %%
violating_datapoints.groupby(
    [violating_datapoints["DT"].dt.year, "STATION_ID"]).count()[["NO2"]]
# Todo Angabe sagt, dass es eigentlich Stationen geben sollte die das Limit überschreiten


# %% [markdown]
# #### b) Ermitteln Sie, an welchen bayerischen Stationen und in welchen Jahren der Jahresmittelwertder Ein-Stunden-Mittelwerte die Grenze von 40μg/m3 ̈uberschritten hat und geben Sie die zugehörigen Jahresmittelwerte an.

# %%

#df_measurements = df_measurements.set_index("DT")

violations_per_station_yearly = df_measurements.groupby(
    ["STATION_ID", pd.Grouper(freq='Y')])

#sums_over_dt = [sum(station) for station in violations_per_station_yearly]

violations_data_points_yearly = violations_per_station_yearly["NO2"].mean()

result = violations_data_points_yearly[violations_data_points_yearly > 40]
result
# TODO In Result stehen jetzt die Jahre und stationen drin die den Grenzwert von 40μg/m3 überschritten habe, aber es wird noch das Datum des letzten Tages des Jahrs in der Spalte dt angezeigt

# endregion

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
# ### Aufgabe 5 (Visualisierung)
# region

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
# Alternative zu meinem iloc
#df_mean_per_season.unstack().loc[:, (slice(None), "Spring")].values
df_mean_per_season.rename_axis(['Year', 'Season'], inplace=True)

# %%
# TODO level=0 durch string ersetzen
x_years = df_mean_per_season.index.get_level_values(level="Year").unique()

mean_yearly_values = []
for year in x_years:
    mean_yearly_values.append(df_mean_per_season.loc[year].values.mean())


fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_years,
    y=df_mean_per_season.iloc[df_mean_per_season.index.isin(
        ["Spring"], level='Season')]["NO2"],
    mode="lines",
    name="Spring NO2 Averages"
))
fig.add_trace(go.Scatter(
    x=x_years,
    y=df_mean_per_season.iloc[df_mean_per_season.index.isin(
        ["Autumn"], level='Season')]["NO2"],
    mode="lines",
    name="Autumn NO2 Averages"
))
fig.add_trace(go.Scatter(
    x=x_years,
    y=df_mean_per_season.iloc[df_mean_per_season.index.isin(
        ["Summer"], level='Season')]["NO2"],
    mode="lines",
    name="Summer NO2 Averages"
))
fig.add_trace(go.Scatter(
    x=x_years,
    y=df_mean_per_season.iloc[df_mean_per_season.index.isin(
        ["Winter"], level='Season')]["NO2"],
    mode="lines",
    name="Winter NO2 Averages"
))
fig.add_trace(go.Scatter(
    x=x_years,
    y=mean_yearly_values,
    mode="lines",
    name="Average yearly NO2 Concentration"
))


fig.show()

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

# endregion

# %%
# # TODO Import aus Datei bei zusammenfügen entfernen
# xls = pd.ExcelFile("Temp_für_3.xlsx")
# df1 = pd.read_excel(xls, 'NO2_Measurements_1', index_col='dp_id')
# # df2 = pd.read_excel(xls, 'NO2_Measurements_2', index_col='dp_id')
# df_measurements = df1  # .append(df2)
# df_stations = pd.read_excel("Stations_BY.xlsx", index_col='ID')

# %% [markdown]
# ### Aufgabe 6  (Interaktives Diagramm)
# region
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

# endregion

# %% [markdown]
# ### Aufgabe 7
#region
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

#endregion
