#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Funciton file for the BFB simulator to handle coordinates of the segments
# Use 0-indexed coordinates, left-inclusive, right-exclusive
#   e.g. (0,5) means positions 0, 1, 2, 3, 4


# In[2]:


import random

# Generate segment lengths to be exactly the mean length given
def SimpleLengthGenerator(mean_len):
    return mean_len

# Generate segment lengths from an exponential distribution
def ExponLengthGenerator(mean_len):
    from numpy.random import exponential
    return exponential(scale = mean_len)
    
# Get the reverse complement of a DNA string
def ReverseComplement(dna_str):
    res = ""
    for nuc in dna_str:
        if (nuc == "A"):
            res = "T" + res
        if (nuc == "T"):
            res = "A" + res
        if (nuc == "G"):
            res = "C" + res
        if (nuc == "C"):
            res = "G" + res
        if (nuc == "N"):
            res = "N" + res
        if (nuc == "a"):
            res = "t" + res
        if (nuc == "t"):
            res = "a" + res
        if (nuc == "c"):
            res = "g" + res
        if (nuc == "g"):
            res = "c" + res
        if (nuc == "n"):
            res = "n" + res
    return res
    
# Use the generator function with the mean length to keep generating until reaching the desired total length
# Truncate the last segment to meet the desired total length
def GenerateSegCoords(chr_str, mean_length, start_coord, end_coord, len_generator_func):
    tot_len = end_coord - start_coord
    accum_len = 0
    seg_lens = []
    while(accum_len < tot_len):
        next_len = round(len_generator_func(mean_length)) # Prefer the generator to provide integer, otherwise simply round
        if (next_len <= 0): # Require each segment to be at least 1 bp long
            next_len = 1
        accum_len += next_len
        seg_lens.append(next_len)
    seg_lens[len(seg_lens) - 1] -= (accum_len - tot_len)
    
    seg_info = [[None, -1, -1]]
    curr_accum_coord = start_coord
    for idx in range(len(seg_lens)):
        seg_info.append([chr_str, curr_accum_coord, curr_accum_coord + seg_lens[idx]])
        curr_accum_coord += seg_lens[idx]
    return seg_info

# Extract sequence(s) from fasta file; use a list of start/end coords
# Coord_list format: [[chrnum1, start1, end1], [chrnum2, start2, end2], …]
def GetSequencesFromGenome(coord_list, fasta_file_path):
    fa_lines = [x.strip() for x in open(fasta_file_path).readlines()]
    needed_chr = [x[0] for x in coord_list]
    needed_chr_str = {}
    
    curr_str = ""
    curr_chrnum = None
    for line in fa_lines:
        if (len(line) == 0):
            continue
        if (line[0] == ">"):
            if (curr_chrnum != None and curr_chrnum in needed_chr):
                needed_chr_str[curr_chrnum] = curr_str
            curr_str = ""
            curr_chrnum = line[4:]
        else:
            curr_str += line
    if (curr_chrnum != None and curr_chrnum in needed_chr):
        needed_chr_str[curr_chrnum] = curr_str
    
    res = []
    for entry in coord_list:
        if (entry[0] not in needed_chr_str.keys() or
            entry[1] < 0 or entry[2] < 0 or entry[2] <= entry[1] or
            len(needed_chr_str[entry[0]]) < entry[2]):
            res.append(None)
        else:
            res.append((needed_chr_str[entry[0]])[entry[1] : entry[2]])
    return res
            
# Add deletion
def AddDeletion(dna_str, deletion_frac, deletion_mean, deletion_l_generator):
    del_rand = random.random()
    if (del_rand > deletion_frac):
        return dna_str, ""
    del_l = round(deletion_l_generator(deletion_mean))
    if (del_l >= len(dna_str)):
        return "", "-(0," + str(len(dna_str)) + ")"
    if (del_l < 1):
        del_l = 1
    del_start = random.randint(0, len(dna_str) - del_l)
    res = dna_str[0 : del_start] + dna_str[del_start + del_l : ]
    return res, "-(" + str(del_start) + "," + str(del_start + del_l) + ")"

# Add duplication
def AddDuplication(dna_str, dup_frac, dup_mean, dup_l_generator):
    dup_rand = random.random()
    if (dup_rand > dup_frac):
        return dna_str, ""
    dup_l = round(dup_l_generator(dup_mean))
    if (dup_l >= len(dna_str)):
        return dna_str + dna_str, "+(0," + str(len(dna_str)) + ")"
    if (dup_l < 1):
        dup_l = 1
    dup_start = random.randint(dup_l, len(dna_str))
    res = dna_str[0 : dup_start] + dna_str[dup_start - dup_l : dup_start] + dna_str[dup_start : ]
    return res, "+(" + str(dup_start - dup_l) + "," + str(dup_start) + ")"

# Add SV: deletion and duplication
def AddSVtoStr(dna_str, deletion_frac, deletion_mean, deletion_l_generator, dup_frac, dup_mean, dup_l_generator, p_del_prev_dup):
    order_rand = random.random()
    info_str = ""
    if (order_rand <= p_del_prev_dup):
        new_str, curr_info = AddDeletion(dna_str, deletion_frac, deletion_mean, deletion_l_generator)
        info_str += curr_info
        new_str, curr_info = AddDuplication(new_str, dup_frac, dup_mean, dup_l_generator)
        info_str += curr_info
    else:
        new_str, curr_info = AddDuplication(dna_str, dup_frac, dup_mean, dup_l_generator)
        info_str += curr_info
        new_str, curr_info = AddDeletion(new_str, deletion_frac, deletion_mean, deletion_l_generator)
        info_str += curr_info
    return new_str, info_str


# In[ ]:




