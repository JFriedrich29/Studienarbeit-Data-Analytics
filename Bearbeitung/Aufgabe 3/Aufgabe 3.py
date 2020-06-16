# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# %%
# TODO Import aus Datei bei zusammenfügen entfernen
xls = pd.ExcelFile("Temp_für_3.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1.append(df2)
df_stations = pd.read_excel("Stations_BY.xlsx", index_col="ID")

# %%


# %% [markdown]
# #### a) Welches ist der in den Jahren 2016-2019 höchste gemessene Ein-Stunden-Mittelwert für NO2? Wann und an welcher Station wurde er gemessen?

# %%
MaxRow_ID, MaxRow_DT, MaxRow_NO2 = df_measurements.iloc[df_measurements["NO2"].idxmax()]
print("Der höchste NO2 Ein-Stunden-Mittelwert betrug " + str(MaxRow_NO2) + "."
      "\nEr wurde an Station " + str(MaxRow_ID) + " '" + df_stations.loc[MaxRow_ID]["Name"] + "' am " + str(MaxRow_DT) + " gemessen.")

# %% [markdown]
# #### b) An welchem Tag im Auswertezeitraum war die durchschnittliche NO2-Konzentration ̈uberalle bayerischen Stationen am höchsten und welchen Wert hatte sie?

# %%
daily_averages_no2 = []
days = df_measurements.groupby("DT")
for id in df_measurements.groupby("DT").groups:
    daily_averages_no2.append((days.get_group(id)["NO2"].mean(), id))
print(max(daily_averages_no2, key=lambda element: element[0]))
# %% [markdown]
# #### c) Ermitteln Sie die 10 höchsten Messwerte und die zugehörigen Messzeitpunkte für die Station in der Nikolaistraße in Weiden.

# %%
id = df_stations.loc[df_stations["Name"] ==
                     "Weiden i.d.OPf./Nikolaistraße"].index[0]
df_measurements_nico = df_measurements.loc[df_measurements["STATION_ID"] == id]
df_measurements_nico.sort_values(by="NO2", ascending=False, inplace=True)
print(df_measurements_nico.iloc[:10].to_string(
    index=False, columns=["DT", "NO2"]))
# %%
