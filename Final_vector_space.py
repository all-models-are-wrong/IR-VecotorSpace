from collections import Counter
import numpy as np
import math 

def sim(ar1,ar2): # method to find inner product of query and document
    array_1 = np.array(ar1)
    array_2 = np.array(ar2)
    prod = sum(array_1 * array_2)
    return prod

letters = ['A','B','C','D','E','F'] 

count_of_letter = []
content = []
len_of_doc = []
doc_cont_let = [10,10,10,10,10,10] # assume all letters are found in all docs, this number is idf for each letter
idf = []
tf = {} # term frequency per char per doc
weight_char = {}
for i in range(10): # loop for reading content of txt docs
    file = open(f'Doc{str(i+1)}.txt')
    word = file.read()
    content.append(word.split()) # creates a list with the content of files
    file.close()   
    count_of_letter.append(Counter(content[i])) # list of dictionary with letter count
    len_of_doc.append(len(content[i]))

    weight_of_char = [] # list of weights of letters, gets updated every iteration with every document
    for j in letters:
        most = count_of_letter[i] # loops over letters in docu
        x = most[j] / len_of_doc[i] # gets weight for each letter and stores in weight_of_char
        weight_of_char.append(x)
    weight_char[f'doc{i+1}'] = weight_of_char

# Vector Space Model
    # this block calculates tf for each letter per doc
    most_freq = count_of_letter[i].most_common(1) # access the most common letter,num per doc as a list containing tuple
    li = most_freq[0] # access the list which only has one element, a tuple
    tf_per = []
    for j in letters:
        most = count_of_letter[i]
        x= most[j]/li[1] # li[1] is the number of the most common letter
        tf_per.append(x) # term freq calculated
    tf[f'doc{i+1}'] = tf_per
    for k in range(len(letters)): # loop to find dfi by subtracting 1 if tf of letter is 0
        if tf_per[k] == 0:
            doc_cont_let[k] = doc_cont_let[k] - 1
    
    

# loop to calculate idf 
for i in range(len(letters)): 
    x = math.log((10/doc_cont_let[i]),2)
    idf.append(x)


matrix  = []
for i in range(10): # loop for making matrix of weights, the num of letters is the num of columns
    a = []
    for j in range(len(letters)):
        x = tf[f'doc{i+1}'][j]
        a.append(round(idf[j] * x,2)) # round float to 2 dec places
    matrix.append(a)

for i in range(10):
    for j in range(len(letters)):
        print(matrix[i][j], end = " ") 
    print()

# Query
print('Enter Letters sperated by enter, when finished type done')
quer = []
count_of_q = []
while True:
    q = input()
    if q == 'done':
        break
    quer.append(q.upper())

count_of_q.append(Counter(quer)) # list of dictionary with letter count
len_of_q = len(quer)
most_f_qu = count_of_q[0].most_common(1) 
li = most_f_qu[0]
highest_occ= li[1] # most common letter per doc

tf_q = [] # calculating the tf of the queue
for i in letters:
    most = count_of_q[0]
    x = most[i]/highest_occ
    tf_q.append(x)
    print('val_x',x)
weight_q = [] # weight of query
for i in range(len(letters)):
    x = idf[i] * tf_q[i]
    weight_q.append(x)

# cosine similarity
cos_sim = {}
for i in range(10):
    we = weight_char[f'doc{i+1}'] # cos_sim = sim(we,weightq)/sqrt(doc_wght_sq * q_wght_sq)
    z = sim(we,weight_q)
    doc_wght_sq = np.array(we) * np.array(we)
    q_wght_sq = np.array(weight_q) * np.array(weight_q)
    denom = sum(doc_wght_sq) * sum(q_wght_sq)
    res = z/math.sqrt(denom)
    cos_sim[f'doc{i+1}'] = res
ordered_vec = sorted(cos_sim.items(), key = lambda t:t[1], reverse = True) # sorts values by best match score
# for k in ordered_dict:
#     print(k)
for k in range(len(ordered_vec)):
    print(ordered_vec[k][0],end=' ')
    x = ordered_vec[k][1]
    print(round(x,4))
