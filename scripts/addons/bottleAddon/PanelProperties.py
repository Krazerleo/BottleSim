import bpy

class BottleSimPanelProperties(bpy.types.PropertyGroup):
    
    deform_frames    : bpy.props.IntProperty(name = "Frames for deform", soft_min = 0, default = 40)
    falling_frames   : bpy.props.IntProperty(name = "Frames for falling", soft_min = 0, default = 100)
    water_frames     : bpy.props.IntProperty(name = "Frames for water simulation", soft_min = 0, default = 150)
    
    water_resolution : bpy.props.IntProperty(name = "Water simulation quality", soft_min = 0, soft_max = 10, default = 7)
    deform_force     : bpy.props.FloatProperty(name = "Deformation force", soft_min = 0, soft_max = 2, default = 0.5)
    
    bottle_type_enum : bpy.props.EnumProperty(
                name = "Select type",
                items = [('WATER_BOTTLE', "Water Bottle",   ""),
                         ('CAN',          "Can",            ""),
                         ('WINE_BOTTLE',  "Wine Bottle",    ""),
                         ('BEER_BOTTLE',  "Beer Bottle",    ""),
                         ('ANY',          "Any Type",       "")],
                default = 'ANY')
    
def register():
    bpy.utils.register_class(BottleSimPanelProperties)
    bpy.types.Scene.BottleSimProperties = bpy.props.PointerProperty(type = BottleSimPanelProperties)
    
def unregister():
    bpy.utils.unregister_class(BottleSimPanelProperties)
    del bpy.types.Scene.BottleSimProperties