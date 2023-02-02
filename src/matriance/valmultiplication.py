import os

def cachegrind(command_args : list):
    new_string = ''
    for arg in command_args:
        new_string += ' '
        new_string += arg
    os.system(f"valgrind --tool=cachegrind --log-file=d1_rates.txt{new_string} o")
    with open("d1_rates.txt") as tempf:
        output = tempf.read()
        crazy_list = output.split("D1  miss rate:")[-1].split(' ')
        for item in crazy_list:
            if item == '': crazy_list.remove('')
        d1_o_rate = float(crazy_list[0].split('%')[0])
    os.system(f"valgrind --tool=cachegrind --log-file=d1_rates.txt{new_string} t")
    with open("d1_rates.txt") as tempf:
        output = tempf.read()
        crazy_list = output.split("D1  miss rate:")[-1].split(' ')
        for item in crazy_list:
            if item == '': crazy_list.remove('')
        d1_t_rate = float(crazy_list[0].split('%')[0])
    print(f"MulM1M2 | D1 Miss Rate: {d1_o_rate}")
    print(f"MulM1M2T | D1 Miss Rate: {d1_t_rate}")
    for path in os.listdir(os.getcwd()):
        if path.startswith("a_matrix") or path.startswith("b_matrix") or path.startswith("result"):
            os.remove(path)