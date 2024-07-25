import pandas as pd
import torch
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

def get_device():
    if torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')  
    return device

def df_to_tensor(df):
    device = get_device()
    return torch.from_numpy(df.values).float().to(device)

def generatePlot(confMat,labels,path):    
    disp = ConfusionMatrixDisplay(confusion_matrix=np.array(confMat),display_labels=labels)
    disp.plot()
    plt.savefig(path.replace(".csv",".png"))

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

def save3DTensorAsStringFile(tensor,filename):
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
    print(filename)
    f = open(filename+'.txt','w')
    f.write(out)
    f.close()

def save2DTensorAsStringFile(tensor,filename):
    out = ""
    for i in range(0, len(tensor)):
       if i==0:
           out+='['
       out+=str(float(tensor[i]))
       if i!=len(tensor)-1:
           out+=','
       else:
           out+=']'            
    out+='\n'
    print(filename)

    f = open(filename+'.txt','w')
    f.write(out)
    f.close()
    
def save2DArrayAsStringFile(array,filename):
    out = ""
    for i in range(0, len(array)):
       if i==0:
           out+='['
       out+=str(array[i])
       if i!=len(array)-1:
           out+=','
       else:
           out+=']'            
    out+='\n'
    print(filename)
    f = open(filename+'.txt','w')
    f.write(out)
    f.close()

def keystoint(x):
    return {int(k): v for k, v in x.items()}