# Import loibraries
import os
import pandas as pd
import json
import random
import sys
import joblib
from sklearn.linear_model import LogisticRegression

script_dir = os.path.dirname(os.path.realpath(__file__))

input_file_path = os.path.join(script_dir, 'in', 'in.json')
dataset_file_path = os.path.join(script_dir, 'data', 'dataset.csv')
output_file_path = os.path.join(script_dir, 'out', 'out.json')
model_file_path = os.path.join(script_dir, 'data', 'model_pipeline.pkl')

def rand():
    return random.randint(pd_out.product_id.min(), pd_out.product_id.max())

# Read in file
with open(input_file_path, 'r') as f:
    file_in = f.read()

# Convert to json
file_in_json = json.loads(file_in)

# Convert to dataframe
pd_in = pd.json_normalize(file_in_json)

# Read all dataset
pd_out = pd.read_csv(dataset_file_path)

# Array of predictions
prod_id_pred_lst = []

# Predict
if sys.argv[1] == 'rand':
    
    # Predict random
    prod_id_pred = rand()
    prod_id_pred_lst.append(prod_id_pred)
    # Get the 2nd value
    for i in range(5):
        prod_id_pred = rand()
        if prod_id_pred not in prod_id_pred_lst:
            prod_id_pred_lst.append(prod_id_pred)
            break
    text = 'Predicted using a random product ids = ' + str(prod_id_pred_lst) 
    
elif sys.argv[1] == 'id':
    
    # Predict id
    prod_id_pred_lst.append(int(sys.argv[2]))
    prod_id_pred_lst.append(int(sys.argv[3]))
    text = 'Predicted using the product ids = ' + str(prod_id_pred_lst)
    
else:
    
    # Predict using model
    model = joblib.load(model_file_path)
    prod_id_pred = model.predict(pd_in)[0]
    prod_id_pred_lst.append(prod_id_pred)
    # Get the 2nd value
    for i in range(5):
        prod_id_pred = rand()
        if prod_id_pred not in prod_id_pred_lst:
            prod_id_pred_lst.append(prod_id_pred)
            break
    text = 'Predicted using the model'

# Lookup to for predicted value
pd_out_pred = pd_out[pd_out.product_id.isin(prod_id_pred_lst)]

# Convert to json
file_out_json = pd_out_pred.to_json(orient="records")

# Save the file
with open(output_file_path, 'w') as f:
    f.write(file_out_json)
    
# Print the result
print(text)