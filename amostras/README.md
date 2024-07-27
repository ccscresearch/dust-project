![DUST Logo](https://github.com/ccscresearch/dust-project/blob/main/img/dust_logo.png)

## Descrição etapa de gerar as amostras adversárias

Esta solução envolve mecanismos que exploram abordagens adversárias para reduzir o desempenho de redes neurais que tentam identificar ataques de varredura de porta. Antes desse passo, também houve a replicação de abordagens adversariais exploradas previamente na literatura.


### Instalação

1. Instalação de dependências: pip3 install -r requirements.txt 

### Estrutura
Para prosseguir, faça o download da estrutura completa de pastas do sistema e cole o diretório src dentro dela, a estrutura arquivos das bases de dados utilizadas, as amostras adversárias geradas, e todos os resultados obtidos durante a pesquisa.

Faça o download nesse link: https://drive.google.com/file/d/1ZULCwrpTP0MvaZVUZCG_tzS_AqjdRcUA/view?usp=sharing

Uma vez que tenha feito o download, copie a pasta src para dentro da estrutura.

Segue a descrição das pastas
- 📂 resultados/: Pasta que contém os resultados dos experimentos de modo  facilitado

- 📂 src/: Pasta que contém o código fonte dos experimentos, da versão final utilizando a biblioteca Adversarial Robustness Toolbox.

- 📂 srcCW2/: Pasta que contém o código fonte dos experimentos, da versão abandonada devido a problemas com a biblioteca Pytorch-CW2.

Na estrutura completa, existem também os diretórios:
- 📂 data/: Bases de dados utilizadas

- 📂 inputs/: Registros de pré-processamento das bases

- 📂 outputs/: Diretório onde os scritps armazenam as saídas, isso inclui as redes treinadas,  acurácias com dados originais, amostras adversárias e acurácias das amostras adversárias.

- 📂 savedModels/: Redes neurais temporárias salvas

### Guia de execução
Após ter baixado a estrutura de pastas completa, e colado o diretório src dentro dela, siga as instruções no diretório src para prosseguir.


