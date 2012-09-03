# Create your views here.
from django.contrib.gis.gdal.prototypes import generation
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from genview.models import Creature
from snag.genview.models import Tasks, Chromosome, Creature
from django.utils.encoding import smart_str, smart_unicode
#from django.contrib.auth.models import Use
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import randint, shuffle, random, seed
from django.db import reset_queries, close_connection
from sys import *

import datetime
import math
import operator
import random

class genetics:
	def __init__(self):
		# gloval vars reproduction
		self.total_test_time = 30
		self.totalBestTimesToPreserve = 4
		
		print("_init_")
		self.reproduce(3)# this is just for testing 

	def reproduce(self, finished_creature_id): ## TODO: add a second argument for current generation
		print("Start reproduce chromosomes")
		self.crom_list = [] # original cromosomes that have finish correct and on time gived
                self.crom_list_selected = [] # the best cromosomes
                self.crom_list_rest = [] # chromosomes which are valid bu not best
		self.crom_list_rest_obj = [] 
		self.crom_reproduced = [] # the cromosomes that we will save to database
		print("1. Get complete generation")
		i = 5
		for m in Chromosome.objects.filter(creature_id=finished_creature_id): ## TODO: add filter(current_generation 
			mytasks = Tasks.objects.get(chromosome_id=m.id)
			l = [m.id, eval(m.data),m.generation,mytasks.test_date,mytasks.total_test_time,mytasks.test_ok ]
			# Step 1: add to list all cromosomes that has respond good and not out of time
			if(mytasks.test_ok==1 and mytasks.total_test_time < self.total_test_time):
				print(l)
				self.crom_list.append(l)
			else:
				print('cromosome discarted')
		# Step 2: Get two best time to preserve 
		# Sort list to get best times first
		# sort by colum 4		
		self.crom_list = sorted(self.crom_list, key=operator.itemgetter(4))		
		print("-----")
		print(self.crom_list)
		
		# Add best cromosomes
		bestTime = self.crom_list[0][4]
		totalBestTimes = 1
		for m in self.crom_list:
			if bestTime != m[4]:
				bestTime = m[4]
				totalBestTimes +=1
				
			# A) The best times
			# In case there where more from each time
			# B) # if there is already too many best chromosomes stop 		
			if self.totalBestTimesToPreserve >=totalBestTimes and len(self.crom_list_selected)>self.totalBestTimesToPreserve:
				self.crom_list_selected.append(m)
				print("best chromosome:")
				print(m[4])
			else:
				self.crom_list_rest.append(m)
				print("add chromosome to middle list ")		
		# Step 3 : cut tree
		print("------")
		testData =["0101", "0202","0303","030104","03010105"]
		p = self.chromosomesToArray(testData)
		print("test data converted to array:")
		print(p)
		b = self.arrayToChromosomes(p)
		print(b)		
		# Step 4 : mutation (set to 0.5% cases)
		for m in self.crom_reproduced:			
			if(random(200)==32 or  random(200)==100):
				self.mutateOneGen(m)

	def parseAndAddGen(self, gen):	
		dataType = {"id":0,"child":[]}
		posGenAr = [] 	
		id = gen[-2:]
		h = gen[:-2]
		for p in range(0, len(gen[:-2]), 2):
			c = int(h[p]+h[p+1])-1
			posGenAr.append(c)	
		print("parseGen")
		dataType["id"] = int(id)
		if(len(posGenAr)==1):
			self.selfChromosomeAr.append(dataType)
		if(len(posGenAr)==2):
			print(posGenAr[0])
			self.selfChromosomeAr[posGenAr[0]]["child"].append(dataType)
		if(len(posGenAr)==3):
                        self.selfChromosomeAr[posGenAr[0]]["child"][posGenAr[1]]["child"].append(dataType)
		if(len(posGenAr)==4):
                        self.selfChromosomeAr[posGenAr[0]]["child"][posGenAr[1]]["child"][posGenAr[2]]["child"].append(dataType)
		if(len(posGenAr)==5):
                        self.selfChromosomeAr[posGenAr[0]]["child"][posGenAr[1]]["child"][posGenAr[2]]["child"][posGenAr[3]]["child"].append(dataType)

	# receive a list of chromosomes in string and return array
	def chromosomesToArray(self, l):
		# to convert i need sort from levels in array (from level 0 to more deep levels)
		lSorted = sorted(l,key=len)
		self.selfChromosomeAr = []
		for i in lSorted:
			self.parseAndAddGen(i)
		print("chromosomes")
		return self.selfChromosomeAr

	def cPrepare(self,value):
		v = str(value)
		if len(v)>2:
			v="0"+v
		return v			

	def arrayToChromosomes(self, ar):
		out = list()
		print("check array len:")
		print(len(ar))
		for a in ar:
			if 'c1' not in locals():
				c1=0
			c1 += 1
			cs1 = self.cPrepare(c1)
			id1 = str(a["id"])
			out.append(cs1+self.cPrepare(id1))			
			for b in a["child"]:
				if 'c2' not in locals():
                                	c2=0
                        	c2 += 1
				id2 = b["id"]
				cs2 = cs1+self.cPrepare(c2)
				out.append(cs2+self.cPrepare(id2))
				for c in b["child"]:
					if 'c3' not in locals():
                                        	c3=0
					c3 += 1
					id3 = c["id"]
					cs3 = cs2+self.cPrepare(c3)
					out.append(cs3+self.cPrepare(id3))
					for d in c["child"]:
						if 'c4' not in locals():
                                        		c4=0
						c4 += 1
						id4 = d["id"]
						cs4 = cs3+self.cPrepare(c4)
						out.append(cs4+self.cPrepare(id4))		
                print("chromosomes")
		return out

	def cutPure(self):
		print("CutPure")
	
	def cutByEditSameLevel(self):
		print("CuteByEditSameLevel")	

	def cutByEditLowerLevel(self):
                print("CuteByEditLowerLevel")

	def findTreeRepitedGens(self):
		print("findRepitedGens")		

	def fillTreeGaps(self):
		print("fillTreeGaps")

 	def mutateOneGen(self, crom):
		r1 = random(self.totalGens)
		r2 = random(self.totalGens)
		temp1 = crom[4][r1]
		temp2 = crom[4][r2]
		crom[4][r1] = temp1[:-2] + temp2[-2:]
		crom[4][r2] = temp2[:-2] + temp1[-2:]
		print("The chromosome had mutated!") 
		
	def saveToBD(self):
		print("Save chromosomes reproduced")
		print(self.crom_reproduced)
		# Save 50 chromosomes with 39 gens each of them with the structure ????
		chromosomes = []
		max = len(self.crom_reproduced)
		for n in range(1, max+1): ## FIXME this is for testiog. The good values is range(1,51)
			shuffle(tags_ids)
			chromosome = []
			c = 0
			for d in struc_base:
				chromosome.append(d+tags_ids[c])
				c = c + 1
		chromosomes.append(chromosome)
		# Inserting new creature (generation 0) in Creature Table
		now = datetime.datetime.now()
		datenow = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
		new = Creature.objects.create(creation_date=datenow, current_generation=0)
		new.save()
		# Inserting the new 50 chromosome and the new 50 pending tasks in Tasks
		mycreature = Creature.objects.latest('id')
		for c in chromosomes:
			newChromosomes = Chromosome(data=str(c), creature_id_id=str(mycreature))
			newChromosomes.save()
			latestId=newChromosomes.id
			newTasks = Tasks(user_id_id=0, chromosome_id_id=str(latestId))
            		newTasks.save()					
		# TODO: update Creatures table with "current_generation"
