import pandas as pd
import os

def convert_parquet_to_csv(parquet_file_path, csv_output_path):
    print(f"Reading Parquet from: {parquet_file_path}")
    
    # 1. Read the Parquet file into a Pandas DataFrame
    try:
        df = pd.read_parquet(parquet_file_path)
    except FileNotFoundError:
        print(f"Error: The file '{parquet_file_path}' was not found.")
        return

    print(f"Successfully loaded {len(df)} rows.")
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(csv_output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Write the DataFrame to a Parquet file (using pyarrow engine by default)
    df.to_csv(csv_output_path, index=False) # index=False prevents saving the Pandas index as a column

    print(f"Successfully converted and saved to: {csv_output_path}")

if __name__ == "__main__":
    # Define your specific input and output paths here
    input_parquet = 'data/processed/btc_1h.parquet'
    output_csv = 'data/processed/btc_1h_from_btc_1h_parquet.csv'
    
    convert_parquet_to_csv(input_parquet, output_csv)