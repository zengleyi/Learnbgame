"""Blender Plug-in for Nif import and export."""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright © 2005-2015, NIF File Format Library and Tools contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****

import sys
import os

import bpy
import bpy.props

from . import modules_path
from . import nif_debug
from . import properties, operators, ui

import logging

#: Blender addon info.
bl_info = {
    "name": "NetImmerse/Gamebryo nif format",
    "description":
    "Import and export files in the NetImmerse/Gamebryo nif format (.nif)",
    "author": "NifTools Team",
    "version": (2, 6, 0),  # can't read from VERSION, blender wants it hardcoded
    "blender": (2, 75, 0),
    "location": "File > Import-Export",
    "warning": "partially functional, port from 2.49 series still in progress",
    "wiki_url": (
        "http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/"\
        "Import-Export/Nif"),
    "tracker_url": (
        "https://github.com/niftools/blender_nif_plugin/issues"),
    "support": "COMMUNITY",
    "category": "Learnbgame",
}


def _init_loggers():
    """Set up loggers."""
    niftoolslogger = logging.getLogger("niftools")
    niftoolslogger.setLevel(logging.WARNING)
    pyffilogger = logging.getLogger("pyffi")
    pyffilogger.setLevel(logging.WARNING)
    loghandler = logging.StreamHandler()
    loghandler.setLevel(logging.DEBUG)
    logformatter = logging.Formatter("%(name)s:%(levelname)s:%(message)s")
    loghandler.setFormatter(logformatter)
    niftoolslogger.addHandler(loghandler)
    pyffilogger.addHandler(loghandler)


def menu_func_import(self, context):
    self.layout.operator(
        operators.nif_import_op.NifImportOperator.bl_idname, text="NetImmerse/Gamebryo (.nif)")


def menu_func_export(self, context):
    self.layout.operator(
        operators.nif_export_op.NifExportOperator.bl_idname, text="NetImmerse/Gamebryo (.nif)")


def register():
    _init_loggers()
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    # no idea how to do this... oh well, let's not lose any sleep over it
    # _uninit_loggers()
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
