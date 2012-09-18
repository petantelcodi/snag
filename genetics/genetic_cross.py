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
		print "delete from list hight than 4th level"
		for a in self.son:
			for b in a["child"]:
				for c in b["child"]:
					for d in c["child"]:
						d["child"] = []
		
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
				if iFather!=iMother:
					l = list()
					# add 1 to random number because our ids start from 1 not 0
					l.append(iFather+1)
					l.append(iMother+1)
					return l
					
					
	def deletedGen(self, genId):
		iLevel1 = -1
		iLevel2 = -1
		iLevel3 = -1
		iLevel4 = -1
		for a in self.son:
			iLevel1 +=1
			if int(a["id"])==genId:
				self.son.pop(iLevel1) 
			for b in a["child"]:
				iLevel2 +=1
				if int(b["id"])==genId:
					self.son[iLevel1]["child"].pop(iLevel2)
					for c in b["child"]:
						iLevel3 +=1
						if int(c["id"])==genId:
							self.son[iLevel1]["child"][iLevel2]["child"].pop(iLevel3)
						for d in c["child"]:
							iLevel4 +=1
							if int(d["id"])==genId:
								self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"].pop(iLevel4)
	
	def repeatedGens(self, gens):
		print "repeatedGens"
		if len(gens)>0:
			for a in gens:
				deletedGen(a["id"])
				for b in a["child"]:
					deletedGen(b["id"])
					for c in b["child"]:
						deletedGen(c["id"])
						for d in c["child"]:
							deletedGen(d["id"])
							
			
		
	def setGen(self,arId,gen,idGen ):
		print "setGen"
		iLevel1 = -1
		iLevel2 = -1
		iLevel3 = -1
		iLevel4 = -1
		for a in self.son:
			iLevel1 +=1
			if int(a["id"])==int(idGen):
				print self.son[iLevel1]
				self.son[iLevel1] = gen
				print self.son[iLevel1]
			for b in a["child"]:
				iLevel2 +=1
				if int(b["id"])==int(idGen):
					print self.son[iLevel1]["child"][iLevel2]
					self.son[iLevel1]["child"][iLevel2] = gen
					print self.son[iLevel1]["child"][iLevel2]
				for c in b["child"]:
					iLevel3 +=1
					if int(c["id"])==int(idGen):
						print self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]
						self.son[iLevel1]["child"][iLevel2]["child"][iLevel3] = gen
						print self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]
					for d in c["child"]:
						iLevel3 +=1
						if int(d["id"])==int(idGen):
							print self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"][iLevel4]
							self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"][iLevel4] = gen
							print self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"][iLevel4]
	
	def getGen(self,l,idGen):
		print "getGens - gen:", idGen
		iLevel1 = -1
		iLevel2 = -1
		iLevel3 = -1
		iLevel4 = -1
		for a in l:
			iLevel1 +=1 
			if int(a["id"])==int(idGen):
				return [[iLevel1],a]
			for b in a["child"]:
				iLevel2 +=1 
				if int(b["id"])==int(idGen):
					return [[iLevel1,iLevel2],b]
				for c in b["child"]:
					iLevel3 +=1 
					if int(c["id"])==int(idGen):
						return [[iLevel1,iLevel2,iLevel3],c]
					for d in c["child"]:
						iLevel4 +=1 
						if int(d["id"])==int(idGen):
							return [[iLevel1,iLevel2,iLevel3,iLevel4],d]

	def shiftFatherToMotherGens(self,idGen):
		print "shiftFatherToMotherGens"
		# 1. 
		genFather = self.getGen(self.father,idGen)
		genMother = self.getGen(self.mother,idGen)
		print "gen-father:", genFather
		print "gen-mother:", genMother
		
		#take gens that will be duplicated
		self.repeatedGens(genMother[1]["child"])
		
		self.setGen(genFather[0],genMother[1],idGen)
		print "new son:", self.father
		
		# 2. Clean errors and fill empty
		self.deleteArrayDeptherThan4Levels()
		self.fillEmptyGens()

	def pureCross(self):
		print "pureCross"
		rGens = self.randomGens()
		print self.father
	
		print "gens:",rGens
		self.shiftFatherToMotherGens(rGens[0])

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