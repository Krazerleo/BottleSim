import bpy

for i in range(0, 10):
    bpy.ops.utils.execute_simulation(deform_frames = 41, falling_frames = 100, 
                                    water_frames = 100, bottle_type = 'ANY', 
                                    water_resolution = 7, deform_force = 0.4)