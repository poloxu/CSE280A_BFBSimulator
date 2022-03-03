#!/usr/bin/env python
# coding: utf-8

# In[61]:


def IsBFB(num_list):
    pos_list = []
    for idx in range(len(num_list) - 1):
        if (num_list[idx] + num_list[idx + 1] == 0):
            pos_list.append(idx)
    return IsBFBHelper(num_list, pos_list)

# The main recursion function
def IsBFBHelper(num_list, pos_list):
    # Base case: no possible reverse center
    if (len(pos_list) == 0):
        for i in range(len(num_list)):
            if (num_list[i] != i + 1):
                return False
        return True
    # Check the rightmost candidate reverse center
    curr_pos = pos_list[len(pos_list) - 1]
    curr_flag = IsBValidRevCtr(num_list, curr_pos)
    if (curr_flag):
        # A valid cutting point; cut the list and continue
        num_list = num_list[0 : curr_pos + 1]
    pos_list.pop()
    return IsBFBHelper(num_list, pos_list)

# Check if a candidate reverse center is a valid cutting point
def IsBValidRevCtr(num_list, pos):
    if (2 + pos * 2 <= len(num_list)):
        return False
    after_str = num_list[pos + 1:]
    before_str = num_list[2 * pos + 2 - len(num_list) : pos + 1]
    return IsReverse(after_str, before_str)

# Check if two numer lists are the BFB reverse of each other
def IsReverse(num_list1, num_list2):
    if (len(num_list1) != len(num_list2)):
        print("Error: length incompatible!")
        return False
    
    list_len = len(num_list1)
    for idx in range(len(num_list1)):
        if (num_list1[idx] + num_list2[list_len - 1 - idx] != 0):
            return False
    return True


# In[ ]:




