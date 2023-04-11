import sys
from os import system
import bpy
from processing import SimExecutioner
import processOperator

bl_info = {
    "name": "BottleSim addon",
    "description": "Trash dataset generator",
    "author": "Leonid Krazer",
    "version": (0, 1),
    "blender": (3, 3, 5),
    "location": "View3D > Add > Mesh",
    "warning": "", 
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Development",
}

class BottleSimPanel(bpy.types.Panel):
    bl_label = "Bottle Sim"
    bl_idname = "BS_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bottle Sim"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        
        row = layout.row()
        row.label(text="MakeSample:")
        print("before hui")
        row.operator("utils.execute_simulation")
        print("after hui")

def register():
    bpy.utils.register_class(BottleSimPanel)
    
if __name__ == "__main__":
    register()