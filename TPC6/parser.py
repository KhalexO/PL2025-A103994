import ply.yacc as yacc
from lexer import tokens

def p_expr_add_sub(p):
    '''expr : expr PLUS term
            | expr MINUS term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term_mul_div(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    else:
        if p[3] == 0:
            raise ZeroDivisionError("Erro: Divisão por zero")
        p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Erro de sintaxe!")

parser = yacc.yacc()
