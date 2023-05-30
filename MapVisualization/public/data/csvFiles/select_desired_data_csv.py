"""
This script reads data from CSV files, performs data transformations, merges the data, and creates a new (merged_selected_columns.csv) file
in the same directory as itself.

Dependencies:
- os
- pandas

The script performs the following steps:
1. Reads ['dienststellen_actualdate', 'prm_platforms', 'verkehrspunktelemente_actualdate']CSV files.
2. Selects specific columns from each CSV file.
3. Renames columns for better readability.
4. Filters rows based on specific conditions.
5. Performs data cleaning and transformation.
6. Merges the data frames based on common columns.
7. Checks the validity of certain entries.
8. Updates values based on specific conditions.
9. Creates a new CSV file with the selected columns.
10. Prints a success message if the code runs successfully.

If any errors occur during the execution, appropriate error messages are printed.

Usage:
- Ensure that the required CSV files are present in the same directory as the script.
- Run the script to perform the data processing steps and create a new CSV file.

"""

import os
import pandas as pd

try:
    # Get the current directory (where the Python file is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the csv_file paths (in the same directory as the Python file)
    csv_path_dienst = os.path.join(current_dir, "dienststellen_actualdate.csv")
    csv_path_prm = os.path.join(current_dir, "prm_platforms.csv")
    csv_path_vk = os.path.join(current_dir, "verkehrspunktelemente_actualdate.csv")

    # Set the columns to select from the CSV file
    selected_columns_dienst = ['SLOID', 'GEMEINDENAME', 'LAENDERCODE', 'IS_HALTESTELLE', 'BEZEICHNUNG_OFFIZIELL', 'ORTSCHAFTSNAME', 'KANTONSNAME', 'E_WGS84', 'N_WGS84', 'GO_ABKUERZUNG_DE', 'BPVH_VERKEHRSMITTEL_TEXT_DE']
    selected_columns_prm = ['SLOID', 'STATUS', 'LEVEL_ACCESS_WHEELCHAIR', 'VALID_TO', 'VEHICLE_ACCESS']
    selected_columns_vk = ['BEZEICHNUNG', 'DS_SLOID', 'SLOID']

    # Read the CSV file and select the specified columns
    try:
        df_from_csv_dienst = pd.read_csv(csv_path_dienst, sep=';', skiprows=6, low_memory=False, usecols=selected_columns_dienst)
    except FileNotFoundError:
        raise FileNotFoundError("dienststellen_actualdate.csv file not found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("dienststellen_actualdate.csv file is empty.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("Error parsing dienststellen_actualdate.csv file.")

    try:
        df_from_csv_prm = pd.read_csv(csv_path_prm, sep=';', skiprows=6, low_memory=False, usecols=selected_columns_prm)
    except FileNotFoundError:
        raise FileNotFoundError("prm_platforms.csv file not found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("prm_platforms.csv file is empty.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("Error parsing prm_platforms.csv file.")

    try:
        df_from_csv_vk = pd.read_csv(csv_path_vk, sep=';', skiprows=6, low_memory=False, usecols=selected_columns_vk)
    except FileNotFoundError:
        raise FileNotFoundError("verkehrspunktelemente_actualdate.csv file not found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("verkehrspunktelemente_actualdate.csv file is empty.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("Error parsing verkehrspunktelemente_actualdate.csv file.")

    # Rename the columns for better readability
    new_column_names_dienst = {
        'BEZEICHNUNG_OFFIZIELL': 'Name',
        'ORTSCHAFTSNAME': 'Ortschaft',
        'GEMEINDENAME': 'Gemeinde',
        'KANTONSNAME': 'Kanton',
        'E_WGS84': 'Longitude',
        'N_WGS84': 'Latitude',
        'GO_ABKUERZUNG_DE' : 'Service',
        'BPVH_VERKEHRSMITTEL_TEXT_DE': 'Verkehrsmittel',
        'SLOID': 'SLOID_dienst'
    }
    new_column_names_prm = {
        'STATUS': 'Status',
        'LEVEL_ACCESS_WHEELCHAIR': 'Rollstuhl',
        'SLOID': 'SLOID_prm'
    }
    new_column_names_vk = {
        'SLOID': 'SLOID_prm',
        'DS_SLOID': 'SLOID_dienst',
        'BEZEICHNUNG': 'Bezeichung'
    }

    df_from_csv_dienst.rename(columns=new_column_names_dienst, inplace=True)
    df_from_csv_prm.rename(columns=new_column_names_prm, inplace=True)
    df_from_csv_vk.rename(columns=new_column_names_vk, inplace=True)

    # Filter:
    # rows where 'Laendercode' == 85, only CH and IS_HALTESTELLE == 1
    df_from_csv_dienst = df_from_csv_dienst[(df_from_csv_dienst['LAENDERCODE'] == 85) & (df_from_csv_dienst['IS_HALTESTELLE'] == 1)]
    # row where 'VALID_TO' == '2099-12-31'
    df_from_csv_prm = df_from_csv_prm[df_from_csv_prm['VALID_TO'] == '2099-12-31']

    # Perform data cleaning and transformation:
    # Remove the tilde (~) characters from 'BPVH_VERKEHRSMITTEL_TEXT_DE' column
    df_from_csv_dienst['Verkehrsmittel'] = df_from_csv_dienst['Verkehrsmittel'].str.replace('~', '')
    # Handle LEVEL_ACCESS_WHEELCHAIR entries, [0 & '' -> Zu vervollständigen, 1 -> Ja, 2 -> Nein]
    replacement_mapping_Rollstuhl = {0: None, 1: 'Yes', 2: 'No'}
    df_from_csv_prm['Rollstuhl'] = df_from_csv_prm['Rollstuhl'].replace(replacement_mapping_Rollstuhl)
    # Handle VEHICLE_ACCESS entries
    replacement_mapping_VEHICLE_ACCESS = {0: None, 11: 'Stufenloser Zugang, niveaugleicher Ein-/Ausstieg.',
                                           12: 'Stufenloser Zugang, Ein-/Ausstieg durch Personalhilfestellung, keine Voranmeldung nötig.',
                                             13: 'Stufenloser Zugang, Ein-/Ausstieg durch Personalhilfestellung, Voranmeldung nötig.',
                                               14: 'Für Rollstühle nicht benutzbar.'}
    df_from_csv_prm['VEHICLE_ACCESS'] = df_from_csv_prm['VEHICLE_ACCESS'].replace(replacement_mapping_VEHICLE_ACCESS)

    # Merge the DataFrames based on SLOIDs
    merged_df = pd.merge(df_from_csv_dienst, df_from_csv_vk, on='SLOID_dienst', how='left')
    merged_df = pd.merge(merged_df, df_from_csv_prm, on='SLOID_prm', how='right')

    # Update status to 0 for empty rows
    #merged_df.loc[merged_df.isnull().any(axis=1), 'Status'] = 0
    # Update status to 0 for rows with empty or null values in any column, except 
    # 'Bezeichung', 'VEHICLE_ACCESS', 'Rollstuhl'
    #columns_to_drop = ['Bezeichung', 'VEHICLE_ACCESS', 'Rollstuhl'] 
    #columns_to_check = merged_df.columns.drop(columns_to_drop)
    #merged_df.loc[merged_df[columns_to_check].isnull().any(axis=1), 'Status'] = 0

    # Create a new CSV file with the selected columns (with error handling)
    try:
        new_csv_file_merged = "merged_selected_columns.csv"
        new_csv_path_merged = os.path.join(current_dir, new_csv_file_merged)
        merged_df.to_csv(new_csv_path_merged, index=False)
    except Exception as e:
        raise Exception("Error occurred while creating the new CSV file:", str(e))

    # Print a success message if the code runs successfully
    print("select_desired_data_csv successful")

except FileNotFoundError as e:
    print("Error occurred: File not found -", str(e))
except pd.errors.EmptyDataError as e:
    print("Error occurred: Empty data -", str(e))
except pd.errors.ParserError as e:
    print("Error occurred: Parsing error -", str(e))
except Exception as e:
    print("Error occurred:", str(e))