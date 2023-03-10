
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import pandas as pd

import csv

def colormap():
    path_file_x = "./csv/ox.csv"
    path_file_y = "./csv/oy.csv"

    path_file_1 = "./csv/o2.csv"
    path_file_2 = "./csv/o3.csv"
    path_file_3 = "./csv/oy.csv"

    
    #m0 = pd.read_csv(path_file_0, sep=";").to_numpy(dtype=np.float64)
    #m1 = pd.read_csv(path_file_1, sep=";").to_numpy(dtype=np.float64)
    #m2 = pd.read_csv(path_file_2, sep=";").to_numpy(dtype=np.float64)
    #m3 = pd.read_csv(path_file_3, sep=";").to_numpy(dtype=np.float64)
    mx = pd.read_csv(path_file_x, sep=";").to_numpy(dtype=np.float64)
    my = pd.read_csv(path_file_y, sep=";").to_numpy(dtype=np.float64)

    mr = mx - my

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = mr
    im = plt.imshow(data2D, cmap="Reds")
    plt.colorbar(im)
    plt.show()


