from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
from .models import User

import os
import numpy as np
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from string import punctuation

import re
import cv2


# basic functions

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)

        # Hash the password before saving
        hashed_password = make_password(password)

        user = User(username=username, password=hashed_password, contact_no=contact, email=email, address=address)
        user.save()
        
        context = {'data': 'Signup Process Completed'}
        return render(request, 'Register.html', context)

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                context = {'data': 'welcome ' + username}
                return render(request, 'UserScreen.html', context)
            else:
                context = {'data': 'login failed'}
                return render(request, 'Login.html', context)
        except User.DoesNotExist:
            context = {'data': 'login failed'}
            return render(request, 'Login.html', context)


# text plagiarism detection

text_files = []
text_data = []

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
porter = PorterStemmer()

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

def UploadSource(request):
    if request.method == 'GET':
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
        output = '<table border=1 align=center><tr><th>Source File Name</th><th>Words in File</th></tr>'
        for i in range(len(text_files)):
            length = len(text_data[i].split(" "))
            output+='<tr><td><font size="" color="white">'+text_files[i]+'</td><td><font size="" color="white">'+str(length)+"</td></tr>"
        context= {'data':output}
        return render(request, 'UploadSource.html', context)

def UploadSuspiciousFile(request):
    if request.method == 'GET':
        return render(request, 'UploadSuspiciousFile.html', {})

def UploadSuspiciousFileAction(request):
    if request.method == 'POST' and request.FILES['t1']:
        output = ''
        myfile = request.FILES['t1']
        fs = FileSystemStorage()
        name = str(myfile)
        filename = fs.save("test.txt", myfile)
        data = ''
        with open("test.txt", "r", encoding='iso-8859-1') as file:
            for line in file:
                line = line.strip('\n')
                line = line.strip()
                data+=line+" "
        file.close()
        os.remove("test.txt")
        data = cleanPost(data.strip().lower())
        sim = 0
        ff = 'No Match Found'
        for i in range(len(text_data)):
            similarity = LCS(text_data[i],data)
            if similarity > sim:
                sim = similarity
                ff = text_files[i]
               
        output = '<table border=1 align=center><tr><th>Source Original File Name</th><th>Suspicious File Name</th><th>LCS Score</th><th>Plagiarism Result</th></tr>'
        result = 'No Plagiarism Detected'
        similarity_percent = 0
        if sim >= 0:
            similarity_percent = sim/len(word_tokenize(data))
            if similarity_percent >= 0.60:
                result = 'Plagiarism Detected'
        output+='<tr><td><font size="" color="white">'+ff+'</td><td><font size="" color="white">'+name+'</td>'
        output+='<td><font size="" color="white">'+str(similarity_percent)+'</td><td><font size="" color="white">'+result+'</td></tr>'
        context= {'data':output}
        return render(request, 'SuspiciousFileResult.html', context)


# image plagiarism detection

image_files = []
image_data = []

def FMM(name):#five modules algorithm
    img = cv2.imread(name)
    img = cv2.resize(img,(50,50))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows,cols = img.shape
    for i in range(rows):
        for j in range(cols):
            if img[i,j] < 120:
                img[i,j] = 210
    for i in range(rows):
        for j in range(cols):
            k = img[i,j]
            if (k % 5) == 4:
                img[i,j] = k + 1
            elif (k % 5) == 3:
                img[i,j] = k + 2
            elif (k % 5) == 2:
                img[i,j] = k - 2
            elif (k % 5) == 1:
                img[i,j] = k - 1
    for i in range(rows):
        for j in range(cols):
            k = img[i,j]
            k = k / 5
            img[i,j] = k
    temp = img.ravel()
    temp = np.min(img)
    for i in range(rows):
        for j in range(cols):
            if img[i,j] > 0:
                img[i,j] = img[i,j] - temp
        
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    return hist    

def UploadSourceImage(request):
    if request.method == 'GET':
        if len(image_files) == 0:
            for root, dirs, directory in os.walk('source-images'):
                for j in range(len(directory)):
                    hist = FMM(root+"/"+directory[j])
                    image_data.append(hist)
                    image_files.append(directory[j])
        output = '<table border=1 align=center><tr><th>Source Image File Name</th><th>Histogram Values</th></tr>'
        for i in range(len(image_files)):
            output+='<tr><td><font size="" color="white">'+image_files[i]+'</td><td><font size="" color="white">'+str(image_data[i])+"</td></tr>"
        context= {'data':output}
        return render(request, 'UploadSourceImage.html', context)

def UploadSuspiciousImage(request):
    if request.method == 'GET':
        return render(request, 'UploadSuspiciousImage.html', {})

def UploadSuspiciousImageAction(request):
    if request.method == 'POST' and request.FILES['t1']:
        output = ''
        myfile = request.FILES['t1']
        fs = FileSystemStorage()
        name = str(myfile)
        filename = fs.save(name, myfile)
        hist = FMM(name)
        os.remove(name)
        similarity = 0
        file = 'No Match Found'
        hist1 = 0
        for i in range(len(image_files)):
            metric_val = cv2.compareHist(hist, image_data[i], cv2.HISTCMP_INTERSECT)
            if metric_val > similarity:
                similarity = metric_val
                file = image_files[i]
                hist1 = image_data[i]
        output = '<table border=1 align=center><tr><th>Source Original Image Name</th><th>Suspicious Image Name</th><th>Histogram Matching Score</th><th>Plagiarism Result</th></tr>'
        result = 'No Plagiarism Detected'
        print(str(name)+" "+str(similarity))
        if similarity >= 2000:
            result = 'Plagiarism Detected'
        output+='<tr><td><font size="" color="white">'+file+'</td><td><font size="" color="white">'+name+'</td>'
        output+='<td><font size="" color="white">'+str(similarity)+'</td><td><font size="" color="white">'+result+'</td></tr>'
        context= {'data':output}
        fig, ax = plt.subplots(2,1)
        ax[0].plot(hist1, color = 'b')
        ax[1].plot(hist, color = 'g')
        plt.xlim([0, 256])
        ax[0].set_title('Original image')
        ax[1].set_title('Plagiarised image')
        plt.show()
        return render(request, 'SuspiciousImageResult.html', context)        
