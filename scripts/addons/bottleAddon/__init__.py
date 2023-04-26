# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "BottleSim addon",
    "description": "Trash dataset generator",
    "author": "Leonid Krazer",
    "version": (0, 2),
    "blender": (3, 3, 5),
    "location": "View3D > Add > Mesh", 
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Add Mesh",
}

if "bpy" in locals():
    import importlib
    if "bottleSimPanel" in locals():
        importlib.reload(bottleSimPanel)
    if "PanelProperties" in locals():
        importlib.reload(PanelProperties)
    if "processOperator" in locals():
        importlib.reload(processOperator)
    if "processing" in locals():
        importlib.reload(processing)
else:
    from . import bottleSimPanel
    from . import PanelProperties
    from . import processOperator
    from . import processing

import bpy

def register():
    bottleSimPanel.register()
    PanelProperties.register()
    processOperator.register()

def unregister():
    processOperator.unregister()
    PanelProperties.unregister()
    bottleSimPanel.unregister()
