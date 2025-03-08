import ply.lex as lex

tokens = (
    'SELECT', 'WHERE', 'LIMIT', 'VARIABLE', 'LANG_TAG', 'URI', 'STRING', 'LBRACE', 'RBRACE', 'DOT', 'NUMBER', 'A'
)

t_SELECT = r'SELECT'
t_WHERE = r'WHERE'
t_LIMIT = r'LIMIT'
t_A = r'a'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_NUMBER = r'[0-9]+'

def t_VARIABLE(t):
    r'\?[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_LANG_TAG(t):
    r'@[a-zA-Z]+'
    return t

def t_URI(t):
    r'(dbo|foaf):[a-zA-Z_]+'
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Erro léxico: caractere inesperado '{t.value[0]}' na posição {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

# Exemplo. talvez faço para ler de um ficheiro como nos outros TPCs
query = '''SELECT ?nome ?desc WHERE {\n?s a dbo:MusicalArtist.\n?s foaf:name "Chuck Berry"@en .\n?w dbo:artist ?s.\n?w foaf:name ?nome.\n?w dbo:abstract ?desc\n} LIMIT 1000'''

lexer.input(query)
for tok in lexer:
    print(tok)

