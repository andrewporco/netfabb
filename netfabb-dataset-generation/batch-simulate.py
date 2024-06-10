import os
import sys
import json
import shutil
import time
import pickle
import subprocess

INPUT_PATH = r"W:\Desktop\netfabb-dataset-generation"
OUTPUT_PATH = rf"C:\Users\{sys.argv[3]}\SandBox"
MESSAGE_PATH = os.path.join(OUTPUT_PATH, "messages.txt")

PRM_RAW = r"EOS M290 Ti-6Al-4V Performance 30 µm.prm"
PRM_TXT = r"EOS_M290_Ti6Al4V_Performance_30um.prm"

MESH_DIR = r"w:/stl" if os.path.exists(r"w:/stl") else rf"C:\Users\{sys.argv[3]}\stl"
JSON_PATH = os.path.join(INPUT_PATH, "simple_train_test.json")

TIME_LIMIT = 5 # minutes of simulation time allowed per part

def print_progress(time, message):
    with open(MESSAGE_PATH, "a") as f:
        print(f"_____________ {time:12.2f} seconds ____________", file=f)
        print(message, file=f)
        print("----------------------------------------------\n", file=f)
    

def get_info_from_argv(loud=True):
    args = sys.argv
    A = int(args[1])
    B = int(args[2])
    user = args[3]
    if loud:
        print(f"Running simulation for shape IDs {A} to {B}")
    return A, B, user

def load_item(path):
    open_file = open(path, "rb")
    this_item=pickle.load(open_file)
    open_file.close()
    return this_item
   
def dump_item(this_item, path):
    open_file = open(path, "wb")
    pickle.dump(this_item, open_file)
    open_file.close()

def setup(start, end, queue):
    os.chdir(INPUT_PATH)
    f = open(queue, "w")
    for part in parts[start:end]:
        mesh_path = os.path.join(MESH_DIR, part+'.stl')
        # print(mesh_path)
        sim_folder = os.path.join(OUTPUT_PATH, part)
        os.makedirs(sim_folder, exist_ok=True)
        shutil.copy(mesh_path, os.path.join(sim_folder,'test.stl'))
        shutil.copy(thermal_in_path, os.path.join(sim_folder,'thermal.in'))
        shutil.copy(mechanical_in_path, os.path.join(sim_folder,'mechanical.in'))
        shutil.copy(prm1_path, os.path.join(sim_folder, PRM_RAW))
        shutil.copy(prm2_path, os.path.join(sim_folder, PRM_TXT))
        f.write('%s/thermal\n'%part)
        f.write('%s/mechanical\n'%part)
    f.close()
    os.chdir(OUTPUT_PATH)

def write_que(start, end, queue):
    os.chdir(INPUT_PATH)
    f = open(queue, "w")
    for part in parts[start:end]:
        f.write('%s/thermal\n'%part)
        f.write('%s/mechanical\n'%part)
    f.close()
    os.chdir(OUTPUT_PATH)


if __name__ == "__main__":
    start_script_time = time.time()
    start, end, user = get_info_from_argv()

    new_path = r"C:\Program Files\Autodesk\Netfabb Ultimate 2024\SIM\Solver\bin"
    current_path = os.environ.get('PATH', '')
    new_path_variable = f'{current_path};{new_path}'
    os.environ['PATH'] = new_path_variable
    
    f=open(JSON_PATH)
    json_loaded = json.load(f)
    parts = [] + json_loaded["train"] + json_loaded["test"]

    thermal_in_path = "input/thermal.in"
    mechanical_in_path = "input/mechanical.in"
    prm1_path = os.path.join("input",PRM_RAW)
    prm2_path = os.path.join("input",PRM_TXT)


    que_path = os.path.join(OUTPUT_PATH,"que.que")
    que_out_path = os.path.join(OUTPUT_PATH,"que.out")

    os.chdir(OUTPUT_PATH)

    setup(start, end, que_path)
    bad_names = []
    command = r"pan -q que"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)

    for idx in range(start, end):
        part = parts[idx]
        start_time = time.time()
        success_run=False    
        mechanical_out_path = OUTPUT_PATH + "/%s/mechanical.out"%part
        print_progress(time.time()-start_script_time, f"Starting part {idx}: {part}")
        for j in range(TIME_LIMIT*60+10): # check if mechanical out is written every TIME_LIMIT minutes
            # wait till mechanical out is generated
            if os.path.exists(mechanical_out_path)==False:
                # print("generating out file")
                time.sleep(1)
                continue
            else:
                try:
                    with open(mechanical_out_path, "rb") as file:
                        # Seek to the end of the file
                        file.seek(-2, os.SEEK_END)
                        # Find the start of the last line
                        while file.read(1) != b'\n':
                            file.seek(-2, os.SEEK_CUR)
                        last_line = file.readline().decode('utf-8')
                    if ("END Autodesk AM Process Simulation LT" in last_line)==True:
                        print("num %s %s success time use %.2f"%(idx, part, time.time()-start_time))
                        success_run=True
                        break
                    else:
                        # print("%s wait"%part)
                        time.sleep(1)
                except:
                    time.sleep(1)
                
        if success_run==False:
            print_progress(time.time()-start_script_time, f"Part {idx} simulation failed ran in {time.time()-start_time:.2f} seconds.\n{part}\nDeleting result files.")
            print("num %s kill %s"%(idx,part))
            command = r"taskkill/f /im pan2.exe"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print("Error executing command:", e)
            time.sleep(0.3)
            bad_names.append(part)
            dump_item(bad_names, "bad_names.pkl")
##            
##            # delete everything in the directory
##            shutil.rmtree(part)
##            os.mkdir(part)
##            
##            # rewrite queue
##            write_que(idx+1, end)
##            time.sleep(1)
##            command = r"pan -q que"
##            try:
##                subprocess.run(command, shell=True, check=True)
##            except subprocess.CalledProcessError as e:
##                print("Error executing command:", e)
        else:
            print_progress(time.time()-start_script_time, f"Part {idx} successfully ran in {time.time()-start_time:.2f} seconds.\n{part}")
            continue
