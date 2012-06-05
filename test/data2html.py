## data to html with class defined

#data = ["0101", "010102", "01010105", "01010208", "01010311", "010203", "01020106", "01020209", "01020312", "010304", "01030107", "01030210", "01030313", "0214", "020115", "02010118", "02010221", "02010324", "020216", "02020119", "02020222", "02020325", "020317", "02030120", "02030223", "02030326", "0327", "030128", "03010131", "03010234", "03010337", "030229", "03020132", "03020235", "03020338", "030330", "03030133", "03030236", "03030339"];


data = ["0101", "010102", "01010105", "01010208", "01010311", "010203", "01020106", "01020209", "01020312", "010304", "01030107", "01030210", "01030313", "0214", "020115", "02010118", "02010221", "02010324", "020216", "02020119", "02020222", "02020325", "020317", "02030120", "0327", "030128", "03010131", "030229", "030330"];

mytree = dict()
for allele in data:
	suf = allele[(len(allele)-2):len(allele)]
	pre = allele[:(len(allele)-2)]
	#print allele+" = "+pre+" + "+suf
	mytree[suf] = pre

# frist nav bar
first = []
nav1 = "<div id='nav1'><ul>"
for  k in mytree.keys():
	if len(mytree[k]) == 2:
		nav1 = nav1+"\n\t<li id='"+k+"' class='first'>"+mytree[k]+"</li>	"
		first.append(mytree[k])
nav1 = nav1+"\n</ul></div>"

#print "First:"
print nav1
#print first

# second nav bar
second = []
nav2 = "<div id ='nav2'><ul>"
for f in first:
	for  k in mytree.keys():
		if f == mytree[k][0:len(f)] and len(mytree[k]) == 4:
			#print "nivell "+f+" elements: "+mytree[k]
			nav2 = nav2+"\n\t<li id='"+k+"' class='"+f+"'>"+mytree[k]+"</li>"			
			second.append(mytree[k])
	#print "---"	
nav2 = nav2+"\n</ul></div>\n"			

#print "Second's bars:"
print nav2
#print second

# third nav bar
third = []
nav3 = "<div id ='nav3'><ul>"
for f in second:
	for  k in mytree.keys():
		if f == mytree[k][0:len(f)] and len(mytree[k]) == 6:
			#print "nivell "+f+" elements: "+mytree[k]
			nav3 = nav3+"\n\t<li id='"+k+"' class='"+f+"'>"+mytree[k]+"</li>"			
	#print "---"	
nav3 = nav3+"\n</ul></div>\n"			

#print "Thitd's bars:"
print nav3
#print third






'''	
Here other tests:

print "mytree: "
print mytree
c = 1
for allele in data:
	sub = allele[0:2]
	if len(allele) == 4:
		print str(c)+") "+allele
		c = c + 1
		tree.append(allele)
'''

'''
tree = []
c = 1
for allele in data:
	sub = allele[0:2]
	if len(allele) == 4:
		print str(c)+") "+allele
		c = c + 1
		tree.append(allele)

tree2 = []
for allele in data:
	if len(allele) == 6:		
		print str(c)+") "+sub+" | "+allele
		c = c + 1

	if len(allele) == 8:	
		subb = allele[0:4]
		print str(c)+") a "+sub+" | "+subb+" | "+allele
		c = c + 1
		##print tree[sub]  ##.append(allele)

print "tree2: "
print tree
'''
