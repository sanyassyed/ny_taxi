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


def extract(url) -> str:
    """
    Extracts the parquet file from the url and writes to the disk
    Args:
        url (str): the url the source data
    Returns:
        f_loc (str): the location where the parquet file is written as a cvs file
    """
    data_dir = 'data'
    f_name = (url.split('.parquet')[0].split('/')[-1]) + '.csv'
    f_loc = os.path.join(data_dir, f_name)
    # reading parquet file from url as df
    df_p = pd.read_parquet(url)
    print(f'Parquet file downloaded from {url}')
    # writing df to disk as csv for future reading by chunking and iteration
    df_p.to_csv(f_loc, index=False)
    print(f'Parquet file written to disk as CSV at {f_loc}')
    return f_loc

def transform(df):
    """
    Extracts sheets from Gdrive by specifying the url in the pandas read_excel function
    Args:
        url (str): the url of the spreadsheet which is the data source
        username (list): names of the sheets to be extracted
    Returns:
        df_i (pandas.dataframe): Pandas df containing inventory data
        df_p (pandas.dataframe): Pandas df containing production data
    """
    # Converting the datatype pf columns total_amount, passenger_count, RatecodeID to appropriate type
    df.passenger_count = df['passenger_count'].fillna(0).astype('int')
    df.RatecodeID = df['RatecodeID'].fillna(0).astype('int')
    df.total_amount = df['total_amount'].fillna(0).astype('int')
    return df

def load(engine, file_loc, taxi_color):
    """
    Extracts sheets from Gdrive by specifying the url in the pandas read_excel function
    Args:
        url (str): the url of the spreadsheet which is the data source
        username (list): names of the sheets to be extracted
    Returns:
        df_i (pandas.dataframe): Pandas df containing inventory data
        df_p (pandas.dataframe): Pandas df containing production data
    """
    df_iter = pd.read_csv(file_loc, iterator=True, chunksize=100000, low_memory=False)
    df = next(df_iter)
    table_name = f'{taxi_color}_taxi_data'
    # inserting only column headers
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    while df is not None:
        s_time = time()
        df = transform(df)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        e_time = time()
        print(f'Inserted chunk in {e_time-s_time:.2f} seconds')
        df = next(df_iter, None)
    return None

def del_download(f_loc):
    """
    Deletes the csv written on disk
    Args:
        file_loc (str): file location on disk
    Return:
        None
    """
    os.remove(f_loc)
    print(f'File deletion from {f_loc} complete')

def main(taxi_color='yellow', year=2021, month=1)->None:
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
    url =f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_color}_tripdata_{year}-{month:02d}.parquet'
    f_loc = extract(url)
    print('Data Extraction Complete')
    engine = con_open(host, username, pwd, port, db_name)
    if engine is not None:
        load(engine, f_loc, taxi_color)
        print("Data Loading to DB Complete")
        con_close(engine)
        del_download(f_loc)

if __name__=="__main__":
    main()