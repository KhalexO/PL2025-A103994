from utils.AST import Node

class ILGenerator:
	def __init__(self, global_scope):
		self.temp_count = 0
		self.label_count = 0
		self.main_instr = []  # Para o código do bloco main
		self.func_instr = []  # Para o código das funções
		self.instructions = self.main_instr  # Por defeito apontar para main_instr
		self.global_scope = global_scope  # Lista de declarações de funções
		self.array_access_cache = {}

	def new_temp(self):
		name = f"t{self.temp_count}"
		self.temp_count += 1
		return name

	def new_label(self):
		label = f"L{self.label_count}"
		self.label_count += 1
		return label

	def emit(self, op, arg1='', arg2='', res=''):
		self.instructions.append((op, arg1, arg2, res))

	def generate(self, node):
		if isinstance(node, (list, tuple)):
			for n in node:
				self.generate(n)
			return None
		method = getattr(self, f"gen_{node.type}", None)
		if not method:
			raise NotImplementedError(f"No IL gen for node {node.type}")
		return method(node)

	def gen_program(self, node):
		args = node.args
		self.instructions = self.main_instr
		for part in args[1:-1]:
			self.generate(part)
		self.generate(args[-1])
		self.emit('HALT')

		# Concatenar as funções ao final das instruções do programa principal
		self.main_instr += self.func_instr


	def gen_block(self, node):
		if len(node.args) >= 2:
			self.generate(node.args[-1])

	def gen_statement_list(self, node):
		#self.clear_array_access_cache()
		self.generate(node.args)

	def gen_expression(self, node):
		#self.clear_array_access_cache()
		return self.generate(node)


	def gen_var(self, node):
		return None

	def gen_assign(self, node):
		dest = node.args[0].args[0]
		src = self.generate(node.args[1])
		self.emit('ASSIGN', src, '', dest)
		return dest

	def gen_op(self, node):
		op = node.args[0].args[0].lower()
		left = self.generate(node.args[1])
		right = self.generate(node.args[2])
		tmp = self.new_temp()
		op_map = {
			'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',
			'div': 'DIV', 'mod': 'MOD',
			'=': 'EQ', '<>': 'NEQ', '<': 'LT', '<=': 'LTE', '>': 'GT', '>=': 'GTE',
			'and': 'AND', 'or': 'OR'
		}
		self.emit(op_map.get(op, op.upper()), left, right, tmp)
		return tmp

	def gen_not(self, node):
		val = self.generate(node.args[0])
		tmp = self.new_temp()
		self.emit('NOT', val, '', tmp)
		return tmp

	def gen_element(self, node):
		child = node.args[0]
		if child.type == 'identifier':
			return child.args[0]
		if child.type in ('integer', 'real'):
			return str(child.args[0])
		if child.type in ('string', 'char'):
			return f'"{child.args[0]}"'
		if child.type == 'boolean':
			return '1' if str(child.args[0]).lower() == 'true' else '0'
		return self.generate(child)

	def gen_boolean(self, node):
		return '1' if str(node.args[0]).lower() == 'true' else '0'

	def clear_array_access_cache(self):
		self.array_access_cache.clear()

	def gen_array_access(self, node):
		arr_name = node.args[0].args[0]
		idx_expr = node.args[1]

		# Generate index value
		idx_val = self.generate(idx_expr)

		key = (arr_name, idx_val)

		if key in self.array_access_cache:
			return self.array_access_cache[key]

		tmp = self.new_temp()
		# Assume non-string type for simplicity, adapt if needed
		self.emit('LOAD', idx_val, arr_name, tmp)

		self.array_access_cache[key] = tmp
		return tmp

	def gen_if(self, node):
		cond = self.generate(node.args[0])
		else_lbl = self.new_label()
		end_lbl = self.new_label()
		self.emit('IFZ', cond, '', else_lbl)
		self.generate(node.args[1])
		self.emit('GOTO', '', '', end_lbl)
		self.emit('LABEL', '', '', else_lbl)
		if len(node.args) > 2:
			self.generate(node.args[2])
		self.emit('LABEL', '', '', end_lbl)

	def gen_while(self, node):
		start = self.new_label()
		end = self.new_label()
		self.emit('LABEL', '', '', start)
		cond = self.generate(node.args[0])
		self.emit('IFZ', cond, '', end)
		self.generate(node.args[1])
		self.emit('GOTO', '', '', start)
		self.emit('LABEL', '', '', end)

	def gen_repeat(self, node):
		start = self.new_label()
		self.emit('LABEL', '', '', start)
		self.generate(node.args[0])
		cond = self.generate(node.args[1])
		self.emit('IFZ', cond, '', start)

	def gen_for(self, node):
		self.generate(node.args[0])
		start = self.new_label()
		end = self.new_label()
		self.emit('LABEL', '', '', start)
		var = node.args[0].args[0].args[0]
		if len(node.args) == 5:
			end_val = self.generate(node.args[3])
			dir_token = node.args[2]
		else:
			end_val = self.generate(node.args[2])
			dir_token = node.args[1]
		if isinstance(dir_token, Node):
			dir_token = dir_token.args[0]
		cmp_op = 'LTE' if dir_token.lower() == 'to' else 'GTE'
		cond_tmp = self.new_temp()
		self.emit(cmp_op, var, end_val, cond_tmp)
		self.emit('IFZ', cond_tmp, '', end)
		self.generate(node.args[-1])
		step_op = 'ADD' if dir_token.lower() == 'to' else 'SUB'
		step_tmp = self.new_temp()
		self.emit(step_op, var, '1', step_tmp)
		self.emit('ASSIGN', step_tmp, '', var)
		self.emit('GOTO', '', '', start)
		self.emit('LABEL', '', '', end)

	def gen_function(self, node):
		# Ao gerar função, muda o destino para func_instr
		old_instr = self.instructions
		self.instructions = self.func_instr
		head, body = node.args
		name = head.args[0].args[0]
		self.emit('LABEL', '', '', name)
		self.generate(body)
		self.emit('RET')
		# Voltar ao main_instr
		self.instructions = old_instr

	def flatten_params(self, param_node):
		if isinstance(param_node, Node):
			if param_node.type == 'parameter':
				return [param_node.args[0]]
			if param_node.type == 'parameter_list':
				flat = []
				for p in param_node.args:
					flat += self.flatten_params(p)
				return flat
			return [param_node]
		return []

	def gen_function_call_inline(self, node):
		name = node.args[0].args[0]
		args = self.flatten_params(node.args[1]) if len(node.args) > 1 else []
		vals = [self.generate(arg) for arg in args]
		
		# Evaluate all arguments first
		arg_vals = [self.generate(arg) for arg in args]
		for val in arg_vals:
			self.emit('ARG', val)
		
		# TRATAR FUNÇÕES EMBUTIDAS (como length)
		if name.lower() == "length":
			tmp = self.new_temp()
			self.emit('LEN', vals[0], '', tmp)
			return tmp
		
		tmp = self.new_temp()
		self.emit('CALL', name, ','.join(vals), tmp)
		return tmp

	def gen_function_call(self, node):
		name = node.args[0].args[0]
		args = self.flatten_params(node.args[1]) if len(node.args) > 1 else []
		# for expr in args:
		# 	val = self.generate(expr)
		# 	self.emit('ARG', val)
		# self.emit('CALL', name, '', '')
		for val in [self.generate(p) for p in args]:
			self.emit('ARG', val)
		self.emit('CALL', name, '', '')

	def gen_readln(self, node):
		target = node.args[0]

		if target.type == 'element' and target.args[0].type == 'array_access':
			arr_node = target.args[0]           # array_access node
			arr_name = arr_node.args[0].args[0]
			def gen_index(node):
				if node.type == 'identifier':
					return node.args[0]
				if node.type == 'integer':
					return str(node.args[0])
				return self.generate(node)
			idx_temp = gen_index(arr_node.args[1])
			tmp_val = self.new_temp()
			self.emit('READ', '', '', tmp_val)
			self.emit('STORE', tmp_val, idx_temp, arr_name)

		else:
			# Caso normal
			if target.type == 'element':
				child = target.args[0]
				if child.type == 'identifier':
					var_name = child.args[0]
					self.emit('READ', var_name)
					return
			var_name = target.args[0]
			self.emit('READ', var_name)



	def gen_writeln(self, node):
		args = self.flatten_params(node.args[0])
		for val_node in args:
			val = self.generate(val_node)
			self.emit('WRITE_STRING', val)

	def gen_sub_declaration_list(self, node):
		self.generate(node.args)




