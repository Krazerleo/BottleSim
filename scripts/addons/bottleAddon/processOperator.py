from datetime import datetime
import sys
import os
import random
import pathlib
import shutil
import json
import bpy
from . processing import SimExecutioner

def Render(output_file_pattern_string = 'render_{time}_{dir}.jpg'):
    output_dir = pathlib.Path(os.getenv("BOTTLE_SIM_DIR")).resolve() / 'Samples'
    my_camera = bpy.data.objects['Camera']
    camera_pos_coords = [(1.2, 0.1, 5.9),
                         (4.5, 0, 1.0)]
                    
    camera_rot_coords = [(0,  0, -3.14),
                         (1.57, 0, 1.57)] 
                                             
    directions = ['up', 'left']
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    
    for i in range(0,2):
        print(f"Begin render {directions[i]}")       
        my_camera.location = camera_pos_coords[i]
        my_camera.rotation_euler = camera_rot_coords[i]
        bpy.context.scene.render.filepath = os.path.join(output_dir, output_file_pattern_string.format(time=now, dir=directions[i]))
        bpy.ops.render.render(write_still = True)
        
    return

def GetPrefabs(type):
    prefs_path = pathlib.Path(os.getenv("BOTTLE_SIM_DIR")).resolve() / 'TrashPrefabs'
    subdirs = [ f.path for f in os.scandir(prefs_path) if f.is_dir() ]
    selected_prefabs = []
    for subdir in subdirs:
        json_file_name = os.path.join(subdir,"settings.json")
        with open(json_file_name) as file:
            json_data = json.load(file)
            if json_data['type'] == type or type == 'ANY':
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
    
def AdjustDeformForce(deform_force):
    for field in bpy.data.objects:
        if field.name.startswith('deform_field'):
            field.field.strength = deform_force

def DeleteObject():
    for trash_obj in bpy.data.objects:
        if trash_obj.name.startswith('trash_obj'):            
            bpy.data.objects.remove(trash_obj, do_unlink=True)
                        
    for mat in bpy.data.materials:
        if mat.name.startswith('trash_mat'):
            bpy.data.materials.remove(mat)
    
    root_dir = pathlib.Path(os.getenv("BOTTLE_SIM_DIR")).resolve()
    subdirs = [ f.path for f in os.scandir(root_dir) if f.is_dir()]
    
    for subdir in subdirs:
        if 'cache_fluid' in subdir:
            shutil.rmtree(subdir)
    
    
class BottleSimOperator(bpy.types.Operator):
    """Make Sample"""
    bl_idname = "utils.execute_simulation"
    bl_label  = "Create Trash Sample"
    
    deform_frames : bpy.props.IntProperty(name = "Frames for deform",
     soft_min = 0, default = 30)
     
    falling_frames : bpy.props.IntProperty(name = "Frames for falling",
     soft_min = 0, default = 100)
     
    water_frames : bpy.props.IntProperty(name = "Frames for water simulation",
     soft_min = 0, default = 150)
     
    water_resolution : bpy.props.IntProperty(name = "Water simulation quality",
     soft_min = 0, soft_max = 10, default = 7)
     
    deform_force : bpy.props.FloatProperty(name = "Deformation force",
     soft_min = 0, soft_max = 2, default = 0.5) 
        
    bottle_type : bpy.props.StringProperty(name = "Bottle Type", default = 'ANY')

    def execute(self, context):
        prefabs = GetPrefabs(self.bottle_type)
        
        if len(prefabs) == 0:
            self.report({"WARNING"}, "No suitable type prefab")
            return {'CANCELLED'}
        
        prefab = random.choice(prefabs)
        
        sim_selected = CreateObject(prefab)
        se = SimExecutioner(self.deform_frames, self.falling_frames, 
            self.water_frames,self.water_resolution)
        
        AdjustDeformForce(self.deform_force)
        
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