import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self, surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #draw button on screen
            surface.blit(self.image, (self.rect.x, self.rect.y))

            return action






pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_paused = False

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (191, 0, 230)

#load button images
resume_img = pygame.image.load("resumeButton.png").convert_alpha()

#create button instances
resume_button = Button(304,125, resume_img, 1)

def draw_text(text,dont,text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

run = True
while run:
    screen.fill((52, 78, 91))

    #check if game is paused
    if game_paused == True:
        resume_button.draw(screen)

        #display menu
    else:
        draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()