import numpy as np
import os

####################################################################################################

FULL_DATASET_PATH = r"example-result-files/ascii"
NEW_DATASET_PATH = r"example-result-files/ascii-npz"
ERROR_FILENAME = r"netfabb-errors.txt"

####################################################################################################

def get_basefile(full_path):
    return os.path.normpath(os.path.basename(full_path))

def extract_frames_from_case(filename):
    with open(filename,'r') as f:
        lines = f.readlines()

    for line in lines:
        if "number of steps:" in line:
            return int(line[17:])

    return []


def get_vertices_from_geo(filename, return_elements=False):
    with open(filename,'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "coordinates" in line:
            break
    i += 1
    if i == len(lines):
        return []
    
    N = int(lines[i])
    verts = np.zeros((N,3))

    for j in range(3):
        for k in range(N):
            i+=1
            verts[k,j] = float(lines[i])

    if not return_elements:
        return verts

    i += 1
    if not "hexa8" in lines[i]:
        return []
    i += 1

    N = int(lines[i])
    elems = np.zeros((N,8))

    for j in range(N):
        i += 1
        int_list = [int(s) for s in lines[i].split(' ') if s != '']
        for k in range(8):
            elems[j,k] = int_list[k]

    return verts, elems


def get_values_from_ens(filename, N):
    with open(filename,'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "coordinates" in line:
            break
    i += 1
    if i == len(lines):
        return []
    
    vals = []
    for j in range(i,len(lines)):
        vals.append(float(lines[j]))
    vals = np.array(vals)
    vals = vals.reshape(len(vals)//N, N).T

    return vals

def get_file_info(filename):
    basename = get_basefile(filename) + "_"
    if not os.path.exists(f"{filename}/results/{basename}mechanical.case"):
        basename = ""
        if not os.path.exists(f"{filename}/results/mechanical.case"):
            return dict(error="Error preparing simulation.")
    with open(f'{filename}/{basename}mechanical.out') as f:
        if 'Analysis terminated' in f.read():
            return dict(error="Error running simulation.")

    case_file = f"{filename}/results/{basename}mechanical.case"

    frame_count = extract_frames_from_case(case_file)
    semi_frame_count = frame_count//2+1
    geo_file = f"{filename}/results/{basename}mechanical_{semi_frame_count}.geo"
    displacement_file = f"{filename}/results/{basename}mechanical00_{frame_count}.dis.ens"
    recoater_clearance_file = f"{filename}/results/{basename}mechanical00_{frame_count}.rct.ens"
    global_geo = f"{filename}/results/{basename}mechanical_0.geof"
    recoater_clearance_file_global = f"{filename}/results/{basename}mechanical00_{frame_count-1}.grd.ens"

    return dict(geo=geo_file, disp=displacement_file, rc=recoater_clearance_file, ggeo=global_geo, grc=recoater_clearance_file_global,
                frame_count=frame_count, semi_frame_count=semi_frame_count)

def get_displacement_results_only(filename):
    info = get_file_info(filename)
    if len(info) == 1:
        return [info["error"],] # Simulation failed
    verts, elems = get_vertices_from_geo(info["geo"], return_elements=True)
    N_verts = verts.shape[0]
    disp = get_values_from_ens(info["disp"], N_verts)
    return verts, elems, disp

status_bar_previous_length = -1
def print_status_bar(i, N):
    global status_bar_previous_length
    if status_bar_previous_length == (i*30//N):
        return
    status_bar_previous_length = (i*30//N)
    print(f"[{'='*status_bar_previous_length:<30}]", end='\r')


def extract_data(full_dataset, new_dataset, error_file):
    if not os.path.isdir(new_dataset):
        os.mkdir(new_dataset)
    names = os.listdir(full_dataset)
    num_files = len(names)
    num_success = 0
    print(f"Loading displacement results from: {full_dataset} into {new_dataset}")
    with open(error_file,"w") as err:
        for i, name in enumerate(names):
            print_status_bar(i,num_files)
            results = get_displacement_results_only(os.path.join(full_dataset, name))
            if len(results) == 1:
                err.write(f'{name}\n')
            else:
                num_success += 1
                verts, elems, disp = results
                output_path = os.path.join(new_dataset, name + '.npz')
                np.savez(output_path, verts=verts.astype(np.float32), elems=elems.astype(np.int32), disp=disp.astype(np.float32))
    print(f"Done. {num_success} of {num_files} simulations successful.             ")
    print(f"Failed simulation file names are logged to {error_file}")


####################################################################################################

if __name__ == "__main__":
    if not os.path.exists(NEW_DATASET_PATH):
        os.mkdir(NEW_DATASET_PATH)
    extract_data(FULL_DATASET_PATH, NEW_DATASET_PATH, ERROR_FILENAME)