from scipy.io import arff
import numpy as np
import json 
import pandas as pd
import os
import torch
from torch.utils.data import DataLoader
from utils.pyTorchUtils import *
from neuralNetwork.TONetModel import *
from neuralNetwork.AttackerModel import *
import random

f = open('settings.json')
settingsJson = json.load(f)
labelsColumn = settingsJson['labelsColumn']


class DualAdversarialDataSet():

    def __init__(self, dataSetsName, adversarialDatasetPath,adversarialLabelsPath, labelsPercentage):
        self.labels = None
        self.labelsStr = None
        self.labelsHashMap = {}
        self.indexToClassMap={}
        self.classToIndexMap={}
        self.tensorDatabase = None
        self.dataSetsName=dataSetsName
        self.adversarialDatasetPath=adversarialDatasetPath
        self.adversarialLabelsPath=adversarialLabelsPath
        self.labelsPercentage = labelsPercentage        
        self.normalize = False

    def upSampleClasses(self, dataset, classesHashMap):
        classesNames = list(classesHashMap.keys())
        maxSize = len(classesHashMap[classesNames[0]])
        for i in range(1, len(classesNames)):
            if len(classesHashMap[classesNames[i]])>maxSize:
                maxSize=len(classesHashMap[classesNames[i]])
        for i in range(0, len(classesNames)):
            while len(classesHashMap[classesNames[i]])<maxSize:
                pickedCopyIndex = random.randint(0,len(classesHashMap[classesNames[i]])-1)
                dataset.append(classesHashMap[classesNames[i]][pickedCopyIndex])                
                classesHashMap[classesNames[i]].append(classesHashMap[classesNames[i]][pickedCopyIndex])
        return [dataset, classesHashMap]

    def writeClassHashMap(self,classesHashMap):
        toWrite = {}
        for cl in classesHashMap.keys():
            toWrite[str(cl)]=len(classesHashMap[cl])
        
        with open('../inputs/'+'originalRegisters.json', 'w') as f:
            json.dump(toWrite, f)

    def writeUpSampledDatabase(self,filteredData):        
        with open('../data/TONet/'+'upscaledDatabase.json', 'w') as f:
            json.dump(filteredData, f)
    
    
    def convertVoidNoneTypesToEmptyStr(self, trafficInstance):
        convertedTrafficInstance = []
        distinctTypes = {}
        for i in range(0, len(trafficInstance)):
            distinctTypes[type(trafficInstance[i])]=trafficInstance[i]                
            if type(trafficInstance[i])==None:
                convertedTrafficInstance.append("")                
            elif type(trafficInstance[i])==bytes:
                try:
                    tmp = str(trafficInstance[i])
                    convertedTrafficInstance.append(tmp)
                except:
                    signedValue = []
                    for j in trafficInstance[i]:
                        if type(trafficInstance[j])==bytes:
                            signedValue.append(str(j))
                            continue
                        signedValue.append(j)
                    
                    convertedTrafficInstance.append(signedValue)
            else:
                convertedTrafficInstance.append(trafficInstance[i])       
        return convertedTrafficInstance

    def keepOnlyUsedColumns(self, trafficInstance):
        usedColumns = settingsJson['colunasConsideradasRawIndex']
        newInstance = []
        for columnIndex in usedColumns:
            newInstance.append(float(trafficInstance[int(columnIndex)]))
        newInstance.append(trafficInstance[-1])
        return newInstance
    
    def removeLabels(self,dataset):
        labels=[]        
        reducedDataset=[]
        for i in range(0,len(dataset)):
            if len(dataset[i])==0:
                emptyLines.append(i)
                continue
            labels.append(dataset[i][-1])
            instance=[]
            for j in range(0, len(dataset[i])-1):
                instance.append(dataset[i][j])
            reducedDataset.append(instance)
            #del dataset[i][-1]
        
        return {'labels':labels,'dataset':reducedDataset}

    def filterClasses(self,arffLoadedData):
        classesHashMap = {} #key: classname value: array [] of registers
        outputDataset = []
        for i in range(0, len(arffLoadedData)):
            arffLoadedData[i] = self.keepOnlyUsedColumns(arffLoadedData[i].tolist())
            arffLoadedData[i] = self.convertVoidNoneTypesToEmptyStr(arffLoadedData[i])      

        for i in range(0,len(arffLoadedData)):            
            className = arffLoadedData[i][-1]
            if className not in classesHashMap:
                classesHashMap[className]=[]
            classesHashMap[className].append(arffLoadedData[i])
                       
        for i in range(0,len(arffLoadedData)):           
            className = arffLoadedData[i][-1]
            if className not in classesHashMap:
                continue
            if len(classesHashMap[className])<=2000:
                del classesHashMap[className]
                continue    
            outputDataset.append(arffLoadedData[i])
        
        upSampleResults = self.upSampleClasses(outputDataset,classesHashMap) 
        classesHashMap = upSampleResults[1]  
        splitDatasetLabels = self.removeLabels(upSampleResults[0])
        return {'database':splitDatasetLabels['dataset'],'labels':splitDatasetLabels['labels']}

    def mountClassesHashMap(self,data,labels):
        classesHashMap = {} #key: classname value: array [] of registers       
        for i in range(0,len(data)):            
            className = labels[i]
            if className not in classesHashMap:
                classesHashMap[className]=[]
            classesHashMap[className].append(data[i])             
        return classesHashMap
        

    def joinUDPColumns(self,totalData):
        for register in totalData:
            if str(register[-1])=="b'FTP-CONTROL'" or str(register[-1])=="b'FTP-PASV'" or str(register[-1])=="b'FTP-DATA'":
                register[-1]='Bulk (UDP)'

    def normalizeData(self, totalData):
        
        characteristics = []
        for i in range(0, len(totalData[0])):
            characteristics.append([])
            for j in range(0,len(totalData)):
                characteristics[i].append(totalData[j][i])

        for i in range(0, len(characteristics)):
            x = np.array(characteristics[i])
            normalized = (x-np.min(x))/(np.max(x)-np.min(x)) 
            characteristics[i]=normalized.tolist()     

        for i in range(0, len(totalData[0])):            
            for j in range(0,len(totalData)):
                totalData[j][i] = characteristics[i][j]

        return totalData    

    def loadDatasetToArray(self,datasetNm,arrayToFill,labelsArray,path,labelsPath):
        if '.pt' not in datasetNm or '.txt' in datasetNm:
            return
        tensor = torch.load(path+datasetNm)
        labelsTensor = torch.load(labelsPath+datasetNm)
        for i in range(0, len(tensor)):                
            arrayToFill.append(tensor[i])
            labelsArray.append(labelsTensor[i])

    def sortByNumericName(self, files):
        numericFiles = []
        for f in files:
            if '.txt' in f:
                continue
            tmp = f.replace('.pt','')
            tmp = tmp.replace('adversarial_examples_','')
            print(tmp)
            numericFiles.append(int(tmp))
        numericFiles.sort()
        return numericFiles

    def loadAdversarialFiles(self,totalData,labels,numberOfConsideredFiles):
        datasets = self.sortByNumericName(os.listdir(self.adversarialDatasetPath))      
        for i in range(0,len(datasets)):
            if i>numberOfConsideredFiles:
                break            
            self.loadDatasetToArray('adversarial_examples_'+str(datasets[i])+'.pt',totalData,labels,self.adversarialDatasetPath,self.adversarialLabelsPath)
    
    def convertToHashMap(self,array):
        outHash = {}
        for i in range(0,len(array)):
            if array[i] not in outHash:
                outHash[array[i].item()]=[i]
            else:
                outHash[array[i].item()].append(i)
        return outHash

    def loadLabelsMapping(self):
        f = open('../outputs/labelsMapping.txt','r')
        completeString = f.read()
        f.close()
        lines = completeString.split('\n')
        classToIndex = {}
        indexToClass = {}
        for l in lines:
            if l.strip()=='':
                continue            
            parts = l.split(',')            
            classToIndex[parts[0]]=int(parts[1])
            indexToClass[int(parts[1])]=parts[0]
        self.classToIndexMap=classToIndex
        self.indexToClassMap=indexToClass

    def mapArffLabels(self, labels):
        out = []
        for lb in labels:
            out.append(torch.tensor(self.classToIndexMap[str(lb)]))
        return out
    
    def preProcessDataset(self):
        totalData = []
        labels = []
        print('Will load the datasets...')
        for dataset in self.dataSetsName:
            data = arff.loadarff(settingsJson[dataset])
            totalData.extend(data[0])                     
        self.joinUDPColumns(totalData)
        filteredData = self.filterClasses(totalData)
        
        self.loadLabelsMapping()
        totalData = filteredData['database']
        labels = self.mapArffLabels(filteredData['labels'])
        if self.labelsPercentage>0:
            numberOfConsideredFiles = int((len(totalData)/1000)*(self.labelsPercentage/100))           
            self.loadAdversarialFiles(totalData,labels,numberOfConsideredFiles)
            numberOfInstances = numberOfConsideredFiles * 1000
        
        if self.normalize:
            totalData = self.normalizeData(totalData)

        print('Raw Datasets loaded: COMPLETE')        
        classesHashMap = self.mountClassesHashMap(totalData, labels)                 
        print('Filter classes: COMPLETE') 
        totalInstances = len(filteredData['database'])        
        print('Porcentagem de amostras adversarias utilizado:'+str(self.labelsPercentage)+'%')
        print('Porcentagem de amostras reais utilizado: 100%')
        print('Qt. de registros na base:'+str(totalInstances))
        return {'database':totalData,'labels':labels,'classesHashMap':classesHashMap}
   

    def loadDataset(self, preProcessed):            
        self.tensorDatabase = torch.tensor(preProcessed['database'])
        tensorSizes = {}
        for tensor in self.tensorDatabase:
            tensorSizes[len(tensor)]=0        
        self.labelsStr=preProcessed['labels']
        self.labelsHashMap = {}
        for i in range(0,len(self.labelsStr)):            
            if self.labelsStr[i].item() not in self.labelsHashMap:
                self.labelsHashMap[self.labelsStr[i].item()]=len(self.labelsHashMap.keys())      
        self.labels = []
        for lb in self.labelsStr:
            self.labels.append(self.labelsHashMap[lb.item()])
        self.labels = torch.tensor(self.labels)
        torch.save(self.tensorDatabase,'../outputs/datasets/dualDatasetLoader-tensorDatabase.pt')
        torch.save(self.labels,'../outputs/datasets/dualDatasetLoader-labels.pt')

    def __getitem__(self, idx):        
        return self.tensorDatabase[idx], self.labels[idx]

    def __len__(self):
        return len(self.labels)

    def __calculate_std_mean__(self):
        return torch.std_mean(self.tensorDatabase, dim=0, keepdim=True)


def agregateTotals():
    files = ['entry1Registers.json','entry2Registers.json','entry3Registers.json','entry4Registers.json','entry5Registers.json','entry6Registers.json','entry7Registers.json','entry8Registers.json','entry9Registers.json','entry10Registers.json']
    totalJson={}
    for f in files:
        with open('../inputs/'+f, 'r') as f:
            data = json.load(f)
            for key in data.keys():
                if key not in totalJson:
                    totalJson[key]=data[key]
                    continue
                totalJson[key]+=data[key]
    with open('../inputs/agregado.json', 'w') as f:
        json.dump(totalJson, f)

def saveTensorAsStringFile(tensor,filename):
    out = ""
    for i in range(0, len(tensor)):
        for j in range(0,len(tensor[i])):
            if j==0:
                out+='['
            out+=str(float(tensor[i][j]))
            if j!=len(tensor[i])-1:
                out+=','
            else:
                out+=']'            
        out+='\n'
    f = open(filename,'w')
    f.write(out)
    f.close()

if __name__=='__main__':    
    originalDatasetPath = '../outputs/adversarialExamples/'
    originalLabelsPath = '../outputs/targets/'
    adversarialDatasetPath = '../outputs/adversarialExamples/'
    adversarialLabelsPath = '../outputs/targets/'
    labelsPercentage = 10
    advDataset = DualAdversarialDataSet(originalDatasetPath, originalLabelsPath,adversarialDatasetPath,adversarialLabelsPath, labelsPercentage)
    preProcessed = advDataset.preProcessDataset()
    advDataset.loadDataset(preProcessed)
    train_dataloader = DataLoader(advDataset, batch_size=1000)
    train_features, train_labels = next(iter(train_dataloader))
    
    for (X, y) in enumerate(train_dataloader):
        print(X)
        print(y)
        exit()