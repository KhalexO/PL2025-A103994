import ply.yacc as yacc
from lexer import tokens
from utils.AST import Node
import sys

"""
===============================================================================

	Parser

===============================================================================
"""

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVISION'),
	('left', 'DIV', 'MOD'),
	('left', 'EQ', 'NEQ', 'LTE','LT','GT','GTE'),
	('left', 'OR', 'AND'),
)

def p_program_start( t ):
	"program : header SEMICOLON global_part block DOT"
	t[0] = Node( 'program', t[1], t[3], t[4] )

def p_header( t ):
	"""header : PROGRAM identifier"""
	t[0] = t[2]

# declarations of functions or procedures or vars
def p_global_part( t ):
	"""global_part : sub_declaration_list
					| empty """
	t[0] = t[1]  # List of declarations
        
def p_empty( t ):
	'empty :'
	t[0] = []

def p_sub_declaration_list( t ):
    """sub_declaration_list : sub_declaration SEMICOLON sub_declaration_list
                            | sub_declaration SEMICOLON"""
    if len( t ) == 3:
        t[0] = Node( 'sub_declaration_list', t[1] )
    else:
        t[0] = Node( 'sub_declaration_list', t[1], t[3] )

# normal variables declaration
def p_variable_declaration_part( t ):
	"""variable_declaration_part : VAR variable_declaration_list"""
	t[0] = t[2]

def p_variable_declaration_list( t ):
	"""variable_declaration_list : variable_declaration variable_declaration_list
								| variable_declaration"""
	if len( t ) == 2:
		t[0] = Node( 'variable_declaration_list', t[1] )
	else:
		t[0] = Node( 'variable_declaration_list', t[1], t[2] )

# variable  
def p_variable_declaration( t ):
	"""variable_declaration : identifier_list COLON type SEMICOLON"""
	t[0] =  Node( 'var', t[1], t[3] )

# names of variables
def p_identifier_list( t ):
	"""identifier_list : identifier COMMA identifier_list
					| identifier"""
	if len( t ) == 2:
		t[0] = Node( 'identifier_list', t[1] )
	else:
		t[0] = Node( 'identifier_list', t[1], t[3] )

def p_identifier( t ):
	"""identifier : IDENTIFIER"""
	t[0] = Node( 'identifier', str( t[1] ).lower() )

def p_sub_declaration( t ):
    """sub_declaration : procedure_declaration
                       | function_declaration"""
    t[0] = t[1]
		
# procedure
def p_procedure_declaration( t ):
	"""procedure_declaration : procedure_heading SEMICOLON block"""
	t[0] = Node( "procedure", t[1], t[3] )		
		
def p_procedure_heading( t ):
	"""procedure_heading : PROCEDURE identifier 
						| PROCEDURE identifier LPAREN RPAREN
						| PROCEDURE identifier LPAREN parameter_list RPAREN"""
	if len( t ) == 3:
		t[0] = Node( "procedure_head", t[2] )
	elif len( t ) == 5:
		t[0] = Node( "procedure_head", t[2] )
	else:
		t[0] = Node( "procedure_head", t[2], t[4] )	
		
def p_function_declaration( t ):
	"""function_declaration : function_heading SEMICOLON block"""
	t[0] =  Node( 'function', t[1], t[3] )
	
def p_function_heading( t ):
	""" function_heading : FUNCTION type
						| FUNCTION identifier LPAREN RPAREN COLON type
						| FUNCTION identifier COLON type
						| FUNCTION identifier LPAREN parameter_list RPAREN COLON type"""
	if len( t ) == 3:
		t[0] = Node( "function_head",t[2] )
	elif len( t ) == 5:
		t[0] = Node( "function_head", t[2], t[4] )
	elif len( t ) == 7:
		t[0] = Node( "function_head", t[2], t[6] )
	else:
		t[0] = Node( "function_head", t[2], t[4], t[7] )

def p_block( t ):
	"""block : optional_vardec statement_part"""
	t[0] = Node( 'block', t[1], t[2] )

def p_optional_vardec( t ):
	"""optional_vardec : variable_declaration_part
					| empty"""
	t[0] = t[1]

def p_parameter_list( t ):
	"""parameter_list : parameter COMMA parameter_list
					| parameter"""
	if len( t ) == 4:
		t[0] = Node( "parameter_list", t[1], t[3] )
	else:
		t[0] = t[1]
		
def p_parameter( t ):
	"""parameter : identifier COLON type"""
	t[0] = Node( "parameter", t[1], t[3] )

def p_type( t ):
	""" type : TREAL 
			| TINTEGER
			| TCHAR
			| TSTRING
			| TBOOLEAN
			| TSTRING LBRACKET integer RBRACKET
			| TARRAY LBRACKET integer DOTDOT integer RBRACKET OF type"""
	if len( t ) == 2:
		t[0] = Node( 'type', t[1].lower() )
	elif len( t ) == 5:
		t[0] = Node( 'array_type', t[3] )
	else:
		t[0] = Node( 'array_type', t[3], t[5], t[8] )
	
def p_statement_part( t ):
	"""statement_part : BEGIN statement_sequence END"""
	t[0] = t[2]
	
def p_statement_sequence( t ):
	"""statement_sequence : statement SEMICOLON statement_sequence
						| statement"""
	if len( t ) == 2:
		t[0] = t[1]
	else:
		t[0] = Node( 'statement_list', t[1], t[3] )
	
def p_statement( t ):
	"""statement : assignment_statement
				| statement_part
				| if_statement
				| while_statement
				| repeat_statement
				| for_statement
				| procedure_or_function_call
				| empty
	"""
	t[0] = t[1]	
	
def p_procedure_or_function_call( p ):
	'''procedure_or_function_call : identifier
								| identifier LPAREN param_list RPAREN'''
	if len( p ) == 2:
		p[0] = Node( "var", p[1] )
	else:
		p[0] = Node( "function_call", p[1], p[3] )

def p_param_list( t ):
	"""param_list : param_list COMMA param
				| param"""
	if len( t ) == 2:
		t[0] = t[1]
	else:
		t[0] = Node( "parameter_list", t[1], t[3] )

def p_param( t ):
	"""param : expression """
	t[0] = Node( "parameter", t[1] )
	
def p_if_statement( t ):
	"""if_statement : IF expression THEN statement ELSE statement
					| IF expression THEN statement
	"""
	if len( t ) == 5:
		t[0] = Node( 'if', t[2], t[4] )
	else:
		t[0] = Node( 'if', t[2], t[4], t[6] )
	
def p_while_statement( t ):
	"""while_statement : WHILE expression DO statement"""
	t[0] = Node( 'while', t[2], t[4] )
	
	
def p_repeat_statement( t ):
	"""repeat_statement : REPEAT statement UNTIL expression"""
	t[0] = Node( 'repeat', t[2], t[4] )
	
def p_for_statement( t ):
	"""for_statement : FOR assignment_statement TO expression DO statement
					| FOR assignment_statement DOWNTO expression DO statement
	"""
	t[0] = Node( 'for', t[2], t[3], t[4], t[6] )
	
def p_assignment_statement( t ):
	"""assignment_statement : identifier ASSIGNMENT expression"""
	t[0] = Node( 'assign', t[1], t[3] )
	
def p_expression( t ):
	"""expression : expression and_or expression_m
				| expression_m
	"""
	if len( t ) == 2:
		t[0] = t[1]
	else:
		t[0] = Node( 'op', t[2], t[1], t[3] )

def p_expression_m( t ):
	"""expression_m : expression_s
					| expression_m sign expression_s"""
	if len( t ) == 2:
		t[0] = t[1]
	else:
		t[0] = Node( 'op', t[2], t[1], t[3] )
	
def p_expression_s( t ):
	"""expression_s : element 
					| expression_s psign element"""
	if len( t ) == 2:
		t[0] = t[1]
	else:
		t[0] = Node( 'op', t[2], t[1], t[3] )

def p_and_or( t ):
	"""and_or : AND
			| OR"""
	t[0] = Node( 'and_or', t[1] )

def p_psign( t ):
	"""psign : TIMES
			| DIVISION"""
	t[0] = Node( 'sign', t[1] )

def p_sign( t ):
	"""sign : PLUS
			| MINUS
			| DIV
			| MOD
			| EQ
			| NEQ
			| LT
			| LTE
			| GT
			| GTE
	"""
	t[0] = Node( 'sign', t[1] )

def p_element( t ):
	"""element : identifier
			| identifier LBRACKET expression RBRACKET
			| real
			| integer
			| string
			| char
			| boolean
			| LPAREN expression RPAREN
			| NOT element
			| function_call_inline
	"""
	if len( t ) == 2:
		t[0] = Node( "element", t[1] )
	elif len( t ) == 5:
		t[0] = Node( "array_access", t[1], t[3] )  # Accessing an array element
	elif len( t ) == 3:
		t[0] = Node( 'not', t[2] )
	else:
		t[0] = Node( 'element', t[2] )
		
def p_function_call_inline( t ):
	"""function_call_inline : identifier LPAREN param_list RPAREN
						| identifier LPAREN RPAREN"""
	if len( t ) == 5:
		t[0] = Node( 'function_call_inline', t[1], t[3] )
	else:
		t[0] = Node( 'function_call_inline', t[1] )
	
def p_real( t ):
	"""real : REAL"""
	t[0] = Node( 'real', t[1] )
	
def p_integer( t ):
	"""integer : INTEGER"""
	t[0] = Node( 'integer', t[1] )

def p_string( t ):
	"""string : STRING"""
	t[0] = Node( 'string', t[1] )

def p_char( t ):
	"""char : CHAR"""
	t[0] = Node( 'char',t[1] )
 
def p_boolean( t ):
	"""boolean : TRUE
			   | FALSE"""
	t[0] = Node( 'boolean', t[1] )

# def p_comment( t ):
#     """comment : COMMENT"""
#     pass

def p_error( t ):
	print( "Syntax error in input, in line %d!" % t.lineno )
	sys.exit()