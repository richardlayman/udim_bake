'''
Filename: udim_bake.py
 
Description: Bakes UDIM texture tiles in Blender 
 
Copyright (C) 2022 Richard Layman, rlayman2000@yahoo.com 
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "UDIM Bake",
    "author": "Richard Layman",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "Render Properties > Bake > UDIM Bake",
    "description": "Bakes UDMI texture tiles",
    "warning": "",
    "doc_url": "",
    "category": "UV",
}


import bpy


def get_filepath(image, tile):
    return image.filepath.replace('<UDIM>',str(tile.number))

def get_tile_offset(tile):
    x = float(str(tile.number)[3]) - 1.0
    y = float(str(tile.number)[2])
    return x,y

def move_uvs(uvmap,x,y):
    for loop in uvmap.data:
        loop.uv.x = loop.uv.x + x
        loop.uv.y = loop.uv.y + y

def udim_bake(self, context):
    # Start
    print("udim bake")

    # SETUP
    obj = bpy.context.active_object
    mat = obj.active_material
    nodes = mat.node_tree.nodes
    udimnode = None
    udim = None # this will get set to the Image

    # verify the selected node is a UDIM
    for node in nodes:
        if node.type == 'TEX_IMAGE' and node.select == True:
            if node.image.source == 'TILED':
                udimnode = node
                udim = node.image

    # Error checking, fail if udim is None
    if udim is None:
        return False
 
    # get the udim info from the image
    tiles = udim.tiles

    # have to make sure we are in OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT') 

    # create the uv map to work on
    uvmaps = obj.data.uv_layers # UVLoopLayers
    uvmap = uvmaps.new(name="BAKE_UDIM_UVMap", do_init=True) # MeshUVLoopLayer
    uvmap.active = True

    # create the uvnode and image texture node we will use to bake off of
    uvnode = nodes.new('ShaderNodeUVMap')
    uvnode.uv_map = uvmap.name
    texnode = nodes.new('ShaderNodeTexImage')
    image = bpy.data.images.load(get_filepath(udim,tiles[0]))
    texnode.image = image
    # need to make the texnode active so it's the one that is baked to
    texnode.select = True
    nodes.active = texnode

    # link up the nodes
    link = mat.node_tree.links.new(uvnode.outputs[0],texnode.inputs[0])    
        
    # bake on of the images for each tile
    for tile in tiles:
        imagepath = get_filepath(udim,tile)
        print(imagepath)
        message = "Baking Tile:" + str(tile.number)
        self.report({'INFO'},message)
        
        image.filepath = imagepath
        image.reload()
        
        # move UVs
        x,y = get_tile_offset(tile)
        move_uvs(uvmap,-x,-y)

        # bake
        if context.scene.render.use_bake_multires:
            bpy.ops.object.bake_image(type=context.scene.cycles.bake_type)
        else:
            bpy.ops.object.bake(type=context.scene.cycles.bake_type, cage_extrusion=context.scene.render.bake.cage_extrusion, max_ray_distance=context.scene.render.bake.max_ray_distance)

        # move UVs back
        move_uvs(uvmap,x,y)

        # update images
        image.save()
        image.update()

    # CLEAN UP
    mat.node_tree.links.remove(link)
    nodes.remove(uvnode)
    bpy.data.images.remove(image)
    nodes.remove(texnode)
    uvmaps.remove(uvmap)

    # reload the udim images
    udim.reload()
    udim.update()
    udimnode.select = True
    nodes.active = udimnode
    return True

class OBJECT_OT_udim_bake(bpy.types.Operator):
    """Bake UDIM Textures"""
    bl_idname = "bake.udim"
    bl_label = "Bake UDIM Tiles"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        result = udim_bake(self, context)
        if result == True:
            self.report({'INFO'},'UDIM Baking Complete')
        else:
            self.report({'ERROR'},'UDIM Baking Failed!, Not a valid UDIM texture selected')

        return {'FINISHED'}


def udim_panel(self, context):
    bl_label = "UDIM Bake"
    bl_context = "render"
    bl_parent_id = "CYCLES_RENDER_PT_bake"
    COMPAT_ENGINES = {'CYCLES'}

    layout = self.layout
    row = layout.row()
    row.operator("bake.udim")


# Registration

def register():
    bpy.utils.register_class(OBJECT_OT_udim_bake)
    bpy.types.CYCLES_RENDER_PT_bake.append(udim_panel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_udim_bake)
    bpy.types.CYCLES_RENDER_PT_bake.remove(udim_panel)

if __name__ == "__main__":
    register()
