
data = ["0101", "010102", "010203", "01010104", "01010205", "01020106", "01020207", "0208", "020109", "020210", "02010111", "02010212", "02020113", "02020214"]
# Get number of levels
levels = (len(max(data, key=len))-2)/2
alleles = len(max(data, key=len))
print "levels: "+str(levels)
print "alleles: "+str(alleles)

# Getting the min len elleles, this is first level alleles
allele_min = len(min(data, key=len))
for allele in data:
  if len(allele) == allele_min:
	print allele


#########3  A PARTIR D'AQUI SON TESTS NOMES
# array of len per levels
lenXlevel = []
for l in range(4, alleles+2, 2):
	print l
	lenXlevel.append(l)

print "lenXlevel"
print lenXlevel

c = 0
navbar = []
tmp = []
for l in lenXlevel:	
	for d in data:
		print l, d
	c = c +1
print tmp
