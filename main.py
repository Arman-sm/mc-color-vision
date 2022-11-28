from mcpi_e import minecraft
from PIL import Image
from build import *

server = minecraft.Minecraft.create("SERVER_ADDRESS", 4711, "USERNAME")
playerPos = server.player.getTilePos()
server.settings.SYS_SPEED = 0

with Image.open("horse.png") as img:
	image = img.convert("RGBA")
	
for x in range(image.width):
	for y in range(image.height):
		pixelColor = color.fromRGBA255(*image.getpixel((x, y)))
		block = [int(arg) for arg in colors[pixelColor.alpha][pixelColor.hue][pixelColor.lightness].data[0].split(",")]
		server.setBlock(
			playerPos.x + x, playerPos.y, playerPos.z + y,
			*block
	)
