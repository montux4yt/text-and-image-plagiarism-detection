import os
import sys

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from string import punctuation
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
porter = PorterStemmer()


# text plagiarism detection

text_files = []
text_data = []

def LCS(l1,l2): #LCS method
    s1 = word_tokenize(l1)
    s2 = word_tokenize(l2)
    dp = [[None]*(len(s1)+1) for i in range(len(s2)+1)]
    for i in range(len(s2)+1): 
        for j in range(len(s1)+1): 
            if i == 0 or j == 0: 
                dp[i][j] = 0
            elif s2[i-1] == s1[j-1]: 
                dp[i][j] = dp[i-1][j-1]+1
            else: 
                dp[i][j] = max(dp[i-1][j] , dp[i][j-1]) 
    return dp[len(s2)][len(s1)]

def cleanPost(doc):
    tokens = doc.split()
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [word for word in tokens if len(word) > 1]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [porter.stem(token) for token in tokens]
    tokens = ' '.join(tokens)
    return tokens

def LoadSource():
    if len(text_files) == 0:
        for root, dirs, directory in os.walk('source-texts'):
            for j in range(len(directory)):
                data = ''
                with open(root+"/"+directory[j], "r", encoding='iso-8859-1') as file:
                    for line in file:
                        line = line.strip('\n')
                        line = line.strip()
                        data+=line+" "
                file.close()
                data = cleanPost(data.strip().lower())
                text_files.append(directory[j])
                text_data.append(data)
    output = 'Source File Name --- Words in File\n'
    for i in range(len(text_files)):
        length = len(text_data[i].split(" "))
        output+=text_files[i]+' --- '+str(length)+'\n'
    print(output)
    print('\n--------------------------------------------------------------\n')

def TestPlagiarism():
    output = ''
    myfile = sys.argv[1]
    name = str(myfile)
    data = ''
    with open(myfile, "r", encoding='iso-8859-1') as file:
        for line in file:
            line = line.strip('\n')
            line = line.strip()
            data+=line+" "
    file.close()
    data = cleanPost(data.strip().lower())
    sim = 0
    ff = 'No Match Found'
    for i in range(len(text_data)):
        similarity = LCS(text_data[i],data)
        if similarity > sim:
            sim = similarity
            ff = text_files[i]
           
    result = 'No Plagiarism Detected'
    similarity_percent = 0
    if sim >= 0:
        similarity_percent = sim/len(word_tokenize(data))
        if similarity_percent >= 0.60:
            result = 'Plagiarism Detected'
    print('Source File Name: \t'+ff+'\nSuspicious File Name: \t'+name+'\nLCS Score: \t\t'+str(similarity_percent)+'\nPlagiarism Result: \t'+result)
    print('\n--------------------------------------------------------------\n')


# driver code

LoadSource()
TestPlagiarism()

