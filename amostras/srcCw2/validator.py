from scipy.io import arff
import json 
import pandas as pd
import torch

from neuralNetwork.lossFunctions import *
from torch.utils.data import DataLoader
from utils.pyTorchUtils import *
from neuralNetwork.AttackerModel import *
from datasetLoaders.datasetLoader import TonetDataSet
from datasetLoaders.old.datasetLoaderAdversarialSort import AdversarialDataSet
from datasetLoaders.dualDatasetLoader import DualAdversarialDataSet
from torchmetrics import ConfusionMatrix
import gc

f = open('settings.json')
settingsJson = json.load(f)
DEVICE=get_device()
datasets = ['entry1','entry2','entry3','entry4','entry5','entry6','entry7','entry8','entry9','entry10']
NORMALIZE=True
if NORMALIZE:
    trainingPath = '../savedModels/attack/normalized/normalized'
    adversarialSamplesPath = settingsJson['adversarialExamplesSamplesPathML']
    adversarialTargetsPath = settingsJson['adversarialExamplesTargetsPathML']
else:
    adversarialSamplesPath = settingsJson['adversarialExamplesSamplesNotNormalizedPathML']
    adversarialTargetsPath = settingsJson['adversarialExamplesTargetsNotNormalizedPathML']
    trainingPath = '../savedModels/attack/notNormalized/notNormalized'
debugMode = True

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    running_loss = 0.0
    for batch, (X, y) in enumerate(dataloader):        
        # Compute prediction error        
        pred = model(X)     
        loss = loss_fn(pred, y)
        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        running_loss+=loss.item()
        if batch % 1000 == 999:
            last_loss = running_loss / 1000
            print('  batch {} loss: {}'.format(batch + 1, last_loss))
            current = (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")  
            running_loss = 0
    return last_loss

def runTraining(model):
    model = model.to(DEVICE)
    articleBatchSize = settingsJson['batchSize']
    articleEpochs = 300    
    best_vloss = 1_000_000.
    tonetDataset = TonetDataSet(datasets)    
    tonetDataset.normalize = NORMALIZE

    validationDataSet = TonetDataSet(datasets)
    validationDataSet.normalize = NORMALIZE

    testDataSet = TonetDataSet(datasets)
    testDataSet.normalize = NORMALIZE

    trainTestValidation = tonetDataset.preProcessDataset()    
    validationDataSet.loadDataset(trainTestValidation['validation'])
    testDataSet.loadDataset(trainTestValidation['test'])
    tonetDataset.loadDataset(trainTestValidation['train'])         
    
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    train_dataloader = DataLoader(tonetDataset, batch_size=articleBatchSize, shuffle=True)
    validation_dataloader = DataLoader(validationDataSet, batch_size=articleBatchSize, shuffle=True)
    test_dataloader = DataLoader(testDataSet, batch_size=articleBatchSize, shuffle=True)
    epochs = articleEpochs
    lossCounter=0
    lossArray = []
    for t in range(epochs):
        model.train(True)
        print(f"Epoch {t+1}\n-------------------------------")
        print('training')
        train_loss = train(train_dataloader, model, loss_fn, optimizer)
        print('validation')
        running_vloss = 0.0
        model.eval()
        with torch.no_grad():
            for i, vdata in enumerate(validation_dataloader):
                vinputs, vlabels = vdata
                voutputs = model(vinputs)
                vloss = loss_fn(voutputs, vlabels)
                running_vloss += vloss
        avg_vloss = running_vloss / (i + 1)

        torch.save(model.state_dict(), trainingPath)
        test(train_dataloader, model, loss_fn)
        if len(lossArray)==0:
            lossArray.append(train_loss)
        else:            
            if train_loss<lossArray[-1]:
                lossCounter+=1
            lossArray.append(train_loss)
        if len(lossArray)>=10:
            if lossCounter==0:
                break
            else:
                lossCounter=0
                lossArray=[] 
    
    print('test on train_dataloader')
    test(train_dataloader, model, loss_fn)
    print('test on test_dataloader')
    test(test_dataloader, model, loss_fn)
    return model


def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    total = 0
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    confMatrix = ConfusionMatrix(task="MultiClass",num_classes=6)
    completeConfMatrix = None
    with torch.no_grad():
        for X, y in dataloader:            
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            results = confMatrix(pred.argmax(1),y)
            if completeConfMatrix is None:
                completeConfMatrix = results
            else:
                completeConfMatrix = torch.add(completeConfMatrix,results)   
            total+=len(y) 
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()            
    test_loss /= num_batches
    correct /= size
    print('Matriz de confusao')    
    print(completeConfMatrix)   
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
    return completeConfMatrix

def runTest(model):
    model.load_state_dict(torch.load(trainingPath))
    articleBatchSize = settingsJson['batchSize']
      
    for testPercentage in settingsJson['testPercentages']:        
        tonetDataset = AdversarialDataSet(adversarialSamplesPath,adversarialTargetsPath,testPercentage)
        tonetDataset.normalize = NORMALIZE
        trainTestValidation = tonetDataset.preProcessDataset()        
        tonetDataset.loadDataset(trainTestValidation['train'])
        loss_fn = nn.CrossEntropyLoss()
        test_dataloader = DataLoader(tonetDataset, batch_size=articleBatchSize, shuffle=True)
        confMat = test(test_dataloader, model, loss_fn)
        df = pd.DataFrame(confMat)
        df.to_csv(adversarialSamplesPath+'confMat.csv', index=False)
        
        generatePlot(convertToPercentageMode(confMat),["WWW","MAIL","Bulk (UDP)","P2P","DB","SERVICES"],adversarialSamplesPath+'confMat.png')
        del test_dataloader
        del loss_fn
        del tonetDataset        
        gc.collect()

def test_adversarialExamples(model):
    tensor = torch.load('adversarial_examples.pt')
    out = ""
    for i in range(0, len(tensor)):
        for j in range(0,len(tensor[i])):
            out+=str(float(tensor[i][j]))+' | '
        out+='\n'
    return model

if __name__=='__main__':   
    model = AttackerNetwork()
    if settingsJson['attackerMode']=='TRAIN':
        runTraining(model)        
    elif settingsJson['attackerMode']=='TEST':
        model.load_state_dict(torch.load(trainingPath))
        model.eval()
        runTest(model)
    else:
        print('Set the attackerMode do "TRAIN" or "TEST" in the settings.json file, then run this script again')
    
    
    
    
    
