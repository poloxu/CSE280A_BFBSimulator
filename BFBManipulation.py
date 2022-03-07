
import random

## Select a break point, duplicate, reverse and append
def BFBOneCycle(input_str, right):
    breakpoint = random.randint(1, len(input_str)-1)
    print(breakpoint)
    if right:
        duplicate = input_str[breakpoint:len(input_str)]
    else:
        duplicate = input_str[0: breakpoint]
    append = []
    for char in range(len(duplicate)-1, -1, -1):
        append.append(-1*duplicate[char])
    if right:
        modified_str = input_str + append
    else:
        modified_str = append + input_str
    return modified_str


## using indexing in an array
def CountBFBSegments(input_str):
    segments = set()
    item = 0
    while item < len(input_str):
        segments.add(abs(input_str[item]))
        item += 1      
    counts = [0]*(len(segments)+1)
    for char in input_str:
        counts[abs(char)] += 1
    return counts

## Main function to simulate BFB cycles given a string of segments and number of cycles 
## returns total count vector after simulating all cycles
def PartOneWrapper(n_segments, n_cycles, right):
    count_array = []
    start_string = []
    for seg in range(1, n_segments+1):
        start_string.append(seg)
    i = 0
    while i < n_cycles:
        new_string = BFBOneCycle(start_string, right)
        counts = CountBFBSegments(new_string)
        count_array.append(counts)
        start_string = new_string
        i += 1
    return count_array, start_string






