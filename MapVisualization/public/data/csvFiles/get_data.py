"""
This script downloads CSV files from the provided URLs using the requests library.

Dependencies:
- requests
- os

The script performs the following steps:
1. Downloads the 'dienststellen_actualdate.csv' file from a given URL.
2. Downloads the 'verkehrspunktelemente_actualdate.csv' file from a given URL.
3. Downloads the 'prm_platforms.csv' file from a given URL.
4. Saves the downloaded files to disk in the current directory.
5. Prints a success message if the code runs successfully.

If any errors occur during the execution, appropriate error messages are printed.

Usage:
- Run the script to download the required CSV files.

"""

import requests
import os

# Try get_data.py
try:
    # Get the current directory (where the Python file is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    #dienststellen_actualdate
    # Permalink URL of the file to download
    permalink_url = 'https://opentransportdata.swiss/en/dataset/didok/resource_permalink/dienststellen_actualdate.csv'

    # Send a GET request to the permalink URL
    response = requests.get(permalink_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the file content from the response
        file_content = response.content

        # Save the file to disk
        file_path = os.path.join(current_dir, 'dienststellen_actualdate.csv')
        with open(file_path, 'wb') as file:
            file.write(file_content)
    else:
        # Handle the case when the request was not successful
        print('Error downloading dienststellen_actualdate file from the permalink.')

    # verkehrspunktelemente_actualdate
    # Permalink URL of the file to download
    permalink_url = 'https://opentransportdata.swiss/en/dataset/didok/resource_permalink/verkehrspunktelemente_actualdate.csv'

    # Send a GET request to the permalink URL
    response = requests.get(permalink_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the file content from the response
        file_content = response.content

        # Save the file to disk
        file_path = os.path.join(current_dir, 'verkehrspunktelemente_actualdate.csv')
        with open(file_path, 'wb') as file:
            file.write(file_content)
    else:
        # Handle the case when the request was not successful
        print('Error downloading verkehrspunktelemente_actualdate file from the permalink.')

    # prm_platforms
    # Permalink URL of the file to download
    permalink_url = 'https://opentransportdata.swiss/de/dataset/prm_data/resource_permalink/prm_platforms.csv'

    # Send a GET request to the permalink URL
    response = requests.get(permalink_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the file content from the response
        file_content = response.content

        # Save the file to disk
        file_path = os.path.join(current_dir, 'prm_platforms.csv')
        with open(file_path, 'wb') as file:
            file.write(file_content)
    else:
        # Handle the case when the request was not successful
        print('Error downloading prm_platforms file from the permalink.')

    # Print if code ran successfull
    print("get_data successfull")
except Exception as e:
    print("Error occurred:", str(e))