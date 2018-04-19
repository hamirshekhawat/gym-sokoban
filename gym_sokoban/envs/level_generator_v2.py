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
	boxes=[]
	target_tile_list=[]
	player_initpos=[]
	player_curpos=[]
	score=0
	swap=0
	empty_spaces=0
	
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
	
#----------------------------------------------------------------------
	
	def topology_gen(self, walk_steps):
		dirn=[1,2,3,4]
		x=np.random.randint(1,self.width-2) 
		y=np.random.randint(1,self.height-2)
		d=np.random.randint(1,4)
		self.update_space(x,y,'E')
		for i in range(walk_steps):
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
		for i in range(self.box_num):
			if self.target_tile_list[i][0]==x and self.target_tile_list[i][1]==y:
				return True
			else:
				return False
	
	def which_box(self, x, y):
		for i in range(self.box_num):
			if self.boxes[i][0]==x and self.boxes[i][1]==y:
				return i
				
	def set_player_curpos(self,x,y):
		self.player_curpos=[]
		self.player_curpos.append(x)
		self.player_curpos.append(y)
	
	def update_box_pos(self, i, x, y):
		self.boxes[i][0]=x
		self.boxes[i][1]=y
	
	def make_move(self,x,y, m):
		if(m==1):
			if(self.get_tile(x-1,y)=='E'):
				self.set_tile(x,y,'E')
				self.set_tile(x-1,y,'P')
				self.set_player_curpos(x-1,y)
				return True
		elif(m==2):
			if(self.get_tile(x+1,y)=='E'):
				self.set_tile(x,y,'E')
				self.set_tile(x+1,y,'P')
				self.set_player_curpos(x+1,y)
				return True
		elif(m==3):
			if(self.get_tile(x,y+1)=='E'):
				
				self.set_tile(x,y,'E')
				self.set_tile(x,y+1,'P')
				self.set_player_curpos(x,y+1)
				return True
		elif(m==4):
			if(self.get_tile(x,y-1)=='E'):
				self.set_tile(x,y,'E')
				self.set_tile(x,y-1,'P')
				self.set_player_curpos(x,y-1)
				return True
		elif(m==5):
			if((self.get_tile(x+1,y)=='B' or self.get_tile(x+1,y)=='X') and self.get_tile(x-1,y)=='E'):
				bi=self.which_box(x+1,y)
				if(self.get_tile(x+1,y)=='X'):
					self.set_tile(x+1,y,'T')
				else:
					self.set_tile(x+1,y,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.update_box_pos(bi, x,y)
				self.set_tile(x-1,y,'P')
				self.set_player_curpos(x-1,y)
				return True		
		elif(m==6):
			if((self.get_tile(x-1,y)=='B' or self.get_tile(x-1,y)=='X') and self.get_tile(x+1,y)=='E'):
				bi=self.which_box(x-1,y)
				if(self.get_tile(x-1,y)=='X'):
					self.set_tile(x-1,y,'T')
				else:
					self.set_tile(x-1,y,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.update_box_pos(bi, x,y)
				self.set_tile(x+1,y,'P')
				self.set_player_curpos(x+1,y)
				return True
		elif(m==7):#down
			if((self.get_tile(x,y-1)=='B' or self.get_tile(x,y-1)=='X') and self.get_tile(x,y+1)=='E'):
				bi=self.which_box(x,y-1)
				if(self.get_tile(x,y-1)=='X'):
					self.set_tile(x,y-1,'T')
				else:
					self.set_tile(x,y-1,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.update_box_pos(bi, x,y)
				self.set_tile(x,y+1,'P')
				self.set_player_curpos(x,y+1)
				return True
		elif(m==8):
			if((self.get_tile(x,y+1)=='B' or self.get_tile(x,y+1)=='X') and self.get_tile(x,y-1)=='E'):
				bi=self.which_box(x,y+1)
				if(self.get_tile(x,y+1)=='X'):
					self.set_tile(x,y+1,'T')
				else:
					self.set_tile(x,y+1,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.update_box_pos(bi, x,y)
				self.set_tile(x,y-1,'P')
				self.set_player_curpos(x,y-1)
				return True
		elif(m==-5):
			bi=self.which_box(x+1,y)#updattetetwgfnbhfu
			if self.is_target_tile(x,y):
				self.set_tile(x,y,'T')
			else:
				self.set_tile(x,y,'E')
			self.set_tile(x+1,y,'P')
			self.set_player_curpos(x+1,y)
			if self.is_target_tile(x+2,y):
				self.set_tile(x+2,y,'X')
			else:
				self.set_tile(x+2,y,'B')
			self.update_box_pos(bi,x+2,y)
			return True
		elif(m==-6):
			bi=self.which_box(x-1,y)
			if self.is_target_tile(x,y):
				self.set_tile(x,y,'T')
			else:
				self.set_tile(x,y,'E')
			self.set_tile(x-1,y,'P')
			self.set_player_curpos(x-1,y)
			if self.is_target_tile(x-2,y):
				self.set_tile(x-2,y,'X')
			else:
				self.set_tile(x-2,y,'B')
			self.update_box_pos(bi,x-2,y)
			return True
		elif(m==-7):
			bi=self.which_box(x,y-1)
			if self.is_target_tile(x,y):
				self.set_tile(x,y,'T')
			else:
				self.set_tile(x,y,'E')
			self.set_tile(x,y-1,'P')
			self.set_player_curpos(x,y-1)
			if self.is_target_tile(x,y-2):
				self.set_tile(x,y-2,'X')
			else:
				self.set_tile(x,y-2,'B')
			self.update_box_pos(bi,x,y-2)
			return True
		elif(m==-8):
			bi=self.which_box(x,y+1)
			if self.is_target_tile(x,y):
				self.set_tile(x,y,'T')
			else:
				self.set_tile(x,y,'E')
			self.set_tile(x,y+1,'P')
			self.set_player_curpos(x,y+1)
			if self.is_target_tile(x,y+2):
				self.set_tile(x,y+2,'X')
			else:
				self.set_tile(x,y+2,'B')
			self.update_box_pos(bi,x,y+2)
			return True
			
			
			
	def position_configuration(self):
		#boxes config
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
		#player config
		while(True):
			x=np.random.randint(1,self.width-2) 
			y=np.random.randint(1,self.height-2)
			if(self.get_tile(x,y)=='E'):
				self.set_tile(x,y,'P')
				self.set_player_curpos(x,y)
				break
			else:
				continue
	
	def reset_position_configuration(self):
		for i in range(self.box_num):
			self.set_tile(self.boxes[i][0],self.boxes[i][1], 'E')
		self.set_tile(self.player_initpos[0],self.player_initpos[1], 'E')
		self.set_tile(self.player_curpos[0],self.player_curpos[1], 'E') 	
	
	
	def create_config_obj(self):
		pos_conf=[]
		for i in range(self.box_num):
			pos_conf.append(self.boxes[i][0])
			pos_conf.append(self.boxes[i][1])
		pos_conf.append(self.player_curpos[0])
		pos_conf.append(self.player_curpos[1])
		return tuple(pos_conf)
		
	'''		
	def reverse_play(self):
		
			to calculate the total number of configs, the best way is to 
			caculate the permuations of selecting num_boxes+1 elements 
			from total empty spaces
		
				
		for i in range(self.height):
			for j in range(self.width):
				if(self.get_tile(i,j) == 'E'):
					self.empty_spaces+=1
		'''	
 				

class Tree:
	root=[]
	def __init__(self):
		
		self.child=[]
		self.data=[]
	
	def create_children(self, amount):
		for i in range(amount):
			self.child.append(Tree())
	
	def set_children_values(self,lis):
		for i in range(len(lis)):
			self.data.append(lis[i])


def create_config_tree(room):
	moves=[1,2,3,4,5,6,7,8]
	moves_made=[]
	explored=set()
	conf_tree=Tree()
	conf_tree.root=room.create_config_obj()
	conf_tree.create_children(8)
	explored.add(tuple(room.create_config_obj()))
	print(explored)
	rn.shuffle(moves)
	for m in moves:
		mm=room.make_move(room.player_curpos[0],room.player_curpos[1],m) #mm: move made bool
		c=room.create_config_obj()
		if tuple(c) not in explored:
			print("move:"+str(m))
			room.print_room()
			explored.add(tuple(c))
			print(explored)
			moves_made.append(tuple(c))
		if m<5 and m%2==0 and mm:
			m-=1
			room.make_move(room.player_curpos[0],room.player_curpos[1],m)
		elif m<5 and mm:
			m+=1
			room.make_move(room.player_curpos[0],room.player_curpos[1],m)
		elif mm:
			m=m*-1
			room.make_move(room.player_curpos[0],room.player_curpos[1],m)
	conf_tree.set_children_values(moves_made)
	
	'''				
	while(True):
		x=room.player_curpos[0]
		y=room.player_curpos[1]
		rn.shuffle(moves)
		
		for m in moves:
			room.make_move(room.player_curpos[0],room.player_curpos[0],m)	
			if room.create_config_obj() not in explored:
				explored.add(room.create_config_obj())
				
	'''	
		
def create_initial_config(width, height, n_box):
	rm=[]
	in_rtp=[]
	for i in range(10):
		rm.append(Room(height,width,n_box))			
		rm[i].topology_gen(int(1.5*(height+width)))
		for j in range(10):
			rm[i].position_configuration()
			in_rtp.append(rm[i].create_config_obj())
			
			#start doing tree search here
			
			
			
		
rm=Room(10,10,2)
rm.topology_gen(int(1.5*(20)))
rm.position_configuration()
rm.print_room()
create_config_tree(rm)			


			
	
		
		
'''
notes:
should the level be generated such that the number empty spaces can be adjusted rather than just keeping it as default 1.5(h+w)
'''		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
