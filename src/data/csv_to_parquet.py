import pandas as pd
import os

def convert_csv_to_parquet(csv_file_path, parquet_output_path):
    print(f"Reading CSV from: {csv_file_path}")
    
    # 1. Read the CSV file into a Pandas DataFrame
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
        return

    print(f"Successfully loaded {len(df)} rows.")
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(parquet_output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Write the DataFrame to a Parquet file (using pyarrow engine by default)
    df.to_parquet(parquet_output_path, index=False) # index=False prevents saving the Pandas index as a column

    print(f"Successfully converted and saved to: {parquet_output_path}")

if __name__ == "__main__":
    # Define your specific input and output paths here
    input_csv = 'data/raw/btc_1h.csv'
    output_parquet = 'data/raw/btc_1h.parquet'
    
    convert_csv_to_parquet(input_csv, output_parquet)
