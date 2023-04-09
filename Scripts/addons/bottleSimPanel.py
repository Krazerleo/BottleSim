import sys
from os import system
import bpy

sys.path.append('C:/Users/Leonid_Krazer/Desktop/ProjectBottleSim/Scripts/modules/')
import processOperator


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


bpy.utils.register_class(BottleSimPanel)