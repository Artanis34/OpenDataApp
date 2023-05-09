import os
import pandas as pd

### ONLY FOR TEST
import numpy as np
###

# Set the variable csv_file to the file you want to read
csv_file = "dienststellen_actualdate.csv"

# Get the csv_file path (should always be in .../OpenDataApp/csvFiles/...)
csv_path = os.path.join(os.getcwd(), "csvFiles", csv_file)

# Read the CSV file, specifying the delimiter and skipping the first few lines
df_from_csv = pd.read_csv(csv_path, delimiter=';', skiprows= 6, low_memory=False)

# Get geoData for map
selected_columns = ['BEZEICHNUNG_OFFIZIELL', 'E_WGS84', 'N_WGS84']
df_selected = df_from_csv[selected_columns]

# Rename the selected columns
new_column_names = {'BEZEICHNUNG_OFFIZIELL': 'name', 'E_WGS84': 'x', 'N_WGS84': 'y'}
df_renamed = df_selected.rename(columns=new_column_names)

### ONLY FOR TEST
# Create a new column with random integers from 1 to 3
df_renamed['status'] = np.random.randint(1, 4, size=len(df_renamed))
###

# Save renamed columns as JSON file
json_file = 'data.json'
df_renamed.to_json(json_file, orient='records')