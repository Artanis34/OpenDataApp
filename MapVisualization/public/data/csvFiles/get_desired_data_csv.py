import os
import pandas as pd

# Get the current directory (where the Python file is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the csv_file paths (in the same directory as the Python file)
csv_path_dienst = os.path.join(current_dir, "dienststellen_actualdate.csv")
csv_path_prm = os.path.join(current_dir, "prm_platforms.csv")

# Set the columns to select from the CSV file
selected_columns_dienst = ['SLOID', 'NUMMER', 'BEZEICHNUNG_OFFIZIELL', 'ORTSCHAFTSNAME', 'KANTONSNAME', 'E_WGS84', 'N_WGS84', 'GO_ABKUERZUNG_DE']
selected_columns_prm = ['DS_SLOID', 'STATUS']

# Rename for the columns
new_column_names_dienst = {
    'BEZEICHNUNG_OFFIZIELL': 'name',
    'ORTSCHAFTSNAME': 'ortschaft',
    'KANTONSNAME': 'kanton',
    'E_WGS84': 'Longitude',
    'N_WGS84': 'Latitude',
    'NUMMER': 'dienststellen-ID',
    'GO_ABKUERZUNG_DE' : 'service'
}
new_column_names_prm = {
    'STATUS': 'status',
    'DS_SLOID': 'SLOID'
}

try:
    # Read the CSV file and select the specified columns
    df_from_csv_dienst = pd.read_csv(csv_path_dienst, sep=';', skiprows=6, low_memory=False, usecols=selected_columns_dienst)
    df_from_csv_prm = pd.read_csv(csv_path_prm, sep=';', skiprows=6, low_memory=False, usecols=selected_columns_prm)

    # Rename the columns
    df_from_csv_dienst.rename(columns=new_column_names_dienst, inplace=True)
    df_from_csv_prm.rename(columns=new_column_names_prm, inplace=True)

    # Merge the two DataFrames based on SLOID, including null values
    merged_df = pd.merge(df_from_csv_dienst, df_from_csv_prm, left_on='SLOID', right_on='SLOID', how='left')

    # Replace NaN values with null and set status to 9 for null SLOID
    merged_df.loc[merged_df['status'].isnull(), 'status'] = 9
    merged_df = merged_df.fillna(99)

    # Create a new CSV file with the selected columns
    file = df_from_csv_dienst
    new_csv_file_merged = "merged_selected_columns.csv"
    new_csv_path_merged = os.path.join(current_dir, new_csv_file_merged)
    merged_df.to_csv(new_csv_path_merged, index=False)


except FileNotFoundError:
    print(f"CSV file not found: {file}")

except Exception as e:
    print(f"An error occurred while processing the CSV file: {str(e)}")