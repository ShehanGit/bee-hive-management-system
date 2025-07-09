import pandas as pd
import numpy as np

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Loads the dataset from an Excel file and performs basic cleaning.
    
    :param file_path: Path to the Excel file.
    :return: Cleaned pandas DataFrame.
    """
    # 1. Load Excel data
    df = pd.read_excel(file_path)
    
    # 2. Basic cleaning: drop duplicates, reset index
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # 3. Handle missing values (Fix inplace issue)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())  # ✅ FIXED
    
    return df

if __name__ == "__main__":
    data = load_and_clean_data(".\data\hive_data.xlsx")    
    print(data.head())
