import sys
from colormap.colormap import colormap
from matriance.ramultiplication import raising_multiplication

if(__name__ == "__main__"):
    c_type = sys.argv[1]
    if(c_type == "-c"):
        colormap()
        
    elif(c_type == "-m"):
        times = int(sys.argv[2])
        raising_multiplication(sys.argv[3:], times)