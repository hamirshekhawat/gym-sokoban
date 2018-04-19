import numpy as np
import random as rn


class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass

class BoxAndEmptySpaceError(Error):
	def __init__(self, message):
		self.message = message
		
			
'''	
class Player:
	init_x=-1
	init_y=-1
	x=-1
	y=-1
	
	def __init__(self, x, y):
		init_x=x
		init_y=y	
	
	def move(new_x, new_y):
		x=new_x
		y=new_y
	
'''

	
class Room:
	boxex=[]
	target_tile_list=[]
	player_initpos=()
	player_curpos=()
	score=0
	swap=0
	
	def __init__(self, height, width, box_num):
		self.width=width
		self.height=height
		self.box_num=box_num
		self.room = np.full((height,width), 'W')
		
	def print_room(self):
		print(self.room)

	def choose_random_dir(self, d):
		'''select a new direction and then check yes(35%) and no(65%). 
		If yes, change, else dont'''
		d1=np.random.randint(1,4)
		b = [0,1]
		c=np.random.choice(b,1,p=[0.65,0.35])
		if(c):
			return d1
		else:
			return d
	def get_tile(self, x, y):
		return self.room[y][x]
	
	def set_tile(self, x, y, c):
		self.room[y][x]=c
	
	def update_space(self, x, y, sym):	
		if(x<=0 or x>=self.width-1 or y<=0 or y>=self.height-1):
			
			return False
		else:
			self.set_tile(x,y,sym)
			return True
	
	def topology_gen(self, walk_steps):
		dirn=[1,2,3,4]
		x=np.random.randint(1,self.width-2) 
		y=np.random.randint(1,self.height-2)
		d=np.random.randint(1,4)
		self.update_space(x,y,'E')
		for i in range(walk_steps):
			print("in topology core:"+str(i))
			t=np.random.randint(1,5)
			if(t==1):
				self.update_space(x-1, y, 'E')
				self.update_space(x+1, y, 'E')
			elif(t==2):
				self.update_space(x, y+1, 'E')
				self.update_space(x, y-1, 'E')
			elif(t==3):
				self.update_space(x-1, y, 'E')
				self.update_space(x, y-1, 'E')
			elif(t==4):
				self.update_space(x, y-1, 'E')
				self.update_space(x-1, y-1, 'E')
				self.update_space(x-1, y, 'E')
			elif(t==5):
				self.update_space(x+1, y, 'E')
				self.update_space(x, y-1, 'E')
			d=self.choose_random_dir(d)
			if(d==1):
				x=x-1
			elif(d==2):
				x=x+1
			elif(d==3):
				y=y-1
			elif(d==4):
				y=y+1
			if(self.update_space(x,y,'E')):
				continue
			else:
				if(d==1):
					x=x+1
				elif(d==2):
					x=x-1
				elif(d==3):
					y=y+1
				elif(d==4):
					y=y-1	
				i-=1
	
	def is_target_tile(self, x, y):
		for i in range(box_num):
			if self.target_tile_list[i][0]==x and self.target_tile_list[i][1]==y:
				return True
			else:
				return False
	
	def make_move(self,x,y, m):
		if(m==1):
			if(self.get_tile(x-1,y)=='E'):
				player_curpos=(x-1,y)
				self.set_tile(x,y,'E')
				self.set_tile(x-1,y,'P')
		elif(m==2):
			if(self.get_tile(x+1,y)=='E'):
				player_curpos=(x+1,y)
				self.set_tile(x,y,'E')
				self.set_tile(x+1,y,'P')
		elif(m==3):
			if(self.get_tile(x,y+1)=='E'):
				player_curpos=(x,y+1)
				self.set_tile(x,y,'E')
				self.set_tile(x,y+1,'P')
		elif(m==4):
			if(self.get_tile(x,y-1)=='E'):
				player_curpos=(x,y-1)
				self.set_tile(x,y,'E')
				self.set_tile(x,y-1,'P')
		elif(m==5):
			if((self.get_tile(x+1,y)=='B' or self.get_tile(x+1,y)=='X') and self.get_tile(x-1,y)=='E'):
				player_curpos=(x-1,y)
				if(self.get_tile(x+1,y)=='X'):
					self.set_tile(x+1,y,'T')
				else:
					self.set_tile(x+1,y,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.set_tile(x-1,y,'P')
				
		elif(m==6):
			if((self.get_tile(x-1,y)=='B' or self.get_tile(x-1,y)=='X') and self.get_tile(x+1,y)=='E'):
				player_curpos=(x+1,y)
				if(self.get_tile(x-1,y)=='X'):
					self.set_tile(x-1,y,'T')
				else:
					self.set_tile(x-1,y,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.set_tile(x+1,y,'P')
		elif(m==7):
			if((self.get_tile(x,y-1)=='B' or self.get_tile(x,y-1)=='X') and self.get_tile(x,y+1)=='E'):
				player_curpos=(x,y+1)
				if(self.get_tile(x,y-1)=='X'):
					self.set_tile(x,y-1,'T')
				else:
					self.set_tile(x,y-1,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.set_tile(x,y+1,'P')
		elif(m==8):
			if((self.get_tile(x,y+1)=='B' or self.get_tile(x,y+1)=='X') and self.get_tile(x,y-1)=='E'):
				player_curpos=(x,y-1)
				if(self.get_tile(x,y+1)=='X'):
					self.set_tile(x,y+1,'T')
				else:
					self.set_tile(x,y+1,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.set_tile(x,y-1,'P')
			
			
	def position_configuration(self):
		for i in range(self.box_num):
			while(True):
				x=np.random.randint(1,self.width-2) 
				y=np.random.randint(1,self.height-2)
				if(self.get_tile(x,y)=='E'):
					self.target_tile_list.append((x,y))
					self.set_tile(x,y,'X') #setting this as X cuz initially B is on T. S
					self.boxes.append([x,y])
					break
				else:
					continue
		
		while(True):
			x=np.random.randint(1,self.width-2) 
			y=np.random.randint(1,self.height-2)
			if(self.get_tile(x,y)=='E'):
				self.target_tile_list.append((x,y))
				self.set_tile(x,y,'P')
				player_initpos=(x,y)
				player_curpos=(x,y)
				break
			else:
				continue
			
			
	'''
	    Reverse play requires you to create a set of boxes/player configs to be stored in a set.
	    Question is when to stop?
	    the max depth of the tree is to be known by permutations.
	    it's DFS so stacks. An efficient stack of lists of box+1 element and a set. Add in stack only if its a new config.
	'''
			
			
			
			
			
			
			
			
height=10
width=10
rm=Room(height,width,2)
rm.topology_gen(int(1.5*(height+width)))		
rm.position_configuration()		
rm.print_room()			
		
		
'''
notes:
should the level be generated such that the number empty spaces can be adjusted rather than just keeping it as default 1.5(h+w)
'''		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
