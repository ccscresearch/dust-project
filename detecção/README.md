## Descrição etapa de Detecção

Esta solução envolve um método de detecção de vulnerabilidades em redes IoT, mais especificamente a detecção de varredura de portas, sem conhecimento prévio da estrutura da rede, dispensando rótulos na base de teste para a detecção.

### Instalação

1. Instalação de dependências: pip3 install -r requirements.txt 

### Estrutura

- 📂 resultados/: Pasta auxiliar para armazenar os resultados das execuções e testes do modelo.

- 📂 pcaps/: Pasta auxiliar para armazenar os pcaps baixados para realizar o pré-processamento.

- 📦 detectorPortscan.py: Script principal que contém a implementação do detector de varredura de portas.

- 📦 matrizConfusao.py: Script utilizado para gerar a matriz de confusão a partir dos resultados do modelo.

- 📦 modelo_treinado.h5: Arquivo contendo o modelo treinado para detecção de varredura de portas em redes IoT.

- 📦 pre-process.py: Script utilizado para realizar o pré-processamento dos pcaps, extraindo as caracteristicas e salvando em csv.

- 📦 requirements.txt: Arquivo contendo as bibliotecas e suas versões para utilização da solução.

### Como Usar

Testar com o modelo ja treinado e os dados processados

	python3 detectorPortscan.py 0

Treinar o modelo e testar com os dados processados

	python3 detectorPortscan.py 1

### Dataset Utilizados

Conjunto de dados de Ataque de Varredura de Portas

- [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)
- [MSCAD](https://ieee-dataport.org/documents/multi-step-cyber-attack-dataset-mscad-intrusion-detection)
- [EDGE-IIOTSET](https://ieee-dataport.org/documents/edge-iiotset-new-comprehensive-realistic-cyber-security-dataset-iot-and-iiot-applications)
- [PORT-ATTACK](https://ieee-dataport.org/documents/dataset-port-scanning-attacks-emulation-testbed-and-hardware-loop-testbed)

Conjunto de dados de Tráfego Normal de dispositivos IoT

- [IoT Traffic Analysis](https://iotanalytics.unsw.edu.au/iottraces.html)
- [Cenário Experimental](https://drive.google.com/file/d/1J4-9eby8X8NYYM0o3cxR75GFdfIiqcVG/view)

### Realizar o Pré-Processamento

Para realizar o pré-processamento dos PCAPs, é necessário baixar os PCAPs de varreduras de portas e tráfego normal disponíveis nos links acima e salvá-los na pasta pcaps, seguindo a estrutura das subpastas:

- 📂 pcaps/port_scan´-> CIC-IDS2017, MSCAD, EDGE-IIOTSET, PORT-ATTACK
- 📂 pcaps/trafego_normal -> IoT Traffic Analysis e Cenário Experimental

Após os pcaps em suas respectivas subpastas, excute:

	python3 pre-process.py

Este script irá gerar dois arquivos CSV contendo os dados de treino e teste necessários para executar o código de detecção:

	python3 detectorPortscan.py 2

Por fim, será retornado os resultados na pasta em questão.