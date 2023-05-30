"""
This script reads a CSV file, processes the data, and creates a GeoJSON file and additional JSON files.

Dependencies:
- json
- os
- pandas (as pd)
- geojson

The script performs the following steps:
1. Read the CSV file.
2. Process the data and create GeoJSON features.
3. Create additional lists for unique values.
4. Create a GeoJSON feature collection.
5. Set the output paths for the GeoJSON and JSON files.
6. Write the GeoJSON feature collection to a GeoJSON file.
7. Write the additional lists to separate JSON files.

If any errors occur during the execution, appropriate error messages are printed.

Usage:
- Ensure that the 'merged_selected_columns.csv' file is in the same directory as this script.
- Run the script to generate the GeoJSON and JSON files.

"""

from datetime import datetime
import json
import os
import pandas as pd
import geojson

# Try geoData.py
try:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Try reading CVS file
    try:
        # Get the current directory (where the Python file is located)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Get the csv_file path (in the same directory as the Python file)
        csv_path = os.path.join(current_dir, "merged_selected_columns.csv")

        # Read the CSV file
        df_from_csv = pd.read_csv(csv_path, sep=',', low_memory=False)
        df_from_csv = df_from_csv.fillna('')
    except Exception as e:
        print("Error occurred while reading the CSV file:", str(e))

    # Try make GeoJSON points/features
    try:
        # Create lists
        features = [] # List to store GeoJSON features
        notFeatures = [] # List to store entries without longitude and/or latitude
        service_list = []  # List to store unique service values
        kanton_list = []  # List to store unique kanton values
        gemeinde_in_kanton = {} # Create a dictionary to map Gemeinde to Kanton

        

        # Iterate over every index
        for index, row in df_from_csv.iterrows():
            if row['Kanton'] != '' and row['Gemeinde'] != '':
                # Add Gemeinde to Kanton mapping to the dictionary
                gemeinde_in_kanton[row['Gemeinde']] = row['Kanton']

        # Create a new dictionary to store Gemeinde under the same Kanton
        kanton_gemeinde_dict = {}

        # Iterate over every Gemeinde and Kanton in the gemeinde_to_kanton dictionary
        for gemeinde, kanton in gemeinde_in_kanton.items():
            if kanton not in kanton_gemeinde_dict:
                # Create a new list for the Gemeinden under the Kanton if it doesn't exist
                kanton_gemeinde_dict[kanton] = [gemeinde]
            else:
                # Append the Gemeinde to the list under the respective Kanton
                kanton_gemeinde_dict[kanton].append(gemeinde)
        # Sort the Gemeinden within each Kanton in alphabetical order
        for kanton, gemeinden in kanton_gemeinde_dict.items():
            kanton_gemeinde_dict[kanton] = sorted(gemeinden)

        # Update the gemeinde_list with the modified structure
        gemeinde_list = []
        for kanton, gemeinden in kanton_gemeinde_dict.items():
            gemeinde_list.append({
                'Kanton': kanton,
                'Gemeinden': gemeinden
            })

        # Iterate over every index
        for index, row in df_from_csv.iterrows():
            if row['Longitude_dienst'] != '' and row['Latitude_dienst'] != '':
                geometry = geojson.Point((row['Longitude_dienst'], row['Latitude_dienst']))
                properties = {
                    'Name': row['Name'],
                    'Ortschaft': row['Ortschaft'],
                    'Gemeinde': row['Gemeinde'],
                    'Kanton': row['Kanton'],
                    'Verkehrsmittel': row['Verkehrsmittel'],
                    'Rollstuhl': row['Rollstuhl'],
                    'Zugang zum Perron/Einstieg ins Fahrzeug': row['VEHICLE_ACCESS'],
                    'Status': row['Status'],
                    'Service': row['Service'],
                    'SLOID': row['SLOID_prm'],
                    'Bezeichnung': row['Bezeichung']
                }
                feature = geojson.Feature(geometry=geometry, properties=properties)
                features.append(feature)
            else:
                # Add properties to the separate JSON file for entries with missing longitude and/or latitude
                properties = {
                    'Name': row['Name'],
                    'Ortschaft': row['Ortschaft'],
                    'Gemeinde': row['Gemeinde'],
                    'Kanton': row['Kanton'],
                    'Verkehrsmittel': row['Verkehrsmittel'],
                    'Rollstuhl': row['Rollstuhl'],
                    'Zugang zum Perron/Einstieg ins Fahrzeug': row['VEHICLE_ACCESS'],
                    'Status': row['Status'],
                    'Service': row['Service'],
                    'SLOID': row['SLOID_prm'],
                    'Bezeichnung': row['Bezeichung']
                }
                notFeatures.append(properties)

            # Add service value to the list if it doesn't already exist
            if row['Service'] != '' and row['Service'] not in service_list:
                service_list.append(row['Service'])

            # Add service value to the list if it doesn't already exist
            if row['Kanton'] != '' and row['Kanton'] not in kanton_list:
                kanton_list.append(row['Kanton'])

    except Exception as e:
        print("Error occurred while processing the data:", str(e))

    # Try to creat GeoJSON feature collection
    try:
        feature_collection = geojson.FeatureCollection(features)
    except Exception as e:
        print("Error occurred while creating the GeoJSON feature collection:", str(e))

    # Try to create a dictionary for the additional lists
    try:
        gemeinde_list = sorted(gemeinde_list, key=lambda x: x['Kanton'])
        additional_lists = {
            'Kanton': sorted(kanton_list),
            'Gemeinde':gemeinde_list,
            'Service': sorted(service_list),
            'Last_modified': current_time
        }
    except Exception as e:
        print("Error occurred while creating the additional lists:", str(e))

    # Try to set output paths for files to save
    try:
        # Get the parent directory of the current directory
        output_dir = os.path.dirname(current_dir)

        # Set the output path for the geoData.geojson file
        geojson_file = "geoData.geojson"
        geojson_path = os.path.join(output_dir, geojson_file)

        # Set the output path for the kantonAndService.json file
        json_file_kAS = "kantonAndService.json"
        json_path_kAS = os.path.join(output_dir, json_file_kAS)

        # Set the output path for the notFeatures.json file
        json_file_nF = "notFeatures.json"
        json_path_nF = os.path.join(output_dir, json_file_nF)
    except Exception as e:
        print("Error occurred while setting the output paths:", str(e))

    # Try to write the GeoJSON feature collection to the GeoJSON file
    try:
        with open(geojson_path, 'w', encoding='utf-8') as geojson_file:
            geojson.dump(feature_collection, geojson_file, ensure_ascii=False)
    except Exception as e:
        print("Error occurred while writing the GeoJSON file:", str(e))

    # Try to write the additional lists to the kantonAndService JSON file
    try:
        with open(json_path_kAS, 'w', encoding='utf-8') as json_file:
            json.dump(additional_lists, json_file, ensure_ascii=False)
    except Exception as e:
        print("Error occurred while writing the kantonAndService JSON file:", str(e))

    # Try to write the additional lists to the notFeatures JSON file
    try:
        with open(json_path_nF, 'w', encoding='utf-8') as json_file:
            json.dump(notFeatures, json_file, ensure_ascii=False)
    except Exception as e:
        print("Error occurred while writing the notFeatures JSON file:", str(e))

except Exception as e:
    print("Error occurred:", str(e))