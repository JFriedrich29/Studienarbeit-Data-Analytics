# %%
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# %%
# TODO Import aus Datei bei zusammenfügen entfernen
xls = pd.ExcelFile("Temp_für_3.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
# df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1  # .append(df2)
df_stations = pd.read_excel("Stations_BY.xlsx", index_col="ID")

# %%


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

# #### d)  Berechnen Sie die Mittelwerte der gemessenen NO2-Konzentrationen  über die einzelnenJahre. Wie haben sich diese zeitlich entwickelt? Unterscheiden Sie dabei auch nach demStations-Typ.
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

# %%
