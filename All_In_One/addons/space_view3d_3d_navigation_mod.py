# 3D NAVIGATION TOOLBAR v1.2 - 3Dview Addon - Blender 2.5x
#
# THIS SCRIPT IS LICENSED UNDER GPL, 
# please read the license block.
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "3D Navigation",
    "author": "Demohero, uriel, et all",
    "version": (1, 2),
    "blender": (2, 57, 0),
    "location": "View3D > Tool Shelf > 3D Nav",
    "description": "Navigate the Camera & 3D View from the Toolshelf",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"\
        "Scripts/3D_interaction/3D_Navigation",
    "tracker_url": "http://projects.blender.org/tracker/index.php?"\
	    "func=detail&aid=23530",
    "category": "Learnbgame",
}

# import the basic library
import bpy

# main class of this toolbar
class VIEW3D_PT_3dnavigationPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "3D Nav"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        view = context.space_data

        # pan tools
        col = layout.column(align=True)
        col.label(text="Pan:")
        row = col.row()
        row.operator("view3d.view_pan", text="up").type='PANUP'
        row.operator("view3d.view_pan", text="down").type='PANDOWN'
        row.operator("view3d.view_pan", text="<").type='PANLEFT'
        row.operator("view3d.view_pan", text=">").type='PANRIGHT'

        # orbit tools
        col = layout.column(align=True)
        col.label(text="Orbit:")
        row = col.row()
        row.operator("view3d.view_orbit", text="up").type='ORBITUP'
        row.operator("view3d.view_orbit", text="down").type='ORBITDOWN'
        row.operator("view3d.view_orbit", text="<").type='ORBITLEFT'
        row.operator("view3d.view_orbit", text=">").type='ORBITRIGHT'
       

# Triple boutons        
        col = layout.column(align=True)
        col.label(text="Misc view tools:")
        col.operator("view3d.viewnumpad", text="View Camera", icon='CAMERA_DATA').type='CAMERA'
        col.operator("view3d.localview", text="View Global/Local")
        col.operator("view3d.view_persportho", text="View Persp/Ortho")  

# group of 6 buttons
        col = layout.column(align=True)
        col.label(text="Align view from:")
        row = col.row()
        row.operator("view3d.viewnumpad", text="Front").type='FRONT'
        row.operator("view3d.viewnumpad", text="Back").type='BACK'
        row = col.row()
        row.operator("view3d.viewnumpad", text="Left").type='LEFT'
        row.operator("view3d.viewnumpad", text="Right").type='RIGHT'
        row = col.row()
        row.operator("view3d.viewnumpad", text="Top").type='TOP'
        row.operator("view3d.viewnumpad", text="Bottom").type='BOTTOM'

# group of 2 buttons
        col = layout.column(align=True)
        col.label(text="View to Object:")
        col.prop(view, "lock_object", text="")
        col.operator("view3d.view_selected", text="View to Selected") 
        
        col = layout.column(align=True)
        col.label(text="Cursor:")
        
        row = col.row()
        row.operator("view3d.snap_cursor_to_center", text="Center")
        row.operator("view3d.view_center_cursor", text="View")
        
        col.operator("view3d.snap_cursor_to_selected", text="Cursor to Selected")

# register the class
def register():
    bpy.utils.register_module(__name__)
 
    pass 

def unregister():
    bpy.utils.unregister_module(__name__)
 
    pass 

if __name__ == "__main__": 
    register()
