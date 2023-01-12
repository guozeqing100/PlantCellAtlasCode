import pandas as pd
import numpy as np

data_dict = {
    "temperature": ['43', '23', '34', '32', 23.23, 45],
    "humidity": [4, 2, 34, 32, 23, 45],
    "wind_scale": [4.1, 2.3, 3.4, 3.5, 2.3, 4.6]
}
data = pd.DataFrame(data_dict)
print(data)
data['mean'] = data.mean(axis=1)
print(data)
