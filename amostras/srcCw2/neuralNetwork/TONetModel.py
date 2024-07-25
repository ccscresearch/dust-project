import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

class ToNetNeuralNetwork(nn.Module):
       
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

if __name__=='__main__':
    model = ToNetNeuralNetwork(6)
    model = model.to("cpu")
    print(model)
