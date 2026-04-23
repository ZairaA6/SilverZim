import pygame, sys
from config import *
from ui.button import Button
from ui.dashboard import get_font, get_dashboard_font
from persistence.records import save_data, load_records, get_user_score

def viewstats(screen, statsBG, user_nickname, on_back):
    pygame.display.set_caption("View Stats")
    all_user_records = load_records()          # creates variable for all dictionaries in json file - to be used in return_user_score()
    view_user_score = get_user_score(user_nickname, all_user_records)

    while True:
        VIEWSTATS_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(statsBG, (0,0))

        VIEWSTATS_TEXT = get_font(50).render("VIEW STATS", True, "White")   #title 
        VIEWSTATS_RECT = VIEWSTATS_TEXT.get_rect(center = (640, 240))
        screen.blit(VIEWSTATS_TEXT, VIEWSTATS_RECT)

        VIEWSTATS_TEXT = get_font(18).render("Make sure to SAVE STATS in the main menu before you view stats.", True, "White")  #view stats extra info
        VIEWSTATS_RECT = VIEWSTATS_TEXT.get_rect(center = (640, 280))
        screen.blit(VIEWSTATS_TEXT, VIEWSTATS_RECT)

        VIEWSTATS_BACK = Button(image=None, pos = (200, 200),
                           text_input="<- BACK", font=get_font(25), base_color = "White", hovering_color = "Green")   #back button
        VIEWSTATS_BACK.changeColor(VIEWSTATS_MOUSE_POS)
        VIEWSTATS_BACK.update(screen)

        PLAYER_TEXT = get_dashboard_font(45).render("Nickname: "+user_nickname, True, "White")    #print user nicknaname
        PLAYER_RECT = PLAYER_TEXT.get_rect(center = (640, 360))
        screen.blit(PLAYER_TEXT, PLAYER_RECT)

        SCORE_TEXT = get_dashboard_font(45).render("All Time Score: "+ str(view_user_score), True, "White")  # print user all time score
        SCORE_RECT = SCORE_TEXT.get_rect(center = (640, 410))
        screen.blit(SCORE_TEXT, SCORE_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VIEWSTATS_BACK.checkForInput(VIEWSTATS_MOUSE_POS):  #return to main menu if back button pressed
                    on_back()
                    return

        pygame.display.update()

def savestats(screen, statsBG, user_nickname, all_time_score, on_back):
    pygame.display.set_caption("Save Stats")
    while True:
        SAVESTATS_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(statsBG, (0,0))

        SAVESTATS_TEXT = get_font(25).render("SAVE STATS: Press the button below & press Back!", True, "white")
        SAVESTATS_RECT = SAVESTATS_TEXT.get_rect(center = (640, 280))
        screen.blit(SAVESTATS_TEXT, SAVESTATS_RECT)

        SAVESTATS_BACK = Button(image=None, pos = (200, 200),
                           text_input="<- BACK", font=get_font(30), base_color = "white", hovering_color = "Green")
        SAVESTATS_BACK.changeColor(SAVESTATS_MOUSE_POS)
        SAVESTATS_BACK.update(screen)

        SAVESTATS_BUTTON = Button(image = pygame.image.load("assets/Play Rect.png"), pos=(640,370),
                             text_input="SAVE STATS", font=get_font(50), base_color="#b68f40", hovering_color="Green")

        for button in [SAVESTATS_BACK, SAVESTATS_BUTTON]:
            button.changeColor(SAVESTATS_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SAVESTATS_BACK.checkForInput(SAVESTATS_MOUSE_POS):
                    on_back()
                    return
                if SAVESTATS_BUTTON.checkForInput(SAVESTATS_MOUSE_POS):  # data saved here
                    save_data(user_nickname, all_time_score)   
          
        pygame.display.update()

