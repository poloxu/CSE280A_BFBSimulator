# Documentation on BFB Simulations

## Parameters

<p>usage: BFBSimulator.py num_cycles chr_str start_pos end_pos genome<br>
                       [-h] [-l L] [-ld {expo,simple}] [-df DF] [-dl DL]<br>
                       [-dd {expo,simple}] [-xf XF] [-xl XL]<br>
                       [-xd {expo,simple}] [-o O] [-rev] [-p P] <br>[-b B]<br>
                       [-bl BL]</p>

<p>positional arguments:
  num_cycles         Number of BFB cycles to simulate
  chr_str            Name of the chromosome to simulate BFB on
  start_pos          Start position of the genome section to simulate BFB on
                     (0-indexed, inclusive)
  end_pos            End position of the genome section to simulate BFB on
                     (0-indexed, exclusive)
  genome             FASTA file of the genome</p>

optional arguments:
  -h, --help         show this help message and exit
  -l L               Mean length of the BFB segments (default 600000)
  -ld {expo,simple}  Distribution of the BFB segment lengths. "expo"(default):
                     exponential; "simple": all use the same value as the mean
                     length
  -df DF             Probability for each BFB segment to have one deletion
                     (default 0.1)
  -dl DL             Mean deletion length of the BFB segments (default 50000)
  -dd {expo,simple}  Distribution of the BFB segment deletion lengths.
                     "expo"(default): exponential; "simple": all use the same
                     value as the mean deletion length
  -xf XF             Probability for each BFB segment to have one duplication
                     (default 0.1)
  -xl XL             Mean duplication length of the BFB segments (default
                     10000)
  -xd {expo,simple}  Distribution of the BFB segment duplication lengths.
                     "expo"(default): exponential; "simple": all use the same
                     value as the mean duplication length
  -o O               Prefix of the output files
  -rev               If this option is specified, BFB simulation will append
                     string to the 5' side of the region
  -p P               For each segment, the probability that deletion is
                     simulated before duplication (default 0.5)
  -b B               Probability that there is a deletion when appending
                     duplicated segment. (default 0.1)
  -bl BL             Length of deletion when appending duplicated segment.
                     (default 50000)
