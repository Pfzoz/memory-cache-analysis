import csv

def colormap(file_1, file_2, file_3):
    path_file_1 = file_1
    path_file_2 = "./csv/"+file_2
    path_file_3 = "./csv/"+file_3

    with open("o1.csv") as File:
        Line_reader = csv.reader(File)
        print(Line_reader)