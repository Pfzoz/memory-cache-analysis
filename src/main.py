import sys
from colormap.colormap import colormap

O1_FILE_NAME = "o1.csv"
O2_FILE_NAME = "o2.csv"
O3_FILE_NAME = "o3.csv"

if(__name__ == "__main__"):
    type = sys.argv[1]
    if(type == "-c"):
        colormap(O1_FILE_NAME, O2_FILE_NAME, O3_FILE_NAME)
        

    elif(type == "-m"):
        # c_file_name = 
        # matrix_size_1 = 
        # matrix_size_2 =
        pass