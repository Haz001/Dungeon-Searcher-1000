import pygame
pygame.init()
import random as rn
import time

class depe:#dependencys
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((1024,768))
class pres:#presets
	tick = 10
	class color:
		red = (238,22,26)
		green = (25,230,19)
		blue = (18,25,234)
		c1 = (86,84,88)#wall
		c2 = (190,190,190)#floor-1
		c3 = (190,190,23)#floor-2
		c9 = (0,0,0)#unknown

class draw:
	def rec(x,y,w,h,c):#draw rectangle
		pygame.draw.rect(depe.screen, c, pygame.Rect(x,y,w,h))
	def squ(x,y,w,c):#draw cube
		pygame.draw.rect(depe.screen, c, pygame.Rect(x,y,w,w))
	def string(x,y,txt,c,height):
		s = depe.screen
		font = pygame.font.SysFont('Consolas', 15)
		if(height != None):
			font = pygame.font.SysFont('Consolas', height)
		else:
			height = 15
		if (len(txt.split("\n"))>0):
			for i in range(len(txt.split("\n"))):
				text = font.render(txt.split("\n")[i], False, c)
				s.blit(text,(x,y+(height*i)))
		else:
			text = font.render(txt, False, c)
			s.blit(text,(x,y))

class g:
	pxls = 64

class main:
	class enemy:
		elist = []
		def create():
			for i in range(100):
				main.enemy.elist.append(main.enemy.witch())


		class sprites:
			witch = None
			action1 = None
			action2 = None
		class witch(object):
			def __init__(self):
				self.x = rn.randint(-10,10)
				self.y = rn.randint(-10,10)
				self.state = 0
				self.time = 0
				self.lvl = 0
			def draw(self):
				gx = self.x+-main.player.x
				gy = self.y-main.player.y

				depe.screen.blit(main.enemy.sprites.witch,((gx)*g.pxls,(gy)*g.pxls))
				if(self.state == 1):
					if(self.time<=0):
						self.state = 0
					else:
						self.time -=1

					depe.screen.blit(main.enemy.sprites.action1,((gx)*g.pxls-64,(gy)*g.pxls-64))
			def action(self):
				tmp = rn.randint(0,4)
				print("action - "+str(tmp)+"|dist - "+str(((self.x-main.player.x)**2+(self.y-main.player.y)**2)**0.5))
				if(tmp==0):
					self.move(rn.randint(-1,1),rn.randint(-1,1))
				elif(tmp==1):
					dist = ( (self.x-(main.player.x+main.player.offx))**2+( self.y-(main.player.y+main.player.offy) )**2 )**0.5
					if(dist <=1):
						self.state = 1
						self.time = 2
						main.player.hp -= 10
			def move(self,x,y):
				gx = self.x+-main.player.x+x
				gy = self.y-main.player.y+y
				if(main.grid.get(gx,gy) != pres.color.c1):
					self.x +=x
					self.y +=y


				


	class player:
		sprite = None
		x = 0
		y = 0
		offx= 8
		offy= 6
		hp = 250

	run = True
	def draw():
		for x in range(0,16):
				for y in range(0,12):
					gx = x+main.player.x
					gy = y+main.player.y
					draw.squ(x*g.pxls,y*g.pxls,g.pxls,main.grid.get(gx,gy))

		text = "X - "+str(main.player.x)+"|Y - "+str(main.player.y)+"|Witch: X - "+str(main.enemy.elist[0].x)+"|Y - "+str(main.enemy.elist[0].y)
		draw.string(2,2,text,(0,0,0),32)		
		draw.string(0,0,text,(255,255,255),32)



		##draw.squ((main.player.offx)*g.pxls,(main.player.offy)*g.pxls,g.pxls,pres.color.blue)
		depe.screen.blit(main.player.sprite,((main.player.offx)*g.pxls,(main.player.offy)*g.pxls))
		for i in range(len(main.enemy.elist)-1):
			main.enemy.elist[i].draw()
		draw.rec(300,0,main.player.hp,20,(0,255,0))
		draw.rec(300+main.player.hp,0,250-main.player.hp,20,(255,0,0))

	class grid:
		dcoor = {}
		def setup():

			main.player.sprite = pygame.image.load('hunter1.gif')
			main.enemy.sprites.witch = pygame.image.load('witch/char.gif')
			main.enemy.sprites.action1 = pygame.image.load('witch/action1.gif')
			main.enemy.sprites.action2 = pygame.image.load('witch/action2.gif')
			main.enemy.create()
			for x in range(-10,10):
				for y in range(-10,10):
					main.grid.create(x,y)
		def create(x,y):
			z=rn.randint(0,2)
			if(z == 0):
				main.grid.dcoor[str(x)+"-"+str(y)]=(pres.color.c1)
			elif(z==1):
				main.grid.dcoor[str(x)+"-"+str(y)]=(pres.color.c2)
			elif(z==2):
				main.grid.dcoor[str(x)+"-"+str(y)]=(pres.color.c3)
			else:
				main.grid.dcoor[str(x)+"-"+str(y)]=(pres.color.c9)
		def get(x,y):
			if( str(x)+"-"+str(y) not in main.grid.dcoor):
				main.grid.create(x,y)
			return main.grid.dcoor[str(x)+"-"+str(y)]

					
	def keyd():
		moved = False
		pressed = pygame.key.get_pressed()
		y = main.player.y+main.player.offy
		x = main.player.x+main.player.offx
		if pressed[pygame.K_UP]:
			if(main.grid.get(x,y-1) != pres.color.c1):
				main.player.y-=1
				moved = True
		elif pressed[pygame.K_RIGHT]:
			if(main.grid.get(x+1,y) != pres.color.c1):
				main.player.x+=1
				moved = True
		elif pressed[pygame.K_DOWN]:
			if(main.grid.get(x,y+1) != pres.color.c1):
				main.player.y+=1
				moved = True
		elif pressed[pygame.K_LEFT]:
			if(main.grid.get(x-1,y) != pres.color.c1):
				main.player.x-=1
				moved = True
		elif pressed[pygame.K_w]:
			print("wait")
			moved = True
		if(moved == True):
			for i in range(len(main.enemy.elist)-1):
				main.enemy.elist[i].action()


main.grid.setup()

while main.run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			
			main.run = False
	main.keyd()
	main.draw()
	
	pygame.display.flip()
	depe.clock.tick(pres.tick)

