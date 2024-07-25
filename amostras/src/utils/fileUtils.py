import numpy as np
import pandas as pd
import random

def readLabels(dataframe):
    out = dataframe.to_numpy()
    out = np.argmax(out, axis=1)    
    return out

def returnLabelsCount(labels):
    labelsCount = {} #key:label, value:qtde instances
    for lb in labels:
        if lb not in labelsCount:
            labelsCount[lb]=0
        labelsCount[lb]+=1
    return labelsCount

'''
Agrupa dois hashmaps numericos, em caso de conflito de chaves, os valores sao somados
'''
def sumHashes(hashesArray):
    finalHash = {}
    for hashMap in hashesArray:
        for key in hashMap.keys():
            if key not in finalHash:
                finalHash[key]=hashMap[key]
            else:
                finalHash[key]+=hashMap[key]
    return finalHash

def loadCsvs(file_paths):
    dfs = []
    for path in file_paths:        
        df = pd.read_csv(path)         
        dfs.append(df)
    complete = pd.concat(dfs, axis=0, ignore_index=True)
    return complete

def convertY(yData, nbClasses):
    outputY = []    
    for y in yData:        
        currentLabel = np.zeros(nbClasses)
        currentLabel[int(y)] = 1        
        outputY.append(currentLabel)
    return np.array(outputY)



def saveTrainTestAsCsv(train_test,outputBasePath, qtClasses):    
    x_train = np.array(train_test[0]).astype(np.float32)
    x_test = np.array(train_test[1]).astype(np.float32)
    y_train = np.array(train_test[2]).astype(np.float32)
    y_test = np.array(train_test[3]).astype(np.float32)

    df = pd.DataFrame(x_train)
    df.to_csv(outputBasePath+'train_og.csv', index=False)

    df = pd.DataFrame(x_test)
    df.to_csv(outputBasePath+'test_og.csv', index=False)

    df = pd.DataFrame(convertY(y_test, qtClasses).astype(np.float32))
    df.to_csv(outputBasePath+'y_test_og.csv', index=False)

    df = pd.DataFrame(convertY(y_train, qtClasses).astype(np.float32))
    df.to_csv(outputBasePath+'y_train_og.csv', index=False)

def reduceDataset(size,dataset,labels):
    print('Downscaling dataset to size:'+str(size))
    labelsHash = returnLabelsCount(labels)
    labelsRegisters = {} #key:labelstr, value: array of registers
    for i in range(0,len(labels)):
        if labels[i] not in labelsRegisters:
            labelsRegisters[labels[i]]=[]
        labelsRegisters[labels[i]].append(dataset[i])
    qtdePerClass = int(size/len(labelsHash.keys()))
    newDataset = []
    newLabels = []
    for label in labelsHash:        
        selectedIndexes = random.sample(range(0,len(labelsRegisters[label])),qtdePerClass)
        for ind in selectedIndexes:
            newDataset.append(labelsRegisters[label][ind])
            newLabels.append(label)
    return {'dataset':newDataset,'labels':newLabels}
    




