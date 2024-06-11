# import trimesh
# import vtk
# import pyvista as pv
# import os
# import matplotlib.pyplot as plt

import numpy as np
import open3d as o3d

filename = r"dataset/02.npz"
data = np.load(filename)

verts = data['verts']
elems = data['elems']
disp = data['disp']

# Create a TriangleMesh from vertices
mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(verts)

triangles = []
for polygon in elems:
    for i in range(1, len(polygon) - 1):
        triangles.append([polygon[0], polygon[i], polygon[i + 1]])

# Convert the list of triangles to a NumPy array
triangles = np.array(triangles)

# Create mesh connectivity from elements
mesh.triangles = o3d.utility.Vector3iVector(triangles)

# Color the mesh vertices based on displacements
mesh.vertex_colors = o3d.utility.Vector3dVector(disp)

# Visualize the mesh
o3d.visualization.draw_geometries([mesh])


#######################################################################


# verts = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
# faces = np.array([[0, 1, 2], [0, 2, 3]])

# new_faces = np.hstack((np.full((faces.shape[0], 1), 3), faces))

# mesh = pv.PolyData(verts, new_faces)

# mesh.save('example_mesh.vtk')

# plotter = pv.Plotter()
# plotter.add_mesh(mesh)
# plotter.show()


# verts = data['verts']
# faces = data['elems']

# triangles = []
# for polygon in faces:
#     # Split the polygon into triangles
#     for i in range(1, len(polygon) - 1):
#         triangles.append([polygon[0], polygon[i], polygon[i + 1]])

# # Convert the list of triangles to a NumPy array
# triangles = np.array(triangles)

# # faces_pyvista =  np.hstack((np.full((faces.shape[0], 1), 3), faces))

# mesh = pv.PolyData(verts, triangles)

# mesh.save('dataset/01.vtk')

# plotter = pv.Plotter()
# plotter.add_mesh(mesh)
# plotter.show()