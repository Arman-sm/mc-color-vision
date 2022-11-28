def overlapList(baseList: list | tuple, topList: list | tuple) -> list:
	try:
		return [*topList, *baseList[len(topList):]]
	except IndexError:
		return topList