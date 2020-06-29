### API ACCESS FUNCTIONS ###
import pandas as pd
import requests
import json
import numpy as np


# Public variables
components = ["PM10", "CO", "O3", "SO2", "NO2"]

# Private module variables
__base_URL = "https://www.umweltbundesamt.de/api/"
__component_ids = {"PM10": "1", "CO": "2", "O3": "3", "SO2": "4", "NO2": "5"}


def GetMeasurements_MeanPerHour_SingleComponent(station_id, component, date_from, date_to):
    global __base_URL
    global __component_ids

    component_id = __component_ids[component]
    # Make api call
    response = requests.get(
        __base_URL + 'air_data/v2/measures/json',
        params={
            'use': 'measure',
            'date_from': date_from,
            'date_to': date_to,
            'time_to': '24',
            'time_from': '1',
            'scope': '2',
            'component': component_id,
            'station': station_id
        }
    )
    if(response.status_code != 200):
        print(
            f"Failed request for: station_id {station_id}, component_id {component_id}, component_{component}, date_from {date_from}, date_to {date_to}")

    # Get raw station data from json
    raw_data = json.loads(response.text)
    station_data_dict = raw_data['data'].get(station_id)
    if station_data_dict == None:
        raise Exception("Station provides no data for given parameters!")

    # Parse to dataframe
    station_data_df = pd.DataFrame.from_dict(
        station_data_dict,
        orient="index",
        columns=["component id", "scope id", component, "date end", "index"]
    )

    return station_data_df


def GetMeasurements_MeanPerHour_MultiComponents(station_id, components, date_from, date_to):

    # Create empty df with index, that will be used to left join the single component data
    start_time = pd.to_datetime(date_from + ' 00:00:00',
                                infer_datetime_format=True)
    end_time = pd.to_datetime(date_to + ' 23:00:00',
                              infer_datetime_format=True)
    df_multi_component = pd.DataFrame(pd.date_range(
        start_time, end_time, freq='h'), columns=["DT"])
    df_multi_component.set_index("DT", inplace=True)

    for component in components:
        try:
            df_single_component = GetMeasurements_MeanPerHour_SingleComponent(
                station_id=station_id,
                component=component,
                date_from=date_from,
                date_to=date_to)
        except:
            # If station provides no data, Insert empty column named after component
            df_multi_component.insert(
                len(df_multi_component.columns), component, np.NaN)
            continue

        # Drop unnecessary columns
        # df_single_component.drop(
        #     ['component id', 'scope id', 'date end', 'index'],
        #     inplace=True,
        #     axis=1
        # )

        # Convert index to datetime
        station_data_df = station_data_df.replace(
            to_replace='24:00:00',
            value="00:00:00",
            regex=True
        )
        station_data_df.index = pd.to_datetime(station_data_df.index)
        station_data_df.index.rename("DT", inplace=True)

        # Left join single component data on datetime index
        df_multi_component = df_multi_component.merge(
            df_single_component[component],
            how='left',
            left_index=True,
            right_index=True,
        )

        # df_multi_component.rename(
        #     {"VALUE": component}, axis=1, inplace=True)

    return df_multi_component
