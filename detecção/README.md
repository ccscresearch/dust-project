## Descrição etapa de Detecção

Esta solução envolve um método de detecção de vulnerabilidades em redes IoT, mais especificamente a detecção de varredura de portas, sem conhecimento prévio da estrutura da rede, dispensando rótulos na base de teste para a detecção.

### Instalação

1. Instalação de dependências: pip3 install -r requirements.txt 

### Estrutura

- 📂 resultados/: Pasta auxiliar para armazenar os resultados das execuções e testes do modelo.

- 📦 detectorPortscan.py: Script principal que contém a implementação do detector de varredura de portas.

- 📦 matrizConfusao.py: Script utilizado para gerar a matriz de confusão a partir dos resultados do modelo.

- 📦 modelo_treinado.h5: Arquivo contendo o modelo treinado para detecção de varredura de portas em redes IoT.

### Como Usar
Testar com o modelo ja treinado

	python3 detectorPortscan.py 0

Treinar o modelo e testar

	python3 detectorPortscan.py 1

### Dataset Utilizados

Conjunto de dados de Ataque de Varredura de Portas

- [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)
- [MSCAD](https://ieee-dataport.org/documents/multi-step-cyber-attack-dataset-mscad-intrusion-detection)
- [EDGE-IIOTSET](https://ieee-dataport.org/documents/edge-iiotset-new-comprehensive-realistic-cyber-security-dataset-iot-and-iiot-applications)
- [PORT-ATACK](https://ieee-dataport.org/documents/dataset-port-scanning-attacks-emulation-testbed-and-hardware-loop-testbed)

Conjunto de dados de Tráfego Normal de dispositivos IoT

- [IoT Traffic Analysis](https://iotanalytics.unsw.edu.au/iottraces.html)
- [Cenário Experimental](https://drive.google.com/file/d/1J4-9eby8X8NYYM0o3cxR75GFdfIiqcVG/view)