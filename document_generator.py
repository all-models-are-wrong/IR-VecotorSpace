import random
letters = ['A','B','C','D','E','F'] 


for j in range(1,11):
    doc = []
    letters_per_doc = random.randint(20,30) # number of letters in doc 
    print(f'letters in doc{j}',letters_per_doc)
    doc = random.choices(letters, k = letters_per_doc) # Generated letters and pasted them in txt file
    file = open(f'Doc{j}.txt','w')
    for i in doc:
        file.write(f'{i} ')
    file.close()
