import os
import pandas as pd

#set variable csv_file to file you want to read
csv_file = "./dienststellen_actualdate.csv"
#read csv file 
df_from_csv = pd.read_csv(os.path.join(os.path.dirname(__file__), csv_file))
