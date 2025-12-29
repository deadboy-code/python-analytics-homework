import pandas as pd
import datetime as dt
from pathlib import Path

def eda_open(file='data.csv'):
    """
    This function reads a CSV file into a pandas DataFrame and creates a backup
    of the file with the current date in a 'backups' directory if a backup for
    today does not already exist.

    Parameters:
    file (str): The path to the CSV file to be read. Default is 'data.csv'.

    Returns:
    pd.DataFrame: The DataFrame containing the data from the CSV file.
    """

    df = pd.read_csv(file)
    today = dt.datetime.today().strftime('%d_%m_%Y')
    Path("backups").mkdir(parents=True, exist_ok=True)
    file_list = list(Path("backups").iterdir())
    for i in Path('backups').iterdir():
        file_list.append(i.name)
    if f"backup_{today}.csv" in file_list:
        with (Path("backups") / f"backup_{today}.csv").open("a") as f:
            f.write(f"\n{'='*100}\n{dt.datetime.now()}\n{'='*100}\n")
            df.to_csv(f, index=False)
        print("Appended new data to the existing backup.")
        return df
    else:
        with (Path("backups") / f"backup_{today}.csv").open("x") as f:
            f.write(f"{'='*100}\n{dt.datetime.now()}\n{'='*100}\n")
            df.to_csv(f, index=False)
        print("Created a new backup.")
        return df

def eda_nan_check(df):
    """
    This function takes a pandas DataFrame as input and returns a DataFrame
    showing the count and percentage of missing values for each column.

    Parameters:
    df (pd.DataFrame): The input DataFrame to check for missing values.

    Returns:
    pd.DataFrame: A DataFrame with columns 'Missing Values' and 'Percentage'
                  indicating the count and percentage of missing values per column.
    """
    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100

    missing_df = pd.DataFrame({
        'Missing Values': missing_count,
        'Percentage': missing_percentage
    })

    return missing_df[missing_df['Missing Values'] > 0]