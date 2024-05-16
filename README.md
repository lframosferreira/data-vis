# Projeto final de Visualização de Dados

- Caio Teles Cunha
- Deborah Santos Andrade Guimarães
- Diogo Oliveira Neiss
- Igor Lacerda Faria da Silva
- Ivan Vilaça de Assis
- Luís Felipe Ramos Ferreira

## Base de dados

Para realizar o _download_ da base de dados necessária para o projeto, absta executar o comando `bash scripts/get_data.sh` no diretório raiz. O _script_ disponibilizado irá carregar todos os dados do repositório oficial para na pasta `/data/wyscout`.

Os dados relativos aos minutos jogados por cada jogador não estão disponibilizados por meio desse _script_, e devem ser obtidos manualmente na seguinte URL: https://github.com/soccermatics/Soccermatics/tree/main/course/lessons/minutes_played

Para converter os dados carregados para o formato SPADL, basta executar o comando `python3 scripts/convert_to_spadl.py` no diretório raiz. O _script_ irá armazenar os dados no formato correto na pasta `/data/spadl`.

