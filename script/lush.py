import os
import pandas as pd
import json

# Get the directory in which this Python script resides
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct absolute file paths
input_file_path = os.path.join(script_dir, 'in', 'in.json')
dataset_file_path = os.path.join(script_dir, 'data', 'dataset.csv')
output_file_path = os.path.join(script_dir, 'out', 'out.json')

# Read in file
with open(input_file_path, 'r') as f:
    file_in = f.read()

# Convert to json
file_in_json = json.loads(file_in)

# Convert to dataframe
pd_in = pd.json_normalize(file_in_json)

# Predict
prod_id_pred = 881331

# Read all dataset
pd_out = pd.read_csv(dataset_file_path)

# Lookup to for predicted value
pd_out_pred = pd_out[pd_out.product_id == prod_id_pred]

# Convert to json
file_out_json = pd_out_pred.to_json()

# Save the file
with open(output_file_path, 'w') as f:
    f.write(file_out_json)