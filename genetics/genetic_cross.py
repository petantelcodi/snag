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
		iLevel1 = -1
		iLevel2 = -1
		iLevel3 = -1
		iLevel4 = -1
		for a in self.son:
			iLevel1 +=1
			iLevel2 = -1
			iLevel3 = -1
			iLevel4 = -1
			for b in a["child"]:
				iLevel2 +=1
				iLevel3 = -1
				iLevel4 = -1
				for c in b["child"]:
					iLevel3 +=1
					iLevel4 = -1
					for d in c["child"]:
						iLevel4 +=1
						if len(self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"][iLevel4]["child"])>0:
							self.gensDeleted.append(self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"][iLevel4]["child"])
						self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"][iLevel4]["child"]=[]
		
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
					
					
	def deletedSimpleGen(self, genId,shiftGen):
		iLevel1 = -1
		iLevel2 = -1
		iLevel3 = -1
		iLevel4 = -1
		for a in self.son:
			iLevel1 +=1
			iLevel2 = -1
			iLevel3 = -1
			iLevel4 = -1
			if a!=shiftGen and int(a["id"])==genId:
				self.son.pop(iLevel1) 
			for b in a["child"]:
				iLevel2 +=1
				iLevel3 = -1
				iLevel4 = -1
				if b!=shiftGen and int(b["id"])==genId:
					self.son[iLevel1]["child"].pop(iLevel2)
					for c in b["child"]:
						iLevel3 +=1
						iLevel4 = -1
						if c!=shiftGen and int(c["id"])==genId:
							self.son[iLevel1]["child"][iLevel2]["child"].pop(iLevel3)
						for d in c["child"]:
							iLevel4 +=1
							if d!=shiftGen and int(d["id"])==genId:
								self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"].pop(iLevel4)
	
	def deletedGetChildGen(self, genId):
		iLevel1 = -1
		iLevel2 = -1
		iLevel3 = -1
		iLevel4 = -1
		for a in self.son:
			iLevel1 +=1
			iLevel2 = -1
			if int(a["id"])==genId:
				self.son[iLevel1] = self.son[iLevel1]["child"] 
				break
			for b in a["child"]:
				iLevel2 +=1
				iLevel3 = -1
				if int(b["id"])==genId:
					self.son[iLevel1]["child"][iLevel2] = self.son[iLevel1]["child"][iLevel2]["child"]
					break
					for c in b["child"]:
						iLevel3 +=1
						iLevel4 = -1
						if int(c["id"])==genId:
							self.son[iLevel1]["child"][iLevel2]["child"][iLevel3] = self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"]
							break
						for d in c["child"]:
							iLevel4 +=1
							print "d:",d
							if int(d["id"])==genId:
								self.son[iLevel1]["child"][iLevel2]["child"][iLevel3]["child"].pop(iLevel4)
								break
								
	def repeatedGensSmart(self, gens):
		print "repeatedGens"
		if len(gens)>0:
			for a in gens:
				deletedGetChildGen(a["id"])
				for b in a["child"]:
					deletedGetChildGen(b["id"])
					for c in b["child"]:
						deletedGetChildGen(c["id"])
						for d in c["child"]:
							deletedGetChildGen(d["id"])
							
	def repeatedGens(self, gens,shiftGen):
		print "repeatedGens"
		if len(gens)>0:
			for a in gens:
				self.deletedSimpleGen(a["id"],shiftGen)
				for b in a["child"]:
					self.deletedSimpleGen(b["id"],shiftGen)
					for c in b["child"]:
						self.deletedSimpleGen(c["id"],shiftGen)
						for d in c["child"]:
							self.deletedSimpleGen(d["id"],shiftGen)
							
			
		
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
		
		
		self.setGen(genFather[0],genMother[1],idGen)
		print "new son:", self.father
		
		# 2. Clean errors and fill empty
		self.deleteArrayDeptherThan4Levels()
		self.repeatedGens(genMother[1]["child"],genMother[1])
		
		self.fillEmptyGens()

	
	def shiftInferiorLevelGens(self, gen1, gen2):
		print "shiftInferiorLevelGens"
		
	def shiftSameLevelGens(self, gen1, gen2):
		print "shiftSameLevelGens"
	
	def pureCross(self):
		print "pureCross"
		rGens = self.randomGens()
		print self.father
	
		print "gens:",rGens
		# shift two gens
		self.shiftFatherToMotherGens(rGens[0])
		self.shiftFatherToMotherGens(rGens[1])

	def sameLevelCross(self):
		print "same level cross"
		rGens = self.randomGens()
		self.shiftSameLevelGens(rGens[0],rGens[1])


	def inferiorLevelCross(self):
		print "inferior level cross"
		rGens = self.randomGens()
		self.shiftInferiorLevelGens(rGens[0],rGens[1])

if __name__=="__main__":
	father = [{'id': 1, 'child': [{'id': 5, 'child': [{'id': 4, 'child': []}]}]},{'id': 2, 'child': []},{'id': 3, 'child': []}]
	mother = [{'id': 2, 'child': [{'id': 4, 'child': [{'id': 5, 'child': []}]}]},{'id': 1, 'child': []},{'id': 3, 'child': []}]
	g = genetic_cross(father,mother,"pure",5)
	print g