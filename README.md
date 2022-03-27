UDIM Bake
=======

![3D View](https://raw.githubusercontent.com/richardlayman/udim_bake/master/img/udim_multires_baked_object.png)
![UDIM Tiles](https://raw.githubusercontent.com/richardlayman/udim_bake/master/img/udim_multires_baked_tiles.png)

Blender script that will bake all the tiles of a UDIM texture.

Introduction
---------------
Currenly Blender is not able to bake UDIM tiles, only the first tile will bake. There is a manual way to overcome this but it's very time consuming and prone to human error. The UDIM Bake script automates this process.

Current Status
---------------
The plugin has been tested for both multires and source/target objects using normals maps. It should work on all over types but has not been tested fully. Any problems that you encounter should be reported so it can be fixed.

Installation
---------------
Copy the udim_bake.py into the blender/scripts/addons/ folder. In Blender, go to the Preferences and enable the UDIM Bake addon. A 'Bake UDIM Tiles' button will appear in the Bake section of the Render Properties panel. This button will only be used for UDIM texture nodes; all other images will use the normal 'Bake' button.
![UI](https://raw.githubusercontent.com/richardlayman/udim_bake/master/img/udim_bake_ui.png)


