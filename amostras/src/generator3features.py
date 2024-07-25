import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from classifiers.classifiers import *
from art.attacks.evasion import FastGradientMethod
from art.attacks.evasion import CarliniL2Method
from art.estimators.classification import PyTorchClassifier
import json
import pandas as pd
from utils.fileUtils import saveTrainTestAsCsv
from utils.fileUtils import convertY
from utils.fileUtils import reduceDataset
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline

f = open('settings.json')
settingsJson = json.load(f)
QT_CLASSES = int(settingsJson['qt_classes'])
method = settingsJson['method'] #carlini or fgsm
outputBasePath = '../outputs/portscan3'+method+'/'
if method!='carlini' and method!='fgsm':
    print('Wrong method, please set the method to be carlini or fgsm on settings.json')
    exit()

def countLabels(labels):
    count = {}
    for lb in labels:
        if lb not in count:
            count[lb]=0
        count[lb]+=1
    return count

class DustNet(nn.Module):
       
    def __init__(self,qt_classes,qt_features):
        self.qt_classes = qt_classes
        self.qt_features = qt_features
        super().__init__()
        
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(self.qt_features, 64),
            nn.LeakyReLU(),
            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(),
            nn.Linear(256,self.qt_features),
            nn.BatchNorm1d(self.qt_features),
            nn.Tanh(),       
            nn.Linear(self.qt_features, self.qt_classes)           
        )
        
    def forward(self, x):        
        logits = self.linear_relu_stack(x)
        return logits

# Step 1: Load the dataset 
df = pd.read_csv('../data/IoT_and_PortScan_format0.csv')
df.drop('device_mac', axis=1, inplace=True)
df.drop('label_name', axis=1, inplace=True)
df.drop(df.columns[0], axis=1, inplace=True)
labels = df['label'].to_numpy()
df.drop('label', axis=1, inplace=True)

df_min_max_scaled = df.copy()
for column in df.columns:
    df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())

dataset = df_min_max_scaled.to_numpy()

oversample = RandomOverSampler(sampling_strategy='not majority', random_state = 42)    
under_sampling = RandomUnderSampler(sampling_strategy='not minority', random_state = 42)
pipeline = Pipeline([
('oversampling', oversample),
('undersampling', under_sampling)
])
if settingsJson['scaling']=='downscaling':
    downscaled = reduceDataset(40000,dataset,labels)
    dataset = downscaled['dataset']
    labels = downscaled['labels']
train_test = trainTestSplit(labels, dataset )
saveTrainTestAsCsv(train_test,outputBasePath,QT_CLASSES)
x_train = np.array(train_test[0]).astype(np.float32)
x_test = np.array(train_test[1]).astype(np.float32)
y_train = np.array(train_test[2]).astype(np.float32)
y_test = np.array(train_test[3]).astype(np.float32)

x_train, y_train = pipeline.fit_resample(x_train, y_train)
x_test, y_test = pipeline.fit_resample(x_test, y_test)

print('Labels map train:')
print(countLabels(y_train))
print("Labels map test")
print(countLabels(y_test))
y_train = convertY(y_train, QT_CLASSES).astype(np.float32)
y_test = convertY(y_test, QT_CLASSES).astype(np.float32)

min_value = 0
max_value = 1

# Step 2: Create the model

model = DustNet(QT_CLASSES,3)

# Step 2a: Define the loss function and the optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Step 3: Create the ART classifier

classifier = PyTorchClassifier(
    model=model,
    clip_values=(min_value, max_value),
    loss=criterion,
    optimizer=optimizer,
    input_shape=(1, 1, 3),
    nb_classes=QT_CLASSES,
)

# Step 4: Train the ART classifier
print('Will run the train function on x_train')
classifier.fit(x_train, y_train, batch_size=1000, nb_epochs=200)

# Step 5: Evaluate the ART classifier on benign test examples
predictions = classifier.predict(x_test)
confMat0 = confusion_matrix(np.argmax(y_test, axis=1),np.argmax(predictions, axis=1))

accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print("Accuracy on benign test examples: {}%".format(accuracy * 100))

# Step 6: Generate adversarial test examples
attack = CarliniL2Method(classifier=classifier,learning_rate=0.1) if method=='carlini' else FastGradientMethod(estimator=classifier, eps=0.5)

x_test_adv = attack.generate(x=x_test)

# Step 7: Evaluate the ART classifier on adversarial test examples
predictions = classifier.predict(x_test_adv)

confMat = confusion_matrix(np.argmax(y_test, axis=1),np.argmax(predictions, axis=1))
print(confMat)
print(type(confMat))

df = pd.DataFrame(x_test_adv)
df.to_csv(outputBasePath+'adversaries.csv', index=False)

df = pd.DataFrame(x_train)
df.to_csv(outputBasePath+'train.csv', index=False)

df = pd.DataFrame(x_test)
df.to_csv(outputBasePath+'test.csv', index=False)

df = pd.DataFrame(y_test)
df.to_csv(outputBasePath+'y_test.csv', index=False)

df = pd.DataFrame(y_train)
df.to_csv(outputBasePath+'y_train.csv', index=False)

df = pd.DataFrame(confMat)
df.to_csv(outputBasePath+'confMat.csv', index=False)

df = pd.DataFrame(confMat0)
df.to_csv(outputBasePath+'confMatOriginal.csv', index=False)

accuracy2 = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print("Accuracy on adversarial test examples: {}%".format(accuracy2 * 100))
f = open(outputBasePath+'accuracies.txt','w')
f.write('['+str(accuracy*100)+','+str(accuracy2*100)+']')
f.close()