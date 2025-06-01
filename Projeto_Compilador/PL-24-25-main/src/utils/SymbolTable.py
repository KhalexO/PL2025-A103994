from enum import Enum, auto

"""
===============================================================================

	Symbol Table
 
===============================================================================
"""

class dimension_type( Enum ):
    SCALAR = 0
    ARRAY_1D = 1
    ARRAY_2D = 2
    ARRAY_3D = 3

# variable -> size, address, dimension, type 
class SymbolTable:
	def __init__( self, name = None ):
		self.variables = {}
		self.var_count = {}
		self.name = name
		self.address_counter = 0

	def set_var( self, name, var_info ):
		self.address_counter += var_info["size"]
		self.variables[name] = var_info
		self.variables[name]["address"] = self.address_counter
		self.var_count[name] = 0
	
	def get_var( self, name ):
		return self.variables[name]

	def has_var( self, name ):
		return name in self.variables