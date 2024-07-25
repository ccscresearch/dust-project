import csv
import json
import numpy as np
from classifiers.classifiers import *
from utils.fileUtils import readLabels,returnLabelsCount, sumHashes
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

DFLOW_HEADER={"0":"WWW","1":"MAIL","2":"Bulk (UDP)","3":"P2P","4":"DB","5":"SERVICES"}
PORTSCAN_HEADER = {"0":"DADOS","1":"ATAQUE"} #0: data, 1:attack
BASE_PATHS = [ ['../outputs/1-10/carlini/','../outputs/1-10/fgsm/'],['../outputs/portscan10carlini/','../outputs/portscan10fgsm/'],['../outputs/portscan3carlini/','../outputs/portscan3fgsm/'] ] 
DATASETS_HEADERS = [ DFLOW_HEADER, PORTSCAN_HEADER, PORTSCAN_HEADER ]

def convertToPercentageMode(confMat):
    newConfMat = []
    for l in confMat:
        total = 0
        for c in l:
            total+=c
        newConfMat.append([])
        for c in l:
            percentage = (c/total)*100
            displayPercentage = round(float(percentage),2)            
            if displayPercentage>=99:
                newConfMat[-1].append(99)
            else:
                newConfMat[-1].append(displayPercentage)
    return newConfMat

def read_conf_mat(path):
    confusion_matrix_array = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            confusion_matrix_array.append([])
            columns = row.keys()
            for c in columns:
                confusion_matrix_array[-1].append(int(row[c]))
    return confusion_matrix_array

def persistResults(methodName, datasetName):
    methodIndex = 1 if 'fgsm' == methodName else 0
    datasetHash = {'tonet':0,'portscan10':1,'portscan3':2}
    datasetIndex = datasetHash[datasetName]
    basePath = BASE_PATHS[datasetIndex][methodIndex]
    header = DATASETS_HEADERS[datasetIndex]
    csvs_path = [basePath+'confMat.csv',basePath+'confMatOriginal.csv']
    accuracies_path = basePath+'accuracies.txt'
    JSON_PATH = basePath+'results.json'
    f = open(accuracies_path, 'r')
    strAcc = f.read()
    f.close()
    accuraciesArray = json.loads(strAcc)
    finalJson = {'labels_map':header,'accuracies':{'adversaries':accuraciesArray[1],'original':accuraciesArray[0]}}
    for path in csvs_path:  
        confMat = read_conf_mat(path)        
        percentageConfMat = convertToPercentageMode(confMat)
        generatePlot(percentageConfMat,header.values(),path)
        finalJson[path.replace('.csv','_by_percentage').replace(basePath,'')] = percentageConfMat
        finalJson[path.replace('.csv','_by_instances').replace(basePath,'')] = confMat       
    
    dataObjectOriginal = {'y_train_og':readLabels(pd.read_csv(basePath+'y_train_og.csv')),'y_test_og':readLabels(pd.read_csv(basePath+'y_test_og.csv'))}
    dataObjectUpscaled = {'y_train':readLabels(pd.read_csv(basePath+'y_train.csv')),'y_test':readLabels(pd.read_csv(basePath+'y_test.csv'))}
    classesMapOg=sumHashes([returnLabelsCount(dataObjectOriginal['y_train_og']),returnLabelsCount(dataObjectOriginal['y_test_og'])])
    classesMapUpscaled=sumHashes([returnLabelsCount(dataObjectUpscaled['y_train']),returnLabelsCount(dataObjectUpscaled['y_test'])])
    finalJson['sizes'] = {'original':{},'upscaled':{}}
    finalJson['sizes']['original']['dataset']=len(dataObjectOriginal['y_train_og'])+len(dataObjectOriginal['y_test_og'])
    for key in classesMapOg:
        finalJson['sizes']['original'][str(key)]=classesMapOg[key]
    finalJson['sizes']['upscaled']['dataset']=len(dataObjectUpscaled['y_train'])+len(dataObjectUpscaled['y_test'])
    for key in classesMapUpscaled:
        finalJson['sizes']['upscaled'][str(key)]=classesMapUpscaled[key]
    with open(JSON_PATH, 'w') as fp:
        json.dump(finalJson, fp)

def generatePlot(confMat,labels,path):    
    disp = ConfusionMatrixDisplay(confusion_matrix=np.array(confMat),display_labels=labels)
    disp.plot()
    plt.ylabel('Rótulo Verdadeiro',  fontsize=10)
    plt.xlabel('Rótulo Previsto',  fontsize=10)
    plt.tight_layout()
    plt.savefig(path.replace(".csv",".png"))

if __name__=='__main__':     
    combinations = [['fgsm','tonet'],['fgsm','portscan10'],['fgsm','portscan3'],['carlini','tonet'],['carlini','portscan10'],['carlini','portscan3']]
    
    for methodAndDb in combinations:
        try:
            persistResults(methodAndDb[0],methodAndDb[1])
        except:            
            continue
    