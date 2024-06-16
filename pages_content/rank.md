Já pensou em simular seu campeonato favorito e acompanhar os resultados, a cada rodada? Para saber como as coisas poderiam ter sido!

Com o ESAK você pode explorar simulações de alguns campeonatos!

#### Funcionamento

Para prever um campeonato, só é necessário ter um método para prever partidas. É claro que modelos podem ser tão complexos quanto se desejar, mas o espírito da coisa é justamente conseguir prever uma partida e reaplicar a lógica para todas as outras.

Maravilha! Como vamos fazer isso? Os dados de cada campeonato são alimentados em um clássico modelo de **Poisson**, que considera somente a diferença de gols entre os times. Para os propósitos de visualização, este modelo funciona como mágica! No entanto, é importante destacar que ele possui uma limitação severa: ele tende a exagerar extremos! Ou seja, times _bons_ são considerados _muito bons_ e times _ruins_ são considerados _muito ruins_. Você vai poder explorar isso na visualização!

#### _Pipeline_ de dados

Os _scripts_ para se gerar os dados estão, convenientemente, na pasta `scripts`. O modelo de **Poisson** é criado e cada partida é simulada. Depois, os dados são agregados em tabelas no clássico formato de campeonatos, com quantidade de jogos, número de vitórias e derrotas, informações sobre a quantidade de gols e afins. Essa simulação é feita para toda quantidade de partidas no campeonato e, depois, agregada novamente. Ou seja, no final dessa etapa, o arquivo resultante tem as colunas descritas anteriormente, mas cada time aparece $2(n - 1)$ vezes, para cada rodada. O arquivo que lida com isso é o `gen_bump_plot_data.py`.

Pra finalizar o processo, basta converter os dados num formato mais próximo do _ranking_ esperado em _bump chart_. Isso não é muito complicado e felizmente a biblioteca `pandas` provê um método para facilitar a conversão. Essa procedimento é executado pelo arquivo `gen_rank_bump_plot.py`.

#### Instruções

Selecione a liga (e o intervalo, no fim da página) que desejar. O gráfico é super interativo! Ele parece meio confuso a princípio, mas você pode, por exemplo, visualizar os dados só de um time, encontrando ele na legenda e dando um clique duplo. Você também pode esconder e mostrar times dando um clique simples na legenda.

O nome das ligas está abreviado. Por exemplo, a Série A está representada como "BRA1".
