import bpy
import processing

class BottleSimPanel(bpy.types.Panel):
    bl_label = "Bottle Sim"
    bl_idname = "BS_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bottle Sim"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.label(text=" Simple Row:")

        


def register():
    bpy.utils.register_class(BottleSimPanel)


def unregister():
    bpy.utils.unregister_class(BottleSimPanel)


if __name__ == "__main__":
    register()
