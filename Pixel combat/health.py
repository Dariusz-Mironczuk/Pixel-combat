#Importing libraries
import pygame

#Making a health_bar class
class Health():

    #The constructor
    def __init__(self):
        
        #Health bar color 
        self.HEALTH_BAR_COLOR = (0, 255, 0)
        self.LOOSING_HEALTH_COLOR = (255, 0, 0)
        self.HEALTH_OUTLINE_COLOR = (255, 255, 255)
        


    #Function for drawing the health bar
    def draw_health_bar(self, x, y, display, health):
        ratio = health / 100
        pygame.draw.rect(display, self.HEALTH_OUTLINE_COLOR, (x-3, y-3, 406, 36))
        pygame.draw.rect(display, self.LOOSING_HEALTH_COLOR, (x, y, 400, 30))
        pygame.draw.rect(display, self.HEALTH_BAR_COLOR, (x, y, 400 * ratio, 30))
        


