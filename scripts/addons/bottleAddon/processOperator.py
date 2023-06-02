from datetime import datetime
import os
import random
import pathlib
import shutil
import json
import bpy
from . processing import SimExecutioner

metal_colors = [ (195 / 255, 33 / 255, 72 / 255, 1), 
                (117 / 255, 117 / 255, 117 / 255, 1), 
                (26 / 255, 17 / 255, 16 / 255, 1), 
                (254 / 255, 254 / 255, 254 / 255, 1), 
                (33 / 255, 79 / 255, 198 / 255, 1)]

glass_colors = [ (147 / 255, 204 / 255, 234 / 255, 1),
                  (236 / 255, 235 / 255, 189 / 255, 1),
                  (143 / 255, 212 / 255, 0, 1),
                  (160 / 255, 230 / 255, 1, 1),
                  (200 / 255, 200 / 255, 205 / 255, 1)]

plastic_colors = [ (102 / 255, 1, 102 / 255, 1),
                  (93 / 255, 173 / 255, 236 / 255, 1),
                   (206 / 255, 200 / 255, 239 / 255, 1)]

def Render(output_file_pattern_string = 'render_{time}_{dir}.jpg'):
    output_dir = pathlib.Path(os.getenv("BOTTLE_SIM_DIR")).resolve() / 'Samples'
    my_camera = bpy.data.objects['Camera']
    camera_pos_coords = [(1.2, 0.1, 5.3),
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

def UseMaterial():
    for mat in bpy.data.materials:
        mat.use_nodes = True
        mat_nodes = mat.node_tree.nodes
        if mat.name.startswith('trash_mat_glass'):
            mat_nodes['Group'].inputs['Color'].default_value=random.choice(glass_colors)
        if mat.name.startswith('trash_mat_plastic'):
            mat_nodes['Principled BSDF'].inputs['Base Color'].default_value=random.choice(plastic_colors)
        if mat.name.startswith('trash_mat_metal'):
            mat_nodes['Principled BSDF'].inputs['Base Color'].default_value=random.choice(metal_colors)
        if mat.name.startswith('trash_mat_etiq'):
            tex_image = mat_nodes.get("Image Texture")       
            label_path = pathlib.Path(os.getenv("BOTTLE_SIM_DIR")).resolve() / 'Labels'
            images_path = [ f.path for f in os.scandir(label_path) if f.is_file() ]
            label_path = os.path.join(pathlib.Path(os.getenv("BOTTLE_SIM_DIR")).resolve() / 'Labels', random.choice(images_path))           
            tex_image.image = bpy.data.images.load(label_path)

def AdjustDeformForce(deform_force):
    for field in bpy.data.objects:
        if field.name.startswith('deform_field'):
            field.field.strength = deform_force

def DeleteObject():
    for trash_obj in bpy.data.objects:
        if trash_obj.name.startswith('trash_obj'):            
            bpy.data.objects.remove(trash_obj, do_unlink=True)                    

def DeleteMaterials():
    for mat in bpy.data.materials:
        if mat.name.startswith('trash_mat'):
            bpy.data.materials.remove(mat)

def DeleteCache():
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
        UseMaterial()
        
        se.Process(sim_selected)
        Render()
        DeleteObject()
        DeleteMaterials()
        DeleteCache()
                
        return {'FINISHED'}        

    def invoke(self, context, event):
        return self.execute(context)


def register():
    bpy.utils.register_class(BottleSimOperator)
    

def unregister():
    bpy.utils.unregister_class(BottleSimOperator)