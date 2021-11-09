
from colorama import init, Fore, Back, Style
from copy import deepcopy

init(autoreset=True)

#===================================================================

class Cube:
	
	__author__  = 'LawlietJH'
	__version__ = 'v1.0.1'
	__description = '''
		Esta clase es una Abstracción del Cubo de Rubik de x*x*x dimensiones.
		Permite manipular el cubo y visualizarlo en consola.
	'''
	
	def __init__(self, len_c=3, color_list=['Azul','Verde','Rojo','Morado','Amarillo','Negro'], singmasterNotation=False):
		
		if not type(color_list) in [list, tuple] and not len(color_list) == 6:
			msg_error = 'The list of colors for the cube is incomplete, please select 6 colors.'
			raise ColorListIncomplete(msg_error)
		
		layers_min = 2
		layers_max = 5
		
		if not layers_min <= len_c <= layers_max:
			msg  = 'Currently only {} to {} '.format(layers_min, layers_max)
			msg += 'layer cubes can be solved.'
			raise self.NotSupported(msg)
		
		self.color_list = color_list
		self.cube_resolve = []
		self.move_logs = []
		self.len_c = len_c
		self.generateCube()
		
		self.adjust = len(str(len_c**3))+1
		self.cube = deepcopy(self.cube_resolve)
		
		self.cube_colors_resolve = {
			'F': [[self.color_list[0] for j in range(self.len_c)] for i in range(self.len_c)],
			'B': [[self.color_list[1] for j in range(self.len_c)] for i in range(self.len_c)],
			'R': [[self.color_list[2] for j in range(self.len_c)] for i in range(self.len_c)],
			'L': [[self.color_list[3] for j in range(self.len_c)] for i in range(self.len_c)],
			'U': [[self.color_list[4] for j in range(self.len_c)] for i in range(self.len_c)],
			'D': [[self.color_list[5] for j in range(self.len_c)] for i in range(self.len_c)]
		}
		
		self.cube_colors = deepcopy(self.cube_colors_resolve)
		
		self.updateLayerList()
		
		self.moves_availables  = list(self.layers_list.keys())
		self.moves_availables += [ _ + '\'' for _ in list(self.layers_list.keys()) ]
		self.moves_availables += [ _ + '2'  for _ in list(self.layers_list.keys()) ]
		self.moves_availables += ['x', 'x\'', 'x2',		# Rotar sobre el eje x: rotar el cubo entero en R.
								  'y', 'y\'', 'y2',		# Rotar sobre el eje y: rotar el cubo entero en U.
								  'z', 'z\'', 'z2']		# Rotar sobre el eje z: rotar el cubo entero en F.
		
		self.singmasterNotation = singmasterNotation
	
	#===================================================================
	# Manejo de Errores:
	
	class ColorListIncomplete(Exception): pass
	class LayerDoesNotExist(Exception): pass
	class LayersExceeded(Exception): pass
	class NotSupported(Exception): pass
	class OutOfRange(Exception): pass
	
	#===================================================================
	# Manipulación del Objeto:
	
	def getPieceByLetters(self, piece, layer):
		
		#Obtiene el número de pieza basado en las capa indicada en la primer letra en la variable 'piece'
		
		item = None
		
		if   piece in ['FUL','FLU']: item = layer[0][0]
		elif piece == 'FU':          item = layer[0][1]
		elif piece in ['FUR','FRU']: item = layer[0][2]
		elif piece == 'FL':          item = layer[1][0]
		elif piece == 'FC':          item = layer[1][1]
		elif piece == 'FR':          item = layer[1][2]
		elif piece in ['FDL','FLD']: item = layer[2][0]
		elif piece == 'FD':          item = layer[2][1]
		elif piece in ['FDR','FRD']: item = layer[2][2]
		
		elif piece in ['BUR','BRU']: item = layer[0][0]
		elif piece == 'BU':          item = layer[0][1]
		elif piece in ['BUL','BLU']: item = layer[0][2]
		elif piece == 'BR':          item = layer[1][0]
		elif piece == 'BC':          item = layer[1][1]
		elif piece == 'BL':          item = layer[1][2]
		elif piece in ['BDR','BRD']: item = layer[2][0]
		elif piece == 'BD':          item = layer[2][1]
		elif piece in ['BDL','BLD']: item = layer[2][2]
		
		elif piece in ['UBL','ULB']: item = layer[0][0]
		elif piece == 'UB':          item = layer[0][1]
		elif piece in ['UBR','URB']: item = layer[0][2]
		elif piece == 'UL':          item = layer[1][0]
		elif piece == 'UC':          item = layer[1][1]
		elif piece == 'UR':          item = layer[1][2]
		elif piece in ['UFL','ULF']: item = layer[2][0]
		elif piece == 'UF':          item = layer[2][1]
		elif piece in ['UFR','URF']: item = layer[2][2]
		
		elif piece in ['DFL','DLF']: item = layer[0][0]
		elif piece == 'DF':          item = layer[0][1]
		elif piece in ['DFR','DRF']: item = layer[0][2]
		elif piece == 'DL':          item = layer[1][0]
		elif piece == 'DC':          item = layer[1][1]
		elif piece == 'DR':          item = layer[1][2]
		elif piece in ['DBL','DLB']: item = layer[2][0]
		elif piece == 'DB':          item = layer[2][1]
		elif piece in ['DBR','DRB']: item = layer[2][2]
		
		elif piece in ['RUF','RFU']: item = layer[0][0]
		elif piece == 'RU':          item = layer[0][1]
		elif piece in ['RUB','RBU']: item = layer[0][2]
		elif piece == 'RF':          item = layer[1][0]
		elif piece == 'RC':          item = layer[1][1]
		elif piece == 'RB':          item = layer[1][2]
		elif piece in ['RDF','RFD']: item = layer[2][0]
		elif piece == 'RD':          item = layer[2][1]
		elif piece in ['RDB','RBD']: item = layer[2][2]
		
		elif piece in ['LUB','LBU']: item = layer[0][0]
		elif piece == 'LU':          item = layer[0][1]
		elif piece in ['LUF','LFU']: item = layer[0][2]
		elif piece == 'LB':          item = layer[1][0]
		elif piece == 'LC':          item = layer[1][1]
		elif piece == 'LF':          item = layer[1][2]
		elif piece in ['LDB','LBD']: item = layer[2][0]
		elif piece == 'LD':          item = layer[2][1]
		elif piece in ['LDF','LFD']: item = layer[2][2]
		
		return item
	
	def __getitem__(self, items):	# Muestra el número de pieza en la posición x, y, z.
		
		if type(items) == int and 0 < items <= self.len_c:
			
			return self.cube[0][0][items-1]
		
		elif type(items) == str and 1 <= len(items) <= 3:
			
			letters = items
			
			if not self.len_c == 3:
				msg_error  = 'Lettered function not supported in a '
				msg_error += '{0}x{0}x{0} cube.'.format(self.len_c)
				raise NotSupported(msg_error)
			
			if letters in self.layers_list:
				
				return self.layers_list[items]['layer']
				
			else:
				
				for i in items:
					if not i in self.layers_list and not i == 'C':
						msg_error  = 'Layer {} does not exist.\n'.format(repr(i))
						msg_error += 'Use: F, B, R, L, U, D.'
						raise self.LayerDoesNotExist(msg_error)
				
				item = self.layers_list[items[0]]['layer']
				item = self.getPieceByLetters(letters, item)
				
				return item
		
		elif type(items) == tuple:
			
			if items[0] in ['F','B','R','L','U','D']:
				y = items[1]-1
				x = items[2]-1
				return self.layers_list[items[0]]['layer'][y][x]
			else:
				y = items[0]-1
				x = items[1]-1
				if len(items) == 2: return self.cube[0][y][x]
				elif len(items) == 3: z = items[2]-1; return self.cube[z][y][x]
				else: raise self.LayersExceeded('A cube only has 3 dimensions...')
			
		else: raise self.OutOfRange()
	
	#===================================================================
	# Básicas:
	
	#Potencias:
	def pow(self, b, e): return b**e
	
	#Invierte las listas en una lista:
	def invElems(self, l): return [ e[::-1] for e in l ] 
	
	#Obtiene las letras de las capas de toda una cadena o lista de letras.
	def getLayerLetters(self, letters):
		
		if not letters.count('(') == letters.count(')'):
			msg_error = 'Missing Parentheses: ' + (repr(')') if letters.count('(') > letters.count(')') else repr('('))
			msg_error += '\n In: "' + letters + '"'
			raise self.OutOfRange(msg_error)
		
		if not type(letters) in [str, list, tuple]:
			raise NotSupported(repr(str(letters)))
		
		letters = str(letters)
		letters = letters.translate({ord(' '):None})					#Elimina todos los espacios
		# ~ letters = letters.translate({ord(i): None for i in 'abc'})	#Opcion 2: Elimina cada caracter indicado, en toda la cadena
		
		output = []
		
		tmp = []
		tmp_saving = False
		parentheses = False
		qty = ''
		
		for l in letters:
			
			if parentheses:
				
				try:
					l = int(l)
					
					qty += str(l)
					continue
					
				except ValueError:
					parentheses = False
					output += (tmp * ((int(qty)) if qty else 1))
					tmp = []
			
			if l in ['(',')',','] or tmp_saving:
				
				if l == ',': continue
				
				if l == ')':
					tmp_saving = False
					parentheses = True
					continue
				
				if tmp_saving:
					if l in ['\'','2','w']:
						tmp[-1] += l
					else:
						tmp.append(l)
					continue
				
				if l == '(':
					tmp_saving = True
				
				continue
			
			if l in ['\'','2','w']:
				output[-1] += l
			else:
				output.append(l)
		
		if parentheses: output += (tmp * ((int(qty)) if qty else 1))
		
		return output
	
	@property
	def is_solved(self):
		return self.cube_resolve == self.cube
	
	#===================================================================
	# Mover:
	
	def moveAssign(self, move, qty=1):
		
		for _ in range(qty):
			
			new = deepcopy(self.cube)					#Copia del estado actual del cubo (basado en las capas primordiales F, todas las S y B)
			new_colors = deepcopy(self.cube_colors)		#Copia del estado actual de los colores en las capas.
			
			for i in range(self.len_c):
				for j, m in enumerate(move):
					for x in range(len(m)):
						if j == 0:
							#Intercambio de Piezas:
							if i == self.len_c-1: continue				# Evita repetir el primer cambio de pieza
							exec('new'+m[x]+' = self.cube'+m[(x+1)%4])
						else:
							#Intercambio de Colores:
							exec('new_colors'+m[x]+' = self.cube_colors'+m[(x+1)%4])
			
			self.cube_colors = deepcopy(new_colors)
			self.cube = deepcopy(new)
			self.updateLayerList()
	
	def move(self, algorithm, log=True):
		
		algorithm = self.getLayerLetters(algorithm)
		algorithm = self.reduceAlgorithm(algorithm)
		
		movements = {
			'F': [
				["[0][i][0]",       "[0][-1][i]",   "[0][-1-i][-1]", "[0][0][-1-i]"   ],		#Intercambio de piezas de la capa F en sentido horario. Orden: [z][y][x]
				["['U'][-1][-1-i]", "['L'][i][-1]", "['D'][0][i]",   "['R'][-1-i][0]" ],		#Intercambio de Colores Exteriores en piezas de la capa F en sentido horario.
				["['F'][0][-1-i]",  "['F'][i][0]",  "['F'][-1][i]",  "['F'][-1-i][-1]"]			#Intercambio de Colores Interiores en piezas de la capa F en sentido horario.
			],
			'B': [
				["[-1][0][i]",     "[-1][i][-1]",  "[-1][-1][-1-i]",  "[-1][-1-i][0]"  ],		#Intercambio de piezas de la capa B en sentido horario.
				["['U'][0][i]",    "['R'][i][-1]", "['D'][-1][-1-i]", "['L'][-1-i][0]" ],		#Intercambio de Colores Exteriores en piezas de la capa B en sentido horario.
				["['B'][0][-1-i]", "['B'][i][0]",  "['B'][-1][i]",    "['B'][-1-i][-1]"]		#Intercambio de Colores Interiores en piezas de la capa B en sentido horario.
			],
			'R': [
				["[-1-i][0][-1]",  "[0][i][-1]",   "[i][-1][-1]",  "[-1][-1-i][-1]" ],			#Intercambio de piezas de la capa R en sentido horario.
				["['U'][i][-1]",   "['F'][i][-1]", "['D'][i][-1]", "['B'][-1-i][0]" ],			#Intercambio de Colores Exteriores en piezas de la capa R en sentido horario.
				["['R'][0][-1-i]", "['R'][i][0]",  "['R'][-1][i]", "['R'][-1-i][-1]"]			#Intercambio de Colores Interiores en piezas de la capa R en sentido horario.
			],
			'L': [
				["[i][0][0]",      "[-1][i][0]",   "[-1-i][-1][0]",  "[0][-1-i][0]"],			#Intercambio de piezas de la capa L en sentido horario.
				["['U'][-1-i][0]", "['B'][i][-1]", "['D'][-1-i][0]", "['F'][-1-i][0]"],			#Intercambio de Colores Exteriores en piezas de la capa L en sentido horario.
				["['L'][0][-1-i]", "['L'][i][0]",  "['L'][-1][i]",   "['L'][-1-i][-1]"]			#Intercambio de Colores Interiores en piezas de la capa L en sentido horario.
			],
			'U': [
				["[-1][0][-1-i]",  "[-1-i][0][0]", "[0][0][i]",    "[i][0][-1]"     ],			#Intercambio de piezas de la capa U en sentido horario.
				["['B'][0][i]",    "['L'][0][i]",  "['F'][0][i]",  "['R'][0][i]"    ],			#Intercambio de Colores Exteriores en piezas de la capa U en sentido horario.
				["['U'][0][-1-i]", "['U'][i][0]",  "['U'][-1][i]", "['U'][-1-i][-1]"]			#Intercambio de Colores Interiores en piezas de la capa U en sentido horario.
			],
			'D': [
				["[0][-1][-1-i]",   "[i][-1][0]",      "[-1][-1][i]",     "[-1-i][-1][-1]" ],	#Intercambio de piezas de la capa D en sentido horario.
				["['F'][-1][-1-i]", "['L'][-1][-1-i]", "['B'][-1][-1-i]", "['R'][-1][-1-i]"],	#Intercambio de Colores Exteriores en piezas de la capa D en sentido horario.
				["['D'][0][-1-i]",  "['D'][i][0]",     "['D'][-1][i]",    "['D'][-1-i][-1]"]	#Intercambio de Colores Interiores en piezas de la capa D en sentido horario.
			],
			'M': [
				["[i][0][(self.len_c-1)//2]",      "[-1][i][(self.len_c-1)//2]",  "[-1-i][-1][(self.len_c-1)//2]",  "[0][-1-i][(self.len_c-1)//2]"  ],		#Intercambio de piezas de la capa M en sentido horario.
				["['U'][-1-i][(self.len_c-1)//2]", "['B'][i][(self.len_c-1)//2]", "['D'][-1-i][(self.len_c-1)//2]", "['F'][-1-i][(self.len_c-1)//2]"]		#Intercambio de Colores Exteriores en piezas de la capa M en sentido horario.
			],
			'E': [
				["[-1-i][(self.len_c-1)//2][-1]",  "[-1][(self.len_c-1)//2][i]",     "[i][(self.len_c-1)//2][0]",      "[0][(self.len_c-1)//2][-1-i]"  ],	#Intercambio de piezas de la capa E en sentido horario.
				["['R'][(self.len_c-1)//2][-1-i]", "['B'][(self.len_c-1)//2][-1-i]", "['L'][(self.len_c-1)//2][-1-i]", "['F'][(self.len_c-1)//2][-1-i]"]	#Intercambio de Colores Exteriores en piezas de la capa E en sentido horario.
			],
			'S': [
				["[(self.len_c-1)//2][0][-1-i]",   "[(self.len_c-1)//2][i][0]",   "[(self.len_c-1)//2][-1][i]",  "[(self.len_c-1)//2][-1-i][-1]" ],			#Intercambio de piezas de la capa S en sentido horario.
				["['U'][(self.len_c-1)//2][-1-i]", "['L'][i][(self.len_c-1)//2]", "['D'][(self.len_c-1)//2][i]", "['R'][-1-i][(self.len_c-1)//2]"]			#Intercambio de Colores Exteriores en piezas de la capa S en sentido horario.
			]
		}
		
		for layer in algorithm:
			
			if not layer in self.moves_availables:
				msg_error  = 'Layer {} does not exist.\n'.format(repr(layer))
				msg_error += 'Use: F, F\' or F2, same for B, R, L, U, D, f or Fw, b or Bw, r or Rw, l or Lw, u or Uw, d or Dw or S, M, E or x, y, z.'
				raise self.LayerDoesNotExist(msg_error)
			
			xyorz = layer[0] in ['x','y','z']
			
			if layer[0].islower() and not xyorz:
				if '\'' in layer or '2' in layer:
					layer = layer[0].upper() + 'w' + layer[-1]
				else:
					layer = layer[0].upper() + 'w'
			
			if xyorz:
				
				if layer[0] == 'x':
					layer = 'Rw' + ('\'' if '\'' in layer else ('2' if '2' in layer else ''))
					let = "L"
				elif layer[0] == 'y':
					layer = 'Uw' + ('\'' if '\'' in layer else ('2' if '2' in layer else ''))
					let = "D"
				elif layer[0] == 'z':
					layer = 'Fw' + ('\'' if '\'' in layer else ('2' if '2' in layer else ''))
					let = "B"
				
				if '\'' in layer:
					move = movements[let]
					self.moveAssign(move)
				elif '2' in layer:
					move = movements[let]
					self.moveAssign(move, 2)
				else:
					move = movements[let]
					move = self.invElems(move)
					self.moveAssign(move)
			
			W = None
			if 'w' in layer:
				if layer[0] == 'F': W = movements['S']
				if layer[0] == 'B': W = self.invElems(movements['S'])
				if layer[0] == 'R': W = self.invElems(movements['M'])
				if layer[0] == 'L': W = movements['M']
				if layer[0] == 'U': W = movements['E']
				if layer[0] == 'D': W = self.invElems(movements['E'])
			
			if '\'' in layer:
				if W: self.moveAssign(self.invElems(W))
				move = self.invElems(movements[layer[0]])
				self.moveAssign(move)
			elif '2' in layer:
				if W: self.moveAssign(W, 2)
				move = movements[layer[0]]
				self.moveAssign(move, 2)
			else:
				if W: self.moveAssign(W)
				move = movements[layer[0]]
				self.moveAssign(move)
			
			# Restaurando:
			if xyorz:
				if layer[0] == 'R': layer = 'x' + ('\'' if '\'' in layer else ('2' if '2' in layer else ''))
				if layer[0] == 'U': layer = 'y' + ('\'' if '\'' in layer else ('2' if '2' in layer else ''))
				if layer[0] == 'F': layer = 'z' + ('\'' if '\'' in layer else ('2' if '2' in layer else ''))
			
			if self.singmasterNotation:
				if 'w' in layer:
					if '\'' in layer or '2' in layer:
						layer = layer[0].lower() + layer[-1]
					else:
						layer = layer[0].lower()
			
			if log: self.move_logs.append(layer)
	
	#===================================================================
	# Mostrar:
	
	def layer(self, layer):
		cube = self.getCube()
		rows = cube[layer]
		layer = '\r{}\n\r{}\n\r{}\n\r{}\n\r{}\n\r{}\n\r{}'.format(*rows)
		return layer
	
	def showLayer(self, layer):
		
		if not layer in self.layers_list:
			msg_error  = 'Layer {} does not exist.\n'.format(repr(layer))
			msg_error += 'Use: F, B, R, L, U, D, f or Fw, b or Bw, r or Rw, l or Lw, u or Uw, d or Dw, S, M, E.'
			raise self.LayerDoesNotExist(msg_error)
		
		print('\n Layer {}:\n'.format(self.layers_list[layer]['desc']))
		
		for y in self.layers_list[layer]['layer']:
			for x in y:
				print(str(x).rjust(self.adjust), end='')
			print()
		print()
	
	def prettyColors(self, layers=['U','F','R','L','B','D'], on_list=False, with_letters=True):
		
		out = self.getCube(layers)
		
		if on_list:
			
			for layer, rows in out.items():
				
				if not with_letters:
					print(' Layer ' + layer + ':')
				
				for i, row in enumerate(rows):
					if i == 0:
						print(row + (layer if with_letters else ''))
					else:
						print(row)
				print()
			
		else:
			
			if 'U' in layers:
				for pos in range(len(out['U'])):
					row  = ' '*(18 if with_letters else 17)
					row += out['U'][pos]
					if pos == 0:
						print(row + ('U' if with_letters else ''))
					else:
						print(row)
			
			for pos in range(len(out['L'])):
				if pos == 0:
					row = ''
					if 'L' in layers:
						row += out['L'][pos] + ('L' if with_letters else '')
					else:
						row += ' '*(18 if with_letters else 17)
					if 'F' in layers:
						row += out['F'][pos] + ('F' if with_letters else '')
					else:
						row += ' '*(18 if with_letters else 17)
					if 'R' in layers:
						row += out['R'][pos] + ('R' if with_letters else '')
					else:
						row += ' '*(18 if with_letters else 17)
					if 'B' in layers:
						row += out['B'][pos] + ('B' if with_letters else '')
					else:
						row += ' '*(18 if with_letters else 17)
				else:
					row = ''
					if 'L' in layers:
						row += out['L'][pos] + (' ' if with_letters else '')
					else:
						row += ' '*(18 if with_letters else 17)
					if 'F' in layers:
						row += out['F'][pos] + (' ' if with_letters else '')
					else:
						row += ' '*(18 if with_letters else 17)
					if 'R' in layers:
						row += out['R'][pos] + (' ' if with_letters else '')
					else:
						row += ' '*(18 if with_letters else 17)
					if 'B' in layers:
						row += out['B'][pos] + (' ' if with_letters else '')
					else:
						row += ' '*(18 if with_letters else 17)
				print(row)
			
			if 'D' in layers:
				for pos in range(len(out['D'])):
					row  = ' '*(18 if with_letters else 17)
					row += out['D'][pos]
					if pos == 0:
						print(row + ('D' if with_letters else ''))
					else:
						print(row)
	
	def showPieceEnum(self, cube=None, verb=False):	# Muestra todas las capas de cubo en su estado actual.
		
		cube = self.cube if not cube else cube
		
		if verb:
			print(
			'''
			\r	Características:
			
			\r	    Esta enumeración  fue dada tomando como punto de vista
			\r	    de referencia  la capa  F,  todas las otras "capas" se
			\r	    miran desde la misma perspectiva.
			
			\r	Ejemplo: La capa B  se verá de espaldas al verla  desde la
			\r	    perspectiva de F.
			
			\r	    Además,  la capa central en su pieza central  en cubos
			\r	    de número impar,  en  realidad  es una pieza que nunca
			\r	    se moverá.
			
			\r	Ejemplo: En un cubo de  3*3*3  la pieza  14  representa el
			\r	    centro  de  todo  el  cubo,  que únicamente permite el
			\r	    intercambio de las piezas.  Por ello,  en este cubo la
			\r	    pieza  14  nunca  se  moverá,  ni  se tomará en cuenta
			\r	    al mostrar las capas de colores.
			'''
			)
		
		for i, z in enumerate(cube[::-1]):
			i = self.len_c-i-1
			print('\nLayer {}: {}\n'.format(i+1, 'Front (F)' if i == 0 else ('Back (B)' if i == self.len_c-1 else 'S')))
			for y in z:
				for x in y:
					print(str(x).rjust(self.adjust), end='')
				print()
		print()
	
	def reduceAlgorithm(self, algorithm):
		
		algorithm = algorithm[::-1]
		
		temp = []
		len_a = len(algorithm)
		
		for x in range(len_a):
			
			if algorithm[x] == None: continue
			
			try:
				
				if  algorithm[x] == algorithm[x+1] \
				and algorithm[x] == algorithm[x+2] \
				and algorithm[x] == algorithm[x+3]:
					
					for i in range(4): algorithm[x+i] = None
			
			except: pass
			
			try:
				
				if  algorithm[x] == algorithm[x+1] \
				and algorithm[x] == algorithm[x+2]:
					
					for i in range(1, 3): algorithm[x+i] = None
					
					if algorithm[x][-1] == '\'':
						algorithm[x] = algorithm[x][:-1]
					else:
						algorithm[x] += '\''
			
			except: pass
			
			try:
				
				if algorithm[x] == algorithm[x+1]:
					
					if algorithm[x][-1] == '\'':
						algorithm[x] = algorithm[x][:-1]+'2'
					elif algorithm[x][-1] == '2':
						algorithm[x] = None
					else:
						algorithm[x] += '2'
					
					algorithm[x+1] = None
				
			except: pass
			
			try:
				if algorithm[x][0] == algorithm[x+1][0]:
					
					if len(algorithm[x]) == 2 and len(algorithm[x+1]) == 2:
						
						if algorithm[x][-1] == "'" and algorithm[x+1][-1] == '2':
							algorithm[x]   = None
							algorithm[x+1] = algorithm[x+1][:-1]
						elif algorithm[x][-1] == '2' and algorithm[x+1][-1] == "'":
							algorithm[x]   = None
							algorithm[x+1] = algorithm[x+1][:-1]
						
					elif len(algorithm[x]) == 1 and len(algorithm[x+1]) == 2:
						
						if algorithm[x+1][-1] == '2':
							algorithm[x]   = None
							algorithm[x+1] = algorithm[x+1][:-1] + "'"
						elif algorithm[x+1][-1] == "'":
							algorithm[x]   = None
							algorithm[x+1] = None
						
					elif len(algorithm[x]) == 2 and len(algorithm[x+1]) == 1:
						
						if algorithm[x][-1] == "'":
							algorithm[x]   = None
							algorithm[x+1] = None
						elif algorithm[x][-1] == '2':
							algorithm[x]    = None
							algorithm[x+1] += "'"
			except: pass
		
		while None in algorithm: algorithm.remove(None)
		
		return algorithm[::-1]
	
	def setNone(self, lis, ini, end):
		
		for r in range(ini, end):
			lis[r] = None
		
		return lis
	
	def reduce(self, algorithm, subreduce=True):
		
		algorithm = deepcopy(algorithm)
		len_a = len(algorithm)
		
		for z in list(range(1, len_a//2+1))[::-1]:
			
			for y in range(0, len_a-(z*2)+1):
				
				parts = []
				for x in range(len_a//z+1):
					
					ini = y+x*z
					des = y+x*z+z
					
					if des > len_a: break
					
					part = algorithm[ini:des]
					parts.append((part, ini))
				
				cur = []
				qty = 0
				for i, (part, ini) in enumerate(parts):
					
					if None in part:
						if qty >= 1:
							algorithm = self.setNone(algorithm, ini-(z*(qty+1)), ini)
							temp = parts[i-1][0]
							if subreduce: temp = self.reduce(temp)
							algorithm[ini-(z*(qty+1))] = (temp, qty+1)
							qty = 0
						continue
					
					if cur == part:
						qty += 1
						if i == len(parts)-1:
							algorithm = self.setNone(algorithm, ini-(z*qty), ini+z)
							algorithm[ini-(z*qty)] = (part, qty+1)
					else:
						if qty >= 1:
							algorithm = self.setNone(algorithm, ini-(z*(qty+1)), ini)
							temp = parts[i-1][0]
							if subreduce: temp = self.reduce(temp)
							algorithm[ini-(z*(qty+1))] = (temp, qty+1)
							qty = 0
						cur = part
		
		while None in algorithm: algorithm.remove(None)
		
		return algorithm
	
	def logParentheses(self, algorithm):
		
		pass
	
	def showLogs(self):
		
		#--------------------------------------------------
		#Reduce a parentesis cuando hay un patron de movimientos seguidos.
		self.move_logs = self.reduce(self.move_logs)
		#--------------------------------------------------
		
		print('\n Moves:', ('None' if not self.move_logs else ''), end='')
		
		for i, log in enumerate(self.move_logs):
			
			if log.__class__ == tuple:
				# ~ log = self.logParentheses(log)
				print(log, end='')
			else:
				print(log, end='')
			
			if not i == len(self.move_logs)-1:
				
				print(',', end=' ')
		
		if self.is_solved: print('\n\n Status: Solved!', end='')
		
		print('\n')
	
	#===================================================================
	# Generales:
	
	def generateCube(self):
		
		cube = [
			[
				[ 
					col + self.len_c*row + self.pow(self.len_c, 2)*layer + 1
					for col in range(self.len_c)
				]
				for row in range(self.len_c)
			]
			for layer in range(self.len_c)
		]
		
		self.cube_resolve = cube
	
	def getCube(self, layers=['U','F','R','L','B','D']):
		
		text = Fore.WHITE + Style.BRIGHT
		colors = {
			'Negro':    Back.BLACK   + text,
			'Rojo':     Back.RED     + text,
			'Verde':    Back.GREEN   + text,
			'Amarillo': Back.YELLOW  + text,
			'Azul':     Back.BLUE    + text,
			'Morado':   Back.MAGENTA + text,
			'Cyan':     Back.CYAN    + text,
			'Blanco':   Back.WHITE   + text
		}
		reset = Back.RESET + Fore.RESET
		color_list = []
		
		if type(layers) in [list, tuple]:
			for l in layers:
				color_list.append(
					( l, deepcopy(self.cube_colors[l]) )
				)
		out = {}
		for l, z in color_list:
			
			out[l] = []
			out[l].append(' ┌' + '─'*self.adjust + (('─┬'+'─'*self.adjust)*(self.len_c-1)) + '─┐')
			
			for j, y in enumerate(z):
				
				out[l].append(' ')
				
				for i, x in enumerate(y):
					
					layer = self.layers_list[l]['layer']
					
					piece = str(layer[j][i]).rjust(self.adjust) + ' '
					
					try:
						out[l][-1] += '│' + colors[x] + piece + reset
					except KeyError:
						msg_error = 'Color {} is not supported.'.format(x)
						msg_error += '\nUse: Negro, Rojo, Verde, Amarillo, Azul, Morado, Cyan o Blanco.'
						raise self.NotSupported(msg_error)
					
					if i == len(y)-1:
						out[l][-1] += '│'
					
				if 0 <= j < len(z)-1:
					out[l].append(' ├'+'─'*self.adjust + (('─┼'+'─'*self.adjust)*(self.len_c-1)) + '─┤')
				else:
					out[l].append(' └'+'─'*self.adjust + (('─┴'+'─'*self.adjust)*(self.len_c-1)) + '─┘')
		
		return out
	
	def updateLayerList(self):
		
		self.layers_list = {
			'F':  {'layer':self.get_F,  'colors': self.cube_colors['F'], 'desc':'F (Front)' },
			'B':  {'layer':self.get_B,  'colors': self.cube_colors['B'], 'desc':'B (Back)'},
			'R':  {'layer':self.get_R,  'colors': self.cube_colors['R'], 'desc':'R (Rigth)'},
			'L':  {'layer':self.get_L,  'colors': self.cube_colors['L'], 'desc':'L (Left)'},
			'U':  {'layer':self.get_U,  'colors': self.cube_colors['U'], 'desc':'U (Up)'},
			'D':  {'layer':self.get_D,  'colors': self.cube_colors['D'], 'desc':'D (Down)'},
			
			'Fw': {'layer':self.get_Fw, 'desc':'Fw (Front Double)'},
			'Bw': {'layer':self.get_Bw, 'desc':'Bw (Back Double)'},
			'Rw': {'layer':self.get_Rw, 'desc':'Rw (Rigth Double)'},
			'Lw': {'layer':self.get_Lw, 'desc':'Lw (Left Double)'},
			'Uw': {'layer':self.get_Uw, 'desc':'Uw (Up Double)'},
			'Dw': {'layer':self.get_Dw, 'desc':'Dw (Down Double)'},
			
			'f': {'layer':self.get_Fw,  'desc':'f (Front Double)'},
			'b': {'layer':self.get_Bw,  'desc':'b (Back Double)'},
			'r': {'layer':self.get_Rw,  'desc':'r (Rigth Double)'},
			'l': {'layer':self.get_Lw,  'desc':'l (Left Double)'},
			'u': {'layer':self.get_Uw,  'desc':'u (Up Double)'},
			'd': {'layer':self.get_Dw,  'desc':'d (Down Double)'},
			
			'M':  {'layer':self.get_M,  'desc':'M (Middle)'},			# Middle layer turn - in the same direction as an L turn between R and L.
			'E':  {'layer':self.get_E,  'desc':'E (Equatorial)'},		# Equatorial layer - direction as a U turn between U and D.
			'S':  {'layer':self.get_S,  'desc':'S (Standing)'}			# Standing layer - direction as an F turn between F and B.
		}
	
	def reset(self):
		self.cube = deepcopy(self.cube_resolve)
		self.cube_colors = deepcopy(self.cube_colors_resolve)
		self.updateLayerList()
	
	#===================================================================
	# Obtener:
	
	@property
	def get_F(self):
		return self.cube[0]
	
	@property
	def get_B(self):
		return self.invElems(self.cube[-1])
	
	@property
	def get_R(self):
		layer = [[] for _ in range(self.len_c)]
		for z in self.cube:
			for i, y in enumerate(z):
				layer[i].append(y[-1])
		return layer
	
	@property
	def get_L(self):
		layer = [[] for _ in range(self.len_c)]
		for z in self.cube:
			for i, y in enumerate(z):
				layer[i].append(y[0])
		return self.invElems(layer)
	
	@property
	def get_U(self):
		layer = []
		for z in self.cube: layer.append(z[0])
		return layer[::-1]
	
	@property
	def get_D(self):
		layer = []
		for z in self.cube: layer.append(z[-1])
		return layer
	
	@property
	def get_Fw(self):
		return self.get_F+['']+self.cube[1]
	
	@property
	def get_Bw(self):
		layer = []
		c = self.cube[-2]
		for l in c: layer.append(l[::-1])
		return self.get_B+['']+layer
	
	@property
	def get_Rw(self):
		layer = [[] for _ in range(self.len_c)]
		for z in self.cube:
			for i, y in enumerate(z):
				layer[i].append(y[-2])
		return self.get_R+['']+layer
	
	@property
	def get_Lw(self):
		layer = [[] for _ in range(self.len_c)]
		for z in self.cube:
			for i, y in enumerate(z):
				layer[i].append(y[1])
		return self.get_L+['']+self.invElems(layer)
	
	@property
	def get_Uw(self):
		layer = []
		for z in self.cube: layer.append(z[1])
		return self.get_U+['']+layer[::-1]
	
	@property
	def get_Dw(self):
		layer = []
		for z in self.cube: layer.append(z[-2])
		return self.get_D+['']+layer
	
	@property
	def get_M(self):
		layer = [[] for _ in range(self.len_c)]
		for z in self.cube:
			for i, y in enumerate(z):
				layer[i].append(y[self.len_c//2])
		return self.invElems(layer)
	
	@property
	def get_E(self):
		layer = []
		for z in self.cube: layer.append(z[(self.len_c-1)//2])
		return layer
	
	@property
	def get_S(self):
		return self.cube[(self.len_c-1)//2]

#===================================================================

# Algoritmos del Método Fridrich:

class Algorithms:
	
	def __init__(self):
		
		self.Fridrich = self.Fridrich()
	
	class Fridrich:
		
		def __init__(self):
			
			self.PLL = self.PLL()
		
		class PLL:
			
			def __init__(self):
				
				self.cube = Cube()
				values = (
					self.cube,
					self.prettyColors
				)
				
				self.A1 = self.A1(*values)
				self.T  = self.T(*values)
			
			def prettyColors(self, layers=['U','F','R','L','B','D'], with_letters=True):
				
				out = self.cube.getCube()
				
				if 'U' in layers:
					for pos in range(len(out['U'])):
						row  = ' '*(18 if with_letters else 17)
						row += out['U'][pos]
						if pos == 0:
							print(row + ('U' if with_letters else ''))
						else:
							print(row)
				
				for pos in range(len(out['L'])):
					if pos == 0:
						row = ''
						if 'L' in layers:
							row += out['L'][pos] + ('L' if with_letters else '')
						else:
							row += ' '*(18 if with_letters else 17)
						if 'F' in layers:
							row += out['F'][pos] + ('F' if with_letters else '')
						else:
							row += ' '*(18 if with_letters else 17)
						if 'R' in layers:
							row += out['R'][pos] + ('R' if with_letters else '')
						else:
							row += ' '*(18 if with_letters else 17)
						if 'B' in layers:
							row += out['B'][pos] + ('B' if with_letters else '')
						else:
							row += ' '*(18 if with_letters else 17)
					else:
						row = ''
						if 'L' in layers:
							row += out['L'][pos] + (' ' if with_letters else '')
						else:
							row += ' '*(18 if with_letters else 17)
						if 'F' in layers:
							row += out['F'][pos] + (' ' if with_letters else '')
						else:
							row += ' '*(18 if with_letters else 17)
						if 'R' in layers:
							row += out['R'][pos] + (' ' if with_letters else '')
						else:
							row += ' '*(18 if with_letters else 17)
						if 'B' in layers:
							row += out['B'][pos] + (' ' if with_letters else '')
						else:
							row += ' '*(18 if with_letters else 17)
					print(row)
				
				if 'D' in layers:
					for pos in range(len(out['D'])):
						row  = ' '*(18 if with_letters else 17)
						row += out['D'][pos]
						if pos == 0:
							print(row + ('D' if with_letters else ''))
						else:
							print(row)
		
			class A1:
				
				def __init__(self, cube, prettyColors):
					
					self.algo = "(R' F R' B2) (R F' R' B2) R2"
					cube.move(self.algo)
					self.cube = cube.getCube()
					self.prettyColors = prettyColors
					cube.reset()
			
			class T:
				
				def __init__(self, cube, prettyColors):
					
					self.info = '''
					\r	Fridrich PLL: T
					\r	┌───┬───┬───┐
					\r	│   │   │ ↑ │
					\r	├───┼───┼─│─┤
					\r	│ ← ───── → │
					\r	├───┼───┼─│─┤
					\r	│   │   │ ↓ │
					\r	└───┴───┴───┘
					'''
					
					self.algo = "(R U R' U') R' F R2 U' R' U' R U R' F'"
					cube.move(self.algo)
					self.cube = cube.getCube()
					self.prettyColors = prettyColors
					cube.reset()


Algo = Algorithms()

#=======================================================================

# ~ cube = Cube(color_list=['Azul','Verde','Rojo','Morado','Amarillo','Negro'])
# ~ cube.move('(R U R' U')')	# Mueve el cubo virtual
# ~ cube.showLogs()				# Muestra los movimientos realizados
# ~ cube.prettyColors()			# Muestra todas las capas del cubo virtual en su estado actual.

# ~ print(cube['F'])		# Muestra las piezas en la capa.
# ~ print(cube[3,2,1])		# Muestra el número de pieza en la posición y, x, z.
# ~ print(cube['F',2,1])	# Muestra el número de pieza en la capa F con la posicion y, x.
# ~ print(cube['FU'])		# Muestra el número de pieza en la interseccion de las 2 capas.
# ~ print(cube['FUR'])		# Muestra el número de pieza en la interseccion de las 3 capas.

# ~ cube = Cube(color_list=['Verde','Azul','Rojo','Morado','Negro','Amarillo'])
# ~ cube.showPieceEnum(verb=True)

# Mover:

cube = Cube()

T = Algo.Fridrich.PLL.T
# ~ print(T.info)
# ~ print(T.cube)
T.prettyColors()

# ~ cube.move("URU'R'")
# ~ cube.reset()
# ~ cube.showLogs()
# ~ cube.prettyColors()


#=======================================================================

