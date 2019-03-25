import os
import sys
import xml.etree.ElementTree as ET
import Bio
import Bio.Blast
from Bio.Blast import NCBIXML

#choose the saved BLAST XML file to process
infile = input("Type or paste the file with path here: \n")
infilename = infile.split("/")[-1]
infileshortname = infilename.split(".")[0]
#group_name = (infile.split("_")[0])
print(infileshortname)
prefix = infilename.split("_")[0]
print(prefix)
infileV2 = infileshortname + "V2.txt"
print(infileV2)
outfilename = prefix + "-top_BLAST_hits"
print(outfilename)


#group_name = (infile.split(".")[0])

#A new version V2 of the BLAST XML file will be written that the second half of the script will work with.

#Parsing the saved BLAST XML file so the vaklue for Hsp_postive is replaced by the calculated % Identity * 10000, which makes it an integer.
tree = ET.parse(infile)
root = tree.getroot()


for elem in root.iter(tag = "Hsp"):
	#print(elem[11].text)
	
	param1 = int(elem[10].text)
	#print(param1)
	param2 = int(elem[13].text)
	#print(param2)

	postiv = (param1 / param2) * 10000
	#print(postiv)

	bits = elem[1].text
	evalue = elem[3].text
	alignlen = elem[10].text
	identity = postiv / 100

	elem[11].text = str('{:.0f}'.format(postiv))
	#print(elem[11].text)

tree.write(infileV2)	#Now the values for Hsp.positive are replaced with % Identity.

#This writes the BLAST ouput header back to the beginning of rhe file so the BioPython NCBI_XML parser recognizes the file.
with open(infileV2, "r+") as f:
	line = ('<?xml version="1.0"?>'"\n"
'<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "http://www.ncbi.nlm.nih.gov/dtd/NCBI_BlastOutput.dtd">'"\n")
	content = f.read()
	f.seek(0,0)
	f.write(line + content)


#Now the BioPython NCBI_XML parser is put to work to find the max values in 4 Hit categories.
with open(infileV2, "r") as result_handle:
	
	with open(outfilename, "a") as f:
		f.write("Query " + "\t " + "Max bit score hit\t " + "Max E value hit\t " + "Max align length hit\t " + "Max identity hit\t " + "\n")
	
		for record in NCBIXML.parse(result_handle):
	
			if record.alignments:
						
				print(record.query)

				
				record.alignments.sort(key = lambda align: -max(hsp.bits for hsp in align.hsps))	
				Id_percent_bit = str((record.alignments[0].hsps[0].positives) / 100)
				Bit_score = (Id_percent_bit + "% " + str(record.alignments[0].hsps[0].bits) + " " + record.alignments[0].hit_id + " " + record.alignments[0].hit_def)
				#print(record.alignments[0].hsps[0].bits)
				print("Max bit score hit: " + "\n" + record.alignments[0].hit_id + record.alignments[0].hit_def)

				record.alignments.sort(key = lambda align: -max(hsp.expect for hsp in align.hsps))
				Id_percent_Eval = str((record.alignments[0].hsps[0].positives) / 100)
				E_score = (Id_percent_Eval + "% " + " " + str(record.alignments[0].hsps[0].expect) + " " + record.alignments[0].hit_id + " " + record.alignments[0].hit_def)
				print("Max expect value hit: " + "\n" + record.alignments[0].hit_id + record.alignments[0].hit_def)

				record.alignments.sort(key = lambda align: -max(hsp.align_length for hsp in align.hsps))
				Id_percent_algnlgth = str((record.alignments[0].hsps[0].positives) / 100)
				Align_score = (Id_percent_algnlgth + "% " + " " + str(record.alignments[0].hsps[0].align_length) + " " + record.alignments[0].hit_id + " " + record.alignments[0].hit_def)
				print("Max alignment length hit: " + "\n" + record.alignments[0].hit_id + record.alignments[0].hit_def)

				record.alignments.sort(key = lambda align: -max(hsp.positives for hsp in align.hsps))
				Identity_score = (str((record.alignments[0].hsps[0].positives) / 100) + " " + record.alignments[0].hit_id + record.alignments[0].hit_def)
				print("Max Identity hit: " + "\n" + record.alignments[0].hit_id + record.alignments[0].hit_def + "\n")
			
				f.write((record.query.split(".")[0]) +  "\t " + (record.query.split("_#")[1]) + "\t " + Bit_score + "\t " + E_score + "\t " + Align_score + "\t " + Identity_score + "\n")
	