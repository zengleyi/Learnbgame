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
    "name": "Cell Fracture",
    "author": "ideasman42",
    "version": (0, 1),
    "blender": (2, 6, 4),
    "location": "Search > Fracture Object & Add -> Fracture Helper Objects",
    "description": "Fractured Object, Bomb, Projectile, Recorder",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"\
        "Scripts/Object/Fracture",
    "tracker_url": "https://projects.blender.org/tracker/index.php?"\
        "func=detail&aid=21793",
    "category": "Learnbgame",
}


#if "bpy" in locals():
#    import imp
#    imp.reload(fracture_cell_setup)

#import bpy

#def register():
#    bpy.utils.register_class(FractureCell)
#
#    # Add the "add fracture objects" menu to the "Add" menu
#    # bpy.types.INFO_MT_add.append(menu_func)
#
#
#def unregister():
#    bpy.utils.unregister_class(FractureCell)
#
#    # Remove "add fracture objects" menu from the "Add" menu.
#    # bpy.types.INFO_MT_add.remove(menu_func)
#
#
#if __name__ == "__main__":
#    register()
