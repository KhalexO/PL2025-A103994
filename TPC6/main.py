from parser import parser

while True:
    try:
        expr = input("Digite uma expressão: ")
        if not expr:
            continue
        result = parser.parse(expr)
        print(f"Resultado: {result}")
    except Exception as e:
        print(f"Erro: {e}")
