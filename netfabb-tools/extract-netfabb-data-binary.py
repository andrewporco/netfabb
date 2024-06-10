import numpy as np
import os
import struct

####################################################################################################


FULL_DATASET_PATH = r"example-result-files/binary"
NEW_DATASET_PATH = r"example-result-files/binary-npz"
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

####################################################################################################

def read80(f):
    return f.read(80).decode('utf-8').strip()

def read_floats(f,N):
    arr = np.array(struct.unpack(f"<{N}f", f.read(4*N)))
    return arr[0] if N == 1 else arr

def read_ints(f,N):
    arr = np.array(struct.unpack(f"<{N}i", f.read(4*N)))
    return arr[0] if N == 1 else arr

def read_geo_binary(path):
    with open(path, 'rb') as f:

        ############ Info
        assert read80(f) == 'Fortran Binary'
        description1 = read80(f)
        description2 = read80(f)
        assert read80(f) == 'node id off'
        assert read80(f) == 'element id off'
        # extents_str = read80(f)       # No extents
        # extents = read_floats(f,6)    # No extents

        ############ Begin part 1
        assert read80(f) == 'part'
        assert read_ints(f,1) == 1 # Should be 1 part only
        description3 = read80(f)

        ############ Coordinates
        assert read80(f) == 'coordinates'
        nn = read_ints(f,1)
        # node_ids = read_ints(f,nn) # node id is off
        x = read_floats(f,nn)
        y = read_floats(f,nn)
        z = read_floats(f,nn)
        nodes = np.vstack([x,y,z]).T

        ############ Elements
        element_type = read80(f)
        assert(element_type == 'hexa8')
        # element_ids = read_ints(f,nn) # element id is off
        ne = read_ints(f, 1)
        elems = read_ints(f, 8*ne).reshape(ne,8)

    data = dict(description1=description1, description2=description2, description3=description3, 
                nn=nn, nodes=nodes, element_type=element_type, ne=ne, elems=elems)
    return data


def read_ens_binary(path, num_nodes, num_values):
    with open(path, 'rb') as f:
        description = read80(f)
        assert(read80(f) == 'part')
        assert(read_ints(f,1) == 1)
        assert(read80(f) == 'coordinates')
        arr = read_floats(f,num_nodes*num_values)
    data = arr.reshape(num_values, num_nodes).T
    return dict(description=description, data=data)

####################################################################################################

def get_vertices_from_geo(filename, return_elements=False):
    data = read_geo_binary(filename)
    if not return_elements:
        return data["nodes"]
    else:
        return data["nodes"], data["elems"]


def get_values_from_ens(filename, N, nv):
    data = read_ens_binary(filename, N, nv)
    return data["data"]

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
    disp = get_values_from_ens(info["disp"], N_verts, 3)
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