from os import system
import typing
import random
import math
import bpy

def apply_modifier(obj, mod):
    
    ctx = bpy.context.copy()
    ctx['object'] = obj
    ctx['modifier'] = mod
    bpy.ops.object.modifier_apply(ctx, modifier=mod.name)


class SimExecutioner():    
    obj_types_available = [ "Bottle", "Others types to implement" ]
    deformable_objects  = { "Bottle" : True }
    
    def __init__(self, deform_frames : int = 30, 
                    fall_frames : int = 80,):
        
        self.deform_frames = deform_frames
        self.fall_frames = fall_frames
        self.total_frames = deform_frames+fall_frames

        world = bpy.context.scene
        world.frame_start = 0
        world.frame_end = self.total_frames
        
        scene  = bpy.data.objects     
        self.my_obj = scene['trash_obj']
    
    def deform_object(self):        
        my_obj = self.my_obj
        my_obj.select_set(True)
        softbody_mod = [mod for mod in my_obj.modifiers if mod.type == 'SOFT_BODY']
        if len(softbody_mod) == 0:
            softbody_mod = my_obj.modifiers.new(name = "Softbody", type = "SOFT_BODY")
            print(softbody_mod, '========================')
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
        
        for frame in range(0,self.deform_frames):
            world.frame_set(frame)
        
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
        
        for frame in range(self.deform_frames, self.total_frames+1):
            world.frame_set(frame)       
    
    
    def fill_water_obj(self):
        pass


    def Process(self, sim_selected):
        if sim_selected[0]:
            self.deform_object()
            
        self.drop_object()
        
        if sim_selected[1]:
            self.fill_water_obj()