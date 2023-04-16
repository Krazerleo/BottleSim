import bpy

class BottleSimPanelProperties(bpy.types.PropertyGroup):
    
    deform_frames    : bpy.props.IntProperty(name = "Amount frame for deformation", soft_min = 0, soft_max = 40)
    falling_frames   : bpy.props.IntProperty(name = "Amount frame for falling in pit", soft_min = 0)
    
    bottle_type_enum : bpy.props.EnumProperty(
                name = "Select bottle type",
                items = [('PLASTIC_BOTTLE',    "Plastic Bottle"   , "")
                         ('CAN',               "Aluminium Can"    , "")
                         ('GLASS_BOTTLE_SODA', "Glass Bottle Soda", "")]
                        
def register():
    bpy.utils.register_class(BottleSimPanelProperties)
    bpy.types.Scene.BottleSimProperties = bpy.props.PointerProperty(type = BottleSimPanelProperties)
    
def unregister():
    bpy.utils.unregister_class(BottleSimPanelProperties)
    del bpy.types.Scene.BottleSimProperties
    
if __name__ == "__main__":
    register()