from os import system
import random
import math
import bpy

deform_frames = 30
fall_frames = 50
total_frames = deform_frames+fall_frames

world = bpy.context.scene
world.frame_start = 0
world.frame_end = total_frames

def duplicate(obj, data=True, actions=True, collection=None):
    obj_copy = obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
    collection.objects.link(obj_copy)
    return obj_copy

def apply_modifier(obj, mod):
    ctx = bpy.context.copy()
    ctx['object'] = obj
    ctx['modifier'] = mod
    bpy.ops.object.modifier_apply(ctx, modifier=mod.name)

scene  = bpy.data.objects
original_obj = scene["Bottle"]

my_obj = duplicate(original_obj, actions = False, 
                    collection = bpy.context.scene.collection)

bpy.context.view_layer.objects.active = my_obj
bpy.context.active_object.name = 'bottle_copy'

def deform_object():
    softbody_mod = [mod for mod in my_obj.modifiers if mod.type == 'SOFT_BODY']
    if softbody_mod is None:
        softbody_mod = my_obj.modifiers.new(name = "Softbody", type = "SOFT_BODY")
        conf = softbody_mod[0].settings
        conf.bend = 1.500
        conf.damping = 0.5
        conf.friction = 0.5
        conf.mass = 0.2
        conf.plastic = 99
        conf.pull = 0.5
        conf.push = 0.5
        conf.shear = 0.6
        conf.use_edges = True
        conf.goal = False
    else:
        softbody_mod = softbody_mod[0] 
        
    spawn_loc = (30.115+random.uniform(0,3),
                 0+random.uniform(-2,2),
                 2+random.uniform(0,2))
    spawn_rot = (random.uniform(-math.pi,math.pi),
                random.uniform(-math.pi,math.pi),
                random.uniform(-math.pi,math.pi))
                
    my_obj.location = spawn_loc
    my_obj.rotation_euler = spawn_rot
    
    for frame in range(0,deform_frames):
        world.frame_set(frame)
    
    apply_modifier(my_obj, softbody_mod)
        
def drop_object():
    my_obj.select_set(True)
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

    for frame in range(deform_frames, world.frame_end+1):
        world.frame_set(frame)        
    
def Process():
    system('cls')
    deform_object()
    drop_object()