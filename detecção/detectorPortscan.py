import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import regularizers
from sklearn import preprocessing
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.models import save_model, load_model
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
import tensorflow as tf
from tqdm import tqdm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from matrizConfusao import *
import requests
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

tf.compat.v1.disable_eager_execution()

def redeNeural(train_x, train_y):

    modelo = Sequential([
        Dense(64, activation='relu', input_shape=(train_x.shape[1],)),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')  
    ])

    modelo.compile(optimizer='adam',
                   loss='binary_crossentropy',
                   metrics=['accuracy'])
    
    print(modelo.summary())

    modelo.fit(train_x, train_y, epochs=10,batch_size=64,shuffle = True,validation_split=0.1)

    # Salvar o modelo treinado
    #modelo.save('modelo_treinado.h5')
    return modelo

# Função para baixar o arquivo
def download_file(url, local_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def train_model(local=None):

    if local is None:
        dropbox_link = "https://www.dropbox.com/scl/fi/8tmdh5awggj5el6kmjcwl/IoT_and_PortScan.csv?rlkey=gzf35kfpzv1p4o9agnnvhrzyr&st=khp16n8u&dl=1"
        local_filename = "arquivo_csv"
        print("\n")
        print(f"Iniciando download de {dropbox_link}...")
        download_file(dropbox_link, local_filename)
    else:
        local_filename = 'treino-preProcessamento.csv'

    df1 = pd.read_csv(local_filename, index_col = 0, low_memory=False)

    train_x = df1.drop(['label','device_mac','label_name'], axis = 1) # seleciona features e ignora a primeira coluna do csv
    y = df1['label']  # seleciona rotulos "primeira linha do csv"

    le = preprocessing.LabelEncoder()
    train_y = le.fit_transform(y)

    oversample = RandomOverSampler(sampling_strategy='not majority', random_state = 42)    
    under_sampling = RandomUnderSampler(sampling_strategy='not minority', random_state = 42)

    pipeline = Pipeline([
    ('over_sampling', oversample),
    ('undersampling', under_sampling)
    ])

    print("balanceamento dataset........")
    train_x, train_y = pipeline.fit_resample(train_x, train_y)
    modeloNovo = redeNeural(train_x, train_y)
    test_model(modeloNovo,local='1')


def test_model(modeloNovo=None,local=None):

    if modeloNovo is None:
        modelo = load_model('modelo_treinado.h5')             
        print('\n### -- Modelo carregado -- ###\n')

    else:
        modelo = modeloNovo

    if local is None:
        dropbox_link = "https://www.dropbox.com/scl/fi/7gg3jh03rrv4xmke9zzgl/Teste_Normal_and_PortScan.csv?rlkey=9pcq9szqa9ednh36v9ftzyigy&st=a4k166de&dl=1"
        local_filename = "csv_teste"
        print(f"Iniciando download de {dropbox_link}...")
        download_file(dropbox_link, local_filename)
    else:
        local_filename = 'teste-preProcessamento.csv'

    df2 = pd.read_csv(local_filename, index_col = 0, low_memory=False)
    rotulosDF2 = df2['label'].values
    df2 = df2.drop(['label','device_mac'],  axis = 1)

    ###  Predição sem rotulos #####
    print("predizendo.....")

    probabilidades = modelo.predict(df2)

    # Calcular a estimativa da probabilidade média de ataque
    estimativa_probabilidade_ataque = np.mean(probabilidades)

    # Exibir a estimativa
    print("\nEstimativa da probabilidade média de tráfego estar associado a um ataque:", estimativa_probabilidade_ataque)

    limiar = 0.5
    predicoes = np.where(probabilidades > limiar,'Ataque','Tráfego Normal')

    print("\n")
    # Conta o número de instâncias classificadas como ataque e tráfego normal
    contagem_ataque = np.sum(predicoes == 'Ataque')
    contagem_normal = np.sum(predicoes == 'Tráfego Normal')

    # Calcula a proporção de instâncias classificadas como ataque
    proporcao_ataque = contagem_ataque / len(predicoes)
    proporcao_normal = contagem_normal / len(predicoes)

    print("Número de amostras classificadas como ataque:", contagem_ataque)
    print("Número de amostras classificadas como tráfego normal:", contagem_normal)
    print('\n')
    print("[Taxa Verdadeiro positivo] Proporção de amostras classificadas como ataque:", proporcao_ataque)
    print("[Taxa Falso Negativo] Proporção de amostras classificadas como tráfego normal:", proporcao_normal)
    print("\n")


    ######################### prevdisões com os rotulos #################

    print("#### Predições com Rotulos ####")
    verdadeiros_positivos = 0
    falsos_positivos = 0
    verdadeiros_negativos = 0
    falsos_negativos = 0

    # Realiza a contagem elemento a elemento
    for predicao, rotulo in zip(predicoes, rotulosDF2):
        if predicao == 'Ataque' and rotulo == 1:
            verdadeiros_positivos += 1
        elif predicao == 'Ataque' and rotulo == 0:
            falsos_positivos += 1

        elif predicao == 'Tráfego Normal' and rotulo == 0:
            verdadeiros_negativos += 1
        elif predicao == 'Tráfego Normal' and rotulo == 1:
            falsos_negativos += 1

    # Calcular acurácia, precisão, recall, e F1-score
    acuracia = (verdadeiros_positivos + verdadeiros_negativos) / len(rotulosDF2)
    precisao = verdadeiros_positivos / (verdadeiros_positivos + falsos_positivos) if (verdadeiros_positivos + falsos_positivos) != 0 else 0
    recall = verdadeiros_positivos / (verdadeiros_positivos + falsos_negativos) if (verdadeiros_positivos + falsos_negativos) != 0 else 0
    f1_score = 2 * (precisao * recall) / (precisao + recall) if (precisao + recall) != 0 else 0

    # Imprime as métricas
    print(f'Acurácia: {acuracia:.2f}')
    print(f'Precisão: {precisao:.2f}')
    print(f'Recall: {recall:.2f}')
    print(f'F1-score: {f1_score:.2f}')

    # Fazendo previsões no conjunto de teste
    y_pred_classes = (probabilidades > limiar).astype(int)
    y_test_classes = rotulosDF2

    accuracy = accuracy_score(y_test_classes, y_pred_classes)
    precision = precision_score(y_test_classes, y_pred_classes, average='weighted')
    recall = recall_score(y_test_classes, y_pred_classes, average='weighted')
    #f1 = f1_score(y_test_classes, y_pred_classes, average='weighted')

    # Imprimindo as métricas
    print(f'Acurácia: {accuracy}')
    print(f'Precisão: {precision}')
    print(f'Recall: {recall}')
    #print(f'F1-score: {f1}')

    target_names = ['Normal','Ataque']

    # Relatório de Classificação detalhado
    print('\nRelatório de Classificação:')
    print(classification_report(y_test_classes, y_pred_classes, target_names=target_names))

    rounded = y_pred_classes.astype(int)
    matrizdeconfusao(rounded, target_names, y_test_classes)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <train_again>")
        sys.exit(1)

    try:
        train_again = int(sys.argv[1])
    except ValueError:
        print("O argumento deve ser um número inteiro (1 para treinar, 0 para testar).")
        sys.exit(1)

    if train_again == 1:
        train_model()
    elif train_again == 0:
        test_model()
    elif train_again == 2:
        train_model(local='1')
    else:
        print("O argumento deve ser 1 (para treinar) ou 0 (para testar).")
        sys.exit(1)