import pygame,sys, random, os, math
from pygame.locals import *
from pygame import mixer
pygame.mixer.pre_init(44100, 16, 2, 4096)

#Start pygame
pygame.init()
mixer.init()

#Screen and clock
screenw, screenh= 1080, 720
size= (screenw, screenh)
screen = pygame.display.set_mode((size))
bg = pygame.image.load('C:/Users/isaac/IH/Proyecto/Miniproyecto/Try 2/Assets/Fight/bg.png')
props = pygame.image.load('C:/Users/isaac/IH/Proyecto/Miniproyecto/Try 2/Assets/Fight/props.png') 

screen_size = screen.get_size()
bg_size = bg.get_size()
bg_x = (bg_size[0]-screen_size[0]) // 2
bg_y = (bg_size[1]-screen_size[1]) // 2


pygame.display.set_caption('Try 2')
clock = pygame.time.Clock()




#FPS
FPS = 60

#Game Variables
#gravity = 0.50


#Colores
black=(0,0,0)
white=(255,255,255)
green=(192,192,192)
crean=(255,255,204)
lime=(153,255,51)
orange=(255,178,102)
blue=(102,255,255)

#Music and sounds
pygame.mixer.music.load('C:/Users/isaac/IH/Proyecto/Miniproyecto/Try 2/Assets/Music/Loops/selectedfx.wav')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1, 0.0,5000)
punch_sound = pygame.mixer.Sound('C:/Users/isaac/IH/Proyecto/Miniproyecto/Try 2/Assets/RPG/Type 4/attack2fx.wav')



#Player Movement
move_left = False
move_right = False
move_up = False
move_down = False
punch = False
kick = False
hook = False
hkick = False

#Currently off
jump = False 

vel_y = 0




#General class
class npc(pygame.sprite.Sprite):
	def __init__(self, npc_type, x,y, scale, mvupnd, mvside, sound):
		pygame.sprite.Sprite.__init__(self)

		self.npc_type = npc_type

		

		#Movement
		self.mvupnd = mvupnd
		self.mvside = mvside
		self.direction = 1
		self.flip = False

		#Jumping Movement
		self.jump = jump
		self.vel_y = vel_y
		self.in_air = False
		
		#Fight Movement
		self.punch = punch
		self.kick = kick
		self.hook = hook
		self.hkick = hkick

		#Fight commands
		self.attacking = False
		self.attack_type = 0
		self.attack_cooldown = 0
		self.attack_sound = sound
		self.hit = False
		self.health = 100

	    #Dead or Alive
		self.alive = True
		
		#Animations
		self.update_timer = pygame.time.get_ticks()
		self.animation_list = []
		self.frame = 0
		self.action = 0
		temp_list = []
		
		#Action Types
		action_types = ['idle', 'walk', 'punch', 'jump', 'kick']

		for type in action_types:

			temp_list = []
			num_frames= len(os.listdir(f'C:/Users/isaac/IH/Proyecto/Miniproyecto/Try 2/Assets/Fight/{self.npc_type}/{type}'))

		#Action Animations
			for i in range(num_frames):
				#Imgs
				img= pygame.image.load(f'C:/Users/isaac/IH/Proyecto/Miniproyecto/Try 2/Assets/Fight/{self.npc_type}/{type}/{type}{i+1}.png')
				img= pygame.transform.scale(img, (img.get_width() *scale,img.get_height()* scale))
				temp_list.append(img)
			self.animation_list.append(temp_list)


		#Img
		self.img = self.animation_list[self.action][self.frame]
		self.hitbox=self.img.get_rect()
		self.hitbox.center=(x,y)

		#Movement
	def move(self, move_left, move_right, move_up, move_down, target):
		dx = 0
		dy = 0


		#Jump
		# if self.jump == True and self.in_air == False:

		# 	self.vel_y = -10
		# 	self.jump = False
		# 	self.in_air = True
			
		# if vel_y > 0:
		# 	self.vel_y += gravity
		# 	dy += self.vel_y
		# 	if self.vel_y > 10:
		# 		self.vel_y
		if self.attacking == False and self.alive == True:
			#Left
			if move_left:
				dx = -self.mvside
				self.flip = True
				self.direction = -1
			#Right
			if move_right:
				dx = self.mvside
				self.flip = False
				self.direction = 1

			#Up
			if move_up:
				dy = -self.mvupnd
			#Down
			if move_down:
				dy = self.mvupnd


	# def attack(self, target):
	# 	if sel.attack_cooldown == 0:
	# 		self.attacking = True
	# 		self.attack_sound.play()
	# 		attacking_rect = pygame.hitbox(self.hitbox.centerx -  (2 * self.rect.width * self.flip), self.hitbox.y, 2* self.hitbox.width, self.hitbox.height)
	# 		if attacking_rect.colliderect(target.rect):
	# 			taget.health -= 1
	# 			target.hit = True
			# a

	# 	#Collision

		#UPND
		if self.hitbox.bottom + dy > 700:
			dy = 700 - self.hitbox.bottom
			self.in_air = False
		if self.hitbox.top + dy < 163:
			dy = 163 - self.hitbox.top

		#RNL
		if self.hitbox.left +dx < -95:
			dx = -self.hitbox.left -90
		if self.hitbox.right+dx> screenw + 95:
			dx= screenw - self.hitbox.right+90



		self.hitbox.x += dx
		self.hitbox.y += dy

	def animation(self):
		#Timer
		animation_cd = 225

		#Updating img 
		self.img = self.animation_list[self.action][self.frame]
		#Check for update

	
		if pygame.time.get_ticks() - self.update_timer > animation_cd:
			self.update_timer = pygame.time.get_ticks()
			self.frame += 1

		#Reset Animation
		if self.frame  >= len(self.animation_list[self.action]):
			self.frame = 0

	def change_action(self, new_action):
		#Checking for new actions
		if new_action != self.action:
			self.action = new_action
		#Updating the action
			self.frame = 0
			self.update_timer = pygame.time.get_ticks()

	def draw(self):
		screen.blit(pygame.transform.flip(self.img, self.flip, False), self.hitbox)
		pygame.draw.line(screen, white, (0,720), (1080,720))

#Characters
	# class player(npc):
	# def __init__(self, npc_type, x,y, scale, mvupnd, mvside):
	# 	self.npc_type = 'Brawler-Girl'
	# 	self.x = 200
	# 	self.y = 400
	# 	self.scale = 2.4
	# 	self.mvupnd = 3
	# 	self.mvside = 5

player = npc('Brawler-Girl',500,400,2.4, 2, 2, punch_sound)


enemy = npc('Enemy-Punk',400,400,2, 2, 3, punch_sound)

while True:
	clock.tick(FPS)

	keys = pygame.key.get_pressed()
	if keys[pygame.K_a]:
	    bg_x -= 7.5
	if keys[pygame.K_d]:
	    bg_x += 7.5

	bg_x = max(0, min(bg_size[0]-screen_size[0], bg_x)) 
	bg_y = max(0, min(bg_size[1]-screen_size[1], bg_y))

	screen.blit(bg, (-bg_x, -bg_y))


	#Player
	player.animation()
	player.draw()

	#NPCS
	player.move(move_left, move_right, move_up, move_down, enemy)

	#Player Actions 
	if player.alive:
		if move_down or move_up or move_left or move_right:
			player.change_action(1)
		elif punch:
			player.change_action(2)
		elif kick:
			player.change_action(4)
		
		else:
			player.change_action(0)



	screen.blit(props, (-bg_x, -bg_y))

	for event in pygame.event.get():
		#quit
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		#key input
		if event.type==pygame.KEYDOWN:
			if event.key == pygame.K_a:
				move_left = True
			elif event.key == pygame.K_d:
				move_right = True
			elif event.key == pygame.K_w:
				move_up = True
			elif event.key == pygame.K_s:
				move_down = True
			elif event.key == pygame.K_q:
				punch = True
			elif event.key == pygame.K_e:
				kick = True
			elif event.key == pygame.K_SPACE and player.alive:
				player.jump = True

			if event.key ==pygame.K_ESCAPE:
				pygame.quit()
				exit()

		#key release
		if event.type==pygame.KEYUP:
			if event.key == pygame.K_a:
				move_left = False
			elif event.key == pygame.K_d:
				move_right = False
			elif event.key == pygame.K_w:
				move_up = False
			elif event.key == pygame.K_s:
				move_down = False
			elif event.key == pygame.K_q:
				punch = False
			elif event.key == pygame.K_e:
				kick = False

	#Display	
	pygame.display.flip()
	pygame.display.update

screen.blit(surface,(0,0))

pygame.display.update()



