import ply.lex as lex
import ply.yacc as yacc

from lexer import *
from parser import *
from SemanticAnalyser import *
from ILGenerator import *
from CodeGenerator import *

"""
===============================================================================

	Main

===============================================================================
"""

if __name__ == "__main__":
	
	source_path = sys.argv[1]

	try:
		with open(source_path, 'r', encoding='utf-8') as f:
			test_code = f.read()
	except Exception as e:
		print(f"Failed to read source file: {e}")
		sys.exit(1)
		
        
	# lexer
	lexer = lex.lex()
	lexer.input( test_code )
 
	# parser
	parser = yacc.yacc()
	ast = parser.parse( test_code )
 
	# semantic analyser
	semantic_analyser = SemanticAnalyser()
	try:
		semantic_analyser.check( ast )
	except Exception as e:
		print( "Error: %s" % e )
		sys.exit()

	# Intermediate Language generation
	try:
		ilgen = ILGenerator(semantic_analyser.global_scope)
		ilgen.generate(ast)
		il = ilgen.instructions
		print(str(il))
	except Exception as e:
		print("Error: %s" % e)
		sys.exit()

    # VM Assembly generation
    # global_scope[0] holds the global symbol table
	try:
		cg = CodeGenerator()
		asm = cg.translate(il, semantic_analyser.global_scope)
		print("VM Assembly:")
		for line in asm:
			print(line)
	except Exception as e:
		print("Error: %s" % e)
		sys.exit()