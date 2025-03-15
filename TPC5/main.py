import json
import re

FILENAME = "stock.json"

VALORES_MOEDAS = {"2e": 200, "1e": 100, "50c": 50, "20c": 20, "10c": 10, "5c": 5, "2c": 2, "1c": 1}
MOEDAS_ORDENADAS = sorted(VALORES_MOEDAS.items(), key=lambda x: -x[1])

def carregar_stock():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_stock(stock):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4)

def listar_produtos(stock):
    print("maq:\ncod | nome | quantidade | preço")
    print("-" * 40)
    for produto in stock:
        print(f"{produto['cod']} {produto['nome']} {produto['quant']} {produto['preco']}€")

def parse_moedas(entrada):
    padrao_moeda = re.compile(r"^\s*(\d+[ec])\s*$", re.IGNORECASE)
    moedas = entrada.lower().split(",")
    saldo = 0

    for moeda in moedas:
        moeda = moeda.strip()
        match = padrao_moeda.match(moeda)
        if match:
            moeda = match.group(1)
            if moeda in VALORES_MOEDAS:
                saldo += VALORES_MOEDAS[moeda]
            else:
                print(f"maq: Moeda inválida: {moeda}")
        else:
            print(f"maq: Moeda inválida: {moeda}")

    return saldo

def selecionar_produto(stock, saldo, codigo):
    for produto in stock:
        if produto["cod"] == codigo:
            if produto["quant"] > 0:
                preco_em_cents = int(produto["preco"] * 100)
                if saldo >= preco_em_cents:
                    produto["quant"] -= 1
                    saldo -= preco_em_cents
                    print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
                    print(f"maq: Saldo = {saldo}c")
                    return saldo
                else:
                    print("maq: Saldo insuficiente para satisfazer o seu pedido")
                    print(f"maq: Saldo = {saldo}c; Pedido = {preco_em_cents}c")
                    return saldo
            else:
                print("maq: Produto esgotado!")
                return saldo
    print("maq: Código inválido!")
    return saldo

def calcular_troco(saldo):
    troco = []
    for moeda, valor in MOEDAS_ORDENADAS:
        quantidade = saldo // valor
        if quantidade > 0:
            troco.append(f"{quantidade}x {moeda}")
            saldo -= quantidade * valor

    return ", ".join(troco) if troco else None

def main():
    stock = carregar_stock()
    saldo = 0
    print("maq: Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    
    while True:
        comando = input(">> ").strip().upper()

        if comando == "LISTAR":
            listar_produtos(stock)

        elif comando.startswith("MOEDA"):
            moedas = comando[6:].strip()
            saldo += parse_moedas(moedas)
            print(f"maq: Saldo = {saldo}c")

        elif comando.startswith("SELECIONAR"):
            partes = comando.split()
            if len(partes) < 2:
                print("maq: Código do produto não fornecido!")
            else:
                codigo = partes[1]
                saldo = selecionar_produto(stock, saldo, codigo)

        elif comando == "SAIR":
            troco = calcular_troco(saldo)
            if troco:
                print(f"maq: Pode retirar o troco: {troco}.")
            print("maq: Até à próxima!")
            guardar_stock(stock)
            break

        else:
            print("maq: Comando inválido!")

if __name__ == "__main__":
    main()
