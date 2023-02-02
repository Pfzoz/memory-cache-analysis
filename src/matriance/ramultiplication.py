from subprocess import check_output
import numpy as np

# ./mulmatriz.x 500 500 500 500

def raising_multiplication(command_args : list, times : int = 10):
    command = command_args[0]
    specify = 'n'
    if len(command_args) >= 6:
        specify = command_args[5]
    o_elapsed_list = []
    t_elapsed_list = []
    tt_elapsed_list = []
    # normal
    original_shape = [int(n) for n in command_args[1:5]]
    shape = [int(n) for n in command_args[1:5]]
    print(f"=== (MulM1M2) * {times} ===")
    for i in range(times):
        shape[1] = original_shape[1] + i*200
        shape[2] = original_shape[2] + i*200
        output = check_output([command,] + [str(n) for n in shape] + ['o',])
        elapsed = str(output).split("Elapsed time: ")[1].split('s')[0]
        o_elapsed_list.append(float(elapsed))
        print(f"Elapsed time: {elapsed}s | {shape[0]}x{shape[1]}*{shape[2]}x{shape[3]}")
    # transposed
    shape = [int(n) for n in command_args[1:5]]
    print(f"=== (MulM1M2T e M2T) * {times} ===")
    for i in range(times):
        shape[1] = original_shape[1] + i*200
        shape[2] = original_shape[2] + i*200
        output = check_output([command,] + [str(n) for n in shape] + ['t',])
        elapsed = str(output).split("Elapsed time: ")[1].split('s')[0]
        t_elapsed_list.append(float(elapsed))
        time_saved = float(elapsed)/o_elapsed_list[i]
        print(f"Elapsed time: {elapsed}s | Speedup: {round(1-time_saved, 2)*100}% | {shape[0]}x{shape[1]}*{shape[2]}x{shape[3]}")
    # transposed without transpose
    shape = [int(n) for n in command_args[1:5]]
    if specify == 't':
        print(f"=== (MulM1M2T) * {times} ===")
        for i in range(times):
            shape[1] = original_shape[1] + i*200
            shape[2] = original_shape[2] + i*200
            output = check_output([command,] + [str(n) for n in shape] + ['t',])
            elapsed = str(output).split("Elapsed time: ")[1].split('s')[0]
            tt_elapsed_list.append(float(elapsed))
            time_saved = float(elapsed)/o_elapsed_list[i]
            print(f"Elapsed time: {elapsed}s | Speedup: {round(1-time_saved, 2)*100}% | {shape[0]}x{shape[1]}*{shape[2]}x{shape[3]}")

