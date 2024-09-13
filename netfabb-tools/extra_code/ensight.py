import numpy as np
import struct

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