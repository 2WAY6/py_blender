
import bpy

path_xyz = r""
r = 0.1

for line in open(path_xyz):
    try:
        x, y, z = [float(a) for a in line.split()]
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x,y,z), radius=r)
    except:
        pass