import random
import math
import numpy as np
from mathutils import Vector
import bpy
import bmesh

def apply_modifier(obj, mod):
    ctx = bpy.context.copy()
    ctx['object'] = obj
    ctx['modifier'] = mod
    bpy.ops.object.modifier_apply(ctx, modifier=mod.name)
    
class SimExecutioner():        
    def __init__(self, deform_frames, fall_frames, water_frames, water_resolution):
        
        self.deform_frames = deform_frames
        self.fall_frames = fall_frames
        self.water_frames = water_frames
        self.water_resolution = water_resolution
        
        self.current_frame = 0
        world = bpy.context.scene
        world.frame_start = 0
        world.frame_end = 0
        scene  = bpy.data.objects     
        self.my_obj = scene['trash_obj']
    
    def deform_object(self):        
        my_obj = self.my_obj
        my_obj.select_set(True)
        softbody_mod = [mod for mod in my_obj.modifiers if mod.type == 'SOFT_BODY']
        if len(softbody_mod) == 0:
            softbody_mod = my_obj.modifiers.new(name = "Softbody", type = "SOFT_BODY")
            conf = softbody_mod.settings
            conf.bend = 1.500
            conf.damping = 0.5
            conf.friction = 0.5
            conf.mass = 0.2
            conf.plastic = 99
            conf.pull = 0.5
            conf.push = 0.5
            conf.shear = 0.6
            conf.use_edges = True
            conf.use_goal = False
        else:
            softbody_mod = softbody_mod[0] 

        spawn_loc = (30+random.uniform(0,3),
                     0+random.uniform(-2,2),
                     2+random.uniform(0,2))
                     
        spawn_rot = (random.uniform(-math.pi,math.pi),
                    random.uniform(-math.pi,math.pi),
                    random.uniform(-math.pi,math.pi))
                    
        my_obj.location = spawn_loc
        my_obj.rotation_euler = spawn_rot
        world = bpy.context.scene
        
        for frame in range(self.current_frame, self.current_frame + self.deform_frames):
            world.frame_set(frame)
        
        self.current_frame = self.current_frame + self.deform_frames
        apply_modifier(my_obj, softbody_mod)
        
    def drop_object(self):        
        my_obj = self.my_obj
        my_obj.select_set(True)
        bpy.context.view_layer.objects.active = my_obj
        bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY', 
                                  center = 'MEDIAN')                          
        bpy.ops.rigidbody.object_add(type='ACTIVE')
        
        spawn_loc = (random.uniform(-2.5,2.5),
                    random.uniform(-1,1),
                    random.uniform(9,10.5))
                    
        spawn_rot = (random.uniform(-math.pi,math.pi),
                    random.uniform(-math.pi,math.pi),
                    random.uniform(-math.pi,math.pi))

        my_obj.location = spawn_loc
        my_obj.rotation_euler = spawn_rot
        world = bpy.context.scene
        
        for frame in range(self.current_frame, self.current_frame + self.fall_frames):
            world.frame_set(frame)       
        
        self.current_frame = self.current_frame + self.fall_frames
        bpy.ops.object.visual_transform_apply()
        bpy.ops.rigidbody.object_remove()
        
    def fill_water_obj(self):
        my_obj = self.my_obj
        verts_sel = [v.co for v in my_obj.data.vertices]
        pivot = my_obj.matrix_world @ (sum(verts_sel, Vector()) / len(verts_sel))
        
        fluid_mesh = bpy.data.meshes.new('trash_obj_fluid_output')
        fluid_sphere = bpy.data.objects.new("trash_obj_fluid_output", fluid_mesh)
        bpy.context.collection.objects.link(fluid_sphere)
        bpy.context.view_layer.objects.active = fluid_sphere
        bmesh_instance = bmesh.new()
        bmesh.ops.create_uvsphere(bmesh_instance, u_segments=32, v_segments=16, radius=0.2)
        bmesh_instance.to_mesh(fluid_mesh)
        bmesh_instance.free()
        fluid_sphere.location = pivot
        
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, 
        location = my_obj.location, rotation = my_obj.rotation_euler)
        bpy.context.active_object.dimensions = my_obj.dimensions
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.context.active_object.name = 'trash_obj_domain'
        bpy.ops.object.shade_smooth(use_auto_smooth=False)
        
        domain_box = bpy.context.scene.objects['trash_obj_domain']
        mat = bpy.data.materials.get('water')
        mat.node_tree.nodes['Volume Absorption'].inputs[0].default_value = (np.random.uniform(),np.random.uniform(), np.random.uniform(), 1.0)
        
        if domain_box.data.materials:
            domain_box.data.materials[0] = mat
        else:
            domain_box.data.materials.append(mat)
        
        fluid_mod = domain_box.modifiers.new(name = "Fluid Modifier", type = "FLUID")
        fluid_mod.fluid_type = 'DOMAIN'
        settings = fluid_mod.domain_settings
        settings.domain_type = 'LIQUID'
        settings.resolution_max = 2 ** self.water_resolution
        settings.use_mesh = True
        settings.effector_weights.force = 0
        settings.cache_frame_start = self.current_frame
        settings.cache_frame_end = self.current_frame + self.water_frames
        
        fluid_sphere.select_set(True)
        fluid_mod = fluid_sphere.modifiers.new(name = "Fluid Modifier", type = "FLUID")
        fluid_mod.fluid_type = 'FLOW'
        settings = fluid_mod.flow_settings 
        settings.flow_type = 'LIQUID' 
        fluid_sphere.hide_render = True
        
        my_obj.select_set(True)
        fluid_mod = my_obj.modifiers.new(name = "Fluid Modifier", type = "FLUID")
        fluid_mod.fluid_type = 'EFFECTOR'
        settings = fluid_mod.effector_settings 
        settings.surface_distance = 0.5
        
        world = bpy.context.scene
        for frame in range(self.current_frame, self.current_frame + self.water_frames):
            world.frame_set(frame) 
        
    def Process(self, sim_selected):
        world = bpy.context.scene
        if sim_selected[0]:
            print("Started deformation simulation")
            world.frame_end += self.deform_frames
            self.deform_object()
            
        print("Started falling simulation") 
        world.frame_end += self.fall_frames          
        self.drop_object()
        
        if sim_selected[1]:
            print("Started fluid simulation")
            world.frame_end += self.water_frames
            self.fill_water_obj()

        me = self.my_obj.data

        bm = bmesh.new()
  
        bm.from_mesh(me)

        bmesh.ops.subdivide_edges(bm, edges=bm.edges,
                                cuts=2, use_grid_fill=True)

        bm.to_mesh(me)
        me.update()