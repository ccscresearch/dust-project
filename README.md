![DUST Logo](https://github.com/ccscresearch/dust-project/blob/main/img/dust_logo.png)

# Projeto DUST

**Identificação e Ofuscação de Vulnerabilidades de Segurança e de Comportamentos na IoT**

## Dados do Projeto

**Instituições Participantes do projeto:**
 - Universidade Federal de Minas Gerais (UFMG)
 - Universidade Federal de Santa Maria (UFSM)
 - Universidade Federal do Paraná (UFPR)

**Número do Processo FAPESP:**
 - 2021/06733-6

## Resumo

Este projeto atua na prevenção de vazamentos de informações na transmissão de mensagens de redes. A privacidade dos dados é cada vez mais necessária diante do advento da IoT, que gera mais dados sensíveis, e da implantação da Lei Geral de Proteção dos Dados (LGPD). Na academia, investigam-se com afinco os ataques side-channel, os quais apenas observando o tráfego de rede e por meio de métodos estatísticos e de Inteligência Artificial inferem padrões e comportamentos reveladores de informações sensíveis para os usuários, comprometendo sua privacidade. Assim, este projeto busca modelar o vazamento de informação na IoT e propor soluções efetivas para: (i) a identificação automatizada de vulnerabilidades de segurança associadas à privacidade dos dados e (ii) a ofuscação das vulnerabilidades identificadas.

## Descrição deste repositório

Este repositório está organizado em uma estrutura de diretórios onde cada um representa uma linha de ações do projeto. A descrição dos diretórios é como segue:

 - [Amostras](https://github.com/ccscresearch/dust-project/tree/main/amostras) - Arquivos relacionados ao modelo de geração de amostras adversariais
 - [Apresentações](https://github.com/ccscresearch/dust-project/tree/main/apresentacoes) - Apresentações realizadas por membros do projeto
 - [Detecção](https://github.com/ccscresearch/dust-project/tree/main/detec%C3%A7%C3%A3o "detecção") - Arquivos relacionados ao modelo de detecção de comportamentos
 - [Portal](https://github.com/ccscresearch/dust-project/tree/main/interface) - Arquivos relacionados à interface gráfica de gerenciamento e exibição de resultados

## Resultados

Resultado proveniente da primeira linha de pesquisa que investigou a possibilidade de detectar um comportamento específico baseado em características encontradas no tráfego de uma rede de computadores. O modelo de detecção proposto foi configurado para identificar um ataque de varredura de dados a partir de uma captura de tráfego de rede. Embora o comportamento detectado neste caso especificamente é relacionado a um ataque, é possível criar perfis de comportamento para dispositivos e ameaças. O modelo é capaz de identificar o ataque em questão com alta acurácia.
<img src="https://github.com/ccscresearch/dust-project/blob/main/img/matrixConfusion.png" alt="drawing" width="450"/>

O próximo resultado está relacionado à capacidade de um modelo de aprendizagem de máquina adversarial (modelo que gera amostras adversariais a partir do tráfego real), em induzir ao erro um segundo modelo que tenha alta acurácia na classificação de dados. Neste cenário específico, utilizou-se um conjunto de dados composto por diversas classes que representam tipos de tráfego de rede. O modelo originalmente tem a capacidade de classificar corretamente as classes com uma acurácia de aproximadamente 99%. A figura abaixo ilustra o resultado da classificação após a geração e inserção das amostras adversariais geradas pelo modelo adversarial. 
<img src="https://github.com/ccscresearch/dust-project/blob/main/img/confMat20.png" alt="drawing" width="450"/>

Os próximos resultados estão relacionados ao modelo desenvolvido dentro do escopo do projeto. O modelo é capaz de ofuscar um comportamento previamente modelado ao inserir amostras adversariais no conjunto de dados que representa o tráfego de uma rede. Na primeira imagem as amostras são geradas a partir da técnica Carlini&Wagner (CW2) e na segunda imagem a partir da técnica Fast Gradient Sign Method (FGSM). Em ambos os casos as técnicas empregadas no modelo de aprendizagem de máquina adversário são capazes de reduzir a identificação de um comportamento de aproximadamente 99% para cerca de 23,9% no caso da técnica CW2 e cerca de 58% para técnica FGSM.
<img src="https://github.com/ccscresearch/dust-project/blob/main/img/confMatCarlini3.png" alt="drawing" width="450"/>
<img src="https://github.com/ccscresearch/dust-project/blob/main/img/confMatFGSM3.png" 
alt="drawing" width="450"/>

Finalmente, a união das linhas de pesquisa considerando a detecção de um comportamento identificado em no tráfego de rede a partir de características específicas (tamanho do pacote, direção do pacote, informações temporais, etc) e a ofuscação desse comportamento pode ser observada no resultado final. Na figura abaixo nota-se que o mesmo modelo que tinha a capacidade de reconhecer ataques com cerca de 99% de acurácia consegue aproximadamente 86% de acurácia com as amostras adversariais. A queda bruta na capacidade de reconhecimento do ataque é cerca de 13%, mas uma observação importante é que todas as amostras apresentadas no último teste são adversariais, ou seja, não existem informações provenientes de um conjunto de dados real. 
<img src="https://github.com/ccscresearch/dust-project/blob/main/img/matrixConfusionAdv.png" 
alt="drawing" width="450"/>

## Membros do projeto
**Equipe de pesquisa**
 - Aldri Luiz dos Santos  UFMG
 - Michele Nogueira Lima  UFMG
 - Aurora Pozo  UFPR
 - Ricardo T. Macedo  UFSM

**Corpo técnico**
 - Fernando Nakayama - Bolsista TT4A
 - Uelinton Brzolin - Bolsista TT4
 - Thiago Nakao - Bolsista TT4

**Voluntários** 
 - Ana Luiza Macêdo
 - Guilherme Guerra
 - João Vitor Ferreira
