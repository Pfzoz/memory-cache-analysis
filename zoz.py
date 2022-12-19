from os import system, remove, listdir, getcwd
from subprocess import check_output, run
from sys import argv

if __name__ != '__main__':
    # python ./mulmatriz.c 750 750 750 750 200 t
    # 0      1             2   3   4   5   6   7
    total_o_elapsed = 0
    total_t_elapsed = 0
    total_tt_elapsed = 0
    common_elapsed = []
    d1_rate = None
    d1_t_rate = None
    print("==Valgrinding...==\n")
    if "-val" in argv:
        k_flag = False
        if "-k" in argv:
            k_flag = True
            argv.remove('-k')
        argv.remove("-val")
        system(f"valgrind --tool=cachegrind --log-file=d1_rates.txt {argv[1]} {argv[2]} {argv[3]} {argv[4]} {argv[5]} o")
        with open("d1_rates.txt") as tempf:
            val_output = tempf.read()
            crazy_list = val_output.split("D1  miss rate:")[-1].split(' ')
            for item in crazy_list:
                if item == '': crazy_list.remove('')
            d1_rate = float(crazy_list[0].split('%')[0])
        system(f"valgrind --tool=cachegrind --log-file=d1_t_rates.txt {argv[1]} {argv[2]} {argv[3]} {argv[4]} {argv[5]} t")
        with open("d1_t_rates.txt") as tempf:
            val_output = tempf.read()
            crazy_list = val_output.split("D1  miss rate:")[-1].split(' ')
            for item in crazy_list:
                if item == '': crazy_list.remove('')
            d1_t_rate = float(crazy_list[0].split('%')[0])
        if not k_flag:
            for p in listdir(getcwd()):
                if p.startswith("cachegrind"):
                    remove(p)
    print("== Execuções Comuns: ==\n")
    for i in range(int(argv[6])):
        to_execute = [arg for arg in argv[1:6]]
        to_execute[1] = str(int(to_execute[1]) + i*200)
        to_execute[4] = str(int(to_execute[4]) + i*200)
        to_execute.append('o')
        my_output = check_output(to_execute)
        elapsed = float(str(my_output).split("Elapsed time:")[-1].split('s')[0])
        total_o_elapsed += elapsed
        common_elapsed.append(elapsed)
        print(f"IT{i}, {to_execute[1]}X{to_execute[2]}*{to_execute[3]}X{to_execute[4]} = {elapsed}s")
    print("\n== Execuções Otimizadas: ==\n")
    for i in range(int(argv[6])):
        to_execute = [arg for arg in argv[1:6]]
        to_execute[1] = str(int(to_execute[1]) + i*200)
        to_execute[4] = str(int(to_execute[4]) + i*200)
        to_execute.append('t')
        my_output = check_output(to_execute)
        elapsed = float(str(my_output).split("Elapsed time:")[-1].split('s')[0])
        total_t_elapsed += elapsed
        print(f"IT{i}, {to_execute[1]}X{to_execute[2]}*{to_execute[3]}X{to_execute[4]} = {elapsed}s (speedup={elapsed/common_elapsed[i]})")
    if len(argv) >= 8 and argv[7] == 't':
        print("\n==Execuções Otimizadas: (Transposição Calculada)==\n")
        for i in range(int(argv[6])):
            to_execute = [arg for arg in argv[1:6]]
            to_execute[1] = str(int(to_execute[1]) + i*200)
            to_execute[4] = str(int(to_execute[4]) + i*200)
            to_execute.append('t')
            to_execute.append(argv[7])
            my_output = check_output(to_execute)
            elapsed = float(str(my_output).split("Elapsed time:")[-1].split('s')[0])
            total_tt_elapsed += elapsed
            print(f"IT{i}, {to_execute[1]}X{to_execute[2]}*{to_execute[3]}X{to_execute[4]} = {elapsed}s (speedup={elapsed/common_elapsed[i]})")

    common_mean = total_o_elapsed/int(argv[6])
    optimized_mean = total_t_elapsed/int(argv[6])
    optimized_t_mean = total_tt_elapsed/int(argv[6])

    print("\n== Resultados: ==\n")
    print(f"Média MulM1M2: {common_mean}s\nMédia MulM1M2T: {optimized_mean}s")
    if len(argv) >= 8: print(f"Média MulM1M2T+Transposta: {optimized_t_mean}s")
    if d1_rate: print(f"Taxa de acertos MulM1M2 (D1): {d1_rate}%\nTaxa de acertos MulM1M2T (D1): {d1_t_rate}%")


