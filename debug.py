import os
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
#import bpy
#
# Input values
folder = r"/media/z/Work"
name_mesh = "system.2dm"
name_dat = "DEPTH_max.dat"
mode = "depth"
epsilon = 0.01
#
#
# Global
valid_modes = ["depth", "wspl"]
#
#
# Creating paths
path_twodm = os.path.join(folder, name_mesh)
path_dat = None
if mode in valid_modes:
    path_dat = os.path.join(folder, name_dat)
#
#
# Reading Mesh
verts = []
edges = [] # can be left empty
faces = []
for line in open(path_twodm):
    if line.startswith("ND"):
        parts = line.split()
        verts.append([float(n) for n in parts[2:]])
        #
    elif line.startswith("E3T") or line.startswith("E4Q"):
        parts = line.split()
        if line.startswith("E3T"):
            nids = [int(nid) - 1 for nid in parts[2:5]]
            faces.append(nids)
        else:
            nids = [int(n) - 1 for n in line.split()[2:6]]
            faces.append([nids[0], nids[1], nids[2]])
            faces.append([nids[0], nids[2], nids[3]])
#
#
x_min = 999999999999999
y_min = 999999999999999
z_min = 999999999999999
x_max = 0
y_max = 0
z_max = 0
#
for v in verts:
    if v[0] < x_min:
        x_min = v[0]
    if v[1] < y_min:
        y_min = v[1]
    if v[2] < z_min:
        z_min = v[2]
    if v[0] > x_max:
        x_max = v[0]
    if v[1] > y_max:
        y_max = v[1]
    if v[2] > z_max:
        z_max = v[2]
#
for i, v in enumerate(verts):
    verts[i][0] = v[0] - (x_min + x_max) / 2
    verts[i][1] = v[1] - (y_min + y_max) / 2
    verts[i][2] = v[2] - z_min
#
#
if mode in valid_modes:
    # Reading dat
    wspls = []
    i = 0
    for line in open(path_dat):
        try:
            val = float(line)
            if mode == "depth":
                val = val + verts[i][2]
            else:
                val -= z_min
            wspls.append(val)
            i += 1
        except:
            pass
    #
    # Getting wet nodes
    wet_node_ids = []
    faces_wspl = []
    for eid, (nid1, nid2, nid3) in enumerate(faces):
        is_wet = [wspls[nid1] > verts[nid1][2] + epsilon, wspls[nid2] > verts[nid2][2] + epsilon, wspls[nid3] > verts[nid3][2] + epsilon]
        if all(is_wet):
            faces_wspl.append([nid1, nid2, nid3])
            wet_node_ids += [nid1, nid2, nid3]
    wet_node_ids = list(set(wet_node_ids))
    #
    verts_wspl_wet = [[verts[nid][0], verts[nid][1], wspls[nid]] for nid in wet_node_ids]
    #
    # Changind node ids
    old_to_new_nid = {o: n for o, n in zip(wet_node_ids, range(len(wet_node_ids)))}
    faces_wspl_wet = []
    for eid, (nid1, nid2, nid3) in enumerate(faces_wspl):
        faces_wspl_wet.append([old_to_new_nid[nid1], old_to_new_nid[nid2], old_to_new_nid[nid3]])
#
#
tri = Triangulation([v[0] for v in verts_wspl_wet], [v[1] for v in verts_wspl_wet], triangles=faces_wspl_wet)
plt.triplot(tri)
# plt.scatter([v[0] for v in verts_wspl_wet], [v[1] for v in verts_wspl_wet])
plt.show()

a = 1