class genetic_cross{
	def __init__(self, father, mother, type):
		self.totalGens = 27 # or 32
		self.father = father
		self.mother = mother
		self.son = self.father
		if type=="pure":
			self.pureCross()
		else if type=="same_level":
			self.sameLevelCross()
		else if type=="inferior_level":
			self.sameLevelCross()
	
	def deleteArrayDeptherThan4Levels(self):
		print "delete more than 4 levels"
	def fillEmptyGens(self):
		print "fill empty gens"
		
	def randomGens(self):
		iFatherGen = 0
        iMotherGen = 0
		while iFatherGen !=iMotherGen and len(p)>2:
                iFather = randrange(0,self.totalGens)
                iMother = randrange(0,self.totalGens)
                # father lower number because is the better gen
                if self.father[iFather]["id"]!=self.mother[iMother]["id"]:
                	return [iFather,iMother]
                	
	def repetedGens(self):
		print repeatedGens
		
		
	def getGen(self):
		print "getGens"
    
    def shiftFatherToMotherGens(self,idGen):
    	print "shiftFatherToMotherGens"            	
		# 1. 
		#self.son
		
		# 2. Clean errors and fill empty
		self.deleteArrayDeptherThan4Levels()
		self.repetedGens()
		self.fillEmptyGens()
		
	def pureCross(self):
		print "pureCross"
		rGens = self.randomGens()
		idFather = self.father[rGens[0]]["id"]
		idMother = self.mother[rGens[1]]["id"]
		shiftFatherToMotherGens(idFather)
		shiftFatherToMotherGens(idMother)
		
	def sameLevelCross(self):
		print "same level cross"
		rGens = self.randomGens()
		
	def inferiorLevelCross(self):
		print "inferior level cross"
		rGens = self.randomGens()
}

