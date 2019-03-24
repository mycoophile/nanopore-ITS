# nanopore-ITS
A series of python scripts for processing fungal ITS nanopore DNA sequence data.


This data analysis process assumes you have run a 1D barcoded library of ITS amplicons on a MinION nanopore sequencer and Albacore (The base-calling and demultiplexing program provided by Oxford Nanopore Technologies) has sorted the sequences into barcode bins and you have combined all the sequences for each barcode into a directory labelled for the barcode.  We further assume that you will be keeping data organized in separate directories for each barcode as you work through the data analysis process. The data will be processed in a Linux-like environment using mothur, phylip, bash, and the python scripts housed here.  The mothur program starts with a multiple sequence alignment for each barcode data set.  The full-length ITS amplicons are ~1000-1500bp long and aligning a large number of such sequences has a RAM requirement that grows with the square of the number of sequences, O(n2).  You probably will not be able to use all the data the MinION may have generated.  

A Note About Directory and File Naming - The Python scripts used here rely on the names of directories for naming the files produced or modified within.  They will not work if there are spaces in the names of the directories, or in the names of any directories in the paths you may specify, so be sure before you start that you have a naming scheme that is compatible.  Same applies to the filenames themselves.

A Note About Computational Demands - We have found that using the GINS1 version of mafft you can align ~3000 sequences with 32GB RAM, ~4000 Sequences with 48GB RAM, and 6000 sequences needs over 200 GB RAM.  The more threads you can use the faster it will be.  The other steps in the analysis process are quick and do not need a lot of RAM, except for step 2, producing the DNA distance matrix from the alignment using Phylip.  Phylip only runs on one thread and calculating the matrix for ~6000 sequences takes several days and will require almost 6GB of RAM.  You can run several Phylip processes in parallel on a multicore computer, determined by how many of the processes will use most of the available RAM.

Outline of Data Processing Steps

1.	Albacore will have either been run online while the MinION was collecting data or will have been run on a local computer, and will have sorted the sequences into barcode groups with fasta formatted output,  Each sequence read gives an individual fasta file.  Further, you will have filtered the raw sequence reads by quality score using a program such as NanoFilt which can be found on the Nanopore Community pages.  If your MinION run produced output with an average Q score of 10 we suggest using that as the filter value.  It may be possible to use higher Q-scores depending on the quality of your data.  

2.	Use the fasta_reparser_v4.py script to select the number of sequences for a given barcode group that will be aligned, shorten the fasta names to 10 characters, and write the chosen number of raw sequences into a multi-fasta file named for the barcode number.

3.	With all the multi-fasta files you are working with placed in a directory you can easily set mafft to aligning them sequentially with a bash one-liner like this:

for i in *.fasta; 
do mafft --globalpair --thread 10 --op 0.5 --gop -0.5 "$i" >  $(basename "$i").NS2algnmnt; done;

4.	Make distance matrices from the alignments using Phylip:

./dnadist

provide input filename

F to allow a new file to be made with a specified name.

Provide input filename again then change extension to .dist or similar.

The default settings include Jukes-Cantor

Y to accept settings

Repeat as needed to start the number of Phylip threads you can given available RAM.

5.	Form clusters in mothur using :

./mothur  then -
mothur > cluster(phylip=BC#_filename.dist, method=opti, cutoff=0.08 or 0.10)

6.	Convert the raw clustered fasta file from mothur opticlust to a fasta organized by OTU number:

mothur > bin.seqs(list=BC#_filename.list, fasta=BC#_filename.fasta)

This uses the BC#_filename.list file output from opticlust and the original BC#_filename.fasta that was aligned for the given barcode group by mafft in step 1.  This outputs a fasta file with a name that includes the clustering method and clustering cut-off, like this:
BC#_filename.opti_mcc.0.10.fasta
Each fasta header line is like this example:  >U68686	Otu01
That gap in the fasta header is a tab.
You must remove the tab and replace it with an underline like this, >U68686_Otu01, before undertaking the next step.  This can be conveniently done in TextEdit (Mac) or with a word processor.

7.	Separate the comprehensive fasta into individual otu fasta's using the python script fasta_otu_collater2.py.  This script uses the BioPython module and assumes you have it installed.  It also assumes you have the fasta file for each barcode in a separate directory for the barcode which contains only the one fasta file.  Other files may also be present as long as they do not have the .fasta extension.
Your directory will now copntain an individual fasta file for each otu, where otu 1 will be the largest file and the other otus will be smaller.  Some ways down the list the higher number otu fasta files may contain only one sequence.  We find that otu's with less than 5 sequences are not worth processing further as they do not yield a highly accurate consensus sequence.

8.	Align the sequences within each otu using mafft, see step 3.  This can step be done on a desktop computer, but be sure to first move the large multi-fasta file out of the directory or mafft will start a process with very large RAM requirements and will probably crash on the desktop PC.  In the end you will have a directory containing a fasta file for each otu and an alignment file for each otu.
For the next step the top level working directory should only contain the alignment files.  Before starting step 9 create a subdirectory for the individual otu fasta files and move them into it.

9.	Find the un-gapped consensus sequence for each otu using the OTU_UnGapCons_v4.py python script.  This will write all the consensus sequences to a new multi-fasta text file called BC#_Otu_consensi and also saves individual fasta files for each otu.  The number of sequences in the otus will now be added to the fasta headers in a way that is easily handled in Excel in the final output.
This script also uses BioPython.


The last two steps assume you are using BLAST, either locally or online at NCBI, to find identity matches for your otu consensus sequences.  You may choose to use a different database such as UNITE for some projects.  We have so far used BLAST at NCBI for greatest breadth of coverage.

10.    Run  a BLAST search with the BC#_filename_consensi file for each barcode set and download the output as an xml file.  Do not use the xml2 download options as BioPython does not work with that format.

11.  	 Run the downloaded xml file (which saves as a .txt file) through the script Top4_BLASTXMLhits_V3.py to create a tab-delimited text file that is easily imported into Excel to display the results.  The script will output a hit in 4 BLAST fields, the hit with highest bit score, the hit with highest E value, the hit with longest alignment, and the hit with highest %identity match.  The % identity for each of these hits is also listed.
The accuracy of results is mainly limited by the available database contents.  If you could ID a species of fungus with a full length Sanger ITS sequence in your database search you can probably get the same result with this procedure.
