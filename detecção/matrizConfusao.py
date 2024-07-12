import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools


# Função para plotar a matriz de confusão
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Matriz de Confusão',
                          cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Matriz de Confusão Normalizada")
    else:
        print('Matriz de Confusão sem Normalização')

    print(cm)

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('Rótulo Verdadeiro',  fontsize=10)
    plt.xlabel('Rótulo Previsto',  fontsize=10)
    plt.tight_layout()


def matrizdeconfusao(rounded_cw2_predictions, outcome,y_test):
    
  cm = confusion_matrix(y_test,rounded_cw2_predictions)

  class_names = ['Normal','Ataque']
  plot_confusion_matrix(cm, classes=class_names, normalize=True)
  plt.savefig("resultados/matrixConfusion.png")


