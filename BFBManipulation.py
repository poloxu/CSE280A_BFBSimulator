
import random


## Select a break point, duplicate, reverse and append
def BFBOneCycle(input_str):
    breakpoint = random.randint(1, len(input_str)-1)
    duplicate = input_str[breakpoint:len(input_str)]
    append = []
    for char in range(len(duplicate)-1, -1, -1):
        append.append(-1*duplicate[char])
    modified_str = input_str + append
    return modified_str


## using indexing in an array
def CountBFBSegments(input_str):
    segments = set()
    item = 0
    while abs(input_str[item]) not in segments:
        segments.add(input_str[item])
        item += 1      
    counts = [0]*(len(segments)+1)
    for char in input_str:
        counts[abs(char)] += 1
    return counts






