# Essa é a implementação generativa das amostras que não obteve resultados consistentes
Para visualizar os resultados bem sucedidos, verifique o src do nível acima, o srcCw2 é o registro dos códigos desenvolvidos com uma adaptação da biblioteca pytorch-cw2, mas que apresentou resultados inconsistentes. Caso queira replicar os seus passos, essa página disponibiliza uma explicação da estrutura, e um guia rápido de execução.

# Atenção, antes de executar você precisa fazer o download do ambiente e das bases de dados
Antes de executar, você precisa fazer o download dos datasets,das amostras que foram geradas nos experimentos, e a estrutura de pastas adequada está disponível nesse link:
https://drive.google.com/file/d/1ZULCwrpTP0MvaZVUZCG_tzS_AqjdRcUA/view?usp=sharing


Depois de fazer o download, extraia o zip, e cole o diretório src dentro dele. Agora já é possível realizar as execuções.

Ao extrair os arquivos zipados, você verá a seguinte estrutura de pastas:
- 📂 classifiers (Códigos associados a divisão dos registros)
- 📂 cwLibrary (Biblioteca adversarial adaptada de https://github.com/kkew3/pytorch-cw2/)
- 📂 datasetLoaders (Código dos scripts dos objetos que carregam os registros de tráfego em memória)
- 📂 neuralNetwork (Modelos das redes neurais)
- 📂 utils (Scripts de suporte)

# Guia de execução
Para gerar exemplos adversariais através da rede artificial, utilize o script:
```bash
python3 generator.py
```
Esse script irá treinar uma rede neural, e executar o teste com os dados originais sobre ela. Para então gerar as amostras adversárias, salvas em ../outputs/normalized/adversarial1-10/ e ../outputs/normalized/targets1-10/

O próximo passo é avaliação das amostras em outra rede neural, defina o modo de execução alterando a variável 'attackerMode' no arquivo settings.json para 'TRAIN' ou 'TEST'. Por padrão, o modo 'TEST' está definido, e então invoque:
```bash
python3 validator.py
```
Esse script treina uma rede neural com os dados originais quando definido no modo 'TRAIN', no modo 'TEST', ele 
testa as amostras adversárias salvas em ../outputs/normalized/adversarial1-10/ e ../outputs/normalized/targets1-10/ na
rede treinada com os dados originais.





