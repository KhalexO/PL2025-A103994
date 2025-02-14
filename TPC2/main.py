import re

file_path = "obras.csv"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.readlines()

clean_lines = []
buffer = ""

for line in content:
    line = line.strip()
    if buffer:
        buffer += " " + line
    else:
        buffer = line
    
    if buffer.count(";") >= 6:
        clean_lines.append(buffer)
        buffer = ""

header = clean_lines[0].split(";")
data_lines = clean_lines[1:]

compositores = set()
obras_por_periodo = {}
titulos_por_periodo = {}

def parse_line(line):
    """Divide uma linha em campos corretamente."""
    fields = re.split(r';(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
    #print(fields[4]) debug
    if len(fields) < 7:
        return None
    return {
        #não sei se é necessário todos os fields
        "nome": fields[0].strip(),
        "descricao": fields[1].strip(),
        "ano": fields[2].strip(),
        "periodo": fields[3].strip(),
        "compositor": fields[4].strip(),
        "duracao": fields[5].strip(),
        "id": fields[6].strip()
    }

obras = [parse_line(line) for line in data_lines if parse_line(line)]

for obra in obras:
    compositores.add(obra["compositor"])
    
    if obra["periodo"] not in obras_por_periodo:
        obras_por_periodo[obra["periodo"]] = 0
    obras_por_periodo[obra["periodo"]] += 1

    if obra["periodo"] not in titulos_por_periodo:
        titulos_por_periodo[obra["periodo"]] = []
    titulos_por_periodo[obra["periodo"].strip()].append(obra["nome"])

compositores_ordenados = sorted(compositores)
for periodo in titulos_por_periodo:
    titulos_por_periodo[periodo].sort()
    
# prints dos resultados. não sei se vou mudar a forma deles.
print("Lista ordenada dos compositores:")
print(compositores_ordenados[:10])

print("\nDistribuição das obras por período:")
for periodo, count in obras_por_periodo.items():
    print(f"{periodo}: {count} obras")

print("\nTítulos das obras por período:")
for periodo, titulos in titulos_por_periodo.items():
    print(f"{periodo}: {titulos[:5]}")
