
import matplotlib.pyplot as plt
import numpy as np

## plot count vector as a histogram
## given: count vector and n number of cycles
def plotCountsHist(count_array, n):
    labels = [i for i in range(1, len(count_array[0]))]
    X = np.arange(len(labels))
    
    length = len(count_array[0])
    y1_index = 0
    y2_index = (len(count_array)//2)-1
    y3_index = (4*len(count_array)//5)-1
    y4_index = len(count_array)-1
    
    w = 0.5/3
    ax = plt.subplot(111)
    ax.bar(X-2*w, count_array[y1_index][1:length], width = w, label = "1 cycle")
    ax.bar(X-w,count_array[y2_index][1:length], width = w, label = str(y2_index+1) + " cycles", color = "red")
    ax.bar(X+w, count_array[y3_index][1:length], width = w, label = str(y3_index+1) + " cycles", color = "purple")
    ax.bar(X+2*w, count_array[y4_index][1:length], width = w, label = str(y4_index+1) + " cycles", color = "green")
    
    ax.set_ylabel('Frequencies')
    ax.set_title('Segment Counts after ' + str(n) + ' BFB cycles')
    ax.set_xticks(X)
    ax.set_xticklabels(labels)
    ax.set_xticks(X, labels)
    ax.set_xlabel("Segments")
    ax.legend()
    
    plt.show()
    
## plot count vector as a line    
def plotCountsLine(count_array, n):
    labels = [i for i in range(1, len(count_array[0]))]
    X = labels
    
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
        ax.plot(X, Y, label = str(item+1) + " cycles")
    
    ax.set_ylabel('Frequencies')
    ax.set_title('Segment Counts after ' + str(n) + ' BFB cycles')
    ax.set_xticks(X)
    ax.set_xticklabels(labels)
    ax.set_xticks(X, labels)
    ax.set_xlabel("Segments")
    ax.legend()
    
    plt.show()
