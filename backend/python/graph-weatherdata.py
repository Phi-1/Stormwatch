from sqlalchemy import create_engine
import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fuzzywuzzy import process
from datetime import datetime as dt, time
from datetime import timedelta
import json
import sys


def cout(data):
    print(data)

def getDataFromDatabase() -> pd.DataFrame:
    """Returns dataframe containing weatherdata from database"""

    engine = create_engine("sqlite:///C:\\Users\\Phi\\Documents\\Code\\JavaScript\\Stormwatch\\backend\\database\\weatherdata.db")
    df = pd.read_sql("SELECT * FROM Weather", engine)
    
    dtypes = {"Temperature": float, "Precipitation": float, "Wind_speed": float, "Wind_direction": "category", "Barometer": float, "Dewpoint": float, "Humidity": float, "Solar_radiation": float, "UV_index": float}
    df = df.astype(dtypes)
    df["Time"] = pd.to_datetime(df["Time"])

    return df


def processVariableArguments(names, *args) -> list:
    """Returns best matches of arguments and variable names"""

    vars = []
    for var in args:
        res = process.extract(var, names, limit=1)
        if res[0][1] >= 80:
            vars.append(res[0][0])
        else:
            return "What the fuck did you even enter this shit is unintelligible"
    
    return vars



def generateDefaultDataset() -> dict:
    """Returns dictionary of latest weather data values"""
    
    df = getDataFromDatabase()
    df["Time"] = pd.to_datetime(df["Time"])
    latest_data = pd.Series(df.iloc[-1])
    latest_data["Time"] = latest_data["Time"].strftime("%H:%M")
    latest_dict = latest_data.to_dict()
    last_day = dt.today() - timedelta(days = 1) 
    latest_dict["temp_day"] = df[df["Time"] > last_day]["Temperature"].to_list()
    last_day_timestamps = df[df["Time"] > last_day]["Time"].to_list()
    last_day_timestamps_s = map(lambda v: v.strftime("%H:%M"), last_day_timestamps)
    latest_dict["temp_day"] = dict(zip(last_day_timestamps_s, latest_dict["temp_day"]))
    return json.dumps(latest_dict)


def graphRelational(weatherdata, var1, var2):
    plt.plot(weatherdata[var1], weatherdata[var2], "o", alpha=0.5)
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.show()


def graphTimeSeries(weatherdata, start, stop, vars):
    start = pd.to_datetime(start)
    stop = pd.to_datetime(stop)
    timeframe = weatherdata[(weatherdata["Time"] > start) & (weatherdata["Time"] < stop)]

    ax = timeframe.plot(x="Time", y=vars[0], color="#1E88E5", legend=False, ylabel=vars[0])
    colors = {0:"#004D40", 1:"#D81B60", 2:"#FFC107", 3:"#1E88E5"}
    
    for i, var in enumerate(vars[1:]):
        twinx = ax.twinx()
        timeframe.plot(x="Time", y=var, ax=twinx, color=colors[i], legend=False, ylabel=var)


    ax.figure.legend()
    plt.show()


def generateRegressionChart(weatherdata, vars):
    if len(vars) <= 1:
        return "Insufficient variables provided to regression, enter at least one dependent and one independent variable"

    yvar = vars[0]
    varsstr = " + ".join(vars[1:])

    res = smf.ols(f"{yvar} ~ {varsstr}", data=weatherdata).fit()
    return res.predict(weatherdata[["Wind_speed", "Precipitation"]])


def main():
    weatherdata = getDataFromDatabase()

    # CL Argument syntax: nothing = default weather page

    if len(sys.argv) <= 1:
        cout(generateDefaultDataset())
    else:
        vars = []
        # for timeseries the first two arguments shouldn't be processed as variables
        if sys.argv[1] =="timeseries": 
            vars = processVariableArguments(weatherdata.columns, *sys.argv[4:])
        else:
            vars = processVariableArguments(weatherdata.columns, *sys.argv[2:])

        if type(vars) == "string":
            cout(vars)
            return

        if sys.argv[1] == "basic":
            graphRelational(weatherdata, vars[0], vars[1])
        elif sys.argv[1] == "timeseries":
            graphTimeSeries(weatherdata, sys.argv[2], sys.argv[3], vars)
        elif sys.argv[1] == "regression":
            cout(generateRegressionChart(weatherdata, vars))
           

if __name__ == "__main__":
    main()