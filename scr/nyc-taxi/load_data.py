import numpy as np
import pandas as pd
import json
import datetime
from sqlalchemy import create_engine
import psycopg2
import numpy as np
import pyarrow


def openFile(path):
    """
    Opens CSV file

    Args:
        path: path to data
    Return:
        df: pandas DataFrame
    """
    df = pd.read_parquet(path)
    return df


def create_dfs(df):
    """
    Transforms original dataset into statistiks metrics

    Args:
        df: pandas DataFrame
    Return:
        3 pandas dataframes
    """
    df['trip_distance'] = df['trip_distance'] * 1.60934
    df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
    df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)
    df['trip_duration_seconds'] = df.apply(lambda x: (x.tpep_dropoff_datetime - x.tpep_pickup_datetime).total_seconds(), axis=1)
    
    durLimits  = [np.percentile(df['trip_duration_seconds'], 2), np.percentile(df['trip_duration_seconds'], 98.5)]
    df = df[(df['trip_duration_seconds'] >= durLimits[0]) & (df['trip_duration_seconds'] <= durLimits[1])]

    distLimits  = [np.percentile(df['trip_distance'], 1), np.percentile(df['trip_distance'], 98.5)]
    df = df[(df['trip_distance'] >= distLimits[0]) & (df['trip_distance'] <= distLimits[1])]

    df = df.reset_index(drop=True)
    
    
    df['pickup_weekday'] = df['tpep_pickup_datetime'].dt.weekday
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    df['pickup_week_hour'] = df['pickup_weekday'] * 24 + df['pickup_hour']
    
    df.loc[:, 'avg_speed_h'] = df['trip_distance'] / (df['trip_duration_seconds'] / 3600)
    
    df_hours = df.groupby('pickup_hour').mean()['avg_speed_h']
    df_weekday = df.groupby('pickup_weekday').mean()['avg_speed_h']
    df_weekday_hour = df.groupby('pickup_week_hour').mean()['avg_speed_h']
    
    return df_hours.reset_index(), df_weekday.reset_index(), df_weekday_hour.reset_index()


def load_to_postgres(df, tableName: str, engine):
    """
    Query database for median session duration before buying

    Args:
        df: pandas DataFrame
        tableName: string, table name
        engine: sqlachemy engine
    """
    df.to_sql(tableName, engine)


def upload_data(engine) -> dict:
    """
    Query database for median session duration before buying

    Args:
        engine: sqlachemy engine
    Return:
        dict
    """
    filePath = "yellow_tripdata_2022-05.parquet"
    file = openFile(filePath)
    df_hours, df_weekday, df_weekday_hour = create_dfs(file)
    load_to_postgres(df_hours, 'datahour', engine)
    load_to_postgres(df_weekday, 'dataday', engine)
    load_to_postgres(df_weekday_hour, 'dataweekhour', engine)

    return {"data status" : "ready"}