from dataclasses import dataclass
from math import floor

def indexByKey(iterable: tuple | list, key):
	for item in iterable:
		if key(item):
			return item

@dataclass(slots=True)
class linearDictItem:
	data: any
	position: float

class linearDict:
	__slots__ = ["_items", "_lastId", "__compiled"]
	def __init__(self, items: tuple[linearDictItem] = ()):
		self._items = sorted(items, key = lambda item: item.position)
		# self._lastId = max(items, key = lambda item: item.id).id
		self.__compiled = self._compile()

	@classmethod
	def fromPositionList(cls, positions):
		return cls(linearDictItem(index, position, None) for index, position in enumerate(positions))

	# def getById(self, id) -> linearDictItem:
	# 	return indexByKey(self._items, lambda item: item.id == id)

	def add(self, position, data):
		self._items = tuple(self._items | linearDictItem)

	def get(self, position) -> linearDictItem:
		for index, item in enumerate(self.__compiled):
			if position < item:
				return self._items[index-1]
		return self._items[0]
	
	def getByIndex(self, index: int) -> any:
		return self._items[index]

	def _compile(self) -> tuple[int]:
		return tuple((0, *(item.position - ((item.position - self._items[index - 1].position) / 2) for index, item in enumerate(self._items[1:], 1))))

	def __getitem__(self, position) -> linearDictItem:
		return self.get(position)

	def __iter__(self):
		for item in self._items:
			yield item

	def __repr__(self) -> str:
		return f"linearDict({self._items})"

class evenLinearDict:
	def __init__(self, items: list, spacing: float):
		self.items: list = items
		self.spacing: float = spacing

	def indexCalculation(self, position) -> linearDictItem:
		return int(position//self.spacing)

	def __getitem__(self, position) -> linearDictItem:
		if isinstance(position, slice):
			return self.items[self.indexCalculation(position.start):self.indexCalculation(position.stop):position.step]
		try:
			return self.items[self.indexCalculation(position)] 
		except IndexError:
			return self.items[-1]

	def __iter__(self):
		for item in self.items:
			yield item

	def __repr__(self) -> str:
		return f"evenLinearDict(items={self.items}, spacing={self.spacing})"

def group(items: list | tuple, precision: float, *, key = lambda item: item, startValue: int = None):
	#Sorting the items using the key and returning the data and the groupId
	items = ((data, key(data) // precision) for data in sorted(items, key = key))
	#Initializing variables
	result = [[None]]
	result[0][0], lastGroupId = next(items)
	#The amount of amplification needed for filling the blank areas in the list
	amplification = int(lastGroupId - startValue) if startValue != None else 0
	# amplification = 0
	for data, groupId in items:
		#Check if it's one or more steps bigger
		if lastGroupId < groupId:
			result.extend([result[-1]] * amplification)
			amplification = 0
			#Check if it's more than one step bigger
			if 1 < (difference := groupId - lastGroupId): #
				result.extend([result[-1]] * int(difference - (difference // 2)))
				amplification = int(difference // 2)
			result.append([])
		result[-1].append(data)
		lastGroupId = groupId
	result.extend([result[-1]] * amplification)
	
	return result

def makeDictItems(items, positionKey = lambda item: item):
	return [linearDictItem(item, positionKey(item)) for item in items]