import dask.dataframe as dd
from src.config import DATA_PATH

def load_data():
    """
    carga de datos parquet con dask 
    """
    df = dd.read_parquet(DATA_PATH)
    return df
