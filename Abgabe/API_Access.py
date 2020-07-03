### API ACCESS FUNCTIONS ###
import pandas as pd
import requests
import json
import numpy as np
from enum import Enum


class ComponentEnum(Enum):
    # All components the api provides data for
    PM10 = "1"
    CO = "2"
    O3 = "3"
    SO2 = "4"
    NO2 = "5"


# Constants
__BASE_URL = "https://www.umweltbundesamt.de/api/"


def GetMetaData_Stations_All(date_from, date_to):
    # Make api call
    response = requests.get(
        __BASE_URL + 'air_data/v2/meta/json',
        params={
            'use': 'measure',
            'date_from': date_from,
            'date_to': date_to
        }
    )
    if(response.status_code != 200):
        print(
            f"Failed meta data request: use {'measure'}, date_from {date_from}, date_to {date_to}")

    # Get raw station data from json
    raw_data = json.loads(response.text)
    station_data_dict = raw_data.get('stations')

    # Parse into custom column names
    df_stations_meta = pd.DataFrame.from_dict(station_data_dict,
                                              orient="index",
                                              columns=["ID", "Code", "Name", "Location", "Code_Name", "Construction_Date", "Deconstruction_Date", "Longtitude", "Latitude",
                                                       "Network_ID", "Settings_ID", "Type_ID", "Network_Code", "Network_Name", "Settings_Long",
                                                       "Settings_Short", "Type", "Street_Name", "Street_Number", "ZIP_Code"],
                                              )

    df_stations_meta.set_index('ID', inplace=True)

    # Convert to numeric
    conv_to_int_cols = ["Longtitude", "Latitude", "Network_ID", "Settings_ID",
                        "Type_ID"]
    df_stations_meta[conv_to_int_cols] = df_stations_meta[conv_to_int_cols].apply(
        pd.to_numeric, errors='coerce', axis=1)

    # Convert to datetime
    conv_to_date_cols = ["Construction_Date", "Deconstruction_Date"]
    df_stations_meta[conv_to_date_cols] = df_stations_meta[conv_to_date_cols].apply(
        pd.to_datetime, errors='coerce', axis=1)

    return df_stations_meta


def GetMeasurements_MeanPerHour_SingleComponent(station_id, component, date_from, date_to):
    # Resolve component enum info
    component_name = component.name
    component_id = component.value

    # Make api call
    response = requests.get(
        __BASE_URL + 'air_data/v2/measures/json',
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
            f"Failed measurement request: station_id {station_id}, component_id {component_id}, component_{component_name}, date_from {date_from}, date_to {date_to}")

    # Get raw station data from json
    raw_data = json.loads(response.text)
    station_data_dict = raw_data['data'].get(station_id)

    # Inform caller
    if station_data_dict == None:
        raise Exception(f"Station {station_id} provides no data")

    # Parse to dataframe
    df_single_component = pd.DataFrame.from_dict(
        station_data_dict,
        orient="index",
        columns=["component_id", "scope_id",
                 component_name, "date_end", "index"]
    )

    # Drop uninteresting columns
    df_single_component.drop(
        columns=["component_id", "scope_id", "date_end", "index"], inplace=True)

    # Rename index and and convert it to a column
    df_single_component.index.rename("DT", inplace=True)
    df_single_component.reset_index(drop=False, inplace=True)

    # Add the station id as new column
    df_single_component.insert(0, "STATION_ID", station_id)

    return df_single_component


def GetMeasurements_MeanPerHour_MultiComponents(station_id, components, date_from, date_to):

    # Create empty df with datetime-index, that will be used to left join the single component data
    start_time = pd.to_datetime(date_from + ' 00:00:00',
                                infer_datetime_format=True)
    end_time = pd.to_datetime(date_to + ' 23:00:00',
                              infer_datetime_format=True)
    df_multi_component = pd.DataFrame(pd.date_range(
        start_time, end_time, freq='h'), columns=["DT"])
    df_multi_component.set_index("DT", inplace=True)

    # Get measurements of each component
    for component in components:
        try:
            df_single_component = GetMeasurements_MeanPerHour_SingleComponent(
                station_id=station_id,
                component=component,
                date_from=date_from,
                date_to=date_to)
        except:
            # If station provides no data, Insert empty column named after component at the end of df
            df_multi_component.insert(
                len(df_multi_component.columns), component.name, np.NaN)
            continue

        # Set DT column as datetime index
        df_single_component["DT"] = pd.to_datetime(df_single_component["DT"])
        df_single_component.set_index("DT", inplace=True)

        # Left join single component data on datetime index
        df_multi_component = df_multi_component.merge(
            df_single_component[component.name],
            how='left',
            left_index=True,
            right_on="DT"
        )

    return df_multi_component
