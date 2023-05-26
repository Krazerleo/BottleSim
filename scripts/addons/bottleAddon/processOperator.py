from datetime import datetime
import sys
import os
import random
import pathlib
import json
import bpy
from . processing import SimExecutioner

def Render(output_file_pattern_string = 'render_{time}_{dir}.jpg'):
    output_dir = pathlib.Path().resolve() / 'Samples'
    my_camera = bpy.data.objects['Camera']
    camera_pos_coords = [(0.0, 0, 7.8),
                         (-4.0, 0, 1.6),
                         (4.0,  0, 1.6)]
                    
    camera_rot_coords = [(0,  0, -3.14),
                         (1.57, 0, -1.57),
                         (1.57, 0, 1.57)] 
                                             
    directions = ['up', 'left', 'right']
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    
    for i in range(0,3):        
        my_camera.location = camera_pos_coords[i]
        my_camera.rotation_euler = camera_rot_coords[i]
        bpy.context.scene.render.filepath = os.path.join(output_dir, output_file_pattern_string.format(time=now, dir=directions[i]))
        bpy.ops.render.render(write_still = True)
        
    return

def GetPrefabs(type):
    prefs_path = pathlib.Path().resolve() / 'TrashPrefabs'
    subdirs = [ f.path for f in os.scandir(prefs_path) if f.is_dir() ]
    selected_prefabs = []
    for subdir in subdirs:
        json_file_name = os.path.join(subdir,"settings.json")
        with open(json_file_name) as file:
            json_data = json.load(file)
            if json_data['type'] == type:
                selected_prefabs.append(subdir)
        
    return selected_prefabs

def CreateObject(prefab_dir):
    json_file_name = os.path.join(prefab_dir,"settings.json")
    with open(json_file_name) as file:
        json_data = json.load(file)

        prefab_path = os.path.join(prefab_dir, json_data['name']+'.blend')

        with bpy.data.libraries.load(prefab_path) as (data_from, data_to):
            data_to.objects = data_from.objects
 
        for obj in data_to.objects:
            bpy.context.scene.collection.objects.link(obj)            

        sims_available = json_data['sims_available']
        sims_result = [False, False]
        if 'deform' in sims_available:
            sims_result[0] = True
        if 'fill_water' in sims_available:
            sims_result[1] = True
        
        return sims_result
    
def DeleteObject():
    object_to_delete = bpy.data.objects['trash_obj']    
    bpy.data.objects.remove(object_to_delete, do_unlink=True)
    for mat in bpy.data.materials:
        if mat.name.startswith('trash_mat'):
            bpy.data.materials.remove(mat)

class BottleSimOperator(bpy.types.Operator):
    """Make Sample"""
    bl_idname = "utils.execute_simulation"
    bl_label  = "Create Trash Sample"
    
    deform_frames  : bpy.props.IntProperty(name = "Frames for deform",
     soft_min = 0, soft_max = 40, default = 30)
     
    falling_frames : bpy.props.IntProperty(name = "Frames for falling",
     soft_min = 0, soft_max = 100, default = 80) 
        
    bottle_type    : bpy.props.StringProperty(name = "Bottle Type", default = '')

    def execute(self, context):
        prefabs = GetPrefabs(self.bottle_type)
        
        if len(prefabs) == 0:
            self.report({"WARNING"}, "No suitable type prefab")
            return {'CANCELLED'}
        
        prefab = random.choice(prefabs)
        
        sim_selected = CreateObject(prefab)
        se = SimExecutioner(self.deform_frames, self.falling_frames)
        se.Process(sim_selected)
        Render()
        DeleteObject()
        
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    bpy.utils.register_class(BottleSimOperator)
    

def unregister():
    bpy.utils.unregister_class(BottleSimOperator)