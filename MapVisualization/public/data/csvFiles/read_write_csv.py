import json
import os
import pandas as pd
import geojson

# Get the current directory (where the Python file is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the csv_file path (in the same directory as the Python file)
csv_path = os.path.join(current_dir, "merged_selected_columns.csv")

# Read the CSV file
df_from_csv = pd.read_csv(csv_path, sep=',', low_memory=False)
df_from_csv = df_from_csv.fillna('')

# Create lists
features = [] # List to store GeoJSON features
notFeatures = [] # List to store entries without longitude and/or latitude
kanton_list = []  # List to store unique kanton values
service_list = []  # List to store unique service values

 # Iterate over every index
for index, row in df_from_csv.iterrows():
    if row['Longitude'] != '' and row['Latitude'] != '':
        geometry = geojson.Point((row['Longitude'], row['Latitude']))
        properties = {
            'Name': row['Name'],
            'Ortschaft': row['Ortschaft'],
            'Kanton': row['Kanton'],
            'Status': row['Status'],
            'Dienststellen-ID': row['Dienststellen-ID'],
            'Service': row['Service']
        }
        feature = geojson.Feature(geometry=geometry, properties=properties)
        features.append(feature)
    else:
        # Add properties to the separate JSON file for entries with missing longitude and/or latitude
        properties = {
            'Name': row['Name'],
            'Ortschaft': row['Ortschaft'],
            'Kanton': row['Kanton'],
            'Status': row['Status'],
            'Dienststellen-ID': row['Dienststellen-ID'],
            'Service': row['Service']
        }
        notFeatures.append(properties)

    # Add kanton value to the list if it doesn't already exist
    if row['Kanton'] != '' and row['Kanton'] not in kanton_list:
        kanton_list.append(row['Kanton'])

    # Add service value to the list if it doesn't already exist
    if row['Service'] not in service_list:
        service_list.append(row['Service'])



# Create a GeoJSON feature collection
feature_collection = geojson.FeatureCollection(features)

# Create a dictionary for the additional lists
additional_lists = {
    'Kanton': sorted(kanton_list),
    'Service': sorted(service_list)
}

# Get the parent directory of the current directory
output_dir = os.path.dirname(current_dir)

# Set the output path for the geoData.geojson file
geojson_file = "geoData.geojson"
geojson_path = os.path.join(output_dir, geojson_file)

# Set the output path for the kantonAndService.json file
json_file = "kantonAndService.json"
json_path_kAS = os.path.join(output_dir, json_file)

# Set the output path for the notFeatures.json file
json_file = "notFeatures.json"
json_path_nF = os.path.join(output_dir, json_file)

# Write the GeoJSON feature collection to the GeoJSON file
with open(geojson_path, 'w', encoding='utf-8') as geojson_file:
    geojson.dump(feature_collection, geojson_file, ensure_ascii=False)

# Write the additional lists to the JSON file
with open(json_path_kAS, 'w', encoding='utf-8') as json_file:
    json.dump(additional_lists, json_file, ensure_ascii=False)

# Write the additional lists to the JSON file
with open(json_path_nF, 'w', encoding='utf-8') as json_file:
    json.dump(notFeatures, json_file, ensure_ascii=False)