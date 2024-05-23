# Projeto final de Visualização de Dados

- Caio Teles Cunha
- Deborah Santos Andrade Guimarães
- Diogo Oliveira Neiss
- Igor Lacerda Faria da Silva
- Ivan Vilaça de Assis
- Luís Felipe Ramos Ferreira

## Dependências

Todas as dependências necessárias para executar o projeto estão disponíveis no arquivo _environment.yaml_. Utilizamos o _Anaconda3_ para a organização do projeto, mas qualquer gerenciador de pacotes e ambientes em _Python_ pode ser utilizado.

## Base de dados

### Dados de eventos

Para realizar o _download_ da base de dados necessária para o projeto, basta executar o comando `bash scripts/get_event_data.sh` no diretório raiz. O _script_ disponibilizado irá carregar todos os dados do repositório oficial para na pasta `/data/wyscout`.

Para converter os dados carregados para o formato SPADL, basta executar o comando `python3 scripts/convert_to_spadl.py` no diretório raiz. O _script_ irá armazenar os dados no formato correto na pasta `/data/spadl`.

### Dados de Elo

Para realizar o _download_ dos dados de Elo, basta executar o comando `python3 scripts/get_elo_data.py` no diretório raiz, e os dados salvos no diretório `data/elo`. Para obter esses dados, utilizamos a API pública disponibilizada pelo [ClubElo](http://clubelo.com/).
