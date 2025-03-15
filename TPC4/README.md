## Título

- **TPC4**

## Autor

- **Nome:** Alexandre Arantes Dias  
- **Número:** A103994  

## Resumo  

Esta pasta diz respeito ao TPC4. Neste TPC, foi desenvolvido um analisador léxico para uma linguagem de query que permite escrever frases para consultas estruturadas. O analisador identifica os diferentes componentes das queries e os classifica conforme a sintaxe especificada.

## Lista de resultados

O analisador léxico reconhece os seguintes elementos:
- **Cabeçalhos:** Linhas iniciadas por `#`, `##` ou `###`
- **Consultas à DBPedia:** Queries como `# DBPedia: obras de Chuck Berry`
- **Seleção de variáveis:** Queries com `select ?variável ...`
- **Estruturas da linguagem SPARQL:** `where { ... }` e `LIMIT X`  

Este TPC foi desenvolvido no ficheiro [main.py](main.py) presente na pasta **TPC4**. O programa recebe queries como entrada e identifica os tokens correspondentes de acordo com as regras definidas para a linguagem.