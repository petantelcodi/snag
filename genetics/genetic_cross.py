class genetic_cross{
	def __init__(self, father, mother, type):
		self.father = father
		self.mother = mother
		if type=="pure":
			self.pureCross()
		else if type=="same_level":
			self.sameLevelCross()
		else if type=="inferior_level":
			self.sameLevelCross()
			
	def pureCross(self):
		print "pureCross"
		
	def sameLevelCross(self):
		print "same level cross"
		
	def inferiorLevelCross(self):
		print "inferior level cross"
}

