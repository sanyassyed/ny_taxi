import sys
import pandas as pd 
import os
from sqlalchemy import create_engine
from time import time

def con_open(host, username, pwd, port, db_name):
    """
    Connects to postgres DB 
    Args:
        url (str): the url of the spreadsheet which is the data source
        username (list): names of the sheets to be extracted
    Returns:
        df_i (pandas.dataframe): Pandas df containing inventory data
        df_p (pandas.dataframe): Pandas df containing production data
    """
    try: 
        engine = create_engine(f'postgresql://{username}:{pwd}@{host}:{port}/{db_name}')
        print('Connection to DB Opened')
        return engine
    except Exception as e:
        print(f'ERROR: Could not establish connection to db due to error {e}')
    return None
    
def con_close(engine):
    engine.dispose()
    print('Connection to DB Closed')
    return None


def load(engine, url, taxi_color):
    """
    Extracts sheets from Gdrive by specifying the url in the pandas read_excel function
    Args:
        url (str): the url of the spreadsheet which is the data source
        username (list): names of the sheets to be extracted
    Returns:
        df_i (pandas.dataframe): Pandas df containing inventory data
        df_p (pandas.dataframe): Pandas df containing production data
    """
    df_iter = pd.read_csv(url, iterator=True, chunksize=100000, low_memory=False)
    df = next(df_iter)
    table_name = taxi_color
    # inserting only column headers
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    while df is not None:
        s_time = time()
        df.to_sql(name=table_name, con=engine, if_exists='append')
        e_time = time()
        print(f'Inserted chunk in {e_time-s_time:.2f} seconds')
        df = next(df_iter, None)
    return None


def main(taxi_color='zone')->None:
    """
    Main function that calls the ETL functions
    Args:
        taxi_color (str): which taxi data to extract
        year (int): year number
        month (int): month number
    Returns:
        None
    """
    host, username, pwd, port, db_name = 'localhost', 'codespace', 'root', 5432, 'ny_taxi'
    url =f'https://d37ci6vzurychx.cloudfront.net/misc/taxi+_{taxi_color}_lookup.csv'
    engine = con_open(host, username, pwd, port, db_name)
    if engine is not None:
        load(engine, url, taxi_color)
        print("Data Loading to DB Complete")
        con_close(engine)

if __name__=="__main__":
    main()