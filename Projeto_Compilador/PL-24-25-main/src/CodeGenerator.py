class CodeGenerator:
	def __init__(self):
		self.global_indices = {}
		self.temp_indices = {}
		self.next_global_index = 0
		self.next_temp_index = -1
		self.instructions = []
		self.var_types = {}  # Adicionado: armazena os tipos das variáveis
		self.temp_var_types = {}

	def alloc_globals(self, symtab_or_list):
		tables = symtab_or_list if isinstance(symtab_or_list, list) else [symtab_or_list]
		for st in tables:
			for var, varinfo in st.variables.items():
				if var not in self.global_indices:
					self.global_indices[var] = self.next_global_index
					self.next_global_index += 1
				if isinstance(varinfo, dict) and "type" in varinfo:
					self.var_types[var] = varinfo["type"]
				else:
					self.var_types[var] = 'string'

	def emit(self, line: str):
		self.instructions.append(line)

	def get_temp_index(self, name: str) -> int:
		if name not in self.temp_indices:
			self.temp_indices[name] = self.next_temp_index
			self.next_temp_index -= 1
		return self.temp_indices[name]

	def translate(self, il_list: list, global_symtab_list):
		self.alloc_globals(global_symtab_list)
		self.emit('START')
		print("DEBUG: var_types =", self.var_types)
		for idx, (op, a1, a2, res) in enumerate(il_list):
			cmd = op.upper()
			if cmd in ('ADD','SUB','MUL','DIV','MOD','GT','LT','GTE','LTE','EQ','NEQ','AND','OR'):
				self.load_operand(a1)
				self.load_operand(a2)
				map_ops = {
					'ADD':'add','SUB':'sub','MUL':'mul','DIV':'div','MOD':'mod',
					'GT':'sup','LT':'inf','GTE':'supeq','LTE':'infeq',
					'EQ':'equal','NEQ':'neq','AND':'and','OR':'or'
				}
				self.emit(map_ops[cmd].upper())
				self.store_operand(res)
			if res and res.startswith('t'):
				if cmd in ('AND','OR','EQ','NEQ','GT','LT','GTE','LTE'):
					self.temp_var_types[res] = 'boolean'
				elif cmd in ('ADD','SUB','MUL','DIV','MOD'):
					# If either operand is float, treat as float (you can improve this logic)
					type_a1 = self.var_types.get(a1) or self.temp_var_types.get(a1)
					type_a2 = self.var_types.get(a2) or self.temp_var_types.get(a2)
					if type_a1 == 'float' or type_a2 == 'float':
						self.temp_var_types[res] = 'float'
					else:
						self.temp_var_types[res] = 'integer'
				else:
					self.temp_var_types[res] = 'integer'

			elif cmd == 'NOT':
				self.load_operand(a1)
				self.emit('not')
				self.store_operand(res)

			elif cmd == 'ASSIGN':
				self.load_operand(a1)
				self.store_operand(res)

			elif cmd == 'LEN':
				self.load_operand(a1)
				self.emit('STRLEN')
				self.store_operand(res)

			# elif cmd == 'READ':
			#     self.emit('READ')
			#     self.emit('ATOI')
			#     self.store_operand(a1)

			elif cmd == 'ARG':
				continue

			elif cmd == 'CALL':
				fn = a1.lower()
				args = []
				j = idx - 1
				while j >= 0 and il_list[j][0] == 'ARG':
					args.insert(0, il_list[j][1])
					j -= 1

				if fn == 'writeln':
					for arg in args:
						if arg.startswith('"') and arg.endswith('"'):
							lit = arg[1:-1]
							self.emit(f'PUSHS "{lit}"')
							self.emit('WRITES')
						elif arg.lstrip('-').isdigit():
							self.emit(f'PUSHI {arg}')
							self.emit('WRITEI')
						else:
							self.load_operand(arg)
							self.emit('WRITEI')
					self.emit('WRITELN')

				elif fn == 'readln':
					for target in args:
						target_type = self.var_types.get(target, None)
						if target_type is None and target.startswith('t'):
							target_type = self.temp_var_types.get(target)
						self.emit('READ')
						if target_type == 'string':
							self.store_operand(target)
						elif target_type in ('integer', 'boolean'):
							self.emit('ATOI')
							self.store_operand(target)
						elif target_type == 'float':
							self.emit('ATOF')
							self.store_operand(target)
						elif target_type == 'char':
							self.emit('ATOC')
							self.store_operand(target)
						else:
							self.store_operand(target)

				else:
					for arg in args:
						self.load_operand(arg)
					self.emit(f'PUSHA {a1}')
					self.emit('CALL')

			elif cmd == 'LABEL':
				self.emit(f'{res}:')

			elif cmd == 'GOTO':
				self.emit(f'JUMP {res}')

			elif cmd == 'IFZ':
				self.load_operand(a1)
				self.emit(f'JZ {res}')

			elif cmd == 'HALT':
				self.emit('STOP')
				
			elif cmd == 'RET':
				self.emit('RETURN')

		return self.instructions

	def load_operand(self, src: str):
		if src.lstrip('-').isdigit():
			self.emit(f'PUSHI {src}')
		elif src.startswith('"') and src.endswith('"'):
			lit = src[1:-1]
			if len(lit) == 3 and lit[0] == "'" and lit[2] == "'":
				lit = lit[1]
			self.emit(f'PUSHS "{lit}"')
		elif src in self.global_indices:
			self.emit(f'PUSHG {self.global_indices[src]}')
		elif src.startswith('t') and src[1:].isdigit():
			self.emit(f'PUSHL {self.get_temp_index(src)}')
		else:
			self.emit(f'PUSHL {src}')

	def store_operand(self, name: str):
		if name in self.global_indices:
			self.emit(f'STOREG {self.global_indices[name]}')
		elif name.startswith('t') and name[1:].isdigit():
			self.emit(f'STOREL {self.get_temp_index(name)}')
		else:
		    pass

