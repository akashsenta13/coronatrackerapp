"""
This file will fetch data from csv and store data into sqlite database.
"""
import pandas as pd
from datetime import datetime, timedelta
import os
import sqlite3


def fetchdata():
    """
    hit csv daily and get data and load csv data into pandas
    and insert data into sqlite database
    """
    CONFIRMED_DATA_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    DEATH_DATA_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
    RECOVERED_DATA_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"

    confirmed_data = clean_data(CONFIRMED_DATA_URL, 'confirmed')
    death_data = clean_data(DEATH_DATA_URL, 'deaths')
    recovered_data = clean_data(RECOVERED_DATA_URL, 'recovered')

    combine_data = pd.concat(
        [confirmed_data, death_data['deaths'], recovered_data['recovered']], axis=1)

    combine_data.replace('', None, inplace=True)

    # if database exists, remove it
    if os.path.exists("coronadata.db"):
        os.remove("coronadata.db")

    # create a database
    conn = sqlite3.connect("coronadata.db")

    combine_data.to_sql('combine_data', conn, dtype={
        'state': 'VARCHAR(256)',
        'country': 'VARCHAR(256)',
        'Lat': 'VARCHAR(256)',
        'Long': 'VARCHAR(256)',
        'confirmed': 'VARCHAR(256)',
        'deaths': 'VARCHAR(256)',
        'recovered': 'VARCHAR(256)'
    })
    print("Data insert done")
    return None


def clean_data(filepath, name):
    today = (datetime.now() + timedelta(days=-1)).strftime("%m/%d/%y")[1:]
    headers = ["Province/State", "Country/Region", "Lat", "Long", today]
    confirmed_data = pd.read_csv(filepath, usecols=headers)

    confirmed_data.rename(columns={'Province/State': 'state', 'Country/Region': 'country',
                                   today: name}, inplace=True)

    return confirmed_data


# function call
fetchdata()
