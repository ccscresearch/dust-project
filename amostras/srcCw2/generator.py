from scipy.io import arff
import json 
import pandas as pd
import numpy as np
import torch
from cwLibrary.cwBkp import L2Adversary
from neuralNetwork.lossFunctions import *
from torch.utils.data import DataLoader
from utils.pyTorchUtils import *
from neuralNetwork.TONetModel import *
from datasetLoaders.datasetLoader4D import TonetDataSet


f = open('settings.json')
settingsJson = json.load(f)

datasets = ['entry1','entry2','entry3','entry4','entry5','entry6','entry7','entry8','entry9','entry10']
NORMALIZE='normalized' #normalized or notNormalized
trainingPath='../savedModels/defense/'+NORMALIZE+'/data1-'+str(len(datasets))

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    running_loss = 0.0
    last_loss = 0.0
    for batch, (X, y) in enumerate(dataloader):        
        # Compute prediction error        
        pred = model(X)     
        loss = loss_fn(pred, y)
        
        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        running_loss+=loss.item()
        if batch % 100 == 99:
            last_loss = running_loss / 100
            print('  batch {} loss: {}'.format(batch + 1, last_loss))
            current = (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")  
            running_loss = 0
    return last_loss

def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)    
    num_batches = len(dataloader)
    model.eval()
    preds = []
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:            
            pred = model(X)            
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

def generateAdversarialExamples(model):
    model = model.to(get_device())
    articleBatchSize = settingsJson['batchSize']
    articleEpochs = settingsJson['epochs']    
    best_vloss = 1_000_000.
    tonetDataset = TonetDataSet(datasets)    
    tonetDataset.normalize = NORMALIZE    
    
    dataset = tonetDataset.preProcessDataset()    
    
    tonetDataset.loadDataset(dataset) 
        
    with open('../outputs/labelsMapping.txt','w') as f:
        f.write(tonetDataset.labelsHashMapToString())
    meanStd = tonetDataset.__calculate_std_mean__()
    mean = torch.unsqueeze(meanStd[0],dim=0)
    std = torch.unsqueeze(meanStd[1],dim=0) 
    
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)
    train_dataloader = DataLoader(tonetDataset, batch_size=articleBatchSize, shuffle=True)
    validation_dataloader = DataLoader(tonetDataset, batch_size=articleBatchSize, shuffle=True)
    test_dataloader = DataLoader(tonetDataset, batch_size=articleBatchSize, shuffle=True)
    epochs = 50    
    lossCounter=0
    lossArray = []
    for t in range(epochs):        
        print(f"Epoch {t+1}\n-------------------------------")
        train_loss = train(train_dataloader, model, loss_fn, optimizer)
        running_vloss = 0.0
        model.eval()
        with torch.no_grad():
            for i, vdata in enumerate(validation_dataloader):
                vinputs, vlabels = vdata
                voutputs = model(vinputs)
                vloss = loss_fn(voutputs, vlabels)
                running_vloss += vloss
        avg_vloss = running_vloss / (i + 1)       
        if t==epochs-1:
            torch.save(model.state_dict(), trainingPath)
              
    print('test on train_dataloader')
    test(train_dataloader, model, loss_fn)
    print('test on test_dataloader')
    test(test_dataloader, model, loss_fn)    
    print("Done!")    
    return model

def runTest(model):
    articleBatchSize = settingsJson['batchSize']
    tonetDataset = TonetDataSet(datasets)    
    tonetDataset.normalize = NORMALIZE
    preProcessed = tonetDataset.preProcessDataset()
    tonetDataset.loadDataset(preProcessed)
    loss_fn = nn.CrossEntropyLoss()
    test_dataloader = DataLoader(tonetDataset, batch_size=articleBatchSize, shuffle=True)
    test(test_dataloader, model, loss_fn)

def mountInputsBox(mean,std):    
    zipped = zip(mean, std)    
    
    menor = None
    maior = None
    i = 0
    for m, s in zipped:        
        tmpMin = (0 - m) / s
        tmpMax = (1 - m) / s               
        if i == 0:
            menor = tmpMin
            maior = tmpMax
        else:
            if menor>tmpMin:
                menor=tmpMin
            if maior<tmpMax:
                maior=tmpMax
        i+=1    
    return (min(menor),max(maior))    

def runCw2(net, dataloader, mean, std):    
    inputs_box_old = mountInputsBox(mean,std)
    interval = mean+std
    inputs_box_std = (-1*min(interval[0]), max(interval[0]))
    inputs_box = (min((0 - m[0]) / s[0] for m, s in zip(mean, std)),
              max((1 - m[0]) / s[0] for m, s in zip(mean, std)))
    
    inputs_box_forced  = [-1,1]

    adversary = L2Adversary(targeted=False,confidence=0.0,search_steps=10,box=inputs_box_forced, optimizer_lr=1e-3)
    i = 0
    totalAdversaries = None
    totalY = None
    for batch, (X, y) in enumerate(dataloader):    
        i+=1        
        inputs = X   
        targets = y
        adversarial_examples = adversary(net, inputs, targets, to_numpy=False)
        if totalAdversaries is None:
            totalAdversaries = adversarial_examples
            totalY = targets
        else:
            totalAdversaries = torch.cat((totalAdversaries,adversarial_examples))
            totalY = torch.cat((totalY,targets))        
    torch.save(totalAdversaries, settingsJson['adversarialExamplesSamplesPathML']+'adversarial_examples.pt')
    torch.save(totalY, settingsJson['adversarialExamplesTargetsPathML']+'adversarial_examples.pt')

def testAdvxs_var(model):
    tensor = torch.load('adversarial_examples.pt')    
    save3DTensorAsStringFile(tensor,'adversarial_examples.txt')    
    exit()
    for i in range(0,len(pred)):
        for j in range(0,len(pred[i])):
            print(float(pred[i][j]))
    return model

if __name__=='__main__':    
    #To train a model, we need a loss function and an optimizer.    
    model = ToNetNeuralNetwork(6)   
    model.load_state_dict(torch.load(trainingPath))
    model.eval()
    generateAdversarialExamples(model)
    runTest(model)

    
    
    
    
    
