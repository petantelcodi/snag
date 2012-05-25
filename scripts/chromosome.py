## chromosome.py
# This file manage chromosome data

# Load chromosome data

# a 2x2 example: 2x2 + 2 = 6 alleles. With IDs 61,62,63, 64, 65, 66
mychromosome = ["0161","010162", "010263", "0264", "020165", "020266" ]

# number of allels:
allels_number = len(mychromosome)
print "Number of allels: "+str(allels_number)

# Get dimensions

# How many in the first levels?
level = []
c = 0
tmp = []
for allel in mychromosome:
	print "--"
	print allel
	if len(str(allel)) == 4:
		c = c + 1 
		level = c
		tmp.append(allel)

### Aqui m'he quedat	.....

print "First level: "+str(level)
print str(tmp)


