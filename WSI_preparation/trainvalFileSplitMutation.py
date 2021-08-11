import os, pickle, random, sys, shutil
from PIL import Image
import tensorflow as tf
import numpy as np
import time

def getFileName(fileName):
    lenFIleName = len(fileName)
    nameEnd = 0
    nameStart = 0
    isDot=False
    for i in reversed(range(lenFIleName)):
        if fileName[i] == '.':
            if isDot:
                continue
            else:
                nameEnd = i
                isDot=True
        if fileName[i] == '/':
            nameStart = i + 1
            break
    return fileName[nameStart:nameEnd]

dirName = '/media/jajman/NewVolume/TCGA_STAD_1/'


with open('traintest/10Fold_TCGA_STAD_TP53_WT_Train0.bin', 'rb') as f:
    curTrainFiles=pickle.load(f)
print(len(curTrainFiles))

with open('traintest/10Fold_TCGA_STAD_TP53_WT_Test0.bin', 'rb') as f:
    curTestFiles=pickle.load(f)
print(len(curTestFiles))


with open('traintest/TCGA_STAD_WT_all.bin', 'rb') as f:
    curAllNormFiles=pickle.load(f)
print(len(curAllNormFiles))

with open('traintest/TCGA_STAD_TP53_mut_all.bin', 'rb') as f:
    curAllMutFiles=pickle.load(f)
print(len(curAllMutFiles))

normalTrainLen=len(curTrainFiles)
normalTestLen=len(curTestFiles)
allNormLen=len(curAllNormFiles)
allMutLen=len(curAllMutFiles)

ratio=(allMutLen/allNormLen)*1.5


files = os.listdir(dirName)
files=sorted(files)
fileNum=len(files)
fileCount=0
trainNum=0
testNum=0
for i in files:
    fileCount += 1
    print(str(fileCount) + '/' + str(fileNum))
    files2 = os.listdir(dirName + i)
    for j in files2:
        if j.endswith('svs'):
            fileName =getFileName(j)
            if (fileName in curAllNormFiles) and (fileName in curTestFiles):
                print('test in target')
            if (fileName in curAllNormFiles) and (fileName not in curTestFiles):
                trainNum += 1
                print('train move')
                saveDirName = dirName + i + '/TUMOR/'
                files3 = os.listdir(saveDirName)
                random.shuffle(files3)
                totLen = int(len(files3) * ratio)
                for k in range(totLen):
                    copyName = saveDirName + files3[k]
                    shutil.copy(copyName, '/home/jajman/train/normal/')

            if fileName in curTestFiles:
                testNum += 1
                print('test move')
                saveDirName = dirName + i + '/TUMOR/'
                files3 = os.listdir(saveDirName)
                for k in files3:
                    copyName = saveDirName + k
                    shutil.copy(copyName, '/home/jajman/validation/normal/')


print(trainNum)
print(testNum)

print()
print()

with open('traintest/10Fold_TCGA_STAD_TP53_Train0.bin', 'rb') as f:
    curTrainFiles=pickle.load(f)
print(len(curTrainFiles))

with open('traintest/10Fold_TCGA_STAD_TP53_Test0.bin', 'rb') as f:
    curTestFiles=pickle.load(f)
print(len(curTestFiles))


files = os.listdir(dirName)
files=sorted(files)
fileNum=len(files)
fileCount=0
trainNum=0
testNum=0
for i in files:
    fileCount += 1
    print(str(fileCount) + '/' + str(fileNum))
    files2 = os.listdir(dirName + i)
    for j in files2:
        if j.endswith('svs'):
            fileName =getFileName(j)
            if fileName in curTrainFiles:
                trainNum += 1
                print('train move')
                saveDirName = dirName + i + '/TUMOR/'
                files3 = os.listdir(saveDirName)
                for k in files3:
                    copyName = saveDirName + k
                    shutil.copy(copyName, '/home/jajman/train/tumor/')

            if fileName in curTestFiles:
                testNum += 1
                print('test move')
                saveDirName = dirName + i + '/TUMOR/'
                files3 = os.listdir(saveDirName)
                for k in files3:
                    copyName = saveDirName + k
                    shutil.copy(copyName, '/home/jajman/validation/tumor/')


print(trainNum)
print(testNum)



