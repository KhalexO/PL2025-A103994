from utils.Any import *
from utils.SymbolTable import *
from utils.AST import *

"""
===============================================================================

	Semantic Analyser
 
===============================================================================
"""
class SemanticAnalyser:
	def __init__( self ):
		self.global_scope = []
		self.types = ['integer', 'real', 'char', 'string', 'boolean', 'array', 'void']
		self.functions = {
			'write' 		: ('void', [( "arg", Any() )]),
			'writeln'		: ('void', [( "arg", Any() )]),
			'writeint'		: ('void', [( "arg", 'integer' )]),
			'writereal'		: ('void', [( "arg", 'real' )]),
			'writelnint'	: ('void', [( "arg", 'integer' )]),
			'writelnreal'	: ('void', [( "arg", 'real' )]),
			'readln'		: ('string', [( "arg", Any() )]),
			'length'		: ( 'integer', [( "arg", Any() )] )
		}
	
	def get_size( self, type ):
		if type == 'real':
			size = 8
		elif type == 'integer':
			size = 4
		elif type == 'char':
			size = 1
		elif type == 'boolean':
			size = 1
		else: # string
			size = 255
		return size

	def pop_scope( self ):
		index = next( ( i for i, obj in enumerate( self.global_scope ) if obj.var_count == {} and obj.name == "main" ), None )
		if index is not None:
			self.global_scope.pop( index )
			
	# warning for variables not used
	def unused( self ):
		count = self.global_scope[-1].var_count
		for i in count:
			if count[i] == 0:
				print( "Warning: variable %s was declared, but not used." % i )

	def check_if_function( self, var ):
		if var.lower() in self.functions and not self.is_function_name( var.lower() ):
			raise Exception( "A function called %s already exists" % var )

	def is_function_name( self, var ):
		for symbol_table in self.global_scope[::-1]:
			if symbol_table.name == var:
				return True
		return False
			
	def has_var( self, varn ):
		var = varn.lower()
		self.check_if_function( var )
		for symbol_table in self.global_scope[::-1]:
			if symbol_table.has_var( var ):
				return True
		return False

	def get_var( self, varn ):
		var = varn.lower()
		for symbol_table in self.global_scope[::-1]:
			if symbol_table.has_var( var ):
				symbol_table.var_count[var] += 1
				return symbol_table.get_var( var )
		raise Exception( "Variable %s is referenced before assignment" % var )
		
	def set_var( self, varn, var_info ):
		var = varn.lower()
		self.check_if_function( var )
		now = self.global_scope[-1]
		if now.has_var( var ):
			raise Exception( "Variable %s already defined" % var )
		else:
			now.set_var( var, var_info )
			now.var_count[var] += 1
		
	def get_params( self, node ):
		if node.type == "parameter":
			return [self.check( node.args[0] )]
		else:
			list = []
			for i in node.args:
				list.extend( self.get_params( i ) )
			return list
			
	def flatten( self, node ):
		if not self.is_node( node ): 
			return [node]
		if not node.type.endswith( "_list" ):
			return [node]
		else:
			list = []
			for i in node.args:
				list.extend( self.flatten( i ) )
			return list
			
	def is_node( self, node ):
		return hasattr( node, "type" )

	def check( self, node ):
		if not self.is_node( node ):
			if isinstance( node, ( list, tuple ) ):
				for i in node:
					self.check( i )
			else:
				return node
		else:
			if node.type in ['identifier']:
				return node.args[0]

			elif node.type in ['var_list', 'statement_list', 'function_list']:
				return self.check( node.args )
				
			elif node.type == "program":
				self.global_scope.append( SymbolTable( "main" ) ) # global scope
				self.check( node.args )
				self.unused()
				#self.pop_scope() aparentemente isto tem de sair para o caso sem argumentos
    
			elif node.type == "block":
				if not any( scope.name == "main" for scope in self.global_scope ):
					self.global_scope.append( SymbolTable( "main" ) )
				self.check( node.args )

			elif node.type == "var": # variable definition
				identifiers = self.flatten( node.args[0] )
				var_type = node.args[1]
				for identifier in identifiers:
					var_name = identifier.args[0]
					var_info = {}
					if var_type.type == "array_type":
						type = var_type.args[2].args[0]
						upper_limit = int( var_type.args[1].args[0] )
						lower_limit = int( var_type.args[0].args[0] )
						bound = ( lower_limit, upper_limit )
						if type == 'array_type':
							size = int( type.args[1] )
							dimension = dimension_type.ARRAY_2D
						else:
							size = self.get_size( type )
						size *= ( upper_limit - lower_limit + 1 )
						dimension = dimension_type.ARRAY_1D
						var_info["bound"] = bound
						var_info["type"] = var_type.args[0].type
					else:
						t = var_type.args[0]
						size = self.get_size( t )
						if size == 255:
							dimension = dimension_type.ARRAY_1D
						else:
							dimension = dimension_type.SCALAR
						var_info["type"] = t

					var_info["size"] = size
					var_info["dimension"] = dimension
					self.set_var( var_name, var_info )
				
			elif node.type in ['function', 'procedure']:
				head = node.args[0]

				name = head.args[0].args[0].lower()
				self.check_if_function( name )
				
				if len( head.args ) == 1:
					args = []
				else:
					args = self.flatten( head.args[1] ) if len( head.args ) > 2 else []
					args = [
							( arg.args[0].args[0], arg.args[1].args[0] ) for arg in args
						]  # ( name, return type )
					
				if node.type == 'procedure':
					return_type = 'void'
				else:
					return_type = head.args[-1].args[0].lower()
					
				self.functions[name] = ( return_type, args )
				
				
				self.global_scope.append( SymbolTable( name ) ) # new scope
				for i in args:
					var_info = {
						"type" : i[1]
					}
					size = self.get_size( i[1] )
					var_info["size"] = size
					if i[1] != 'string':
						var_info["dimension"] = dimension_type.SCALAR
					else:
						var_info["dimension"] = dimension_type.ARRAY_1D
					self.set_var( i[0], var_info )
				self.check( node.args[1] )
				self.unused()
				self.pop_scope()
				
			elif node.type in ["function_call", "function_call_inline"]:
				function_name = node.args[0].args[0].lower()
				if function_name not in self.functions:
					raise Exception( "Function %s is not defined" % function_name )
				if len( node.args ) > 1:
					args = self.get_params( node.args[1] )
				else:
					args = []
				return_type, var_args = self.functions[function_name]
			
				if len( args ) != len( var_args ) and function_name not in ["readln", "writeln", "write"]:
					raise Exception( "Function %s is expecting %d parameters and got %d" % ( function_name, len( var_args ), len( args ) ) )
				else:
					for i in range( len( var_args ) ):
						if var_args[i][1] != args[i]:
							raise Exception( "Parameter #%d passed to function %s should be of type %s and not %s" % ( i + 1, function_name, var_args[i][1], args[i] ) )
				
				return return_type
				
			elif node.type == "assign":	
					var_name = self.check( node.args[0] ).lower()
					if self.is_function_name( var_name ):
						var_type = self.functions[var_name][0]
					else:
						if not self.has_var( var_name ):
							raise Exception( "Variable %s not declared" % var_name )
						var_type = self.get_var( var_name )["type"]
					assgntype = self.check( node.args[1] )
					
					if var_type != assgntype:
						raise Exception( "Variable %s is of type %s and does not support %s" % ( var_name, var_type, assgntype ) )
						
			elif node.type == 'and_or':
				op = node.args[0].args[0]
				for i in range( 1, 2 ):
					a = self.check( node.args[i] )
					if a != "boolean":
						raise Exception( "%s requires a boolean. Got %s instead." % ( op, a ) )
		
			elif node.type == "op":	
				op = node.args[0].args[0]
				var1_type = self.check( node.args[1] )
				var2_type = self.check( node.args[2] )
	
				if op == '=' and var1_type == 'string' and var2_type == 'char':
					return 'boolean'
 
				if var1_type != var2_type:
					raise Exception( "Arguments of operation '%s' must be of the same type. Got %s and %s." % ( op, var1_type, var2_type ) )
					
				if op in ['mod', 'div']:
					if var1_type != 'integer':
						raise Exception( "Operation %s requires integers." % op )
				
				if op == '/':
					if var1_type != 'real':
						raise Exception( "Operation %s requires reals." % op )
					
				if op in ['=','<=','>=','>','<','<>']:
					return 'boolean'
				else:
					return var1_type
				
			elif node.type in ['if','while','repeat']:
				if node.type == 'repeat':
					c = 1
				else:
					c = 0
				t = self.check( node.args[c] )
		
				if t != 'boolean':
					raise Exception( "%s condition requires a boolean. Got %s instead." % ( node.type, t ) )
				
				# check body
				self.check( node.args[1 - c] )
				
				# check else
				if len( node.args ) > 2:
					self.check( node.args[2] )
					
			elif node.type == 'for':
				i = node.args[0].args[0].args[0]
				if self.has_var( i ):
					self.global_scope[-1].var_count[i] += 1
				# self.global_scope.append( SymbolTable() ) # new scope
				# var = node.args[0].args[0].args[0].lower()
				# var_info = {
				# 	'type' : 'integer',
				# 	'dimension' : dimension_type.SCALAR,
				# 	'size' : 4
				# }
				#self.set_var( var, var_info )
	
				start_type = self.check( node.args[0].args[1] )
				end_type = self.check( node.args[2] )
	
				if start_type != 'integer':
					raise Exception( 'For requires a integer as a starting value' )
				
				if end_type != 'integer':
					raise Exception( 'For requires a integer as a final value' )
				
				self.check( node.args[3] )
				
			elif node.type == 'not':
				return self.check( node.args[0] )
				
			elif node.type == "element":
				if node.args[0].type == 'identifier':
					var_name = node.args[0].args[0]
					if var_name in self.functions:
						return self.functions[var_name][0]
					else:
						return self.get_var( node.args[0].args[0] )["type"]
				elif node.args[0].type == 'function_call_inline':
					return self.check( node.args[0] )
				else:
					if node.args[0].type in self.types:
						return node.args[0].type
					else:
						return self.check( node.args[0] )
	
			elif node.type == "array_access":
				var_name = node.args[0].args[0]
				index_expr = self.check( node.args[1] )

				if not self.has_var( var_name ):
					raise Exception( f"Variable '{ var_name }' is not declared." )

				var_info = self.get_var( var_name )
				if var_info["dimension"] not in [dimension_type.ARRAY_1D, dimension_type.ARRAY_2D]:
					raise Exception( f"Variable '{ var_name }' is not an array." )

				if index_expr != "integer":
					raise Exception( f"Array index for '{ var_name }' must be an integer. Got { index_expr }." )

				return var_info["type"]

			elif node.type == 'variable_declaration_list':
				for var_decl in node.args:
					self.check( var_decl )
     
			elif node.type == 'sub_declaration_list':
				for sub_decl in node.args:
					self.check( sub_decl )

			else:
				print( "semantic missing:" + node.type )