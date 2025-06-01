<img src='uminho.png' width="30%"/>

<h3 align="center">Licenciatura em Engenharia Informática <br> Trabalho prático de Processamento de Linguagens <br> 2024/2025 </h3>

---

# 🪙 Análise Léxica

## Descrição Geral

O objetivo da análise léxica (ou *lexer*) é transformar o código-fonte escrito em Pascal numa sequência linear de **tokens**, onde cada token representa uma unidade lexical significativa da linguagem — como palavras-chave, operadores, identificadores, literais, entre outros.

Esta fase é fundamental para eliminar ambiguidades e preparar o código para a análise sintática (*parser*), fornecendo uma estrutura mais limpa e uniforme.

Neste projeto, utilizou-se a biblioteca `ply.lex`, que fornece ferramentas para definir padrões lexicais através de expressões regulares.

## Estrutura e Funcionamento

Cada token é definido por uma expressão regular que reconhece padrões específicos no texto de entrada. Os tokens são classificados em várias categorias, conforme descrito abaixo.

## Identificadores e Atribuição

Esta categoria inclui os **nomes de variáveis**, funções e procedimentos definidos pelo utilizador, bem como o **operador de atribuição** (`:=`). Estes elementos são essenciais para associar valores a entidades nomeadas e criar estruturas lógicas no programa.

## Palavras-chave do Ambiente Principal

Incluem palavras reservadas como `program`, `var`, `begin` e `end`, que definem a **estrutura global** de um programa Pascal. Estes tokens marcam o início e o fim do programa, a declaração de variáveis e o início de blocos de código

## Fluxo de Controle

Tokens que representam **instruções de controlo de fluxo**, como `if`, `then`, `else`, `for`, `while`, `repeat`, `until`, `downto`, `to`, `do` e `of`. Estes são fundamentais para expressar decisões condicionais, ciclos e ramificações no código.

## Operadores Lógicos e Literais Booleanos

Incluem operadores como `and`, `or`, `not`, e os literais booleanos `true` e `false`. Estes tokens são utilizados para realizar **operações lógicas** e **expressar condições** booleanas.

## Operadores Aritméticos e Inteiros Especiais

Compreendem os operadores `+`, `-`, `*`, `/`, bem como os operadores específicos de divisão inteira `div` e resto `mod`. Permitem a realização de **operações matemáticas** essenciais em expressões e algoritmos.

## Operadores de Comparação

Incluem os tokens `=`, `<>`, `<`, `>`, `<=`, `>=`. Estes são utilizados para **comparar valores**, sendo fundamentais na avaliação de condições, especialmente em instruções de controlo como `if` e `while`.

## Tipos de Dados

Tokens reservados como `integer`, `real`, `char`, `string`, `boolean`, `array`, entre outros (`TINTEGER`, `TREAL`, `TCHAR`, `TSTRING`, `TBOOLEAN`, `TARRAY`) indicam os **tipos de dados** utilizados na declaração de variáveis e estruturas. São essenciais para a **definição semântica** do programa.

## Definições de Subprogramas

Tokens como `procedure` e `function` identificam **declarações de subprogramas**, fundamentais para modularizar o código e implementar funcionalidades reutilizáveis.

## Pontuação

Inclui símbolos de **pontuação e separação**, como:
- `;` (fim de instrução),
- `:` (declaração de tipo),
- `,` (separação de variáveis ou argumentos),
- `.` (fim do programa),
- `..` (intervalos em arrays).

Estes tokens ajudam a **organizar a sintaxe** e a estruturar o programa corretamente.

---

# 📘 Análise Sintática

## Descrição Geral

A análise sintática, ou *parser*, é a fase responsável por verificar se a sequência de tokens gerada pelo *lexer* forma frases válidas segundo a gramática da linguagem Pascal. 

Neste projeto, é utilizado o módulo `ply.yacc` que permite a definição de regras gramaticais em formato BNF (Backus-Naur Form). A estas regras podem ser associadas ações semânticas, como a construção da árvore sintática abstrata (AST).

Cada regra corresponde a uma função Python cuja docstring contém a definição da produção gramatical. O parser utiliza estas definições para construir automaticamente uma tabela de análise (LR ou LALR).

## Estrutura da Gramática e Funções do Parser

### Programa Principal

Define a estrutura de um programa completo em Pascal, composto por:
- um cabeçalho com o nome do programa,
- uma parte global (opcional) com declarações de variáveis e subprogramas,
- um bloco principal com instruções,
- e um ponto final.

### Cabeçalho (Header)

Reconhece a declaração inicial do programa com a palavra-chave `PROGRAM` seguida de um identificador. Serve para nomear o programa e iniciar a sua estrutura.

### Parte Global

Permite a existência de declarações globais antes do bloco principal. Essas declarações podem ser:
- procedimentos
- funções

Pode também estar ausente, sendo representada por uma regra vazia.

### Declarações de Subprogramas

Agrupa declarações de procedimentos e funções que podem ser chamados ao longo do programa.

### Bloco Principal e Declarações Locais

O bloco principal contém duas partes:
- uma secção opcional de declarações de variáveis locais,
- e uma sequência de comandos delimitada por `BEGIN` e `END`.

### Declarações de Variáveis

Permite declarar uma ou mais variáveis com tipos definidos, utilizando a palavra-chave `VAR`.

As declarações seguem o formato:
- lista de identificadores,
- seguida por dois pontos,
- tipo de dado,
- e ponto e vírgula.

### Tipos de Dados

Inclui tipos básicos como `integer`, `real`, `char`, `string` e `boolean`, bem como tipos compostos:

- **Strings de tamanho fixo**, como `string[20]`
- **Arrays indexados**, como `array[1..10] of integer`

Estas declarações definem a estrutura e o espaço de memória que as variáveis ocuparão.

### Parte de Comandos (Statement Part)

Contém a sequência principal de instruções do programa, delimitadas entre `BEGIN` e `END`. As instruções podem ser:
- comandos de atribuição,
- chamadas a procedimentos ou funções,
- estruturas de controlo (condicionais e ciclos),
- ou blocos aninhados.

#### Atribuições

Representam instruções do tipo `<variável> := <expressão>`, onde o resultado da expressão é atribuído a uma variável.

#### Chamadas de Procedimentos/Funções

Permite chamadas diretas a procedimentos ou funções, com ou sem argumentos. O parser distingue entre chamadas simples e chamadas com parâmetros.

#### Expressões

As expressões podem combinar valores e operadores, respeitando a precedência de operadores:
- **AND, OR** (lógicos),
- **DIV, MOD, =, <>, <, >, <=, >=** (relacionais e aritméticos),
- **+ - * /** (aritméticos básicos).

As regras estão divididas em subníveis para garantir que a ordem das operações é respeitada corretamente.

#### Elementos Básicos

Os elementos representam os operandos das expressões e podem ser:
- variáveis simples ou indexadas (arrays),
- literais (inteiros, reais, strings, chars, booleanos),
- expressões entre parênteses,
- chamadas de função (inline),
- ou operações lógicas como `NOT`.

#### Literais

São os valores constantes utilizados nas expressões:
- inteiros (`INTEGER`),
- reais (`REAL`),
- caracteres (`CHAR`),
- strings (`STRING`),
- booleanos (`TRUE`, `FALSE`).

### Declarações de Parâmetros

Permitem definir os parâmetros esperados por funções e procedimentos. Cada parâmetro é composto por:
- identificador,
- tipo,
- e separadores por vírgula para múltiplos parâmetros.

### Regra Vazia (Empty)

Regra utilizada para representar partes opcionais da gramática. Serve para permitir construções como ausência de declarações globais ou locais, ou instruções vazias.

---

# 🌲 AST

## Descrição Geral

A **AST** (*Abstract Syntax Tree*) é uma estrutura fundamental usada para representar a **estrutura lógica** de um programa, de maneira hierárquica e simplificada, com base nas regras gramaticais da linguagem.

## Classe `Node`

A construção da AST é realizada por meio da classe `Node`, que representa cada **nó** da árvore. Cada nó guarda:

- O **tipo** do nó (ex.: `assign`, `procedure`, `function_call`, etc.),
- Uma sequência de **argumentos** filhos (outros nós ou valores literais).

Esta foi preenchida durante a análise sintática.

---

# 🧠 Analisador Semântico

## Descrição Geral

O **Analisador Semântico** é responsável por validar a **consistência lógica** do código-fonte, assegurando que todos os elementos estejam **corretamente declarados, utilizados e compatíveis** entre si quanto a tipos e escopos. 

Enquanto a análise sintática se preocupa com a forma do código, a **análise semântica verifica o significado**: tipos corretos, variáveis declaradas, escopos, funções com parâmetros corretos, etc.

### Principais Componentes

#### `global_scope`

Lista de escopos (tabelas de símbolos) que representa o **ambiente atual de execução**, permitindo controlo de variáveis locais e globais. Vão existir um escopo por função ou procedimento mais um para o bloco principal.

#### `types`

Lista de tipos válidos suportados:  
`['integer', 'real', 'char', 'string', 'boolean', 'array', 'void']`

#### `functions`

Dicionário com as **funções embutidas** (ex.: `write`, `writeln`, `length`), contendo:
- Tipo de retorno,
- Parâmetros esperados.

## Análise Semântica

O método central é:

### `check(node)`

Este método **visita recursivamente os nós da AST** e vai preenchendo as tabelas de símbolos, validando sua semântica. Algumas verificações realizadas:

- **Declarações de variáveis (`var`)**:
  - Verifica tipo e dimensão (ex.: array, escalar).
  - Calcula o tamanho da variável.
  - Adiciona ao escopo com informações de tipo, dimensão e tamanho.

- **Declarações de funções/procedimentos**:
  - Adiciona a função à lista global.
  - Cria novo escopo para parâmetros locais.
  - Valida o corpo da função.

- **Atribuições (`assign`)**:
  - Verifica se a variável foi declarada.
  - Garante que o tipo do valor atribuído é compatível com o da variável.

- **Chamadas de função (`function_call`)**:
  - Confirma existência da função.
  - Valida número e tipo dos argumentos fornecidos.

- **Expressões aritméticas e booleanas (`op`, `and_or`)**:
  - Garante compatibilidade entre operandos.
  - Checa operadores específicos (ex.: `mod` exige inteiros, `/` exige reais).

- **Controle de fluxo (`if`, `while`, `repeat`, `for`)**:
  - Verifica se as condições possuem tipo `boolean`.
  - Valida o corpo dos blocos.

- **Acesso a arrays (`array_access`)**:
  - Confirma que a variável é um array.
  - Garante que o índice seja um inteiro.

---

# 📐 Tabela de Símbolos

## Descrição Geral

Responsável por armazenar informações sobre as variáveis declaradas num escopo específico do programa.

### Atributos principais
A Tabela de Símbolos usada vai guardas os seguintes parametros:
- Tamanho da variavél (em bytes)
- Endereço de memória
- Tipo da variavel
- Dimensão (escalar ou array, por exemplo)
- Nome
- Boundaries, se array (por exemplo, `array[1..5]` tem `bound(1,5)`) 

---