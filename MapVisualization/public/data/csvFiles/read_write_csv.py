import os
import pandas as pd
import geojson
import math

# Get the current directory (where the Python file is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the csv_file path (in the same directory as the Python file)
csv_path = os.path.join(current_dir, "merged_selected_columns.csv")

# Read the CSV file
df_from_csv = pd.read_csv(csv_path, sep=',', low_memory=False)

# Create a list of GeoJSON features
features = []
for index, row in df_from_csv.iterrows():
    # Check if the coordinates are valid numbers
    if math.isnan(row['Longitude']) or math.isnan(row['Latitude']):
        continue

    # Check if the coordinates are within a reasonable range
    if abs(row['Longitude']) > 180 or abs(row['Latitude']) > 90:
        continue

    geometry = geojson.Point((row['Longitude'], row['Latitude']))
    properties = {
        'status': row['status'],
        'name': row['name']
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