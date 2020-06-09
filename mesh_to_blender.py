import os
import bpy

wsplmode = True

folder = r"D:\Work\2327"
path_twodm = os.path.join(folder, "2327_JJJJMMTT_ISTZUS_STATIO_HQ100.2dm")


if wsplmode:
    path_wspl = os.path.join(folder, "wspl_max.dat")

verts = []
edges = []
faces = []
verts_wspl = []
for line in open(path_twodm):
    if line.startswith("ND"):
        parts = line.split()
        verts.append([float(n) for n in parts[2:]])
        if wsplmode:
            verts_wspl.append([float(n) for n in parts[2:]])
    elif line.startswith("E3T"):
        parts = line.split()
        #if int(parts[-1]) == 0:
        #    continue
        faces.append([int(nid)-1 for nid in parts[2:5]])
    elif line.startswith("E4Q"):
        #if int(parts[-1]) == 0:
        #    continue
        nids = [int(n)-1 for n in line.split()[2:6]]
        faces.append([nids[0], nids[1], nids[2]])
        faces.append([nids[0], nids[2], nids[3]])

if wsplmode:
    i = 0
    for line in open(path_wspl):
        try:
            wspl = float(line)
            if wspl == 0:
                wspl = verts[i][2] - 1
            
            verts_wspl[i][2] = wspl        
            i += 1
        except:
            pass


x_min = 999999999999999
y_min = 999999999999999
z_min = 999999999999999
x_max = 0
y_max = 0
z_max = 0

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

for i, v in enumerate(verts):
    verts[i][0] = v[0] - (x_min + x_max) / 2
    verts[i][1] = v[1] - (y_min + y_max) / 2
    verts[i][2] = v[2] - z_min    
    if wsplmode:
        verts_wspl[i][0] = v[0]
        verts_wspl[i][1] = v[1]
        verts_wspl[i][2] = verts_wspl[i][2] - z_min


# Create mesh object
mesh = bpy.data.meshes.new("Malha")
obj = bpy.data.objects.new("Objeto", mesh)
# Blender 2.8
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(1)
mesh = obj.data
mesh.from_pydata(verts, edges, faces)
mesh.update()

if wsplmode:
    # Create mesh object
    meshwspl = bpy.data.meshes.new("Malhawspl")
    objwspl = bpy.data.objects.new("Objetowspl", meshwspl)
    # Blender 2.8
    bpy.context.collection.objects.link(objwspl)
    bpy.context.view_layer.objects.active = objwspl
    objwspl.select_set(1)
    meshwspl = objwspl.data
    meshwspl.from_pydata(verts_wspl, edges, faces)
    meshwspl.update()


