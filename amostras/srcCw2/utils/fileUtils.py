import numpy as np
import pandas as pd

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