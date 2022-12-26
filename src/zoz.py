from os import system, remove, listdir, getcwd, mkdir, path
import pandas as pd
import numpy as np
from subprocess import check_output, run
from sys import argv

if __name__ == '__main__':
    # ./mulmatriz.c 750 750 750 750 200 -t -val -k
    # 0            1   2   3   4   5   6  7    8
    # -- outputs
    output = ''
    d1_rate = None
    d1_t_rate = None
    # -- flags and args
    argss = []
    flags = []
    for arg in argv[1:]:
        if arg.startswith('-'):
            flags.append(arg[1:])
        else:
            argss.append(arg)
    if argss[0] == "check":
        a = pd.read_csv(argss[1], sep=';')
        line = list(a.columns)
        for i, col in enumerate(a.columns):
            a.rename(columns={col:f"C{i}"}, inplace=True)
        a.at[len(a.index)] = line
        a = a.to_numpy(np.float64)
        b = pd.read_csv(argss[2], sep=';')
        line = list(b.columns)
        for i, col in enumerate(b.columns):
            b.rename(columns={col:f"C{i}"}, inplace=True)
        b.at[len(b.index)] = line
        b = b.to_numpy(np.float64)
        print(a)
        print("==TIMES==")
        print(b)
        print("==EQUALS==")
        print(np.matmul(a, b))
        exit(0)
    # -- valgrind
    if "val" in flags:
        print("==Valgrinding...==\n")
        for i in range(2):
            mode = 'o'
            fname = "d1_rates.txt"
            if i == 1:
                mode = 't'
                fname = "d1_t_rates.txt"
            system(f"""valgrind --tool=cachegrind --log-file={fname}
            {argss[0]} {argss[1]} {argss[2]} {argss[3]} {argss[4]} {mode}""")
            remove("result.csv")
            with open("d1_rates.txt") as tempf:
                val_output = tempf.read()
                crazy_list = val_output.split("D1 missrate:")[-1].split(' ')
                for item in crazy_list:
                    if item == '': crazy_list.remove('')
                if i == 0:
                    output += f"Taxa de acertos MulM1M2 (D1): {crazy_list[0].split('%')[0]}%\n"
                else:
                    output += f"Taxa de acertos MulM1M2T (D1): {crazy_list[0].split('%')[0]}%\n"
        if not 'k' in flags:
            for p in listdir(getcwd()):
                if p.startswith("cachegrind"): remove(p)
    # -- execution
    exes = 2
    title = ["== Execuções Comuns: ==\n", "== Execuções Otimizadas: ==\n", "== Execuções Comuns (Transposição Calculada): ==\n"]
    output += "\n== Resultados: ==\n"
    common_elapsed = []
    if 't' in flags: exes = 3
    if not path.exists("iterations/"): mkdir("iterations/")
    for i in range(exes):
        mean_name = "MulM1M2"
        mode = 'o'
        if i == 1:
            mean_name = "MulM1M2T"
        elif i == 2:
            mean_name = "MulM1M2T+Transposta"
        print(title[i])
        total_elapsed = 0
        total_dfs = []
        if i:
            mode = 't'
        for ia in range(int(argss[5])):
            to_execute = [arg for arg in argss[:5]]
            for ib in range(1, 5):
                to_execute[ib] = str(int(to_execute[ib]) + ia*200)
            to_execute.append(mode)
            if i == 2: to_execute.append('t')
            my_output = check_output(to_execute)
            elapsed = float(str(my_output).split("Elapsed time:")[-1].split('s')[0])
            total_elapsed += elapsed
            little_put = f"IT{ia}, {to_execute[1]}X{to_execute[2]}*{to_execute[3]}X{to_execute[4]} = {elapsed}s"
            if not i:
                common_elapsed.append(elapsed)
            else:
                little_put += f"(speedup={elapsed/common_elapsed[ia]})"
            print(little_put)
            if i < 2:
                total_dfs.append(pd.read_csv("result.csv", sep=';'))
            remove("result.csv")
        for ia, df in enumerate(total_dfs):
            df.to_csv(f"IT{ia}_{mode}.csv", sep=';', index=False)
        output += f"Média {mean_name}: {total_elapsed/int(argss[5])}s\n"