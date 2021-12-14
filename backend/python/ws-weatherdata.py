import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pandas as pd
import datetime as dt
from dotenv import load_dotenv
import sys
import os

def cout(data):
    print(data)

def saveDFToDB(df, db_path):
    engine = create_engine(os.environ.get("DATABASE_PATH"))
    with engine.connect() as con:
        df.to_sql("Weather", con, if_exists = "append", index = False)
        cout("saved data to database")

if __name__ == "__main__":
    load_dotenv()

    page = requests.get("https://www.hetweeractueel.nl/weer/terneuzen/actueel/")
    soup = BeautifulSoup(page.content, "html.parser")

    tds = list(soup.find_all("td"))
    dataTime = str(soup.find_all("div", {"class": "lastupdate"}))
    elementData = [str(i).replace("<td>", "").replace("</td>", "") for i in tds]
    parsedData = {}

    parsedData["Time"] = pd.to_datetime(dataTime.split(" ")[5])
    parsedData["Temperature"] = float(elementData[elementData.index("Temperatuur") + 1].split(" ")[0])
    parsedData["Precipitation"] = float(elementData[elementData.index("Neerslag") + 1].split(" ")[0])
    parsedData["Wind_speed"] = float(elementData[elementData.index("Windsnelheid en -richting") + 1].split(" ")[0])
    parsedData["Wind_direction"] = elementData[elementData.index("Windsnelheid en -richting") + 1].split(" ")[3]
    parsedData["Barometer"] = float(elementData[elementData.index("Barometer") + 1].split(" ")[0])
    parsedData["Dewpoint"] = float(elementData[elementData.index("Dauwpunt") + 1].split(" ")[0])
    parsedData["Humidity"] = float(elementData[elementData.index("Luchtvochtigheid") + 1].split(" ")[0])
    parsedData["Solar_radiation"] = float(elementData[elementData.index("Zonnestraling") + 1].split(" ")[0])
    parsedData["UV_index"] = float(elementData[elementData.index("UV index") + 1])

    currentUpdate = int(parsedData["Time"].strftime("%M"))
    lastUpdate = int(sys.argv[1])
    cout(currentUpdate)

    df_weatherdata = pd.DataFrame(parsedData, index = [0])
    df_weatherdata["Wind_direction"] = df_weatherdata["Wind_direction"].astype("category")

    db_path = os.path.abspath("../database/weatherdata.db")
    
    if lastUpdate < 55 and currentUpdate > lastUpdate:
        saveDFToDB(df_weatherdata, db_path)
    elif lastUpdate >= 55 and currentUpdate == 0:
        saveDFToDB(df_weatherdata, db_path)

