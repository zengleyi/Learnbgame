import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty, EnumProperty
import bmesh
from . fuse import handlemethoditems
from . unfuse import unfuse, get_sweeps
from . unchamfer import unchamfer, unchamfer_intersection
from ..utils.graph import build_mesh_graph
from ..utils.core import get_2_rails, init_sweeps, get_loops, create_loop_intersection_handles, create_face_intersection_handles
from ..utils.debug import debug_sweeps, vert_debug_print
from ..utils.developer import output_traceback
from ..utils.ui import popup_message, step_enum, draw_init, draw_end, draw_title, draw_prop, wrap_mouse
from ..utils import MACHIN3 as m3



class OperatorSettings:
    # see https://blender.stackexchange.com/questions/6520/should-an-operator-remember-its-last-used-settings-when-invoked
    _settings = {}

    def save_settings(self):
        for d in dir(self.properties):
            if d in ['bl_rna', 'rna_type', 'allowmodalslide', 'reverse', 'slide']:
                continue
            try:
                self.__class__._settings[d] = self.properties[d]
            except KeyError:
                # catches __doc__ etc.
                continue

    def load_settings(self):
        # what exception could occur here??
        for d in self.__class__._settings:
            self.properties[d] = self.__class__._settings[d]


class Unbevel(bpy.types.Operator, OperatorSettings):
    bl_idname = "machin3.unbevel"
    bl_label = "MACHIN3: Unbevel"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Unfuse + Unchamfer"

    handlemethod = EnumProperty(name="Unchamfer Method", items=handlemethoditems, default="FACE")

    slide = FloatProperty(name="Slide", default=0, min=-1, max=1)

    reverse = BoolProperty(name="Reverse", default=False)

    sharps = BoolProperty(name="Set Sharps", default=True)
    bweights = BoolProperty(name="Set Bevel Weights", default=False)
    bweight = FloatProperty(name="Weight", default=1, min=0, max=1)

    # hiddden
    cyclic = BoolProperty(name="Cyclic", default=False)
    single = BoolProperty(name="Single", default=False)

    # modal
    allowmodalslide = BoolProperty(default=False)

    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        row = column.row()
        row.prop(self, "handlemethod", expand=True)

        if self.handlemethod == "FACE":
            column.prop(self, "slide")

        column.prop(self, "sharps")

        row = column.row()
        row.prop(self, "bweights")
        row.prop(self, "bweight")

        if self.single:
            column.prop(self, "reverse")

    @classmethod
    def poll(cls, context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        return len([f for f in bm.faces if f.select]) >= 1 or len([e for e in bm.edges if e.select]) >= 1

    def draw_HUD(self, args):
        draw_init(self, args)

        draw_title(self, "Unbevel")

        draw_prop(self, "Handles", self.handlemethod, key="scroll UP/Down")
        self.offset += 10

        if self.handlemethod == "FACE":
            draw_prop(self, "Slide", self.slide, offset=18, decimal=2, active=self.allowmodalslide, key="move LEFT/RIGHT, toggle W, reset ALT + W")
            self.offset += 10

        draw_prop(self, "Set Sharps", self.sharps, offset=18, key="toggle S")
        draw_prop(self, "Set BWeights", self.bweights, offset=18, key="toggle B")
        if self.bweights:
            draw_prop(self, "BWeight", self.bweight, offset=18, key="ALT scroll UP/DOWN")
        self.offset += 10

        if self.single:
            draw_prop(self, "Reverse", self.reverse, offset=18, key="toggle R")

        draw_end()

    def modal(self, context, event):
        context.area.tag_redraw()

        # update mouse postion for HUD
        if event.type == "MOUSEMOVE":
            self.mouse_x = event.mouse_region_x
            self.mouse_y = event.mouse_region_y


        events = ['WHEELUPMOUSE', 'UP_ARROW', 'ONE', 'WHEELDOWNMOUSE', 'DOWN_ARROW', 'TWO', 'S', 'B', 'W', 'R']

        # only consider MOUSEMOVE as a trigger, when modalwidth or modaltension are actually active
        if self.allowmodalslide:
            events.append('MOUSEMOVE')

        if event.type in events:

            # CONTROL slide

            if event.type == 'MOUSEMOVE':
                delta_x = self.mouse_x - self.init_mouse_x  # bigger if going to the right

                if self.allowmodalslide:
                    wrap_mouse(self, context, event, x=True)

                    self.slide = delta_x * 0.01

            # CONTROL segments, method, handlemethod and capdissolveangle

            elif event.type in {'WHEELUPMOUSE', 'UP_ARROW', 'ONE'} and event.value == 'PRESS':
                if event.alt:
                    self.bweight += 0.1
                else:
                    self.handlemethod = step_enum(self.handlemethod, handlemethoditems, 1)

            elif event.type in {'WHEELDOWNMOUSE', 'DOWN_ARROW', 'TWO'} and event.value == 'PRESS':
                if event.alt:
                    self.bweight -= 0.1
                else:
                    self.handlemethod = step_enum(self.handlemethod, handlemethoditems, -1)

            # TOGGLE sharps, bweights and reverse

            elif event.type == 'S' and event.value == "PRESS":
                self.sharps = not self.sharps

            elif event.type == 'B' and event.value == "PRESS":
                self.bweights = not self.bweights

            elif event.type == 'R' and event.value == "PRESS":
                self.reverse = not self.reverse

            # TOGGLE modal slide

            elif event.type == 'W' and event.value == "PRESS":
                if event.alt:
                    self.allowmodalslide = False
                    self.slide = 0
                else:
                    self.allowmodalslide = not self.allowmodalslide

            # modal unbevel
            try:
                self.ret = self.main(self.active, modal=True)

                # success
                if self.ret:
                    self.save_settings()
                # caught an error
                else:
                    bpy.types.SpaceView3D.draw_handler_remove(self.HUD, 'WINDOW')
                    return {'FINISHED'}
            # unexpected error
            except:
                output_traceback(self)
                bpy.types.SpaceView3D.draw_handler_remove(self.HUD, 'WINDOW')
                mode = m3.get_mode()
                if mode == "OBJECT":
                    m3.set_mode("EDIT")
                return {'FINISHED'}

        # VIEWPORT control

        elif event.type in {'MIDDLEMOUSE'}:
            return {'PASS_THROUGH'}

        # FINISH

        elif event.type in {'LEFTMOUSE', 'SPACE'}:
            bpy.types.SpaceView3D.draw_handler_remove(self.HUD, 'WINDOW')
            return {'FINISHED'}

        # CANCEL

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel_modal()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def cancel_modal(self, removeHUD=True):
        if removeHUD:
            bpy.types.SpaceView3D.draw_handler_remove(self.HUD, 'WINDOW')

        m3.set_mode("OBJECT")
        self.initbm.to_mesh(self.active.data)
        m3.set_mode("EDIT")

    def invoke(self, context, event):
        self.load_settings()

        self.active = m3.get_active()

        # make sure the current edit mode state is saved to obj.data
        self.active.update_from_editmode()

        # save this initial mesh state, this will be used when canceling the modal and to reset it for each mousemove event
        self.initbm = bmesh.new()
        self.initbm.from_mesh(self.active.data)

        # mouse positions
        self.mouse_x = self.init_mouse_x = self.fixed_mouse_x = event.mouse_region_x
        self.mouse_y = self.init_mouse_y = self.fixed_mouse_y = event.mouse_region_y

        # first run, this is necessary if there's no mouse movement event
        try:
            self.ret = self.main(self.active, modal=True)
            if self.ret:
                self.save_settings()
            else:
                self.cancel_modal(removeHUD=False)
                return {'FINISHED'}
        except:
            output_traceback(self)
            mode = m3.get_mode()
            if mode == "OBJECT":
                m3.set_mode("EDIT")
            return {'FINISHED'}

        args = (self, context)
        self.HUD = bpy.types.SpaceView3D.draw_handler_add(self.draw_HUD, (args, ), 'WINDOW', 'POST_PIXEL')

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        active = m3.get_active()

        try:
            self.main(active)
        except:
            output_traceback(self)

        return {'FINISHED'}

    def main(self, active, modal=False):
        debug = True
        debug = False

        active = m3.get_active()

        if debug:
            m3.clear()
            # m3.debug_idx()

        m3.set_mode("OBJECT")

        if modal:
            self.initbm.to_mesh(active.data)

        # create bmesh
        bm = bmesh.new()
        bm.from_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        bw = bm.edges.layers.bevel_weight.verify()

        mg = build_mesh_graph(bm, debug=debug)
        verts = [v for v in bm.verts if v.select]
        faces = [f for f in bm.faces if f.select]

        sweeps = get_sweeps(bm, mg, verts, faces, debug=debug)

        if sweeps:
            chamfer_faces = unfuse(bm, faces, sweeps, debug=debug)

            if chamfer_faces:
                if len(chamfer_faces) == 1:
                    self.single = True
                else:
                    self.single = False

                chamfer_verts = [v for v in bm.verts if v.select]
                chamfer_mg = build_mesh_graph(bm, debug=debug)

                ret = get_2_rails(bm, chamfer_mg, chamfer_verts, chamfer_faces, reverse=self.reverse, debug=debug)
                if ret:
                    chamfer_rails, self.cyclic = ret

                    chamfer_sweeps = init_sweeps(bm, active, chamfer_rails, debug=debug)
                    # debug_sweeps(sweeps, self.cyclic)
                    get_loops(bm, chamfer_faces, chamfer_sweeps, debug=debug)

                    if self.handlemethod == "FACE":
                        create_face_intersection_handles(bm, chamfer_sweeps, tension=1, debug=debug)
                        double_verts = unchamfer_intersection(bm, chamfer_sweeps, slide=self.slide, debug=debug)
                    elif self.handlemethod == "LOOP":
                        create_loop_intersection_handles(bm, chamfer_sweeps, tension=1, debug=debug)
                        double_verts = unchamfer(bm, chamfer_sweeps, debug=debug)

                    self.clean_up(bm, chamfer_sweeps, chamfer_faces, double_verts, magicloop=True, initialfaces=True, deselect=False, debug=debug)

                    if double_verts:
                        hardedges = [e for e in bm.edges if e.select]

                        # set hard edge to sharp
                        if any([self.sharps, self.bweights]):
                            if self.sharps:
                                bpy.context.object.data.show_edge_sharp = True
                            if self.bweights:
                                bpy.context.object.data.show_edge_bevel_weight = True

                            for he in hardedges:
                                if self.sharps:
                                    he.smooth = False
                                if self.bweights:
                                    he[bw] = self.bweight

                        bm.to_mesh(active.data)

                        m3.set_mode("EDIT")

                        # m3.set_mode("VERT")
                        # m3.set_mode("EDGE")
                        return True

                    else:
                        if self.single:
                            popup_message(["Loop edges don't intersect. You can't unbevel in this direction!", "Try toggling Reverse."])
                        else:
                            popup_message(["Loop edges don't intersect."])
                else:
                    # abort, but at least bring back the unchamferd state to this point, as without it any ngon warning doesnt make sense
                    bm.to_mesh(active.data)

                    m3.set_mode("EDIT")
                    return True

        m3.set_mode("EDIT")

        return False

    def clean_up(self, bm, sweeps, faces, double_verts=None, magicloop=True, initialfaces=True, deselect=False, debug=False):
        # remove the magic loops
        if magicloop:
            magic_loops = []

            for sweep in sweeps:
                for idx, lt in enumerate(sweep["loop_types"]):
                    if lt in ["MAGIC", "PROJECTED"]:
                        magic_loops.append(sweep["loops"][idx])

            magic_loop_ids = [str(l.index) for l in magic_loops]

            # 1: DEL_VERTS, 2: DEL_EDGES, 3: DEL_ONLYFACES, 4: DEL_EDGESFACES, 5: DEL_FACES, 6: DEL_ALL, 7: DEL_ONLYTAGGED};
            # see https://blender.stackexchange.com/a/1542/33919 for context enum details
            bmesh.ops.delete(bm, geom=magic_loops, context=2)

            if debug:
                print()
                print("Removed magic and projected loops:", ", ".join(magic_loop_ids))

        # remove originally selected faces
        if initialfaces:
            face_ids = [str(f.index) for f in faces]

            bmesh.ops.delete(bm, geom=faces, context=5)

            if debug:
                print()
                print("Removed faces:", ", ".join(face_ids))

        if double_verts:
            bmesh.ops.remove_doubles(bm, verts=double_verts, dist=0.00001)

        # unselect everything
        if deselect:
            if not debug:
                for v in bm.verts:
                    v.select = False

                bm.select_flush(False)
