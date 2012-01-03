"""
	author: Fabian Faessler (Samuirai)
	email: fabi@fabif.de
	description: robot who collects trash cans
"""
import random
from Tkinter import * 

"""
The GENOME. It's a string with a lenght of _life. integers between 0-7 describe the behaviour.
The robot always wants to go to a trash can (he sees the 4 blocks up, right, down and left).
For example if the next step is a 0, he will go up, if on this field is trash. If there is no trash
around him, he also will go up. if only trash is on his right, he will go right.
0-3 normal step towards trash in a direction
4-7 normal step towards trash and also pick it up
	0 : up
	1 : right
	2 : down
	3 : left
	4 : up (and pick up)
	5 : right (and pick up)
	6 : down (and pick up)
	7 : left (and pick up)
"""

# settings:
_life = 100 #genome lenght = step lenght
_x = 10 # field size
_y = 10 # field size
_wallPoint = -10 # points when he hit a wall
_trashPoint = 20 # points for collect trash
_walkPoint = -1 # points for do a normal step

# creates a random genome
def createGenome(anz=10):
	genome = ""
	for i in xrange(0,anz): genome += str(random.randint(0,7))
	return genome

# a robot
class Robot:
	def __init__(self):
		self.age = 0
		self.genome = createGenome(_life)
		self.points = 0	
		self.x = _x/2
		self.y = _y/2

field = []

def generateField():
	_field = [
		['X','X','X','X','X','X','X','X','X','X'],
		['X','0','0','0','0','0','0','1','0','X'],
		['X','0','1','0','1','0','1','1','1','X'],
		['X','0','1','0','1','0','0','1','0','X'],
		['X','0','1','0','1','1','0','0','0','X'],
		['X','0','1','1','1','0','1','1','0','X'],
		['X','0','0','0','0','0','1','1','0','X'],
		['X','0','1','1','0','0','1','1','0','X'],
		['X','0','0','1','1','1','0','0','0','X'],
		['X','X','X','X','X','X','X','X','X','X'],
	]
	return _field
    # random generated field:
	"""_field = []
	for x in xrange(0,_x):
		tmp = []
		for y in xrange(0,_y):
			if y == 0 or y == _y-1 or x == 0 or x == _x-1: tmp.append('X')
			else: tmp.append(str(random.randrange(2)))
		_field.append(tmp)
	return _field"""

#renders the field with characters
def render(robot):
	countX,countY = 0,0
	line = ""
	for x in field:
		countY = 0
		for y in x:
			#print str(robot.x)+'/'+str(robot.y)+' == '+str(countY)+'/'+str(countX)
			if countY == robot.y and countX == robot.x:
				line += ' '
			else:
				line += str(y)
			countY += 1
		countX += 1
		print line
		line = ""
	
		
		
# moves the robot in a specific direction
def robotMove(robot,dir):
	robot.age += 1
	if dir == 0:
		if field[robot.y-1][robot.x] == 'X':
			robot.points += _wallPoint
		else:
			robot.y-=1
			robot.points += _walkPoint
	elif dir == 1:
		if field[robot.y][robot.x+1] == 'X':
			robot.points += _wallPoint
		else:
			robot.x+=1
			robot.points += _walkPoint
	elif dir == 2:
		if field[robot.y+1][robot.x] == 'X':
			robot.points += _wallPoint
		else:
			robot.y+=1
			robot.points += _walkPoint
	elif dir == 3:
		if field[robot.y][robot.x-1] == 'X':
			robot.points += _wallPoint
		else:
			robot.x-=1
			robot.points += _walkPoint
	elif dir == 4:
		if field[robot.y-1][robot.x] == 'X':
			robot.points += _wallPoint
		else:
			if field[robot.y-1][robot.x] == '1':
				field[robot.y-1][robot.x] = '0'
				robot.points += _trashPoint
			robot.y-=1
			robot.points += _walkPoint
	elif dir == 5:
		if field[robot.y][robot.x+1] == 'X':
			robot.points += _wallPoint
		else:
			if field[robot.y][robot.x+1] == '1':
				field[robot.y][robot.x+1] = '0'
				robot.points += _trashPoint
			robot.x+=1
			robot.points += _walkPoint
	elif dir == 6:
		if field[robot.y+1][robot.x] == 'X':
			robot.points += _wallPoint
		else:
			if field[robot.y+1][robot.x] == '1':
				field[robot.y+1][robot.x] = '0'
				robot.points += _trashPoint
			robot.y+=1
			robot.points += _walkPoint
	elif dir == 7:
		if field[robot.y][robot.x-1] == 'X':
			robot.points += _wallPoint
		else:
			if field[robot.y][robot.x-1] == '1':
				field[robot.y][robot.x-1] = '0'
				robot.points += _trashPoint
			robot.x-=1
			robot.points += _walkPoint
	if robby.points<0: robby.points = 0
		
# let the life grow. The life of a robot is simulated here
def run(robot,debug):
	if debug: render(robot)
	for step in robot.genome:
		eye = [0,0,0,0]
		if field[robot.y-1][robot.x] == '1':
			eye[0] = 1
		elif field[robot.y][robot.x+1] == '1':
			eye[1] = 1
		elif field[robot.y+1][robot.x] == '1':
			eye[2] = 1
		elif field[robot.y][robot.x-1] == '1':
			eye[3] = 1
			
		if int(step) < 4:
			if eye[int(step)] == 1:
				robotMove(robot,int(step))
			elif eye[0] == 1:
				robotMove(robot,0)
			elif eye[1] == 1:
				robotMove(robot,1)
			elif eye[2] == 1:
				robotMove(robot,2)
			elif eye[3] == 1:
				robotMove(robot,3)
			else:
				robotMove(robot,int(step))
		elif int(step) >= 4:
			if eye[int(step)%4] == 1:
				robotMove(robot,int(step))
			elif eye[0] == 1:
				robotMove(robot,0)
			elif eye[1] == 1:
				robotMove(robot,1)
			elif eye[2] == 1:
				robotMove(robot,2)
			elif eye[3] == 1:
				robotMove(robot,3)
			else:
				robotMove(robot,int(step))
		if debug: 
			#print ''
			#render(robot)
			renderGui(robot)
		
def sortDict(dic):
    keys = dic.keys()
    keys.sort()
    return map(dic.get, keys)

# evolution through cross ofer of genomes   
def crossover(genome1,genome2,life):
	cut = random.randint(1,life-1)
	part11 = genome1[0:cut]
	part12 = genome1[cut:life]
	part21 = genome2[0:cut]
	part22 = genome2[cut:life]
	return((part11+part22),(part21+part12))

# evolution through mutation
def mutation(genome1,life):
	genome1 = list(genome1)
	for i in xrange(0,life/10): genome1[random.randint(1,life-1)] = str(random.randint(0,7))
	return str(genome1).replace('[','').replace(']','').replace(',','').replace('\'','').replace(' ','')

master = Tk()

# tkInter foo fuer die GUI Animation
w = Canvas(master, width=500, height=500)
w.pack()
import tkFont
helv36 = tkFont.Font ( family="Courier New", size=14, )
field = generateField()

# zeig die Roboter GUI an
def renderGui(robot):
	w.delete("all")
	w.create_rectangle(0, 0, 800, 500, fill="black")
	for x in xrange(0,_x):
		w.create_line(x*50, 0, x*50, 500)
		w.create_line(0, x*50, 500, x*50)
	countX,countY = 0,0
	line = ""
	for x in field:
		countY = 0
		for y in x:
			#print str(robot.x)+'/'+str(robot.y)+' == '+str(countY)+'/'+str(countX)
			if countY == robot.y and countX == robot.x:
				w.create_rectangle(countX*50+5, countY*50+5, countX*50+45, countY*50+45, fill="blue")
			else:
				w.create_rectangle(countX*50, countY*50, countX*50+50, countY*50+50, fill="white")
				if field[countY][countX] == '1':
					w.create_rectangle(countX*50+10, countY*50+10, countX*50+40, countY*50+40, fill="red")
				elif field[countY][countX] == 'X':
					w.create_rectangle(countX*50, countY*50, countX*50+50, countY*50+50, fill="black")
				
			countY += 1
		countX += 1
	if robot.age<=50: w.create_rectangle(50+robot.age*8,455,50+robot.age*8+14,473,fill="green")
	else: w.create_rectangle(50+robot.age%51*8,475,50+robot.age%51*8+14,493,fill="green")
	w.create_text (250,465, text=robot.genome[0:50],fill="white",font=helv36)
	w.create_text (250,484, text=robot.genome[50:100],fill="white",font=helv36)
	master.update()

renderGui(Robot())


master.update()
beste = (0,0)
for j in xrange(0,10):
	population = []	
	ges=0
	for i in xrange(0,100):	
		field = generateField()
		robby = Robot()
		run(robby,False)
		ges += robby.points
		#print robby.genome
		population.append((robby.points,robby.genome))
	tmp = ('',0)
	print str(j)+". Populationsdurchschnitt: "+str(ges/100.0)
	population.sort()
	population.reverse()
	ges = 0
	for p in population[0:10]:
		ges += p[0]
	print str(j)+". Elitedurchschnitt: "+str(ges/10.0)
	
	field = generateField()
	robby = Robot()
	robby.genome = population[random.randint(0,100)][1]
	run(robby,False)
	
	gesold = 0
	for i in xrange(0,10):
		population2 = []	
		ges = 0
		for x in xrange(0,5):
			robby1 = Robot()
			robby2 = Robot()
			robby1.genome,robby2.genome = crossover(population[x][1],population[x+5][1],_life)
			
			robby1.genome = mutation(robby1.genome,_life)
			robby2.genome = mutation(robby2.genome,_life)
			field = generateField()
			run(robby1,False)
			field = generateField()
			run(robby2,False)
			ges += robby1.points+robby2.points
			population2.append((robby1.points,robby1.genome))
			population2.append((robby2.points,robby2.genome))
			if beste[0]<robby1.points: beste = (robby1.points,robby1.genome)
			if beste[0]<robby2.points: beste = (robby2.points,robby2.genome)
		for i in xrange(0,9):
			for p in population2[0:10]:
				ges += p[0]	
				field = generateField()
				robby = Robot()
				robby.genome = mutation(p[1],_life)
				run(robby,False)
				ges += robby.points
				population2.append((robby.points,robby.genome))
				if beste[0]<robby.points: beste = (robby.points,robby.genome)
		
		population2.sort()
		population2.reverse()
		ges2 = 0
		for p in population2[0:10]:
			ges2 += p[0]
		
		if gesold<ges:
			population = population2
			#print str(ges)+" / "+str(gesold)
			gesold = ges
		
	print str(j)+". Populationsdurchschnitt: "+str(ges/100.0)
	print str(j)+". Elitedurchschnitt: "+str(ges2/10.0)+" | highest: "+str(population2[0][0])
	print "------------------------------------------"
print "Beste Evolution: "+str(beste[0])
field = generateField()
robby = Robot()
robby.genome = beste[1]
run(robby,True)
try:
    while 1:
        master.update()
except TclError:
    pass # to avoid errors when the window is closed
