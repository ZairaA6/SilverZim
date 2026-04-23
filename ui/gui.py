
# GUI - mainmenu and dashboard fonts
import pygame
from config import *

def get_font(size): 
    return pygame.font.Font("assets/Inlanders.otf", size)   # most of the main menu buttons will be this font

def get_dashboard_font(size):
    return pygame.font.Font("assets/impact.ttf", size)      # most of dashboard interfaces will be this font

def speedometer(screen, user_speed, position):
    SPEED_TEXT = get_dashboard_font(30).render(str(round(user_speed * 20,2)) + "mph", True, (0,0,0))
    SPEED_RECT = SPEED_TEXT.get_rect(center=position) #reusable
    screen.blit(SPEED_TEXT, SPEED_RECT)

def display_tyres(screen, tyre_compound, acceleration, position):
    if position == (1160, 205):   # tutorial 2 has slightly different GUI so this is required, if GUI changed to be more adaptable, this would be unrequired.
        tyres_words = tyre_compound
        acc_words = str(acceleration)
    else:
        tyres_words = "Tyres:"+ tyre_compound
        acc_words = "Acc: "+ str(acceleration)

    TYRES_TEXT = get_dashboard_font(20).render(tyres_words, True, (38,38,38)) #grey
    TYRES_RECT = TYRES_TEXT.get_rect(center=position)
    screen.blit(TYRES_TEXT, TYRES_RECT)

    ACC_TEXT = get_dashboard_font(20).render(acc_words, True, (38,38,38))
    ACC_RECT = ACC_TEXT.get_rect(center=(position[0],position[1]+20))
    screen.blit(ACC_TEXT, ACC_RECT)