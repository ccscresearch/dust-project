from scipy.io import arff
import numpy as np
import json 
import pandas as pd
import torch
from torch.utils.data import DataLoader
from utils.pyTorchUtils import *
from neuralNetwork.TONetModel import *
import random

class SimpleDataSet():

    def __init__(self,x,y):
        self.labels = y #exemplo de formato, considerando 4 labels: [ 0,1,0,1 ]
        self.tensorDatabase = x #exemplo de formato: [[feature1, feature2, ..., featureN], [feature1, feature2, ..., featureN]]
                
    def __getitem__(self, idx):        
        return self.tensorDatabase[idx], self.labels[idx]

    def __len__(self):
        return len(self.labels)

    def __calculate_std_mean__(self):
        return torch.std_mean(self.tensorDatabase, dim=0, keepdim=True)