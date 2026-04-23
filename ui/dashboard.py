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

# user controls display on dashboard
def draw_controls(screen, circuit, controls):
    steer_text_position = steer_text[circuit]

    colours = {
        "inactive": (38, 38, 38),
        "active": (252, 2, 4),
    }

    left_colour = colours["active"] if controls["left"] else colours["inactive"]
    gas_colour = colours["active"] if controls["gas"] else colours["inactive"]
    right_colour = colours["active"] if controls["right"] else colours["inactive"]
    brake_colour = colours["active"] if controls["brake"] else colours["inactive"]

    # 4 labels for 4 controls - left, gas, right, brake
    L_TEXT = get_dashboard_font(30).render("L", True, left_colour)
    L_RECT = L_TEXT.get_rect(center=steer_text_position[0])
    screen.blit(L_TEXT, L_RECT)

    GAS_TEXT = get_dashboard_font(25).render("GAS", True, gas_colour)
    GAS_RECT = GAS_TEXT.get_rect(center=steer_text_position[1])
    screen.blit(GAS_TEXT, GAS_RECT)

    R_TEXT = get_dashboard_font(30).render("R", True, right_colour)
    R_RECT = R_TEXT.get_rect(center=steer_text_position[2])
    screen.blit(R_TEXT, R_RECT)

    BREAK_TEXT = get_dashboard_font(25).render("BRAKE", True, brake_colour)
    BREAK_RECT = BREAK_TEXT.get_rect(center=steer_text_position[3])
    screen.blit(BREAK_TEXT, BREAK_RECT)

def draw_track_limits_warning(screen, circuit, track_limits_hit):
    if not track_limits_hit:
        return

    position = (435, 660)
    if circuit == "Tutorial1":
        position = (1100, 200)

    text = get_dashboard_font(15).render("track limits!", True, (252, 4, 2))
    rect = text.get_rect(center=position)
    screen.blit(text, rect)

def draw_drs_alert(screen, DRS_available, DRS_alert_image):
    if DRS_available:
        screen.blit(DRS_alert_image, (150, 570))

def draw_pitstop_alert(screen, pitstop_available, pitstop_alert_image):
    if pitstop_available:
        screen.blit(pitstop_alert_image, (150, 570))

def draw_pitstop_screen(screen, pitstop_screen_show, pitstop_screen_image):
    if pitstop_screen_show:
        screen.blit(pitstop_screen_image, (21, 20))