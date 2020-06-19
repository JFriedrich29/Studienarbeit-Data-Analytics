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


# %%
