# Importing libraries
import pygame
from pygame import mixer
import sys
from settings import *
from fighter import *
from health import *
from sprites import *
from countdown import *
from score import *
from audio import *

# PLAYER 1 CONTROLS
# Player 1 uses w,a,s,d to move
# Player 1 uses c,v to attack

# PLAYER 2 CONTROLS
# Player 2 uses arrows to move
# Player 2 uses l,k to attack

# Making the game its own class
class Game:

    # GAME CLASS CONSTRUCTOR
    def __init__(self):
        #Initializing pygame
        pygame.init()
        mixer.init()

        # INITIALIZING WINDOW
        self.DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(NAME)
        pygame.display.set_icon(ICON)

        # INITIALIZING CLOCK
        self.clock = pygame.time.Clock()

        # Battle countdown initializing
        self.battle_countdown = intro_countdown
        self.battle_countdown_timer = last_count_update

        # End of battle
        self.Round_over = round_over
        self.round_over_time = 0  # Initialize round_over_time here

        # End of round image
        self.victory_img = pygame.image.load('assets/images/icons/victory.png').convert_alpha()

        # Background image
        self.background_img = pygame.image.load('assets/images/background/background1.png').convert_alpha()
        self.background_img_transformed = pygame.transform.scale(self.background_img, (WIDTH, HEIGHT))

        # Loading sprites
        worrior_sheet, wizard_sheet = load_sprites()

        # CREATING TWO FIGHTER INSTANCES
        self.fighter_1 = Fighter(1, 260, 320, False, WARRIOR_DATA, worrior_sheet, WARRIOR_ANIMATION_STEPS)
        self.fighter_2 = Fighter(2, 670, 320, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

        # CREATING TWO HEALTH BARS FOR THE FIGHTERS
        self.fighter_1_health = Health()
        self.fighter_2_health = Health()

        #Playing the game music
        Play_music()

    def reset_round(self):
        worrior_sheet, wizard_sheet = load_sprites()
        self.Round_over = False
        self.battle_countdown = 3
        self.fighter_1 = Fighter(1, 260, 320, False, WARRIOR_DATA, worrior_sheet, WARRIOR_ANIMATION_STEPS)
        self.fighter_2 = Fighter(2, 670, 320, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)
        self.battle_countdown_timer = pygame.time.get_ticks()

    def run(self):
        # EVENT LOOP
        while True:
            # Drawing the background
            self.DISPLAY.blit(self.background_img_transformed, (0, 0))

            # Drawing the players' health bars
            self.fighter_1_health.draw_health_bar(20, 20, self.DISPLAY, self.fighter_1.health)
            self.fighter_2_health.draw_health_bar(580, 20, self.DISPLAY, self.fighter_2.health)
            #Drawing player scores
            draw_text('P1: ' + str(score[0]), score_font, (255,0,0), 20, 60, self.DISPLAY)
            draw_text('P2: ' + str(score[1]), score_font, (255,0,0), 580, 60, self.DISPLAY)

            # Checking if the intro stopped counting down
            if self.battle_countdown <= 0:
                # Moving the players
                self.fighter_1.move(self.DISPLAY, self.fighter_2)
                self.fighter_2.move(self.DISPLAY, self.fighter_1)
            else:
                # Display countdown on display
                draw_text(str(self.battle_countdown), countdown_font, countdown_color, WIDTH / 2, HEIGHT / 3, self.DISPLAY)
                # Update count timer
                if pygame.time.get_ticks() - self.battle_countdown_timer >= 1000:
                    self.battle_countdown -= 1
                    self.battle_countdown_timer = pygame.time.get_ticks()

            # Updating the fighter animation
            self.fighter_1.update()
            self.fighter_2.update()

            # Drawing player rectangles
            self.fighter_1.Draw_fighter(self.DISPLAY)
            self.fighter_2.Draw_fighter(self.DISPLAY)

            # Check for player defeat
            if not self.Round_over:
                if not self.fighter_1.alive:
                    score[1] += 1
                    self.Round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                elif not self.fighter_2.alive:
                    score[0] += 1
                    self.Round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                # Display victory image
                self.DISPLAY.blit(self.victory_img, (360, 150))
                if pygame.time.get_ticks() - self.round_over_time > round_over_cooldown:
                    self.reset_round()

            # EVENT HANDLER
            for event in pygame.event.get():
                # Shutting down the game and closing the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Updating the display
            pygame.display.update()
            # Updating the clock
            self.clock.tick(FPS)


# Creating an instance of the game from the Game() class
if __name__ == '__main__':
    game = Game()
    game.run()
