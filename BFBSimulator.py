#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
from SegCoords import SimpleLengthGenerator, ExponLengthGenerator, ReverseComplement, GenerateSegCoords, GetSequencesFromGenome, AddSVtoStr
#from BFBManipulation import 


# In[5]:


parser = argparse.ArgumentParser()
parser.add_argument("num_cycles", type = int, help = "Number of BFB cycles to simulate")
parser.add_argument("chr_str", help = "Name of the chromosome to simulate BFB on")
parser.add_argument("start_pos", type = int, help = "Start position of the genome section to simulate BFB on (0-indexed, inclusive)")
parser.add_argument("end_pos", type = int, help = "End position of the genome section to simulate BFB on (0-indexed, exclusive)")
parser.add_argument("genome", help = "FASTA file of the genome")
parser.add_argument("-l", type = int, default = 400000, help = "Mean length of the BFB segments (default 400000)")
parser.add_argument("-ld", default = "expo", choices = ["expo", "simple"],
                    help = "Distribution of the BFB segment lengths. \"expo\"(default): exponential; \"simple\": all use the same value as the mean length")
parser.add_argument("-df", type = float, default = 0.1, help = "Probability for each BFB segment to have one deletion (default 0.1)")
parser.add_argument("-dl", type = int, default = 50000, help = "Mean deletion length of the BFB segments (default 50000)")
parser.add_argument("-dd", default = "expo", choices = ["expo", "simple"],
                    help = "Distribution of the BFB segment deletion lengths. \"expo\"(default): exponential; \"simple\": all use the same value as the mean deletion length")
parser.add_argument("-xf", type = float, default = 0.1, help = "Probability for each BFB segment to have one duplication (default 0.1)")
parser.add_argument("-xl", type = int, default = 10000, help = "Mean duplication length of the BFB segments (default 10000)")
parser.add_argument("-xd", default = "expo", choices = ["expo", "simple"],
                    help = "Distribution of the BFB segment duplication lengths. \"expo\"(default): exponential; \"simple\": all use the same value as the mean duplication length")
parser.add_argument("-o", default = "BFBSimulateOut", help = "Prefix of the output files")
parser.add_argument("-rev", action = "store_false", default = True, help = "If this option is specified, BFB simulation will append string to the 5' side of the region")
parser.add_argument("-p", type = float, default = 0.5, help = "For each segment, the probability that deletion is simulated before duplication (default 0.5)")

args = parser.parse_args()
n_cycle = args.num_cycles
chr_str = args.chr_str
start_pos = args.start_pos
end_pos = args.end_pos
genome_path = args.genome
mean_l = args.l
seg_d = args.ld
del_f = args.df
del_l = args.dl
del_d = args.dd
dup_f = args.xf
dup_l = args.xl
dup_d = args.xd
output_pref = args.o
rev_flag = args.rev
p_del_prev_dup = args.p

print("Arguments passed in:")
print("Number of BFB cycles: " + str(n_cycle))
print("Genome: " + genome_path)
print("Region: " + chr_str + " " + str(start_pos) + " " + str(end_pos))
print("Mean BFB segment length: " + str(mean_l))
print("BFB segment length distribution: " + seg_d)
print("Probability for each segment to have a deletion: " + str(del_f))
print("Mean BFB segment deletion length: " + str(del_l))
print("BFB segment deletion length distribution: " + del_d)
print("Probability for each segment to have a duplication: " + str(dup_f))
print("Mean BFB segment duplication length: " + str(dup_l))
print("BFB segment duplication length distribution: " + dup_d)
print("Output files prefix: " + output_pref)
print("Adding to 3' end of the specified region: " + str(rev_flag))
print("Probability that deletion is simulated before duplication: " + str(p_del_prev_dup))
print()


# In[7]:


sim_BFB_str = [1, 2, 3, 4, 5, -5, -4]
sim_BFB_cnts = [-1, 1, 1, 1, 2, 2]


# In[ ]:


def DetermineGenerator(generator_str):
    if (generator_str == "expo"):
        return ExponLengthGenerator
    if (generator_str == "simple"):
        return SimpleLengthGenerator

generator = DetermineGenerator(seg_d)
del_generator = DetermineGenerator(del_d)
dup_generator = DetermineGenerator(dup_d)
seg_coords = GenerateSegCoords(chr_str, mean_l, start_pos, end_pos, generator)

# Output the BFB string
output_BFBstr = output_pref + ".BFBAbsStr.tsv"
out_s = open(output_BFBstr, "w")
for i in range(len(sim_BFB_str)):
    if (i > 0):
        out_s.write("\t")
    num = sim_BFB_str[i]
    out_s.write(str(num))
out_s.write("\n")
print("Saved abstracted BFB string to: " + output_BFBstr)
out_s.close()

# Output the count vector
output_counts = output_pref + ".SegCnts.tsv"
out_v = open(output_counts, "w")
for i in range(len(sim_BFB_cnts)):
    if (i == 0):
        continue
    if (i > 1):
        out_v.write("\t")
    num = sim_BFB_cnts[i]
    out_v.write(str(num))
out_v.write("\n")
print("Saved BFB count vector to: " + output_counts)
out_v.close()

# Generate and print the final sequence of the simulated BFB
final_str = ""
seg_strs = GetSequencesFromGenome(seg_coords, genome_path)
seg_strs_wrev = [[None, None]] # Structure: [[None, None], [seg1, reverse_comp_seg1], [seg2, reverse_comp_seg2], ...]
seg_strs_SVinfo = [None]
print_str_flag = True
for i in range(len(seg_strs)):
    if (i == 0):
        continue
    curr_str, curr_info = AddSVtoStr(seg_strs[i], del_f, del_l, del_generator, dup_f, dup_l, dup_generator, p_del_prev_dup)
    if (curr_str == None):
        print("Error: genome coordinates error. Please check if input region coordinates are valid.")
        print_str_flag = False
        break
    seg_strs_wrev.append([curr_str, ReverseComplement(curr_str)])
    seg_strs_SVinfo.append(curr_info)
if (print_str_flag):
    for seg in sim_BFB_str:
        if (seg > 0):
            final_str += (seg_strs_wrev[seg][0])
        if (seg < 0):
            final_str += (seg_strs_wrev[-seg][1])
    output_fa = output_pref + ".BFBFinalSeq.fa"
    out_f = open(output_fa, "w")
    out_f.write(">SimulatedBFB" + "\n")
    out_f.write(final_str)
    out_f.write("\n")
    print("Saved simulated BFB DNA sequence to: " + output_fa)
    out_f.close()
    
# Output coordinates as a bed file (use the fourth column to record SV info)
# SV info string "-(a,b)+(c,d)" or "+(c,d)-(a,b)"; depends on the order of deletion/duplication
# -: deletion, (a,b) is the region deleted on the CURRENT string (if after insertion, string coordinates after insertion)
# +: duplication, (c,d) is the region duplicated on the CURRENT string and another copy appended immediately after this copy
#    (if after deletion, string coordinates after deletion)
# coordinates a,b,c,d are for the segment string, NOT for the genome coordinates
# coordinates a,b,c,d are 0-indexed, left inclusive, right exclusive
output_coords = output_pref + ".SegCoords.bed"
out_c = open(output_coords, "w")
for i in range(len(seg_coords)):
    if (i == 0):
        continue
    entry = seg_coords[i]
    out_c.write(entry[0] + "\t" + str(entry[1]) + "\t" + str(entry[2]) + "\t" + seg_strs_SVinfo[i] + "\n")
print("Saved segment coordinates to: " + output_coords)
out_c.close()

