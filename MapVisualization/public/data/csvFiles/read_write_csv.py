import os
import pandas as pd
import geojson
import math

# Set the variable csv_file to the file you want to read
csv_file = "dienststellen_actualdate.csv"

# Get the current directory (where the Python file is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the csv_file path (in the same directory as the Python file)
csv_path = os.path.join(current_dir, csv_file)

# Read the CSV file and skip the first 6 lines, specifying the separator as ';'
df_from_csv = pd.read_csv(csv_path, sep=';', skiprows=6, low_memory=False)

# Get selected columns for the GeoJSON properties and rename them
selected_columns = ['STATUS', 'BEZEICHNUNG_OFFIZIELL', 'E_WGS84', 'N_WGS84']
column_names = ['Status', 'Name', 'Longitude', 'Latitude']
df_selected = df_from_csv[selected_columns].rename(columns=dict(zip(selected_columns, column_names)))

# Replace NaN values with None
df_selected = df_selected.where(df_selected.notna(), None)

# Create a list of GeoJSON features
features = []
for index, row in df_selected.iterrows():
    # Check if the coordinates are valid numbers
    if math.isnan(row['Longitude']) or math.isnan(row['Latitude']):
        continue

    # Check if the coordinates are within a reasonable range
    if abs(row['Longitude']) > 180 or abs(row['Latitude']) > 90:
        continue

    geometry = geojson.Point((row['Longitude'], row['Latitude']))
    properties = {
        'Status': row['Status'],
        'Name': row['Name']
    }
    feature = geojson.Feature(geometry=geometry, properties=properties)
    features.append(feature)

# Create a GeoJSON feature collection
feature_collection = geojson.FeatureCollection(features)


# Set the output GeoJSON file path to the parent directory of the current directory
geojson_file = "geoData.geojson"
output_dir = os.path.dirname(current_dir)
geojson_path = os.path.join(output_dir, geojson_file)

with open(geojson_path, 'w') as geojson_file:
    geojson.dump(feature_collection, geojson_file)