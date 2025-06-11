import numpy as np
import pandas as pd

def process_data(data_file, params):

    data_points = np.array(pd.read_csv(data_file))  # reads in CSV as dataframe and converts to array

    dx = params['dx']
    dy = params['dy']
    dz  = params['dz']

    x_min = params['x_min']
    y_min = params['y_min']
    z_min = params['z_min']

    x, y, z = data_points[:,0], data_points[:,1], data_points[:,2]

    x_idx = (x - x_min) / dx
    y_idx = (y - y_min) / dy
    z_idx = (z - z_min) / dz

    data_idx = np.array([x_idx, y_idx, z_idx]).T.astype(int)

    return data_points, data_idx

