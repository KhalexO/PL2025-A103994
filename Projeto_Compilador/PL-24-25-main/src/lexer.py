import ply.lex as lex

"""
===============================================================================

	Lexer
 
===============================================================================
"""

tokens = (
	# assignment
	'IDENTIFIER',
	'ASSIGNMENT',
	'SEMICOLON',
	'COLON',
	'COMMA',

	# main
	'PROGRAM',
	'DOT',
	'DOTDOT',

	# blocks
	'VAR',
	'BEGIN',
	'END',

	# control flow
	'IF',
	'THEN',
	'ELSE',
	'FOR',
	'WHILE',
	'REPEAT',
	'UNTIL',
	'DOWNTO',
	'TO',
	'DO',
	'OF',

	# logic
	'AND',
	'OR',
	'NOT',
	'FALSE',
	'TRUE',

	# operations
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVISION',
	'DIV',
	'MOD',

	# comparisons
	'EQ',
	'NEQ',
	'LT',
	'GT',
	'LTE',
	'GTE',

	# functions
	'LPAREN',
	'RPAREN',
	'LBRACKET',
	'RBRACKET',
	'PROCEDURE',
	'FUNCTION',

	# types
	'REAL',
	'INTEGER',
	'STRING',
	'CHAR',

	# type names
	'TREAL',
	'TINTEGER',
	'TSTRING',
	'TCHAR',
	'TBOOLEAN',
	'TARRAY'
)

# Regular statement rules for tokens.
t_DOT			= r"\."
t_DOTDOT        = r'\.\.'

t_ASSIGNMENT	= r":="
t_SEMICOLON		= r";"
t_COLON			= r":"
t_COMMA			= r","

t_PLUS			= r"\+"
t_MINUS			= r"\-"
t_TIMES			= r"\*"
t_DIVISION		= r"/"

t_EQ			= r"\="
t_NEQ			= r"\<\>"
t_LT			= r"\<"
t_GT			= r"\>"
t_LTE			= r"\<\="
t_GTE			= r"\>\="

t_LPAREN		= r"\("
t_RPAREN		= r"\)"
t_LBRACKET		= r"\["
t_RBRACKET		= r"\]"

t_REAL			= r"(\-)*[0-9]+\.[0-9]+"
t_INTEGER		= r"(\-)*[0-9]+"

def t_PROGRAM( t ):		r'\bprogram\b'; return t
def t_VAR( t ):			r'\bvar\b'; return t
def t_BEGIN( t ):		r'\bbegin\b'; return t
def t_END( t ):			r'\bend\b'; return t

def t_IF( t ):			r'\bif\b'; return t
def t_THEN( t ):		r'\bthen\b'; return t
def t_ELSE( t ):		r'\belse\b'; return t
def t_FOR( t ):			r'\bfor\b'; return t
def t_WHILE( t ):		r'\bwhile\b'; return t
def t_REPEAT( t ):		r'\brepeat\b'; return t
def t_DOWNTO( t ):		r'\bdownto\b'; return t
def t_TO( t ):			r'\bto\b'; return t
def t_DO( t ):			r'\bdo\b'; return t
def t_UNTIL( t ):		r'\buntil\b'; return t

def t_AND( t ):			r'\band\b'; return t
def t_OR( t ):			r'\bor\b'; return t
def t_NOT( t ):			r'\bnot\b'; return t
def t_OF( t ):			r'\bof\b'; return t
def t_FALSE( t ):		r'\bfalse\b'; return t
def t_TRUE( t ):		r'\btrue\b'; return t

def t_DIV( t ):			r'\bdiv\b'; return t
def t_MOD( t ):			r'\bmod\b'; return t

def t_PROCEDURE( t ):	r'\bprocedure\b'; return t
def t_FUNCTION( t ):	r'\bfunction\b'; return t

def t_TREAL( t ):		r'\breal\b'; return t
def t_TINTEGER( t ):	r'\binteger\b'; return t
def t_TSTRING( t ):		r'\bstring\b'; return t
def t_TCHAR( t ):		r'\bchar\b'; return t
def t_TBOOLEAN( t ):	r'\bboolean\b'; return t
def t_TARRAY( t ):		r'\barray\b'; return t

def t_IDENTIFIER( t ):
	r"[a-zA-Z]([a-zA-Z0-9])*"
	return t

def t_CHAR( t ):
	r"(\'([^\\\'])\')|(\"([^\\\"])\")"
	return t

def t_STRING( t ): 
	r"(\"([^\\\"]|(\\.))*\")|(\'([^\\\']|(\\.))*\')"
	escaped = 0 
	str = t.value[1:-1] 
	new_str = "" 
	for i in range( 0, len( str ) ): 
		c = str[i] 
		if escaped: 
			if c == "n": 
				c = "\n" 
			elif c == "t": 
				c = "\t" 
			new_str += c 
			escaped = 0 
		else: 
			if c == "\\": 
				escaped = 1 
			else: 
				new_str += c 
	t.value = new_str 
	return t

def t_COMMENT( t ):
	r"{[^}]*}"

def t_newline( t ):
	r'\n+'
	t.lexer.lineno += len( t.value )

t_ignore  = ' \t'

def t_error( t ):
	print( "Illegal character '%s'" % t.value[0] )