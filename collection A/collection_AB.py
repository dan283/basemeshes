bl_info = {
    "name": "Collection Visibility Switcher",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Toggle visibility between two selected collections in the N-panel."
}

import bpy

def get_collection_names(self, context):
    """Returns a list of collection names for the dropdown."""
    return [(col.name, col.name, "") for col in bpy.data.collections]

def toggle_visibility(scene):
    """Toggles visibility between two collections."""
    collection_a = bpy.data.collections.get(scene.collection_a)
    collection_b = bpy.data.collections.get(scene.collection_b)

    if collection_a and collection_b:
        if not collection_a.hide_viewport and collection_b.hide_viewport:
            collection_a.hide_viewport = True
            collection_b.hide_viewport = False
        elif not collection_b.hide_viewport and collection_a.hide_viewport:
            collection_a.hide_viewport = False
            collection_b.hide_viewport = True

class CollectionSwitcherPanel(bpy.types.Panel):
    """UI Panel for the Collection Switcher."""
    bl_label = "Collection Switcher"
    bl_idname = "VIEW3D_PT_collection_switcher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Switcher'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Dropdown menus for collections A and B
        layout.prop(scene, "collection_a", text="Collection A")
        layout.prop(scene, "collection_b", text="Collection B")

        # Button to toggle visibility
        layout.operator("collection.switch_visibility", text="Switch")

class SwitchVisibilityOperator(bpy.types.Operator):
    """Operator to toggle visibility between two collections."""
    bl_idname = "collection.switch_visibility"
    bl_label = "Switch Collection Visibility"

    def execute(self, context):
        scene = context.scene
        collection_a = bpy.data.collections.get(scene.collection_a)
        collection_b = bpy.data.collections.get(scene.collection_b)

        if not collection_a or not collection_b:
            self.report({'WARNING'}, "Both collections must be selected.")
            return {'CANCELLED'}

        toggle_visibility(scene)
        return {'FINISHED'}

classes = [
    CollectionSwitcherPanel,
    SwitchVisibilityOperator
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Add properties to the scene for dropdowns
    bpy.types.Scene.collection_a = bpy.props.EnumProperty(
        name="Collection A",
        description="Select Collection A",
        items=get_collection_names,
    )

    bpy.types.Scene.collection_b = bpy.props.EnumProperty(
        name="Collection B",
        description="Select Collection B",
        items=get_collection_names,
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Remove properties from the scene
    del bpy.types.Scene.collection_a
    del bpy.types.Scene.collection_b

if __name__ == "__main__":
    register()
