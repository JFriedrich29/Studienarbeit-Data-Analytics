# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
# TODO Import aus Datei bei zusammenfügen entfernen
xls = pd.ExcelFile("Temp_für_3.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1.append(df2)

# %% [markdown]
# ### Aufgabe 4 (Verletzung der zul ̈assigen NO2-Grenzwerte)

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
#
# %%
