import pandas as pd
import numpy as np

def find_protocol_proxy(csv_path):
    df = pd.read_csv(csv_path, nrows=5000)
    df.columns = df.columns.str.strip()
    
    potential_cols = []
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64', 'int32', 'uint32']:
            unique_vals = set(df[col].unique())
            # Protocol is typically 6, 17, 0. Let's see if any col contains only these.
            if unique_vals.issubset({0, 6, 17, np.nan}):
                potential_cols.append(col)
    
    return potential_cols

import glob
import os
files = glob.glob('../datasets/*.csv')
if files:
    res = find_protocol_proxy(files[0])
    print(f"Potential protocol columns in {os.path.basename(files[0])}: {res}")
else:
    print("No CSV files found.")
