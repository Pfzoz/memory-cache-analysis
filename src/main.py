import sys
from colormap.colormap import colormap
from matriance.ramultiplication import raising_multiplication
from matriance.valmultiplication import cachegrind

if(__name__ == "__main__"):
    c_type = sys.argv[1]
    if(c_type == "-c"):
        colormap()
        
    elif(c_type == "-m"):
        args = sys.argv[:]
        z_times = int(args[2])
        times = int(args[3])
        raising = 200
        for i, arg in enumerate(args):
            if "raising=" in arg:
                raising = int(arg.split("raising=")[1])
                args.remove(arg)
        raising_multiplication(args[4:], times, z_times=z_times, raising=raising)

    elif(c_type == '-v'):
        args = sys.argv[:]
        args = args[2:]
        cachegrind(args)