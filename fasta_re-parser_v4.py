#This program opens a large multi-sequence fasta file and reduces it's size to a desired number of 
#sequences and sets the length of the individual sequence name headers in the output file at 10 
#characters to be more compatibale with #downstream code.

infile = input("Type or paste the input file name here.  Include the path if it is in an other directory \n")
#hdr_lgth = input("Provide the number of characters after the > you want to retain \n") 
parsed_file = input("Name for modified file?  Include a path if desired \n")
number_of_seqs = input("How many fasta sequences to include in re-parsed fasta output file? \n")

incld_seqs = int(number_of_seqs)
hdr_lgth = 10
header = int(hdr_lgth) + 1
num_fastas = 0

with open(parsed_file, "w") as output:
        with open(infile, "r") as input:
            
            while num_fastas < incld_seqs:
               
                for line in input:
                    if line.startswith(">"):
                        sht_line = line[0:header] + "\n"
                        output.write(sht_line)
                    else:
                        output.write(line)
                        num_fastas += 1
                        break
                        
                        

print(str(incld_seqs) + "sequences with " + str(hdr_lgth) + " character headers written to output file")
