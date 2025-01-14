# Blender FLIP Fluid Add-on
# Copyright (C) 2018 Ryan L. Guy
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "FLIP Fluids",
    "description": "A FLIP Fluid Simulation Tool for Blender",
    "author" : "Ryan Guy <ryan.l.guy[at]gmail.com>, Dennis Fassbaender <info[at]df-videos.de>",
    "version" : (1, 0, 2),
    "blender" : (2, 80, 0),
    "location" : "Properties > Physics > FLIP Fluid",
    "warning" : "",
    "wiki_url" : "https://github.com/rlguy/Blender-FLIP-Fluids-Beta/wiki",
    "tracker_url" : "https://github.com/rlguy/Blender-FLIP-Fluids-Beta/issues",
    "category": "Learnbgame",
}

if "bpy" in locals():
    import importlib
    reloadable_modules = [
        'utils',
        'objects',
        'materials',
        'properties',
        'operators',
        'ui',
        'presets',
        'export',
        'bake',
        'render',
        'global_vars'
    ]
    for module_name in reloadable_modules:
        if module_name in locals():
            importlib.reload(locals()[module_name])

import bpy, atexit, shutil, os
from bpy.props import (
        PointerProperty,
        StringProperty
        )

from . import (
        utils,
        objects,
        materials,
        properties,
        operators,
        ui,
        presets,
        export,
        bake,
        render,
        global_vars
        )


@bpy.app.handlers.persistent
def scene_update_post(scene):
    properties.scene_update_post(scene)
    render.scene_update_post(scene)


@bpy.app.handlers.persistent
def frame_change_pre(scene):
    properties.frame_change_pre(scene)
    render.frame_change_pre(scene)


@bpy.app.handlers.persistent
def render_pre(scene):
    render.render_pre(scene)


@bpy.app.handlers.persistent
def render_post(scene):
    render.render_post(scene)


@bpy.app.handlers.persistent
def render_cancel(scene):
    render.render_cancel(scene)


@bpy.app.handlers.persistent
def render_complete(scene):
    render.render_complete(scene)


@bpy.app.handlers.persistent
def load_pre(nonedata):
    properties.load_pre()


@bpy.app.handlers.persistent
def load_post(nonedata):
    properties.load_post()
    materials.load_post()
    presets.load_post()
    

@bpy.app.handlers.persistent
def save_pre(nonedata):
    properties.save_pre()


@bpy.app.handlers.persistent
def save_post(nonedata):
    properties.save_post()


def on_exit():
    base = os.path.basename(bpy.data.filepath)
    save_file = os.path.splitext(base)[0]
    is_unsaved = not base or not save_file
    if is_unsaved:
        if os.path.exists(global_vars.CACHE_DIRECTORY):
            shutil.rmtree(global_vars.CACHE_DIRECTORY)


def register():
    objects.register()
    materials.register()
    properties.register()
    operators.register()
    ui.register()
    presets.register()

    bpy.app.handlers.scene_update_post.append(scene_update_post)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre)
    bpy.app.handlers.render_pre.append(render_pre)
    bpy.app.handlers.render_post.append(render_post)
    bpy.app.handlers.render_cancel.append(render_cancel)
    bpy.app.handlers.render_complete.append(render_complete)
    bpy.app.handlers.load_pre.append(load_pre)
    bpy.app.handlers.load_post.append(load_post)
    bpy.app.handlers.save_pre.append(save_pre)
    bpy.app.handlers.save_post.append(save_post)
    atexit.register(on_exit)


def unregister():
    objects.unregister()
    materials.unregister()
    properties.unregister()
    operators.unregister()
    ui.unregister()
    presets.unregister()

    bpy.app.handlers.scene_update_post.remove(scene_update_post)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre)
    bpy.app.handlers.render_pre.remove(render_pre)
    bpy.app.handlers.render_post.remove(render_post)
    bpy.app.handlers.render_cancel.remove(render_cancel)
    bpy.app.handlers.render_complete.remove(render_complete)
    bpy.app.handlers.load_pre.remove(load_pre)
    bpy.app.handlers.load_post.remove(load_post)
    bpy.app.handlers.save_pre.remove(save_pre)
    bpy.app.handlers.save_post.remove(save_post)
    atexit.unregister(on_exit)

