#Importing libraries
import pygame


def load_sprites():
    #Loading fighter sprite sheets
    worrior_sheet = pygame.image.load('assets/images/warrior/Sprites/warrior.png').convert_alpha()
    wizard_sheet = pygame.image.load('assets/images/wizard/Sprites/wizard.png').convert_alpha()

    return worrior_sheet, wizard_sheet

#DEFINING SPRITE SHEET DATA
#Size of frames of animation
WARRIOR_SIZE = 162
WIZARD_SIZE = 250
#Scales for the palayer images
WARRIOR_SCALE = 4
WIZARD_SCALE = 3
#Adding offsets for positions
WARRIOR_OFFSET = [72, 51]
WIZARD_OFFSET = [112, 100.2]
#Lists for the data
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#Defining number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]