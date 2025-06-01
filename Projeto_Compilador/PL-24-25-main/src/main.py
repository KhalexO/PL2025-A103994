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
	
	test_code = """
program NumeroPrimo;
var
    num, i: integer;
    primo: boolean;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(num);
    primo := true;
    i := 2;
    while (i <= (num div 2)) and primo do
        begin
            if (num mod i) = 0 then
                primo := false;
            i := i + 1;
        end;
    if primo then
        writeln(num, ' é um número primo')
    else
        writeln(num, ' não é um número primo')
end.
	"""	
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