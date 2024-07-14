#Importing libraries
import pygame
from pygame import mixer

#Initializing
mixer.init()
pygame.init()

#MUSIC SETTINGS
MUSIC = 'assets/audio/music.mp3'
MUSIC_VOL = 0.5

#WARRIOR SOUND SETTINGS
WARRIOR_SOUNDS = 'assets/audio/sword.wav'
WARRIOR_VOL = 0.5

#WIZARD SOUNDS SETTINGS
WIZARD_SOUNDS = 'assets/audio/magic.wav'
WIZARD_VOL = 0.75

#Loading all the music
pygame.mixer.music.load(MUSIC)
WARRIOR_SOUND = pygame.mixer.Sound(WARRIOR_SOUNDS)
WIZZARD_SOUND = pygame.mixer.Sound(WIZARD_SOUNDS)

#Setting the proper volume
pygame.mixer.music.set_volume(MUSIC_VOL)
WARRIOR_SOUND.set_volume(WARRIOR_VOL)
WIZZARD_SOUND.set_volume(WIZARD_VOL)

#Function for player music
def Play_music():

    #Playing the music
    pygame.mixer.music.play(-1, 0.0, 12000)