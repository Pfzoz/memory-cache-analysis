from subprocess import check_output
import os
# ./mulmatriz.x 500 500 500 500

def iter_command(command : str,
                original_shape : list, 
                appends : list, 
                times : int = 10, 
                sped_list : list = None, 
                raising : int = 200) -> list:
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
        os.rename("a_matrix.csv", f"Iteration{raising}/{raising}-I-{i}-{''.join(appends)}-A.csv")
        os.rename("b_matrix.csv", f"Iteration{raising}/{raising}-I-{i}-{''.join(appends)}-B.csv")
        os.rename("result.csv", f"Iteration{raising}/{raising}-I-{i}-{''.join(appends)}-RLT.csv")
        print(f"Elapsed time: {elapsed}s | {shape[0]}x{shape[1]}*{shape[2]}x{shape[3]}{speedup}")
    return elapsed_list

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
