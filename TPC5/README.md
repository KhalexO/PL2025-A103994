## Título

- **TPC5**

## Autor

- **Nome:** Alexandre Arantes Dias  
- **Número:** A103994  

## Resumo  

Esta pasta diz respeito ao TPC5. Neste TPC foi desenvolvida uma máquina de vendas em Python que permite a um utilizador listar produtos, inserir moedas, selecionar produtos e obter troco. O programa lê e atualiza um ficheiro `stock.json`, garantindo que os produtos e os pagamentos são geridos corretamente. Além disso, o sistema devolve o troco da maneira mais eficiente possível.

## Lista de resultados  

Este TPC foi desenvolvido no ficheiro [main.py](main.py) presente na pasta **TPC5**. O sistema lê a informação inicial do ficheiro `stock.json` e interage com o utilizador através de comandos como:

- `LISTAR` → Exibe os produtos disponíveis
- `MOEDA X` → Insere moedas na máquina
- `SELECIONAR CÓDIGO` → Seleciona um produto pelo código
- `SAIR` → Devolve o troco e termina o programa

O troco é calculado automaticamente, devolvendo sempre as moedas de maior valor primeiro.

