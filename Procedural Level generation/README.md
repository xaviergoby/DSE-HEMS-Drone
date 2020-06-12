The content of this folder should go into \AirSim\Unreal\Environments\Blocks\Content
This would result in for example: \AirSim\Unreal\Environments\Blocks\Content\Procedural

It is recommended to set the IncludeFancyTiles Boolean in the Procedural level blueprint to False.
This gives you only tiles based on basic shapes included in the editor.
If you do include the fancy tiles shaders will have to be calculated and this takes time.

Assets from fancy tiles are in the other folders.