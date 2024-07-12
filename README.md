# Dust-Projetct
This repository contains all material produced in the context of the FAPESP/MCTI/CGI DUST. Please, cite us.



## Descrição etapa de Detecção (pasta detecção)

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