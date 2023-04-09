import sys
import bpy

from processing import SimExecutioner

class BottleSimOperator(bpy.types.Operator):
    """Make Sample"""
    bl_idname = "utils.execute_simulation"
    bl_label  = "Create Trash Sample"

    def execute(self, context):
        se = SimExecutioner()
        se.Process()
        return {'FINISHED'}

    def invoke(self, context, event):
        print("chin chin")
        se = SimExecutioner()
        se.Process()
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(BottleSimOperator)
    

def unregister():
    bpy.utils.unregister_class(BottleSimOperator)


bpy.utils.register_class(BottleSimOperator)
