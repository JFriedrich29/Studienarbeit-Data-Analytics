#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

#%%
#TODO Import aus Datei bei zusammenfügen entfernen
xls = pd.ExcelFile("NO2_Measurements.xlsx")
df1 = pd.read_excel(xls, "NO2_Measurements_1", index_col="dp_id")
df2 = pd.read_excel(xls, "NO2_Measurements_2", index_col="dp_id")
df_measurements = df1.append(df2)
df_measurements

#%% [markdown]
# #### a) Welches ist der in den Jahren 2016-2019 höchste gemessene Ein-Stunden-Mittelwert für NO2? Wann und an welcher Station wurde er gemessen?

#%%
row_with_max = df_measurements.iloc[df_measurements["NO2"].idxmax(axis=1)]
print("Der höchste NO2 Ein-Stunden-Mittelwert wurde an Station " + str(row_with_max[0]) + " gemessen. Er wurde am " + str(row_with_max[1]) + " gemessen und betrug " + str(row_with_max[2]) +".")

#%% [markdown]
# #### b) An welchem Tag im Auswertezeitraum war die durchschnittliche NO2-Konzentration ̈uberalle bayerischen Stationen am höchsten und welchen Wert hatte sie?

#%%
#df_measurements["DT"] = pd.to_datetime(df_measurements["DT"], errors="coerce")
print(df_measurements.dtypes)


#%%