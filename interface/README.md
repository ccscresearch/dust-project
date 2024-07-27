![DUST Logo](https://github.com/ccscresearch/dust-project/blob/main/img/dust_logo.png)
## Documentação de Requisitos para Interface Gráfica do Sistema DUST

## 1. Visão Geral

A conjunção das soluções propostas ao longo do projeto originaram a plataforma chamada DUST. O objetivo da plataforma é ser uma alternativa para reforçar a garantia da privacidade dos dados de usuários de dispositivos da IoT.

## 2. Requisitos do Sistema

Para garantir o funcionamento adequado do Dust, certifique-se de que o seu sistema atenda aos seguintes requisitos:

### 2.1. Hardware

- *Memória RAM:* 8GB
- *Espaço em Disco:* 60GB livres
- *Conectividade:* Conexão estável à Internet
- *CPU*: 2 Core

### 2.2. Software

#### 2.2.1. Servidor

- *Sistema Operacional:* Linux (Ubuntu 20.04 ou superior recomendado)
- *Servidor Web:* Nginx
- *Node.js:* Versão 21.6.2
- *npm:* Versão 10.8.2
- *Yarn:* Versão 1.22.21
- *Python:* Versão 3.8
- *Bibliotecas Python:*
    - Pandas
    - Scikit-learn
    - Scipy
    - Pytorch
    - Cleverhans
    - Adversarial Robustness Toolbox (https://github.com/Trusted-AI/adversarial-robustness-toolbox)

#### 2.2.2. Frontend

- *Navegador Web:* Google Chrome ou Mozilla Firefox (últimas versões)
- *Framework:* React com TypeScript
- *Ferramentas de Desenvolvimento:*
    - Vite (bundling e HMR)
    - ESLint (linting)
    - Prettier (formatação de código)
- *Dependências Principais:*
    - Material-UI (componentes de interface)
    - React Router (navegação)

### 2.3. Portas

Certifique-se de que as seguintes portas estejam abertas no Firewall para comunicação:

- *5173:* Acesso à interface web do Dust.
- *3001:*  Comunicação com a API do Dust.

## 3. Instalação

### 3.1. Ambiente de Desenvolvimento

Siga os passos abaixo para configurar o ambiente de desenvolvimento do Dust:

#### 3.1.1. Node.js e Yarn

1. *Instalação do Node Version Manager (nvm):*

   bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
   

2. *Instalação do Node.js:*

   bash
   nvm install 21
   

3. *Verificação da versão do Node.js:*

   bash
   node -v
   

   A saída deve indicar a versão 21.x.x do Node.js.

4. *Verificação da versão do npm:*

   bash
   npm -v
   

   A saída deve indicar a versão 10.8.x do npm.

5. *Instalação do Yarn:*

   bash
   npm install --global yarn
   

6. *Verificação da versão do Yarn:*

   bash
   yarn --version
   

#### 3.1.2 Backend (API)

1. *Clonar o repositório:*

   bash
    https://github.com/ccscresearch/dust-project/tree/main/portal/api
    

2. *Navegar até o diretório do projeto:*

   bash
   cd dust-project/portal/api
   

3. *Instalar as dependências:*

   bash
   npm install
   

4. *Iniciar a API:*

   bash
   npm start
   

#### 3.1.3 Frontend

1. *Clonar o repositório (caso ainda não tenha clonado):*

   bash
   https://github.com/ccscresearch/dust-project/tree/main/portal/frontend
   

2. *Navegar até o diretório do Frontend:*

   bash
   cd dust-project/portal/frontend
   

3. *Instalar as dependências:*

   bash
   npm install
   

4. *Iniciar o servidor de desenvolvimento:*

   bash
   npm run dev --host
   
   O comando --host permite que o servidor seja acessado por outros dispositivos na rede local.

5. *Acessar a interface web:*

   Abra o navegador e acesse http://localhost:5173/.

## 4. Funcionalidades

### 4.1. Autenticação

O Dust utiliza a autenticação federada do Google para garantir a segurança da plataforma. Os usuários podem se autenticar e se cadastrar utilizando suas contas do Google.

### 4.2. Submissão de Capturas de Tráfego

- Os administradores de rede podem submeter arquivos de captura de tráfego no formato PCAP através da interface gráfica.
- O tamanho máximo permitido para cada arquivo é de 1 Gigabyte.

### 4.3. Análise de Tráfego

- O Dust utiliza algoritmos de aprendizado de máquina para analisar os arquivos PCAP submetidos e identificar potenciais ataques de varredura de porta.


### 4.4. Visualização de Resultados

A interface do Dust apresenta os resultados das análises de forma clara e intuitiva, por meio de gráficos e tabelas interativas, organizados em três guias principais:

*1. Base de Dados:*

- *Distribuição dos Dados:* Visualização gráfica da distribuição dos dados em relação às classes (ataque ou tráfego normal), permitindo identificar o balanceamento do conjunto de dados.
- *Matriz de Confusão:* Avaliação da performance do modelo de aprendizado de máquina, mostrando a relação entre os rótulos reais e as previsões do modelo. A precisão geral, baseada nos dados reais, também é exibida.

*2. Amostras Adversariais:*

- *Distribuição de Dados:* Visualização gráfica da distribuição dos dados que foram modificados para induzir erros na classificação do modelo, simulando ataques sofisticados.
- *Comparativo de Performance:* Comparação da performance do modelo em relação aos dados reais e às amostras adversariais, avaliando a robustez do modelo contra ataques.

*3. Modelo de Defesa:*

- *Classificação Final:* Exibição da classificação final dos dados, indicando a probabilidade de um ataque de varredura de porta estar presente.
- *Visualização da Classificação:* Gráfico intuitivo que destaca os dados classificados como ataque e tráfego normal, permitindo uma rápida identificação de potenciais ameaças.
