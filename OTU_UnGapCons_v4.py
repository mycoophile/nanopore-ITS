import os
import sys
from Bio import AlignIO
from Bio.Align import AlignInfo


#The input directory should contain only the alignment files and no other folders or files.
indir = input("Type or paste the directory path here: \n")
sub_name = indir.split("/") 
#print(sub_name)
group_sub_name = ''.join(sub_name[-1]).partition("_")
#print(group_sub_name)
collected_consensus_name = indir + "/" + ''.join(group_sub_name[0]) + "_Otu_consensi"
print(collected_consensus_name)

#The above processes the files in random order.  The below code sorts the file list first and so the 
#collected fasta file comes out in alphanumeric order like you would expect.
#Create the consesnsus for each otu:

for	root, dirs, files in os.walk(indir):
	files.sort()
	for file in files:
		print(file)

		if not file.startswith('.'):
			#print(file)
			alignment = AlignIO.read(os.path.join(indir, file), "fasta")
			num_seqs = len(alignment)
			summary_align = AlignInfo.SummaryInfo(alignment)
			consensus = summary_align.gap_consensus(0.50, "-")
			#print(consensus)

			filename = file
			cons_filename = filename + "_cons"
			gapcons_data = str(consensus)
			with open(os.path.join(indir, cons_filename), "a") as gapcon:
				
				gapcon.write(">" + filename + "_gapped consensus" + "_#" + str(num_seqs) + "#_seqs" + "\n" + gapcons_data)
			with open(collected_consensus_name, "a") as f:
				f.write(">" + filename + "_gapped consensus" + "_#" + str(num_seqs) + "#_seqs" + "\n" + gapcons_data + "\n")
				
                        
                          
#This is where the gap characters get removed

			with open (os.path.join(indir, cons_filename), "r") as file:
				filedata = file.read()
				filedata_nogaps = filedata.replace("-", "") 
				filedata_ungap = filedata_nogaps.replace("_gapped ", "_")
			with open(os.path.join(indir, cons_filename), "w") as file:
				file.write(filedata_ungap)

#And this is where the collected fasta file gets de-gapped

with open (collected_consensus_name, "r") as file:
	filedata = file.read()
	filedata_nogaps = filedata.replace("-", "") 
	filedata_ungap = filedata_nogaps.replace("_gapped ", "_")
with open(collected_consensus_name, "w") as file:
	file.write(filedata_ungap)
	
                       
