import sys
from os import system
import bpy
from . processOperator import BottleSimOperator

class BottleSimPanel(bpy.types.Panel):
    bl_label = "Bottle Sim"
    bl_idname = "BS_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bottle Sim"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        my_props = scene.BottleSimProperties
        layout.prop(my_props, "deform_frames")
        layout.prop(my_props, "falling_frames")
        layout.prop(my_props, "water_frames")
        layout.prop(my_props, "bottle_type_enum")
        layout.prop(my_props, "water_resolution")
        layout.prop(my_props, "deform_force")
        row = layout.row()
        row.label(text="MakeSample:")
        op = row.operator("utils.execute_simulation")
        op.deform_frames=my_props.deform_frames
        op.falling_frames=my_props.falling_frames
        op.water_frames=my_props.water_frames
        op.bottle_type=my_props.bottle_type_enum
        op.water_resolution=my_props.water_resolution
        op.deform_force = my_props.deform_force

def register():
    bpy.utils.register_class(BottleSimPanel)
    
def unregister():
    bpy.utils.unregister_class(BottleSimPanel)