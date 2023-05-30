"""
Executes multiple Python scripts to perform data processing tasks.

This function runs three Python scripts in separate processes to perform data processing tasks:
1. get_data.py: Downloads files from specified URLs.
2. select_desired_data_csv.py: Reads and filters CSV files, performs column renaming and merging.
3. geoData.py: Processes geographical data.

Each script is executed using `subprocess.run()` to run it in a separate process.

Raises:
    Exception: If an error occurs while executing any of the Python scripts.
"""

import subprocess
import os
import schedule

def data():
    # Get the current directory (where the Python file is located)
    directory_path = os.path.join(os.path.dirname(__file__), 'csvFiles')

    try:
        # Run get_data.py script
        file_path = os.path.join(directory_path, 'get_data.py')
        subprocess.run(['python', file_path], check=True)
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        # Run select_desired_data_csv.py script
        file_path = os.path.join(directory_path, 'select_desired_data_csv.py')
        subprocess.run(['python', file_path], check=True)
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        # Run geoData.py script
        file_path = os.path.join(directory_path, 'geoData.py')
        subprocess.run(['python', file_path], check=True)
    except Exception as e:
        print(f"An error occurred: {e}")

data()
# Update data everyday at midnight
#schedule.every().day.at("00:00").do(data())