import pygame
import socket


from math import sqrt, tan, atan
import math
import threading
import time
import random
import copy
import numpy as np
import matplotlib.pyplot as plt




import neat


pygame.font.init()

WIDTH, HEIGHT = 300 , 500

WIN  = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('FLAP')

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY  = (50 , 50, 50)
DARCK_GREY  = (25 , 25, 25)
LIGHT_GREY  = (120 , 120, 120)
RED  = (255 , 0, 0)
GREEN  = (0 , 255, 0)
BULLET_FONT = pygame.font.SysFont('arial',20)
SCORE_FONT = pygame.font.SysFont('arial',40)
PACKAGE_FONT = pygame.font.SysFont('arial',10)


YOUR_PADDEL = pygame.Rect(1, 1, 50 , 50)

FPS = 60

RUN = True


MID = [WIDTH//2,HEIGHT//2]








class Pipe():

	def __init__(self,x=0):
		self.spacing = x
		self.pos = [copy.copy(WIDTH)+x,0]
		self.width = 40
		self.color = (0,255,0)
		self.space = 100
		self.margin = 10
		#print(self.space,HEIGHT-self.margin-self.space)
		self.top = random.randint(self.margin,HEIGHT-self.margin-self.space)
		self.speed = 1

		
	def update(self):
		self.pos[0] -= self.speed
		if self.pos[0] < -self.width:
			self.pos[0] = copy.copy(WIDTH)+300 - self.width
			self.top = random.randint(self.space,HEIGHT-self.margin-self.space)


class Bird():

	def __init__(self, field):
		self.size = [20,20]
		r = random.randint(50,255)
		g = random.randint(50,255)
		b = random.randint(50,255)
		
		self.color = (r,g,b)
		self.pos = [copy.copy(WIDTH)//2-self.size[0]//2,  copy.copy(HEIGHT)//2-self.size[1]//2 ]
		self.velocity = 3
		self.tick_to_space = 0
		self.velocity_space = 3
		self.field = field	
		self.alive =True
		self.fitness = 0

	def update(self):
		self.tick_to_space += 1
		#print(self.pos[1],gravity(self.tick_to_space) )
		self.pos[1] -= self.velocity
		self.velocity -= 0.1
		
	def dead(self):
		#self.pos = [copy.copy(WIDTH)//2-self.size[0]//2,  copy.copy(HEIGHT)//2-self.size[1]//2 ]
		#self.velocity = 3
		self.alive =  False 

	def get_distance(self):
		x = self.pos[0]
		y = self.pos[1]
		yy1 = self.field[0].top
		yy2 = self.field[0].top+self.field[0].space
		xx = self.field[0].pos[0]+self.field[0].width
		maxx = round(sqrt((WIDTH- WIDTH//2)**2+(HEIGHT)**2))
		#d1 = round(sqrt((xx-x)**2+(yy1-y)**2)/maxx,4)
		#d2 = round(sqrt((xx-x)**2+(yy2-y)**2)/maxx,4)
		return (self.field[0].top/HEIGHT,(self.pos[1]/HEIGHT),self.field[0].pos[0]/(WIDTH//2))
	def dead_check(self, field):
		bird = self
		for i in field:
			if  bird.pos[1]+bird.size[1] > i.top+i.space and bird.pos[0]+bird.size[0] >= i.pos[0] and bird.pos[0] < i.pos[0]+i.width:

				bird.dead()

			elif bird.pos[1] <= i.top and bird.pos[0]+bird.size[0] >= i.pos[0] and bird.pos[0] < i.pos[0]+i.width:
				bird.dead()

			elif bird.pos[1]+bird.size[1] > HEIGHT:
				bird.dead()

			elif bird.pos[1] < 0:
				bird.dead()













def draw_window(field, birds):
	global WIN


	WIN.fill(GREY)

	for i in field:

		pygame.draw.rect(WIN,i.color, (i.pos[0], i.pos[1], i.width, i.top))

		pygame.draw.rect(WIN,i.color, (i.pos[0], i.top+i.space, i.width, HEIGHT))
	for bird in birds:
		if bird.alive == True:
			pygame.draw.rect(WIN,bird.color, (bird.pos[0], bird.pos[1], bird.size[0], bird.size[1]))

	

	
	pygame.display.update()




genn = 0
		
def main(genomes, config):
	nets = []
	fit = []
	birds = []
	field = [Pipe(i*200) for i in range(3)]
	for id, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		g.fitness = 0
		birds.append(Bird(field))
	#print(nets[0])
	global RUN
	global genn
	RUN = True
	
	
	genn+=1
	bird= Bird(field)

	clock = pygame.time.Clock()
	t = time.time()
	down =False
	while RUN:
		#global field
		

		clock.tick(FPS)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				
				RUN = False
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE :
					print(genn,alive,i_fit[maxx_in],   i_bird[maxx_in].get_distance(),i)

		i_res = []
		i_fit = []
		i_bird = []
		alive =0
		for index, bird in enumerate(birds):
			

			
			if bird.alive == True:
				alive += 1
				output = nets[index].activate(bird.get_distance())
				i = output[0]
				i_res.append(i)
				if i >0.5:
					bird.velocity = bird.velocity_space
				genomes[index][1].fitness += 1
				i_fit.append(genomes[index][1].fitness)
				i_bird.append(bird)
				bird.update()
				bird.dead_check(field)


		#print(bird.get_distance())




		if alive <= 0:
			break
		maxx_in = i_fit.index(max(i_fit))
		
		if field[0].pos[0]+field[0].width< birds[0].pos[0]:#/2
			field.append(field[0])
			field.pop(0)


		for i in field:
			i.update()
			
			


		keys_pressed = pygame.key.get_pressed()
		draw_window(field,birds)
		


		
		


if __name__ == "__main__":
	config_path = "config-feedforward.txt"
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	# Create core evolution algorithm class
	p = neat.Population(config)

	# Add reporter for fancy statistical result
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	# Run NEAT
	p.run(main, 1000)
