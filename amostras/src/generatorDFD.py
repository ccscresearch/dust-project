import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import os
from utils.fileUtils import saveTrainTestAsCsv

from utils.fileUtils import convertY
from classifiers.classifiers import *
from art.attacks.evasion import FastGradientMethod
from art.attacks.evasion import CarliniL2Method
from art.estimators.classification import PyTorchClassifier
import json
import pandas as pd
from datasetLoaders.datasetLoader import TonetDataSet
from sklearn.metrics import confusion_matrix

f = open('settings.json')
settingsJson = json.load(f)
datasets = ['entry1','entry2','entry3','entry4','entry5','entry6','entry7','entry8','entry9','entry10']

METHOD = settingsJson['fgsm'] #fgsm, carlini
batchSize=1000
# Step 0: Define the neural network model, return logits instead of activation in forward method


class Net(nn.Module):

    def __init__(self,qt_classes):
        self.qt_classes = qt_classes
        super().__init__()
        
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(20, 64),
            nn.LeakyReLU(),
            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(),
            nn.Linear(256,20),
            nn.BatchNorm1d(20),
            nn.Tanh(),       
            nn.Linear(20, self.qt_classes)           
        )
        
    def forward(self, x):        
        logits = self.linear_relu_stack(x)
        return logits


def mountFolderName(datasets):
    if len(datasets)==1:
        return datasets[0].replace('entry','')
    else:
        return datasets[0].replace('entry','')+'-'+datasets[-1].replace('entry','')

def createFolderTree(folderName):
    if os.path.isdir('../outputs/'+folderName):
        return
    else:
        os.mkdir('../outputs/'+folderName)
        os.mkdir('../outputs/'+folderName+'/fgsm')
        os.mkdir('../outputs/'+folderName+'/carlini')

def run(datasets):
    # Step 1: Load the dataset 
    dataset = TonetDataSet(datasets)
    folderNm = mountFolderName(datasets)
    createFolderTree(folderNm)
    dataset.normalize = True
    preProcessed = dataset.preProcessDataset()
    qt_classes = len(preProcessed['classesHashMap'].keys())
    
    train_test = trainTestSplit(preProcessed['labels'], preProcessed['database'])
    saveTrainTestAsCsv(train_test,'../outputs/'+folderNm+'/'+METHOD+'/', QT_CLASSES)
    x_train = np.array(train_test[0]).astype(np.float32)
    x_test = np.array(train_test[1]).astype(np.float32)
    y_train = convertY(train_test[2], qt_classes).astype(np.float32)
    y_test = convertY(train_test[3], qt_classes).astype(np.float32)
    min_value = 0
    max_value = 1
    
    # Step 2: Create the model
    model = Net(qt_classes)

    # Step 2a: Define the loss function and the optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    # Step 3: Create the ART classifier

    classifier = PyTorchClassifier(
        model=model,
        clip_values=(min_value, max_value),
        loss=criterion,
        optimizer=optimizer,
        input_shape=(1, 20),
        nb_classes=qt_classes,
    )

    # Step 4: Train the ART classifier
    print('Will run the train function on x_train')
    classifier.fit(x_train, y_train, batch_size=batchSize, nb_epochs=200)
    classifier.save('PyTorchClassifier','../outputs/'+folderNm+'/'+METHOD+'/')

    # Step 5: Evaluate the ART classifier on benign test examples
    predictions = classifier.predict(x_test)
    confMat0 = confusion_matrix(np.argmax(y_test, axis=1),np.argmax(predictions, axis=1))

    accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
    print("Accuracy on benign test examples: {}%".format(accuracy * 100))

    # Step 6: Generate adversarial test examples
    if METHOD=='carlini':
        attack = CarliniL2Method(classifier=classifier, learning_rate=0.1, batch_size=batchSize)
    elif METHOD=='fgsm':
        attack = FastGradientMethod(estimator=classifier, eps=0.5)
    else:
        print('Wrong method, please set the method to be carlini or fgsm on settings.json')
        exit()

    x_test_adv = attack.generate(x=x_test)

    # Step 7: Evaluate the ART classifier on adversarial test examples
    predictions = classifier.predict(x_test_adv)

    confMat = confusion_matrix(np.argmax(y_test, axis=1),np.argmax(predictions, axis=1))
    print(confMat)
    print(type(confMat))

    df = pd.DataFrame(x_test_adv)
    df.to_csv('../outputs/'+folderNm+'/'+METHOD+'/adversaries.csv', index=False)

    df = pd.DataFrame(x_train)
    df.to_csv('../outputs/'+folderNm+'/'+METHOD+'/train.csv', index=False)

    df = pd.DataFrame(x_test)
    df.to_csv('../outputs/'+folderNm+'/'+METHOD+'/test.csv', index=False)

    df = pd.DataFrame(y_test)
    df.to_csv('../outputs/'+folderNm+'/'+METHOD+'/y_test.csv', index=False)

    df = pd.DataFrame(y_train)
    df.to_csv('../outputs/'+folderNm+'/'+METHOD+'/y_train.csv', index=False)

    df = pd.DataFrame(confMat0)
    df.to_csv('../outputs/'+folderNm+'/'+METHOD+'/confMatOriginal.csv', index=False)

    df = pd.DataFrame(confMat)
    df.to_csv('../outputs/'+folderNm+'/'+METHOD+'/confMat.csv', index=False)

    accuracy2 = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
    print("Accuracy on adversarial test examples: {}%".format(accuracy2 * 100))

    f = open('../outputs/'+folderNm+'/'+METHOD+'/accuracies.txt','w')
    f.write('['+str(accuracy*100)+','+str(accuracy2*100)+']')
    f.close()

if __name__=='__main__':
    run(datasets)
    #for i in range(0, len(datasets)):
    #    run([datasets[i]])
