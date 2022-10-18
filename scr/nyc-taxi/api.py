from sqlalchemy import create_engine
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import joblib

def getEngine():
    """
    Gets credentials from .env file and created engine for DB
     
    Return:
        sqlalchemy.engine.base.Engine
    """
    load_dotenv()
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    engine = create_engine(f'postgresql://{user}:{password}@db:5432/sessions')
    return engine


def executeQuery(statement: str, engine):
    """
    Executes statement
    
    Args:
        statement: string with SQL query
    Return:
        result: integer or error name
    """
    try:
        conn = engine.connect()
        result = conn.execute(statement).fetchone()[0]
        return result
    except Exception as e:
        return {"error" : str(e)}


def prepareOutput(metrics: str, value: int) -> dict:
    """
    Make output in readable format
    
    Args:
        metrics: str, measue value
        value: resutl of query
    Return:
        respond: dict
    """
    respond = {f"Average speed per {metrics} " : value}
    return respond


def getStatistiksForDay(day: str, engine) -> int:
    """
    Query database to get day statistics

    Args:
        day: string
    Return:
        result: integer
    """
    dayNumber = mapDayNumber(day)
    statement = f"select avg_speed_h from dataday where pickup_weekday = {dayNumber};"
    result = executeQuery(statement, engine)
    return result
    

def getStatistiksForHour(hour: int, engine) -> int:
    """
    Query database to get week statistics

    Args:
        week: string
    Return:
        result: integer
    """
    statement = f"select avg_speed_h from datahour where pickup_hour = {hour};"
    result = executeQuery(statement, engine)
    return result


def mapDayNumber(day: str) -> int:
    """
    Transforms day into day number

    Args:
        day: string
        hour: integer
    Result:
        weekHour: integer
    """
    mapDict = {"monday" : 0,
               "tuesday" : 1,
               "wednesday" : 2,
               "thursday" : 3,
               "friday" : 4,
               "saturday" : 5,
               "sunday" : 6}
    dayNumber = mapDict.get(day.lower())
    return dayNumber


def getStatistiksForWeekHour(hour: int, day: str, engine) -> int:
    """
    Query database to get week statistics

    Args:
        week: string
    Return:
        result: integer
    """
    dayNumber = mapDayNumber(day)
    weekDay = dayNumber * 24 + hour
    statement = f"select avg_speed_h from dataweekhour where pickup_week_hour = '{weekDay}';"
    result = executeQuery(statement, engine)
    return result


def getForest():
    """
    Gets pickle with RandomForestRegressor object

    Return:
        sklearn.ensemble._forest.RandomForestRegressor
    """
    filepath = 'model.joblib'
    forest = joblib.load(filepath) 
    return forest


def calculate(tripDistance, day, hour, minute, engine):
    """
    Calculate time to travel 

    Args:
        week: string
    Return:
        result: integer
    """
    dayNumber = mapDayNumber(day)
    weekHour = dayNumber * 24 + hour
    avgSpeedThisHour = getStatistiksForHour(hour, engine)
    avgSpeedThisDay = getStatistiksForDay(day, engine)
    avgSpeedThisWeekHour= getStatistiksForWeekHour(hour, day, engine)
    featureDict = {'trip_distance' : [tripDistance],
                   'pickup_weekday': [dayNumber],
                   'pickup_hour': [hour],
                   'pickup_minute' : [minute],
                   'pickup_week_hour' : [weekHour],
                   'avg_speed_this_hour' : [avgSpeedThisHour],
                   'avg_speed_this_day' : [avgSpeedThisDay],
                   'avg_speed_this_dayweek' : [avgSpeedThisWeekHour]}
    df = pd.DataFrame.from_dict(featureDict)
    forest = getForest()
    time = forest.predict(df)
    time2 = time / 60
    return {"ans" : time2}
    