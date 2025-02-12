import bpy
import bge_netlogic

class BGELogicPanel(bpy.types.Panel):
    bl_label = "BGE Logic Tree"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    #bl_category = "BGE Logic Tree"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGELogicTree.bl_idname)
        if enabled and (context.space_data.edit_tree is not None):
            bge_netlogic._consume_update_tree_code_queue()
            if not bge_netlogic._tree_code_writer_started:
                bge_netlogic._tree_code_writer_started = True
                bpy.ops.bgenetlogic.treecodewriter_operator()
        return enabled

    def get_combined_status_of_tree_items(self, tree_item_list):
        last = None
        for e in tree_item_list:
            initial_status = e.tree_initial_status
            if last == None: last = initial_status
            elif last != initial_status: return None#None means undefined, mixed, some are enabled, some are disabled
        return last

    def draw(self, context):
        layout = self.layout
        layout.operator(bge_netlogic.ops.NLPopupTemplatesOperator.bl_idname, text="Custom Nodes Templates...")
        layout.operator(bge_netlogic.ops.NLImportProjectNodes.bl_idname, text="Import logic nodes")
        layout.operator(bge_netlogic.ops.NLLoadProjectNodes.bl_idname, text="Refresh Imported Nodes")
        layout.operator(bge_netlogic.ops.NLApplyLogicOperator.bl_idname, text="Apply logic to selected objects").owner = "BGELogicPanel"
        layout.separator()
        layout.operator(bge_netlogic.ops.NLGenerateLogicNetworkOperator.bl_idname, text="Force Code Update")
        selected_objects = [ob for ob in context.scene.objects if ob.select]
        active_tree_items = {}
        #current elements box
        box = layout.box()
        box.label(text="Applied Trees")
        for ob in selected_objects:
            for e in ob.bgelogic_treelist:
                data = active_tree_items.get(e.tree_name)
                if data is None:
                    data = []
                    active_tree_items[e.tree_name] = data
                data.append(e)
        for name in active_tree_items:
            status = self.get_combined_status_of_tree_items(active_tree_items[name])
            status_icon = "CHECKBOX_DEHLT"
            if status is None:
                status_icon = "QUESTION"
                status = False#For mixed states, apply means "set it to enabled"
            elif status is True:
                status_icon = "CHECKBOX_HLT"
            row = box.row(align=True)
            row.label(name)
            op_data = row.operator(bge_netlogic.ops.NLSwitchInitialNetworkStatusOperator.bl_idname, text="", icon=status_icon)
            op_data.tree_name = name
            op_data.current_status = status
            row.operator(bge_netlogic.ops.NLSelectTreeByNameOperator.bl_idname, text="", icon="NODETREE").tree_name = name
            row.operator(bge_netlogic.ops.NLRemoveTreeByNameOperator.bl_idname, text="", icon="X").tree_name = name
        pass


def update_tree_code(self, context):
    bge_netlogic.update_current_tree_code()


class BGELogicTree(bpy.types.NodeTree):
    bl_idname = "BGELogicTree"
    bl_label = "BGE Logic Tree"
    bl_icon = "NODE"

    @classmethod
    def poll(cls, context):
        return True

    def update(self):
        bge_netlogic.update_current_tree_code()
    pass