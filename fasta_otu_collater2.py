import os
import sys
from Bio import SeqIO

indir = input("Type or paste the directory path here: \n")
print(indir)

for file in os.listdir(indir):
	if not file.startswith('.'):

		filename = str(indir) + "/" + str(file)
		print(filename)

records = list(SeqIO.parse(filename, "fasta"))
last_record = records[-1]
s = last_record.id
print(s)
num_otus = int(s[14:])
hdr = indir.split("_")[-2]
BC = hdr.split("/")[-1]
#print(num_otus, "Otu's")
#print(hdr)
print(BC + " has " + str(num_otus) + " OTU's")

for record in SeqIO.parse(filename, "fasta"):
	otu_number = record.id[14:]
	#print(otu_number)
	for X in range(1, num_otus+1):
		OTU = "Otu" + otu_number
		#print(OTU)
		with open(indir + "/" + BC + "_" + OTU + ".fasta", "a") as f:
			
			if OTU in record.id:
				f.write(">" + str(record.id) + "\n" + str(record.seq) + "\n")
			
			break

		
 