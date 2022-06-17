import bpy
from mathutils import Vector
from bpy.props import IntProperty

class CreateAndParentArmatureForSelected(bpy.types.Operator):
    """ Resets selected objects' origins to Geometry and creates corresponding 
        armature / bone for each selected objects
    """
    bl_idname = "action.create_and_parent_armature_for_selected"
    bl_label = "Create And Parent Armature For Selected"
    
    # needs to be tested
    # https://blender.stackexchange.com/questions/62040/get-center-of-geometry-of-an-object
    def set_origin_cheap(self, selected_objects):
        mesh_objs = [o for o in selected_objects]
        
        for obj in mesh_objs:
            local_bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
            global_bbox_center = obj.matrix_world * local_bbox_center
            
    # Get the name from the object list
    # and operate on said name via builtin modules
    # bpy.data, bpy.ops...
    # But this is very expensive because builtin runs update() apparently :thinking:
    def set_origin_expensive(self, selected_objects):
        for obj in selected_objects:
            try:
                obj_name = obj.name
                object_from_data = bpy.data.objects[obj_name]
                object_from_data.select = True
                bpy.context.view_layer.objects.active = object_from_data
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            except Exception as msg:
                self.report({'ERROR'}, msg)
    
    def create_armature_and_bone(self, name, origin):
        try:
            
        except Exception as msg:
            self.report({'ERROR'}, msg)
            
    
    def create_bones_and_parent(self, selected_objects):
        bpy.ops.object.add(
            type='ARMATURE',
            enter_editmode=True,
            location=(0,0,0))
        obj_b = bpy.context.object
        obj_b.name = obj.name + 'Amt'
        obj_b.show_name = True
        armature = obj_b.data
        armature.name = obj_b.name + 'Amt'
        for obj in selected_objects:
            # Create a single bone
            bone = armature.edit_bones.new(obj.name + 'Bone')
            bone.head = (0,0,0)
            bone.tail = (0,0,1) 
            
            ## set this bone to obj location?
            
        bpy.ops.object.mode_set(mode='OBJECT')   
        obj.select = True
        bone_obj.select = True
        bpy.context.view_layer.objects.active = bone_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO', keep_transform=True)
            
            
    def execute(self, context):
        selected_objects = []
        for obj in bpy.context.selected_objects:
            selected_objects.append(obj)
        
        if len(selected_objects) == 0:
            self.report({'INFO'}, "No mesh is selected...")
            return {'CANCELLED'}
        
        self.set_origin_expensive(selected_objects)
        self.create_bones_and_parent(selected_objects)
        self.report({'INFO'}, "Finished! Set a total of " + str(len(selected_objects)) + " objects")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)

class GetRigidBodyData(bpy.types.Operator):
    """ Get rigid body data from the selected objects
    """
    
    bl_idname = "action.get_rigid_body_data"
    bl_label = "Get rigid body data from selected objects"
    
    # static variable for frame_start, frame_end and step
    op_frame_start = 0
    op_frame_end = 255
    op_frame_step = 1
    
    def bake_rigid_body_to_keyframe(self, selected_rigid_objects):
        bpy.ops.rigidbody.bake_to_keyframes()
    
    def bake_keyframes_from_mesh_to_bones(self, selected_rigid_objects):
        for obj in selected_rigid_objects :
            if obj.type in ['MESH'] and obj.animation_data:
                for fcurve in obj.animation_data.action.fcurves :
                    if fcurve.data_path.endswith(('location','rotation_euler','rotation_quaternion','scale')):
                        print(obj.parent)
                        #for amt_fcurve in obj.parent.animation_data.action.fcurves:
                         #   amt_fcurve = fcurve
                        
                        # for key in fcurve.keyframe_points :
                            # print('frame:',key.co[0],'value:',key.co[1])
    
    # Get all 'ACTIVE' rigid body
    def execute(self, context):
        selected_rigid_objects = []
        for obj in bpy.context.selected_objects:
            if obj.rigid_body is not None and obj.rigid_body.type == 'ACTIVE':
                selected_rigid_objects.append(obj)
        
        if len(selected_rigid_objects) == 0:
            self.report({'INFO'}, "No rigid body mesh is selected...")
            return {'CANCELLED'}
        
        # Bake first
        # Then for each rigid body, get the keyframe data 
        self.bake_rigid_body_to_keyframe(selected_rigid_objects)
        self.bake_keyframes_from_mesh_to_bones(selected_rigid_objects)
        self.report({'INFO'}, "Finished! Set a total of " + str(len(selected_rigid_objects)) + " objects")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)
    

def register():
    bpy.utils.register_class(CreateAndParentArmatureForSelected)
    bpy.utils.register_class(GetRigidBodyData)


def unregister():
    bpy.utils.unregister_class(CreateAndParentArmatureForSelected)
    bpy.utils.unregister_class(GetRigidBodyData)


if __name__ == "__main__":
    register()
