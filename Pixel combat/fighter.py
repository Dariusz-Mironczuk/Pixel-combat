#Importing libraries
import pygame
from settings import *
from health import *
from sprites import *
from audio import *

#Making a fighter class
class Fighter():

    #Fighter class constructor
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):

        #Checking which player is playering
        self.player = player

        #Flipping the fighter if they get behind eachother
        self.Flip_fighter = flip

        #Fighter rectangle
        self.fighter_rect = pygame.Rect((x, y, 80, 200))
        
        #Player velocity
        self.jump = False
        self.velocoty_y = 0

        #Player attacking
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attacking = False
        self.hit = False

        #Player running
        self.running = False

        #Player health
        self.health = 100
        self.HEALTH_BAR = Health()
        self.alive = True

        #Animation information
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        #Checking waht action the player is doing
        self.action = 0     # 0 = idle ; 1 = running ; 2 = jumping ; 3 = attack_1 ; 4 = attack_2 ; 5 = is_hit ; 6 = dying
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()

    #Function for loading images of sprites to the 
    def load_images(self, sprite_sheet, animation_steps):

        #Extraction images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
            
    #Function for fighter movemnt
    def move(self, surface, target):
        SPEED = 10
        GRAVITY = 2
        Dx = 0
        Dy = 0
        self.running = False
        self.attack_type = 0

        #Getting keypresses from player
        key = pygame.key.get_pressed()

        #Checking if the player is attacking and if he can do a move
        if self.attacking == False and self.alive == True:

            #Checking player 1 controlls
            if self.player == 1:
                #Movment
                if key[pygame.K_a]:
                    Dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    Dx = SPEED
                    self.running = True
                #Jumping
                if key[pygame.K_w] and self.jump == False:
                    self.jump = True
                    self.velocoty_y = -30
                #Attacks
                if key[pygame.K_c] or key[pygame.K_v]:
                    self.Attack(surface, target, self.player)
                    #Attack 1
                    if key[pygame.K_c]:
                        self.attack_type = 1

                    #Attack 2
                    if key[pygame.K_v]:
                        self.attack_type = 2
            
            #Checking player 2 controlls
            if self.player == 2:
                #Movment
                if key[pygame.K_LEFT]:
                    Dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    Dx = SPEED
                    self.running = True
                #Jumping
                if key[pygame.K_UP] and self.jump == False:
                    self.jump = True
                    self.velocoty_y = -30
                #Attacks
                if key[pygame.K_l] or key[pygame.K_k]:
                    self.Attack(surface, target, self.player)
                    #Attack 1
                    if key[pygame.K_l]:
                        self.attack_type = 1

                    #Attack 2
                    if key[pygame.K_k]:
                        self.attack_type = 2

        #Applying gravity
        self.velocoty_y += GRAVITY
        Dy += self.velocoty_y

        #Logic check to ensure player didn't run off the display
        if self.fighter_rect.x > WIDTH - self.fighter_rect.w:
            self.fighter_rect.x = WIDTH - self.fighter_rect.w
        if self.fighter_rect.x < 0:
            self.fighter_rect.x = 0
        if self.fighter_rect.bottom + Dy > HEIGHT - 80:
            self.jump = False
            self.velocoty_y = 0
            Dy = HEIGHT - 80 - self.fighter_rect.bottom

        #Ensure players face eachother
        if target.fighter_rect.centerx > self.fighter_rect.centerx:
            self.Flip_fighter = False
        else:
            self.Flip_fighter = True

        #Applying player attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #Uodating the players positions
        self.fighter_rect.x += Dx
        self.fighter_rect.y += Dy

    #Handling animation updates
    def update(self):

        #Check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)       #Player death animation
        elif self.hit == True:
            self.update_action(5)       #Player got hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)   #Attack 1 action
            elif self.attack_type == 2:
                self.update_action(4)   #Attack 2 action
        elif self.jump == True:
            self.update_action(2)   #Jumpng action
        elif self.running == True:
            self.update_action(1)   #Running action
        else:
            self.update_action(0)   #Idle action

        #The animation cooldown will change depending on the action
        if self.action == 6:
            animation_cooldown = 400    #Death animation cooldown
        elif self.action == 5:
            animation_cooldown = 120    #Hit animation cooldown
        elif self.action == 4:
            animation_cooldown = 100    #Attack 2 animation cooldown
        elif self.action == 3:
            animation_cooldown = 80     #Attack 1 animation cooldown
        elif self.action == 2:
            animation_cooldown = 100    #Jumping animation cooldown
        elif self.action == 1:
            animation_cooldown = 80     #Running animation cooldown
        else:
            animation_cooldown = 280    #Idle player animation cooldown
        self.image = self.animation_list[self.action][self.frame_index]

        
        
        #Checking if enought time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        #Checking if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #Check if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #Checking if there was an attack. If yes then we turn off the "Attacking"
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #Checking if there was an hit. If yes then we turn of the "Hit" animation
                if self.action == 5:
                    self.hit = False
                    #If the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20

    #Helper method for the animation
    def update_action(self, new_action):

        #Check if the new action is different to previous one
        if new_action != self.action:
            self.action = new_action

            #Updating the fram index
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #Function for drawing the fighter rectangle
    def Draw_fighter(self, display):
        img = pygame.transform.flip(self.image, self.Flip_fighter, False)
        display.blit(img, (self.fighter_rect.x - (self.offset[0] * self.image_scale), self.fighter_rect.y - (self.offset[1] * self.image_scale)))

    #Function for player attacks
    def Attack(self, surface, target, player):

        #Checking if attack cooldown if up
        if self.attack_cooldown == 0:

            #Player is attacking so he can't do anything else during this
            self.attacking = True

            #Playing sound affect for the player
            if player == 1:
                WARRIOR_SOUND.play()
            elif player == 2:
                WIZZARD_SOUND.play()

            #Making a rectangle to see where the player attack is.
            attacking_rect = pygame.Rect(self.fighter_rect.centerx - (2 * self.fighter_rect.width * self.Flip_fighter), self.fighter_rect.y, self.fighter_rect.width * 2, self.fighter_rect.height)
            
            #Checking if the attack hit the enemy player aka the "target"
            if attacking_rect.colliderect(target.fighter_rect):
                target.health -= 10
                target.hit = True
                
                #IF YOU WOULD LIKE TO SEE THE HIT BOX OF THE PLAYERS
            #Drawing the attacking rectangle on to the display
            #pygame.draw.rect(surface, (255,0,0), attacking_rect)

