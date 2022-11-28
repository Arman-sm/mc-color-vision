import colorsys

from overlap_list import overlapList

# class RGB(NamedTuple):
# 	red: int
# 	green: int
# 	blue: int
# 	alpha: int = 1
	
class color:
	__slots__ = ["rgb", "alpha"]
	def __init__(self, red: float, green: float, blue: float, alpha: float) -> None:
		self.rgb: list = [red, green, blue]
		self.alpha = alpha

	@classmethod
	def fromRGBA255(cls, *args, **kwargs):
		args = [channel / 255 for channel in args]
		kwargs = dict((channelKey, channelValue / 255) for channelKey, channelValue in kwargs.items())
		return cls(*args, **kwargs)

	@property
	def rgba(self) -> tuple[float, float, float, float]:
		return self.rgb + [self.alpha]

	@rgba.setter
	def rgba(self, value):
		self.rgb = (result:=overlapList(self.rgba, value))[:3]
		self.alpha = result[3]

	@property
	def rgb255(self) -> tuple[float, float, float]:
		return [int(channel * 255) for channel in self.rgb]

	@rgb255.setter
	def rgb255(self, value):
		self.rgba = [channel / 255 for channel in value]

	@classmethod
	def createFromHsl(cls, *hsl, alpha: int = 1):
		return cls(*colorsys.hls_to_rgb(hsl[0], hsl[2], hsl[1]), alpha)

	@property
	def hsl(self) -> tuple[float, float, float]:
		return ((hls:=colorsys.rgb_to_hls(*[rgb for rgb in self.rgb]))[0], hls[2], hls[1])

	@property
	def hue(self) -> float:
		return self.hsl[0]

	@property
	def saturation(self):
		return self.hsl[1]

	@property
	def lightness(self) -> float:
		return self.hsl[2]

	def __repr__(self) -> str:
		return f"color(red={self.rgb[0]}, green={self.rgb[1]}, blue={self.rgb[2]}, alpha={self.alpha})"

	def __getitem__(self, index) -> float:
		return [*self.rgb, self.alpha][index]

	def __iter__(self):
		yield self.rgb[0]
		yield self.rgb[1]
		yield self.rgb[2]
		yield self.alpha

	def __add__(self, value):
		return color(*overlapList(self.rgba, [self[index] + channel for index, channel in enumerate(value[:4])]))

	def __sub__(self, value):
		return color(*overlapList(self.rgba, [self[index] - channel for index, channel in enumerate(value[:4])]))
	
	def __eq__(self, value) -> bool:
		return self.rgba == value[:]