import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

__author__ = "William Goble"
__email__ = "will.goble@gmail.com"

def scrapePage():
    website = "https://forecast.weather.gov/MapClick.php?lat=40.2013&lon=-77.1891#.Y8m4Jy-B1pQ"
    page = requests.get(website)
    return page

def createForcast(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    seven_day = soup.find(id="seven-day-forecast")
    forecast_items = seven_day.find_all(class_="tombstone-container")

    return seven_day

def processSevenDay(seven_day):
    period_tags = seven_day.select(".tombstone-container .period-name")
    periods = [pt.get_text() for pt in period_tags]
    short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
    temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
    descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

    weather = pd.DataFrame({
        "period": periods,
        "short_desc": short_descs,
        "temp": temps,
        "desc": descs
    })
    return weather

def main():
    page = scrapePage()
    seven_day = createForcast(page)
    weather = processSevenDay(seven_day)
    print(weather.head())

if __name__ == "__main__":
    main()
