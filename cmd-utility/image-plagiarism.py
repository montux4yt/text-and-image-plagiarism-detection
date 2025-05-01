import os
import sys

import re
import cv2
import numpy as np
import matplotlib.pyplot as plt

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

def LoadSourceImage():
    if len(image_files) == 0:
        for root, dirs, directory in os.walk('source-images'):
            for j in range(len(directory)):
                hist = FMM(root+"/"+directory[j])
                image_data.append(hist)
                image_files.append(directory[j])
    output = 'Source Image File Name --- Histogram Values\n'
    for i in range(len(image_files)):
        output+=image_files[i] +' --- '+ str(image_data[i]) +'\n'
    print(output)
    print('\n------------------------------------------------------\n')

def TestImagePlagiarism():
    output = ''
    myfile = sys.argv[1]
    name = str(myfile)
    hist = FMM(name)
    similarity = 0
    file = 'No Match Found'
    hist1 = 0
    for i in range(len(image_files)):
        metric_val = cv2.compareHist(hist, image_data[i], cv2.HISTCMP_INTERSECT)
        if metric_val > similarity:
            similarity = metric_val
            file = image_files[i]
            hist1 = image_data[i]
    result = 'No Plagiarism Detected'
    if similarity >= 2000:
        result = 'Plagiarism Detected'
    fig, ax = plt.subplots(2,1)
    ax[0].plot(hist1, color = 'b')
    ax[1].plot(hist, color = 'g')
    plt.xlim([0, 256])
    ax[0].set_title('Original image')
    ax[1].set_title('Plagiarised image')
    plt.show()
    print('Source Image: \t\t\t'+file+'\nSuspicious Image: \t\t'+name+'\nHistogram Matching Score: \t'+str(similarity)+'\nPlagiarism Result: \t\t'+result)
    print('\n------------------------------------------------------\n')


# driver code

LoadSourceImage()
TestImagePlagiarism()

