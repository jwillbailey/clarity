import numpy as np
import pandas as pd
import os
import json

filepath = "../../haspi_eval"

files = os.listdir(filepath)

si = {f : pd.read_csv(os.path.join(filepath, f)).describe().to_dict() for f in files}

json.dump(si, open("supplimentary_haspi_scores.json", "w"))