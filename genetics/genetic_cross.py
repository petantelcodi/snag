import random

class genetic_cross:
	def __init__(self, father, mother, type, totalGens):
		self.totalGens = totalGens
		self.father = father
		self.mother = mother
		self.son = self.father
		if type=="pure":
			self.pureCross()
		elif type=="same_level":
			self.sameLevelCross()
		elif type=="inferior_level":
			self.sameLevelCross()

	def deleteArrayDeptherThan4Levels(self):
		print "delete more than 4 levels"
	def fillEmptyGens(self):
		print "fill empty gens"

	def randomGens(self):
		iFatherGen = 0
		iMotherGen = 1
		while iFatherGen !=iMotherGen and len(self.father)>2:
				print "while"
				iFather = random.randrange(0,self.totalGens)
				iMother = random.randrange(0,self.totalGens)
				# father lower number because is the better gen
				if self.father[iFather]["id"]!=self.mother[iMother]["id"]:
					l = list()
					l.append(iFather)
					l.append(iMother)

					return l

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
		print self.father
		print
		print rGens

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

if __name__=="__main__":
	father = [{'id': 1, 'child': [{'id': 5, 'child': [{'id': 4, 'child': []}]}]},{'id': 2, 'child': []},{'id': 3, 'child': []}]
	mother = [{'id': 2, 'child': [{'id': 4, 'child': [{'id': 5, 'child': []}]}]},{'id': 1, 'child': []},{'id': 3, 'child': []}]
	g = genetic_cross(father,mother,"pure",5)
	print g