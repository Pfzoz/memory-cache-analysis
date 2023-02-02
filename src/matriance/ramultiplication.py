from subprocess import check_output
import os
# ./mulmatriz.x 500 500 500 500

# Iter_Command vai pegar o times e fazer as iterações com base nisso
# Original shape é a primeira matriz inserida (Porque elas vão mudando a cada repetição/iteração)

# sped_list é pra que se essa função for executada como multiplicação por transposta, 
# ela pode usar a lista sped_list dos tempos da multiplicação normal
# pra comparar quão rápido foi em relação a uma execução normal

# pra calcular o 'speedup' é só dividir o tempo da execução atual pela execução normal, ai faz 1 - isso pra conseguir a %
# Depois de executar o código em C, ele guarda os arquivos numa pasta 
# Iteration{raising} no formato {raising}-I-{iteração}-{estilo_de_execução}-{matriz}.csv
# No caso {matriz} pode ser a A, B ou a resultado

def iter_command(command : str,
                original_shape : list, 
                appends : list, 
                times : int = 10, 
                sped_list : list = None, 
                raising : int = 200,
                save : bool = True) -> list:
    if not os.path.exists(f"Iteration{raising}"): os.mkdir(f"Iteration{raising}")
    shape = original_shape.copy()
    elapsed_list = []
    for i in range(times):
        shape[1] = original_shape[1] + i*raising
        shape[2] = original_shape[2] + i*raising
        output = check_output([command,] + [str(n) for n in shape] + appends)
        elapsed = str(output).split("Elapsed time: ")[1].split('s')[0]
        elapsed_list.append(float(elapsed))
        speedup = ""
        if not sped_list is None:
            time_saved = float(elapsed)/sped_list[i]
            speedup = f" | Speedup: {round(1-time_saved, 2)*100}%"
        if save:
            os.rename("a_matrix.csv", f"Iteration{raising}/{raising}-I-{i}-{''.join(appends)}-A.csv")
            os.rename("b_matrix.csv", f"Iteration{raising}/{raising}-I-{i}-{''.join(appends)}-B.csv")
            os.rename("result.csv", f"Iteration{raising}/{raising}-I-{i}-{''.join(appends)}-RLT.csv")
        print(f"Elapsed time: {elapsed}s | {shape[0]}x{shape[1]}*{shape[2]}x{shape[3]}{speedup}")
    return elapsed_list

# Raising Multiplication, Utiliza o itercommand para executar o mesmo código em C de diferentes maneiras.
# Times é quantas vezes vai repetir a multiplicação de matriz pra cada tipo de multiplicação (Transposta ou não)
# Raising é quantas colunas de M1 e quantas linhas de M2 vai aumentar a cada repetição (500x500, 500x500 -> 500x700, 700x500 -> ...)

def raising_multiplication(command_args : list, times : int = 10, raising : int = 200):
    command = command_args[0]
    specify = 'n'
    if len(command_args) >= 6:
        specify = command_args[5]
    original_shape = [int(n) for n in command_args[1:5]]
    print(f"=== (MulM1M2) * {times} ===")
    o_elapsed_list = iter_command(command, original_shape, ['o',], times, raising=raising)
    print(f"=== (MulM1M2T e M2T) * {times} ===")
    t_elapsed_list = iter_command(command, original_shape, ['t',], times, sped_list=o_elapsed_list, raising=raising)
    if specify == 'n':
        print(f"=== (MulM1M2T) * {times} ===")
        tt_elapsed_list = iter_command(command, original_shape, ['t', 'n',], times, sped_list=o_elapsed_list, raising=raising)
