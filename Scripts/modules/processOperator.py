from datetime import datetime
import sys
import os
import pathlib
import bpy

from processing import SimExecutioner

def Render(output_file_pattern_string = 'render_{time}.jpg'):
    output_dir = pathlib.Path().resolve() / 'Samples'
    now = datetime.now().strftime('%Y-%m-%d')
    bpy.context.scene.render.filepath = os.path.join(output_dir, output_file_pattern_string.format(time=now))
    bpy.ops.render.render(write_still = True)
    return

class BottleSimOperator(bpy.types.Operator):
    """Make Sample"""
    bl_idname = "utils.execute_simulation"
    bl_label  = "Create Trash Sample"

    def execute(self, context):
        output_path = pathlib.Path().resolve() / 'Samples'
        se = SimExecutioner()
        se.Process()
        Render()
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    bpy.utils.register_class(BottleSimOperator)
    

def unregister():
    bpy.utils.unregister_class(BottleSimOperator)

if __name__ == "__main__":
    register()