Dentro do src, existe a seguinte estrutura de pastas:
- 📂 classifiers (scripts de divisao dos registros)
- 📂 datasetLoaders (Objeto de carregamento  de dados da base de dados Discrimators Flow Dataset)
- 📂 utils (Funções utilitarias)

# Atenção, antes de executar você precisa fazer o download do ambiente e das bases de dados
Antes de executar, você precisa fazer o download dos datasets,das amostras que foram geradas nos experimentos, e a estrutura de pastas adequada está disponível nesse link:
<>

Depois de fazer o download, extraia o zip, e cole o diretório src dentro dele. Agora já é possível realizar as execuções.


# Guia de execução
Os scripts a seguir carregam uma base de dados, dividem-a em duas  partes (treinamento e teste), testam a rede neural com o conjunto de teste, e por fim usam o conjunto de teste para gerar amostras adversárias.

Existem duas abordagens possíveis para gerar amostras, Carlini Wagner L2 e FGSM. Por padrão, o Carlini Wagner L2 está definido. Para testar o FGSM, altere o método no arquivo 'settings.json' para 'fgsm'.

Para executar o experimento na base Discrimators Flow Dataset, use:
```bash
python3 generatorDFD.py
```
Nesse experimento, a abordagem é executada na junção dos 10 datasets que o compõe, os resultados dessa abordagem são salvos em:
Os resultados são escritos nos diretórios 'outputs/1-10' e 'outputs/1-10', que estão na estrutura de pastas que contém as bases de dados e as amostras geradas nos experimentos.

Também são realizados experimentos em cada base individual, em quê os resultados  ficam salvos nos  diretórios 
'outputs/1', 'outputs/2', 'outputs/3', 'outputs/4', 'outputs/5', 'outputs/6', 'outputs/7', 'outputs/8', 'outputs/9' e 'outputs/10'. 


Para executar o experimento nas 6 bases agregadas, com a rede neural de 3 características, use:
```bash
python3 generator3features.py
```
Os resultados são escritos no diretórios 'outputs/portscan3fgsm' e 'outputs/portscan3carlini'


Para executar o experimento nas 6 bases agregadas, com a rede neural de 10 características, use:
```bash
python3 generator10features.py
```
Os resultados são escritos nos diretórios 'outputs/portscan10fgsm' e 'outputs/portscan10carlini'


Para gerar as imagens das matrizes de confusão dos experimentos, use:
```bash
python3 controller.py
```
