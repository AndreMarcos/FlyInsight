# FlyInsight

Aplicação desenvolvida com o objetivo de realizar agregação de informações importantes da aviação de forma a facilitar a análise por parte dos usuários com a permissão de criação de relatórios ad-hoc que atendem diferentes necessiades.
A API escolhida foi a Redemet, com sua documentação  presente no seguinte endereço:  https://ajuda.decea.mil.br/base-de-conhecimento/api-redemet-o-que-e/, pois a mesma ofereçe amplamente dados de aerodromos e dados meteorológicos fundamentais para diversas aplicações na aviação. Através desta API é possível acessar informações detalhadas sobre aeródromos, status operacional, condições meteorológicas e dados de radar, além de relatórios METAR, TAF e SIGMET. Esses dados são essenciais para profissionais que necessitam tomar decisões informadas e garantir a segurança e eficiência de suas operações.

Site da Redemet: https://www.redemet.aer.mil.br/

O público-alvo para aplicação que será desenvolvida utilizando a API Redemet inclui profissionais e entusiastas da aviação, sendo pilotos amadores, em setores de logística e agricultura, um dos principais grupos, pois necessitam de informações precisas para planejar e ajustar seus voos. A motivação para o desenvolvimento da aplicação com o foco em dados de importantes da aviação vêm da aplicação de acessibilidade, pois a aplicação agregará dados de diferentes fontes (METAR, TAF e etc) em uma única plataforma, facilitando a análise por parte dos usuários e permitindo a criação de relatórios ad-hoc que atendem às necessidades específicas de diferentes usuários.  Além disso, a inovação com a utilização de api’s como a Redemet promove a inovação no setor de aviação amadora, proporcionando melhores ferramentas para pilotos e operações amadoras.

Para desenvolver um projeto de geração de relatórios personalizados usando a API da REDEMET, é importante identificar os endpoints relevantes que fornecem dados meteorológicos detalhados. Aqui estão os principais produtos disponíveis e como podem ser utilizados no projeto:

## Endpoints Relevantes da API REDEMET

- Aeródromos
    - Endpoint: /aerodromos
    - Descriçao: API destina à retornar informações de Aeródromos de países disponíveis no banco de dados da REDEMET.
- Aeródromos Status
    - Endpoint: /aerodromos/status
    - Descrição: Fornece o status dos aeródromos, como informações sobre operações e condições atuais.
- Aeródromos Info
    - Endpoint: /aerodromos/info
    - Descrição: Retorna informações das condições meteorológicas de uma localidade disponível no banco de dados da REDEMET.
- Produtos RADAR
    - Endpoint: /produtos/radar
    - Descrição: Fornece dados de radar meteorológico, incluindo imagens de precipitação e tempestades.
- Mensagem METAR
    - Endpoint: 
    - Descrição: Fornece relatórios meteorológicos de aviação que contêm informações sobre as condições meteorológicas em um aeródromo específico.
- Mensagem TAF
    - Endpoint: /mensagem/taf
    - Descrição: Fornece previsões meteorológicas para aeródromos, incluindo condições previstas para um período de até 30 horas.


## Tecnologias Utilizadas
- Python 3.8
- PostgreSQL

## Instalação

```bash
git clone https://github.com/AndreMarcos/FlyInsight.git
cd FlyInsight
```

Instale as dependências necessárias
```bash
cd "ELT - Database"
pip install -r requirements.txt
```

Para executar a criação do banco é necessário adicionar as informações necessárias no arquivo '.env'

```bash
DATABASE_URL=
API_BASE_URL=https://api-redemet.decea.mil.br
API_KEY=
```

Para executar a criação do banco é necessário executar o script 'models_data.py'
```bash
python  '.\ELT - Database\models\models_data.py'
```
