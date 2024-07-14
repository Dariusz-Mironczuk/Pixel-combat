#Improrting libraries
import pygame

#Initializing pygame
pygame.init()

#BATTLE COUNTDOWN SETTINGS
intro_countdown = 3
countdown_color = (255,0,0)
last_count_update = pygame.time.get_ticks()

#Battle countdown font
countdown_font = pygame.font.Font('assets/fonts/turok.ttf', 80)

#Function for drawing text
def draw_text(text, font, text_color, x, y, display):
    img = font.render(text, True, text_color)
    display.blit(img, (x, y))



#Score font
score_font = pygame.font.Font('assets/fonts/turok.ttf', 30)