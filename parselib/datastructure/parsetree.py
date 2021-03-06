from parselib.datastructure.lexlib import Token

DEBUG=False

"""
classes to unfold the parsetree into someting understandable
"""

class UnitNode :
	def __init__ (self, unit, nodetype) :
		self.unit = unit
		self.nodetype = nodetype

	def iscompacted (self) :
		return self.nodetype.find("/") != -1

	def unfold(self, parent=None):
		if DEBUG :
			if self.iscompacted() or parent == self.nodetype :
				return self.unit.unfold(self.nodetype)
			else :#if parent != None :
				return " {} = [\n {} \n]".format(
					self.nodetype,
					self.unit.unfold(self.nodetype),
				)
		else :
			if self.iscompacted() or parent == self.nodetype :
				return self.unit.unfold(self.nodetype)
			else :#if parent != None :
				return [Token (
					self.nodetype,
					self.unit.unfold(self.nodetype), 0
				)]

	def __str__ (self) :
		return self.nodetype

class TokenNode :
	
	def __init__ (self, nodetype, val) :
		self.nodetype = nodetype
		self.val = val

	def unfold(self, parent=None):
		if DEBUG :
			return "{key}({val})".format(
				key=self.nodetype,
				val=self.val
			)
		else :
			return [Token(self.nodetype, self.val, 0)]
	
	def __str__ (self) :
		return self.nodetype

class BinNode :
	def __init__ (self, left, right, nodetype) :
		self.left = left
		self.right = right
		self.nodetype = nodetype

	#forcefully binarized rule
	def iscompacted (self) :
		return self.nodetype.find("/") != -1
	def islistnode (self) :
		return self.right.nodetype == self.left.nodetype

	def unfold(self, parent=None):
		if DEBUG :
			if self.iscompacted() or parent == self.nodetype : 
				return "{} \n {}".format( # make it merge two dicts
					self.left.unfold(self.nodetype),
					self.right.unfold(self.nodetype),
				)
			else :
				return "{} = [\n {} \n {} \n]".format(
					self.nodetype,
					self.left.unfold(self.nodetype),
					self.right.unfold(self.nodetype),
				)
		else :
			if self.iscompacted() or parent == self.nodetype : 
				return self.left.unfold(self.nodetype) + self.right.unfold(self.nodetype)
			else :
				return [Token(
					self.nodetype,
					self.left.unfold(self.nodetype) + self.right.unfold(self.nodetype),
					0
				)]
	
	def __str__ (self) :
		return self.unfold().__str__() #self.nodetype
