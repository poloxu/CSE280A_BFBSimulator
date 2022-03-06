
import random


## Select a break point, duplicate, reverse and append
def BFBOneCycle(input_str, right):
    breakpoint = random.randint(1, len(input_str)-1)
    #print(breakpoint)
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


def plotCountsLine(count_array, n):
    labels = [i for i in range(1, len(count_array[0]))]
    X = labels
    
    print(X)
    
    length = len(count_array[0])
    y1_index = 0
    y2_index = (len(count_array)//2)-1
    y3_index = (4*len(count_array)//5)-1
    y4_index = len(count_array)-1
    indices = [y1_index, y2_index, y3_index, y4_index]
    
    
    w = 0.5/3
    ax = plt.subplot(111)
    for item in indices:
        Y = count_array[item]
        Y = Y[1:len(Y)]
        print(Y)
        ax.plot(X, Y, label = str(item+1) + " cycles")
    
    ax.set_ylabel('Frequencies')
    ax.set_title('Segment Counts after ' + str(n) + ' BFB cycles')
    ax.set_xticks(X)
    ax.set_xticklabels(labels)
    ax.set_xticks(X, labels)
    ax.set_xlabel("Segments")
    ax.legend()
    
    plt.show()


## BFB cycle with set breakpoint input
def BFBSetBreak(input_str, breakpoint, right):
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


def SimDist(breakpoint, n_segments, n_cycles):
    count_array = []
    start_string = []
    for seg in range(1, n_segments+1):
        start_string.append(seg)
    #print(start_string)
    i = 0
    while i < 2:
        new_string = BFBSetBreak(start_string, breakpoint, True)
        counts = CountBFBSegments(new_string)
        count_array.append(counts)
        start_string = new_string
        i += 1
    i = 0
    while i < n_cycles-2:
        new_string = BFBOneCycle(start_string, True)
        #print("new_string: " + str(new_string))
        counts = CountBFBSegments(new_string)
        count_array.append(counts)
        start_string = new_string
        i += 1
    plotCountsLine(count_array, n_cycles)
    #return count_array

SimDist(2, 10, 30)


SimDist(8, 10, 30)






