"""
DISCLAIMER: This python cript is not implemented into the process, since we did not have time to adapt the corrected GeoJSON points in JS
It does point the correct markers accordingly to the Dienststelle but we got problems in the userface so we just kept the other one
with only the GeoPoints of dienstelle.csv.
You have to implement the "select_desired_dat_csv_2" script aswell.

Script: geoData2.py

Description:
This script reads a CSV file containing geographical data, processes the data, and creates a GeoJSON file and additional JSON files. The GeoJSON file contains GeoJSON features representing points within Switzerland, and the additional JSON files contain lists of unique values for kanton, gemeinde, and service.

Dependencies:
- json
- os
- pandas (as pd)
- geojson

Steps:
1. Read the CSV file.
2. Process the data and create GeoJSON features for points within Switzerland.
3. Create additional lists for unique values of kanton, gemeinde, and service.
4. Create a GeoJSON feature collection from the generated features.
5. Set the output paths for the GeoJSON and JSON files.
6. Write the GeoJSON feature collection to a GeoJSON file.
7. Write the additional lists to separate JSON files.

Usage:
- Ensure that the 'merged_selected_columns.csv' file is in the same directory as this script.
- Run the script to generate the GeoJSON and JSON files.

Author: Julien Chopin
Date: 31.05.2023
"""

from datetime import datetime
import json
import os
import pandas as pd
import geojson


# Functions:
# Function to check if a point is within Switzerland
def is_within_switzerland(longitude, latitude):
    switzerland_bbox = (5.9559, 45.818, 10.4921, 47.8084)  # Bounding box coordinates of Switzerland
    if longitude >= switzerland_bbox[0] and longitude <= switzerland_bbox[2] and latitude >= switzerland_bbox[1] and latitude <= switzerland_bbox[3]:
        return True
    else:
        return False
    
# Create a method to create properties for GeoJSON features
def create_properties(row):
    return {
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
            longitude_dienst = row['Longitude_dienst']
            latitude_dienst = row['Latitude_dienst']
            longitude_vk = row['Longitude_vk']
            latitude_vk = row['Latitude_vk']

             # Check if the values are numeric and not empty strings
            if longitude_dienst and latitude_dienst and longitude_vk and latitude_vk:
                try:
                    longitude_dienst = float(longitude_dienst)
                    latitude_dienst = float(latitude_dienst)
                    longitude_vk = float(longitude_vk)
                    latitude_vk = float(latitude_vk)
                except ValueError:
                    # Skip the current iteration if any of the values are non-numeric
                    continue

                if is_within_switzerland(longitude_dienst, latitude_dienst) and is_within_switzerland(longitude_vk, latitude_vk):
                    if longitude_dienst == longitude_vk:
                        geometry = geojson.Point((longitude_dienst, latitude_dienst))
                        properties = create_properties(row)
                        feature = geojson.Feature(geometry=geometry, properties=properties)
                        features.append(feature)
                    else:
                        geometry_dienst = geojson.Point((longitude_dienst, latitude_dienst))
                        properties_dienst = create_properties(row)
                        feature_dienst = geojson.Feature(geometry=geometry_dienst, properties=properties_dienst)
                        features.append(feature_dienst)
                        geometry_vk = geojson.Point((longitude_vk, latitude_vk))
                        properties_vk = create_properties(row)
                        feature_vk = geojson.Feature(geometry=geometry_vk, properties=properties_vk)
                        features.append(feature_vk)
                else:
                    # Add properties to the separate JSON file for entries outside Switzerland
                    properties = create_properties(row)
                    notFeatures.append(properties)
            else:
                # Add properties to the separate JSON file for entries with missing or non-numeric longitude and/or latitude
                properties = create_properties(row)
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