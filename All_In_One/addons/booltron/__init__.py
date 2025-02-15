# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Booltron super add-on for super fast booleans.
#  Copyright (C) 2014-2019  Mikhail Rachinskiy
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Booltron",
    "author": "Mikhail Rachinskiy",
    "version": (2, 4, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Sidebar",
    "description": "Super add-on for super fast booleans.",
    "wiki_url": "https://github.com/mrachinskiy/booltron#readme",
    "tracker_url": "https://github.com/mrachinskiy/booltron/issues",
    "category": "Learnbgame",
}


if "bpy" in locals():
    import importlib

    for entry in os.scandir(var.ADDON_DIR):

        if entry.is_file() and entry.name.endswith(".py") and not entry.name.startswith("__"):
            module = os.path.splitext(entry.name)[0]
            importlib.reload(eval(module))

        elif entry.is_dir() and not entry.name.startswith((".", "__")):

            for subentry in os.scandir(entry.path):
                if subentry.is_file() and subentry.name.endswith(".py"):
                    if subentry.name == "__init__.py":
                        module = os.path.splitext(entry.name)[0]
                    else:
                        module = entry.name + "." + os.path.splitext(subentry.name)[0]
                    importlib.reload(eval(module))
else:
    import os

    import bpy
    import bpy.utils.previews
    from bpy.props import PointerProperty

    from . import (
        localization,
        preferences,
        ops_destructive,
        ops_nondestructive,
        ui,
        var,
        mod_update,
    )


var.UPDATE_CURRENT_VERSION = bl_info["version"]

classes = (
    preferences.BooltronPreferences,
    preferences.BooltronPropertiesWm,
    ui.VIEW3D_PT_booltron_update,
    ui.VIEW3D_PT_booltron_destructive,
    ui.VIEW3D_PT_booltron_nondestructive,
    ops_destructive.OBJECT_OT_booltron_destructive_union,
    ops_destructive.OBJECT_OT_booltron_destructive_difference,
    ops_destructive.OBJECT_OT_booltron_destructive_intersect,
    ops_destructive.OBJECT_OT_booltron_destructive_slice,
    ops_nondestructive.OBJECT_OT_booltron_nondestructive_union,
    ops_nondestructive.OBJECT_OT_booltron_nondestructive_difference,
    ops_nondestructive.OBJECT_OT_booltron_nondestructive_intersect,
    ops_nondestructive.OBJECT_OT_booltron_nondestructive_remove,
    mod_update.WM_OT_booltron_update_check,
    mod_update.WM_OT_booltron_update_download,
    mod_update.WM_OT_booltron_update_whats_new,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.booltron = PointerProperty(type=preferences.BooltronPropertiesWm)

    # Translations
    # ---------------------------

    for k, v in mod_update.DICTIONARY.items():
        if k in localization.DICTIONARY.keys():
            localization.DICTIONARY[k].update(v)
        else:
            localization.DICTIONARY[k] = v

    bpy.app.translations.register(__name__, localization.DICTIONARY)

    mod_update.DICTIONARY.clear()

    # Previews
    # ---------------------------

    pcoll = bpy.utils.previews.new()

    for entry in os.scandir(var.ICONS_DIR):
        if entry.is_dir():
            for subentry in os.scandir(entry.path):
                if subentry.is_file() and subentry.name.endswith(".png"):
                    name = entry.name + os.path.splitext(subentry.name)[0]
                    pcoll.load(name.upper(), subentry.path, "IMAGE")

    var.preview_collections["icons"] = pcoll

    # mod_update
    # ---------------------------

    mod_update.update_init_check()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.booltron

    bpy.app.translations.unregister(__name__)

    # Previews
    # ---------------------------

    for pcoll in var.preview_collections.values():
        bpy.utils.previews.remove(pcoll)

    var.preview_collections.clear()


if __name__ == "__main__":
    register()
