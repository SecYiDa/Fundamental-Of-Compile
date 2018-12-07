
#coding:= utf-8
from math import *
import matplotlib.pyplot as plt

Type = ['ORIGIN','SCALE','ROT','IS','TO','STEP','DRAW',
			'FOR','FROM','T','SEMICO','L_BRACKET','R_BRACKET',
			'COMMA','PLUS','MINUS','MUL','DIV','POWER','FUNC',
			'CONST_ID','NONTOKEN','ERRTOKEN','WHITE_SPACE']

tokenTabType = ['CONST_ID','CONST_ID','T','FUNC','FUNC','FUNC',
				'FUNC','FUNC','FUNC','ORIGIN','SCALE','ROT','IS',
				'FOR','FROM','TO','STEP','DRAW']

tokenTabInput = ['PI','E','T','SIN','COS','TAN','LN','EXP','SQRT',
				'ORIGIN','SCALE','ROT','IS','FOR','FROM','TO',
				'STEP','DRAW']

Value = [3.1415926,2.71828,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
				0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

Address = ['null','null','null','sin','cos','tan','log','exp',
				'sqrt','null','null','null','null','null','null',
				'null','null','null']

class Scanner:
	def __init__(self):
		self.Token = 'null'
		self.Type = 'null'
		self.Value = 0.0
		self.Address = 'null'

	def getToken(self,stream):
		if len(stream) == 0:
			exit(0)
		i = 0
		temp = []
		ch = stream[0]
		if ch.isalpha():
			s = 1
			while(1):
				temp.append(ch)
				i = i + 1
				if i == len(stream):
					break
				ch = stream[i]
				if not ch.isalpha():
					i = i - 1
					break
			if ''.join(temp) in tokenTabInput:
				self.Token = ''.join(temp)
				self.tokenTabInput = ''.join(temp)
				self.location = tokenTabInput.index(''.join(temp))
				self.tokenTabType = tokenTabType[self.location]
				self.Value = Value[self.location]
				self.Address = Address[self.location]
				self.Type = self.tokenTabType
				return i+1
			else:
				print("Token error!")
				exit(-1)
		elif ch.isdigit():
			s = 2
			while(1):
				temp.append(ch)
				i = i+1
				if i == len(stream):
					break
				ch = stream[i]
				if not ch.isdigit() and ch != '.':
					i = i - 1
					break
				if ch == '.' and s == 2:
					s = 3
					continue
				if ch == '.' and s == 3:
					print("Digit error!")
					exit(-1)
			self.Token = ''.join(temp)
			self.Type = 'CONST_ID'
			self.Value = float(self.Token)
			self.Address = 'null'
			return i+1
		elif ch.isalpha():
			s = 1
			while(1):
				temp.append(ch)
				i = i + 1
				if i == len(stream):
					break
				ch = stream[i]
				if not ch.isalpha():
					i = i - 1
					break
			if ''.join(temp) in tokenTabInput:
				self.Token = ''.join(temp)
				self.tokenTabInput = ''.join(temp)
				self.location = tokenTabInput.index(''.join(temp))
				self.tokenTabType = tokenTabType[self.location]
				self.Value = Value[self.location]
				self.Address = Address[self.location]
				self.Type = self.tokenTabType
				return i+1
			else:
				print("Token error!")
				exit(-1)	
		elif ch == '*':
			if len(stream) != 1 and stream[1] == '*':
				self.Token = '**'
				self.Type = 'POWER'
				self.Value = 0.0
				self.Address = 'null'
				return 2
			else:
				self.Token = '*'
				self.Type = 'MUL'
				self.Value = 0.0
				self.Address = 'null'
				return 1
		elif ch == '/':
			if len(stream) != 1 and stream[1] == '/':
				self.Token = '//'
				self.Type = 'COMMENT'
				self.Value = 0.0
				self.Address = 'null'
				return stream.index('\n')+1
			else:
				self.Token = '/'
				self.Type = 'DIV'
				self.Value = 0.0
				self.Address = 'null'
				return 1
		elif ch == '-':
			if len(stream) != 1 and stream[1] == '-':
				self.Token = '--'
				self.Type = 'COMMENT'
				self.Value = 0.0
				self.Address = 'null'
				return stream.index('\n')+1
			else:
				self.Token = '-'
				self.Type = 'MINUS'
				self.Value = 0.0
				self.Address = 'null'
				return 1
		elif ch == '+':
			self.Token = '+'
			self.Type = 'PLUS'
			self.Value = 0.0
			self.Address = 'null'
			return 1
		elif ch == ',':
			self.Token = ','
			self.Type = 'COMMA'
			self.Value = 0.0
			self.Address = 'null'
			return 1
		elif ch == ';':
			self.Token = ';'
			self.Type = 'SEMICO'
			self.Value = 0.0
			self.Address = 'null'
			return 1
		elif ch == '(':
			self.Token = '('
			self.Type = 'L_BRACKET'
			self.Value = 0.0
			self.Address = 'null'
			return 1
		elif ch == ')':
			self.Token = ')'
			self.Type = 'R_BRACKET'
			self.Value = 0.0
			self.Address = 'null'
			return 1
		elif ch == '\n' or ch == ' ' or ch == '\t':
			self.Token = ch
			self.Type = 'WHITE_SPACE'
			self.Value = 0.0
			self.Address = 'null'
			return 1
		else:
			print('Token Error!')
			exit(-1)
			return -1


class Token:
	def __init__(self,T,Tstr,Tvalue,Tpoint):
		self.Type = T
		self.Token = Tstr
		self.Value = Tvalue
		self.Address = Tpoint

class Tree:
	def __init__(self,Token):
		self.Type = Token
		if self.Type in ['PLUS','MINUS','MUL','DIV','POWER']:
			self.leftChild = None
			self.rightChild = None
		elif self.Type == 'CONST_ID':
			self.value = 0.0
		elif self.Type == 'T':
			self.T = None
		elif self.Type == 'FUNC':
			self.child = None
			self.function = None



class Parse:
	def __init__(self,Ts):
		self.Token = None
		self.tokens = Ts
		self.p = 0
		self.flag = 0
		self.parameter = 0
		self.origin_x = 0
		self.origin_y = 0
		self.rot_ang = 0
		self.scale_x = 1
		self.scale_y = 1
		self.Tvalue = 0
		self.draw_List = []

	def BuildTree(self,Token,*arg):
		exprNode = Tree(Token)
		if Token == 'CONST_ID':
			exprNode.value = arg[0]
		elif Token == 'T':
			return exprNode
		elif Token == 'FUNC':
			exprNode.child = arg[1]
			exprNode.function = arg[0]
		else:
			exprNode.leftChild = arg[0]
			exprNode.rightChild = arg[1]
		return exprNode

	def fetchToken(self):
		return self.tokens[self.p]

	def program(self):
		while(1):
			self.flag = 0
			self.Token = self.fetchToken()
			if self.Token.Type == 'NONTOKEN':
				break
			self.statement()
			self.flag = 1
			self.matchToken('SEMICO')

	def statement(self):
		if self.Token.Type == 'ORIGIN':
			self.originStatement()
		elif self.Token.Type == 'SCALE':
			self.scaleStatement()
		elif self.Token.Type == 'ROT':
			self.rotStatement()
		else:
			self.forStatement()

	def originStatement(self):
		self.matchToken('ORIGIN')
		self.matchToken('IS')
		self.matchToken('L_BRACKET')
		left_ptr = self.expression()
		self.printTree(left_ptr,0)
		print("*"*20)
		self.matchToken('COMMA')
		right_ptr = self.expression()
		self.printTree(right_ptr,0)
		print("*"*20)
		self.matchToken('R_BRACKET')
		self.origin_x = self.Calculate(left_ptr)
		self.origin_y = self.Calculate(right_ptr)

	def scaleStatement(self):
		self.matchToken('SCALE')
		self.matchToken('IS')
		self.matchToken('L_BRACKET')
		Scale_X_Expr = self.expression()
		self.matchToken('COMMA')
		Scale_Y_Expr = self.expression()
		self.matchToken('R_BRACKET')
		self.scale_x = self.Calculate(Scale_X_Expr)
		self.scale_y = self.Calculate(Scale_Y_Expr)

	def rotStatement(self):
		self.matchToken('ROT')
		self.matchToken('IS')
		rot_ptr = self.expression()
		self.printTree(rot_ptr,0)
		print("*"*20)
		self.rot_ang = self.Calculate(rot_ptr)

	
	def forStatement(self):
		self.matchToken('FOR')
		self.matchToken('T')
		self.matchToken('FROM')
		start_vlaue = self.expression()
		self.matchToken('TO')
		end_value = self.expression()
		self.matchToken('STEP')
		step_ptr = self.expression()
		self.matchToken('DRAW')
		self.matchToken('L_BRACKET')
		x_Value = self.expression()
		self.matchToken('COMMA')
		y_Value = self.expression()
		self.matchToken('R_BRACKET')
		self.draw(start_vlaue,end_value,step_ptr,x_Value,y_Value)

	def expression(self):
		left = self.term()
		while(1):
			if self.Token.Type == 'PLUS' or self.Token.Type == 'MINUS':
				Token_Tmp = self.Token
				self.matchToken(self.Token.Type)
				right = self.term()
				left = self.BuildTree(Token_Tmp.Type,left,right)
			else:
				break
		return left

	def term(self):
		left = self.factor()
		while(1):
			if self.Token.Type == 'MUL' or self.Token.Type == 'DIV':
				Token_Tmp = self.Token
				self.matchToken(self.Token.Type)
				right = self.factor()
				left = self.BuildTree(Token_Tmp.Type,left,right)
			else:
				break
		return left

	def factor(self):
		if self.Token.Type == 'PLUS':
			self.matchToken('PLUS')
			tree = self.factor()
		elif self.Token.Type == 'MINUS':
			self.matchToken('MINUS')
			padding = Tree('CONST_ID')
			padding.Value = 0.0
			right = self.factor()
			tree = self.BuildTree('MINUS',padding,right)
		else:
			tree = self.component()
		return tree

	def component(self):
		left = self.atom()
		Token_Tmp = 'null'
		if self.p != len(self.tokens)-1:
			Token_Tmp = self.tokens[self.p]
		if Token_Tmp.Type == 'POWER':
			self.matchToken('POWER')
			right = self.component()
			left = self.BuildTree('POWER',left,right)
		return left

	def atom(self):
		if self.Token.Type == 'CONST_ID':
			Token_Tmp = self.Token
			self.matchToken('CONST_ID')
			tree = self.BuildTree('CONST_ID',Token_Tmp.Value)
		elif self.Token.Type == 'T':
			Token_Tmp = self.Token
			self.matchToken('T')
			tree = self.BuildTree('T')
		elif self.Token.Type == 'FUNC':
			Token_Tmp = self.Token
			self.matchToken('FUNC')
			self.matchToken('L_BRACKET')
			tree = self.BuildTree('FUNC',Token_Tmp.Address,self.expression())
			self.matchToken('R_BRACKET')
		else:
			self.matchToken('L_BRACKET')
			tree = self.expression()
			self.matchToken('R_BRACKET')
		return tree

	def matchToken(self,tok):
		self.Token = self.tokens[self.p]
		self.p = self.p + 1
		error = []  
		if self.Token.Type != tok:
			print(tok+"\n")
			for i in range(self.p-3,self.p+3):
				error.append(self.tokens[i].Token)
			print('[!] Error\n')
			print("[!] 错误在\033[32m %s \033[0m附近\n"%(''.join(error)))
			exit(-1)
		if self.p == len(self.tokens) and self.flag == 0:
			print('[!] 代码不完整\n')
			exit(-1) 
		elif self.p == len(self.tokens) and self.flag == 1:
			print('[!] 结束\n')
			plt.plot(*self.draw_List)
			plt.show()

			exit(0) 
		else:
			self.Token = self.fetchToken()
		
	def printTree(self,tree,blank):
		for i in range(0,blank):
			print ('  ',end='')
		if tree.Type in  ['PLUS','MINUS','MUL','DIV','POWER']:
			print(tree.Type)
			if tree.leftChild != None:
				self.printTree(tree.leftChild,blank+1)
			if tree.rightChild != None:
				self.printTree(tree.rightChild,blank+1)
		elif tree.Type == 'FUNC':
			print(tree.function)
			if tree.child != None:
				self.printTree(tree.child,blank+1)
		elif tree.Type == 'CONST_ID':
			print(tree.value)
		elif tree.Type == 'T':
			print('T')
			if tree.T != None:
				self.printTree(tree.T,blank+1)
	
	def Calculate(self,tree):
		if tree.Type == 'PLUS':
			leftValue = self.Calculate(tree.leftChild)
			rightValue = self.Calculate(tree.rightChild)
			return leftValue + rightValue
		if tree.Type == 'MINUS':
			leftValue = self.Calculate(tree.leftChild)
			rightValue = self.Calculate(tree.rightChild)
			return leftValue - rightValue
		if tree.Type == 'MUL':
			leftValue = self.Calculate(tree.leftChild)
			rightValue = self.Calculate(tree.rightChild)
			return leftValue * rightValue
		if tree.Type == 'DIV':
			leftValue = self.Calculate(tree.leftChild)
			rightValue = self.Calculate(tree.rightChild)
			if rightValue == 0:
				print('Error: Divided by zero!')
				exit(-1)
			return leftValue / rightValue
		if tree.Type == 'POWER':
			leftValue = self.Calculate(tree.leftChild)
			rightValue = self.Calculate(tree.rightChild)
			return leftValue**rightValue
		if tree.Type == 'FUNC':
			return eval(tree.function)(self.Calculate(tree.child))
		if tree.Type == 'CONST_ID':
			return tree.value
		if tree.Type == 'T':
			return eval('self.Tvalue')

	def draw(self,start_vlaue,end_value,step_ptr,x_Value,y_Value):
		T_start = self.Calculate(start_vlaue)
		T_end = self.Calculate(end_value)
		step = self.Calculate(step_ptr)
		self.Tvalue = T_start   #init
		xs = []
		ys = []
		while self.Tvalue < T_end:
			x = self.Calculate(x_Value)
			y = self.Calculate(y_Value)
			temp_x = x*self.scale_x
			temp_y = y*self.scale_y
			temp = temp_x*cos(self.rot_ang)+temp_y*sin(self.rot_ang)
			temp_y = temp_y*cos(self.rot_ang)-temp_x*sin(self.rot_ang)
			temp_x = temp
			Now_x = temp_x + self.origin_x
			Now_y = temp_y + self.origin_y
			xs.append(Now_x)
			ys.append(Now_y)
			self.Tvalue = self.Tvalue + step
		x = self.Calculate(x_Value)
		y = self.Calculate(y_Value)
		temp_x = x*self.scale_x
		temp_y = y*self.scale_y
		temp = temp_x*cos(self.rot_ang)+temp_y*sin(self.rot_ang)
		temp_y = temp_y*cos(self.rot_ang)-temp_x*sin(self.rot_ang)
		temp_x = temp
		Now_x = temp_x + self.origin_x
		Now_y = temp_y + self.origin_y
		xs.append(Now_x)
		ys.append(Now_y)
		self.Tvalue = self.Tvalue + step
		self.draw_List.append(xs)
		self.draw_List.append(ys)
	


if __name__ == '__main__':
	fileName = input("[+] PLZ Input File:")
	plt.figure()
	with open(fileName,'r') as fp:
		Context = fp.read()
		Context = Context.upper()
		TokenStream = []
		Scanner = Scanner()
	print("\033[35m[+] 记号流\n")
	while(1):
		p = Scanner.getToken(Context)
		if(p>=len(Context)):
			break
		if Scanner.Type != 'WHITE_SPACE':
			TokenStream.append(Token(Scanner.Type,Scanner.Token,Scanner.Value,Scanner.Address))
		Context = Context[p:]

	for i in range(0,len(TokenStream)):
		print("%12s%12s%12f%12s" % (TokenStream[i].Type,TokenStream[i].Token,TokenStream[i].Value,TokenStream[i].Address))
	print("\033[32m[+] 语法树\n\033[0m")
	cp = Parse(TokenStream)
	cp.program()
	