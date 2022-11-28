import os
import sys

from PIL import Image

from color import color
from linearDict import *
from overlap_list import overlapList

#region color average
def rgbSum(RGBs: tuple[tuple[int, tuple[int, int, int, int]]] | tuple[color]) -> color:
	result = color(0, 0, 0, 0)
	for rgba in RGBs:
		result.rgba = [(addChannel * rgba[0]) + channel for addChannel, channel in zip(rgba[1], result.rgba)]
	result.rgb255 = result.rgba
	return result

def blockColorAverage(path) -> color:
	with Image.open(path) as image:
		image = image.convert("RGBA")
		return color(*[round(channel / (image.width * image.height), 2) for channel in rgbSum(image.getcolors())])
#endregion
points: list[tuple[str, color]] = []

# texturesPath, defaultBuildPath = "textures", "build.py"
texturesPath, buildPath = overlapList(("textures", "build.py"), sys.argv[1:])

print(f"<builder>: textures -> {texturesPath} | build -> {buildPath}")

#Saving color average of png textures with their file names
for file in os.listdir(texturesPath):
	if os.path.isfile(f"{texturesPath}/{file}") and os.path.splitext(f"{texturesPath}/{file}")[1] == ".png":
		points.append(
			(os.path.splitext(file)[0], blockColorAverage(f"{texturesPath}/{file}"))
		)
#alpha:
result = evenLinearDict(
	[],
	spacing = 0.25
)

for alphaGroup in group(items = points, precision = 0.25, key = lambda item: item[1].alpha):
	result.items.append(
		#hue
		evenLinearDict(
			items = [
				linearDict(
					items = makeDictItems(
						items = hueGroup,
						positionKey = lambda item: item[1].lightness
					)
				) for hueGroup in group(points, precision = .2, key = lambda item: item[1].hue)
			],
			spacing = 0.2
		)
	# evenLinearDict(
	# 	[
	# 		linearDict(
	# 			makeDictItems(
	# 				items = lightnessGroup,
	# 				positionKey = lambda item: item.saturation 
	# 			)
	# 		) for lightnessGroup in group(
	# 			items = hueGroup,
	# 			precision = .25
	# 		)
	# 	]
	# )
)
	
# result = group(points, precision = .1, key = lambda item: item[1].saturation)
# for hueGroup in :
# 	for saturationGroup in group(hueGroup, .25):
# 		result.items.append(linearDict(saturationGroup))

with open(buildPath, "w") as file:
	file.write(
		"from linearDict import *\n" \
		"from color import color\n" \
		"colors = " + repr(result)
	)