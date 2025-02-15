bl_info = {
    "name": "Icon Viewer",
    "author": "roaoao",
    "version": (1, 3, 0),
    "blender": (2, 75, 0),
    "location": "Spacebar > Icon Viewer, Text Editor > Properties",
    "wiki_url": (
        "https://wiki.blender.org/index.php/User:Raa/Addons/Icon_Viewer"),
    "tracker_url": "http://blenderartists.org/forum/showthread.php?392912",
    "category": "Learnbgame",
}

import bpy
import math

DPI = 72
POPUP_PADDING = 10
PANEL_PADDING = 44
WIN_PADDING = 32
ICON_SIZE = 20
HISTORY_SIZE = 100
HISTORY = []


def ui_scale():
    ret = bpy.context.user_preferences.system.dpi / DPI
    if bpy.context.user_preferences.system.virtual_pixel_mode == 'DOUBLE':
        ret *= 2
    return ret


def prefs():
    return bpy.context.user_preferences.addons[__name__].preferences


class Icons:
    def __init__(self):
        self._filtered_icons = None
        self._filter = ""
        self.filter = ""
        self.selected_icon = ""

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, value):
        if self._filter == value:
            return

        self._filter = value
        self.update()

    @property
    def filtered_icons(self):
        if self._filtered_icons is None:
            self._filtered_icons = []
            icon_filter = self._filter.upper()
            self.filtered_icons.clear()
            pr = prefs()

            icons = bpy.types.UILayout.bl_rna.functions[
                "prop"].parameters["icon"].enum_items.keys()
            for icon in icons:
                if icon == 'NONE' or \
                        icon_filter and icon_filter not in icon or \
                        not pr.show_brush_icons and "BRUSH_" in icon and \
                        icon != 'BRUSH_DATA' or \
                        not pr.show_matcap_icons and "MATCAP_" in icon or \
                        not pr.show_colorset_icons and "COLORSET_" in icon:
                    continue
                self._filtered_icons.append(icon)

        return self._filtered_icons

    @property
    def num_icons(self):
        return len(self.filtered_icons)

    def update(self):
        if self._filtered_icons is not None:
            self._filtered_icons.clear()
            self._filtered_icons = None

    def draw(self, layout, num_cols=0, icons=None, select=True):
        if icons:
            filtered_icons = reversed(icons)
        else:
            filtered_icons = self.filtered_icons

        column = layout.column(True)
        row = column.row(True)
        row.alignment = 'CENTER'

        op_name = IV_OT_icon_select.bl_idname if select else \
            IV_OT_icon_copy.bl_idname

        col_idx = 0
        for i, icon in enumerate(filtered_icons):
            p = row.operator(
                op_name, "",
                icon=icon, emboss=select and icon == self.selected_icon)
            p.icon = icon

            col_idx += 1
            if col_idx > num_cols - 1:
                if icons:
                    break
                col_idx = 0
                if i < len(filtered_icons) - 1:
                    row = column.row(True)
                    row.alignment = 'CENTER'

        if col_idx != 0 and not icons:
            sub = row.row(True)
            sub.scale_x = num_cols - col_idx
            sub.label("", icon='BLANK1')

        if not filtered_icons:
            row.label("No icons were found")


class IV_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    panel_icons = Icons()
    popup_icons = Icons()

    def update_icons(self, context):
        self.panel_icons.update()
        self.popup_icons.update()

    def set_panel_filter(self, value):
        self.panel_icons.filter = value

    panel_filter = bpy.props.StringProperty(
        description="Filter",
        get=lambda s: s.panel_icons.filter,
        set=set_panel_filter,
        options={'TEXTEDIT_UPDATE'})
    show_brush_icons = bpy.props.BoolProperty(
        name="Show Brush Icons",
        description="Show brush icons", default=True,
        update=update_icons)
    show_matcap_icons = bpy.props.BoolProperty(
        name="Show Matcap Icons",
        description="Show matcap icons", default=True,
        update=update_icons)
    show_colorset_icons = bpy.props.BoolProperty(
        name="Show Colorset Icons",
        description="Show colorset icons", default=True,
        update=update_icons)
    show_panel_icons = bpy.props.BoolProperty(
        name="Show Icons",
        description="Show icons", default=True)
    copy_on_select = bpy.props.BoolProperty(
        name="Copy Icon On Click",
        description="Copy icon on click", default=True)
    close_on_select = bpy.props.BoolProperty(
        name="Close Popup On Click",
        description=(
            "Close the popup on click.\n"
            "Not supported by some windows (User Preferences, Render)."
            ),
        default=False)
    auto_focus_filter = bpy.props.BoolProperty(
        name="Auto Focus Input Field",
        description="Auto focus input field", default=True)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_y = 1.5
        row.operator(IV_OT_icons_show.bl_idname)

        row = layout.row()

        col = row.column(True)
        col.label("Icons:")
        col.prop(self, "show_matcap_icons")
        col.prop(self, "show_brush_icons")
        col.prop(self, "show_colorset_icons")

        col = row.column(True)
        col.label("Popup:")
        col.prop(self, "auto_focus_filter")
        col.prop(self, "copy_on_select")
        if self.copy_on_select:
            col.prop(self, "close_on_select")

        col = row.column(True)
        col.label("Panel:")
        col.prop(self, "show_panel_icons")


class IV_PT_icons(bpy.types.Panel):
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_label = "Icon Viewer"

    def draw(self, context):
        pr = prefs()
        row = self.layout.row(True)
        if pr.show_panel_icons:
            row.prop(pr, "panel_filter", "", icon='FILTER')
        else:
            row.operator(IV_OT_icons_show.bl_idname)
        row.operator(IV_OT_panel_menu_call.bl_idname, "", icon='COLLAPSEMENU')

        if pr.show_panel_icons:
            col = self.layout.column(True)

            _, y0 = context.region.view2d.region_to_view(0, 0)
            _, y1 = context.region.view2d.region_to_view(0, 10)
            region_scale = 10 / abs(y0 - y1)

            num_cols = max(
                1,
                (context.region.width - PANEL_PADDING) //
                math.ceil(ui_scale() * region_scale * ICON_SIZE))

            if HISTORY:
                pr.panel_icons.draw(col.box(), num_cols, HISTORY, False)

            pr.panel_icons.draw(col.box(), num_cols, select=False)


class IV_HT_icons(bpy.types.Header):
    bl_space_type = 'CONSOLE'

    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.operator(IV_OT_icons_show.bl_idname)


class IV_OT_panel_menu_call(bpy.types.Operator):
    bl_idname = "iv.panel_menu_call"
    bl_label = ""
    bl_description = "Menu"
    bl_options = {'INTERNAL'}

    def menu(self, menu, context):
        pr = prefs()
        layout = menu.layout
        layout.prop(pr, "show_panel_icons")

        if not pr.show_panel_icons:
            return

        layout.separator()
        layout.prop(pr, "show_matcap_icons")
        layout.prop(pr, "show_brush_icons")
        layout.prop(pr, "show_colorset_icons")

    def execute(self, context):
        context.window_manager.popup_menu(self.menu, "Icon Viewer")
        return {'FINISHED'}


class IV_OT_icon_copy(bpy.types.Operator):
    bl_idname = "iv.icon_copy"
    bl_label = ""
    bl_description = "Copy the icon"
    bl_options = {'INTERNAL'}

    icon = bpy.props.StringProperty()

    def execute(self, context):
        context.window_manager.clipboard = self.icon
        self.report({'INFO'}, self.icon)

        if self.icon in HISTORY:
            HISTORY.remove(self.icon)
        if len(HISTORY) >= HISTORY_SIZE:
            HISTORY.pop(0)
        HISTORY.append(self.icon)
        return {'FINISHED'}


class IV_OT_icon_select(bpy.types.Operator):
    bl_idname = "iv.icon_select"
    bl_label = ""
    bl_description = "Select the icon"
    bl_options = {'INTERNAL'}

    icon = bpy.props.StringProperty()

    def execute(self, context):
        pr = prefs()
        pr.popup_icons.selected_icon = self.icon
        if pr.copy_on_select:
            context.window_manager.clipboard = self.icon
            self.report({'INFO'}, self.icon)

            if pr.close_on_select and IV_OT_icons_show.instance:
                IV_OT_icons_show.instance.close()

        if self.icon in HISTORY:
            HISTORY.remove(self.icon)
        if len(HISTORY) >= HISTORY_SIZE:
            HISTORY.pop(0)
        HISTORY.append(self.icon)
        return {'FINISHED'}


class IV_OT_icons_show(bpy.types.Operator):
    bl_idname = "iv.icons_show"
    bl_label = "Icon Viewer"
    bl_description = "Icon viewer"
    bl_property = "filter_auto_focus"

    instance = None

    def set_filter(self, value):
        prefs().popup_icons.filter = value

    def set_selected_icon(self, value):
        if IV_OT_icons_show.instance:
            IV_OT_icons_show.instance.auto_focusable = False

    filter_auto_focus = bpy.props.StringProperty(
        description="Filter",
        get=lambda s: prefs().popup_icons.filter,
        set=set_filter,
        options={'TEXTEDIT_UPDATE', 'SKIP_SAVE'})
    filter = bpy.props.StringProperty(
        description="Filter",
        get=lambda s: prefs().popup_icons.filter,
        set=set_filter,
        options={'TEXTEDIT_UPDATE'})
    selected_icon = bpy.props.StringProperty(
        description="Selected Icon",
        get=lambda s: prefs().popup_icons.selected_icon,
        set=set_selected_icon)

    def get_num_cols(self, num_icons):
        return round(1.3 * math.sqrt(num_icons))

    def draw_header(self, layout):
        pr = prefs()
        header = layout.box()
        header = header.split(0.75) if self.selected_icon else header.row()
        row = header.row(True)
        row.prop(pr, "show_matcap_icons", "", icon='SMOOTH')
        row.prop(pr, "show_brush_icons", "", icon='BRUSH_DATA')
        row.prop(pr, "show_colorset_icons", "", icon='COLOR')
        row.separator()

        row.prop(
            pr, "copy_on_select", "",
            icon='BORDER_RECT', toggle=True)
        if pr.copy_on_select:
            sub = row.row(True)
            if bpy.context.window.screen.name == "temp":
                sub.alert = True
            sub.prop(
                pr, "close_on_select", "",
                icon='RESTRICT_SELECT_OFF', toggle=True)
        row.prop(
            pr, "auto_focus_filter", "",
            icon='OUTLINER_DATA_FONT', toggle=True)
        row.separator()

        if self.auto_focusable and pr.auto_focus_filter:
            row.prop(self, "filter_auto_focus", "", icon='FILTER')
        else:
            row.prop(self, "filter", "", icon='FILTER')

        if self.selected_icon:
            row = header.row()
            row.prop(self, "selected_icon", "", icon=self.selected_icon)

    def draw(self, context):
        pr = prefs()
        col = self.layout
        self.draw_header(col)

        subcol = col.column(True)
        box = subcol.box()

        num_cols = min(
            self.get_num_cols(len(pr.popup_icons.filtered_icons)),
            int((self.width - POPUP_PADDING) / (ui_scale() * ICON_SIZE)))

        pr.popup_icons.draw(box, num_cols)

        if HISTORY:
            box = subcol.box()
            pr.popup_icons.draw(box, num_cols, HISTORY)

    def close(self):
        bpy.context.window.screen = bpy.context.window.screen

    def check(self, context):
        return True

    def cancel(self, context):
        IV_OT_icons_show.instance = None

    def execute(self, context):
        if not IV_OT_icons_show.instance:
            return {'CANCELLED'}
        IV_OT_icons_show.instance = None

        pr = prefs()
        if self.selected_icon and not pr.copy_on_select:
            context.window_manager.clipboard = self.selected_icon
            self.report({'INFO'}, self.selected_icon)
        pr.popup_icons.selected_icon = ""
        return {'FINISHED'}

    def invoke(self, context, event):
        pr = prefs()
        pr.popup_icons.selected_icon = ""
        pr.popup_icons.filter = ""
        IV_OT_icons_show.instance = self
        self.auto_focusable = True

        num_cols = self.get_num_cols(len(pr.popup_icons.filtered_icons))
        self.width = min(
            ui_scale() * (num_cols * ICON_SIZE + POPUP_PADDING),
            context.window.width - WIN_PADDING)

        return context.window_manager.invoke_props_dialog(self, self.width)


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
