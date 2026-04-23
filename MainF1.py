import pygame, sys, math, neat, random, json
from ui.button import Button
from config import *
from domain.car import SimCar
from persistence.records import save_data, load_records, get_user_score
from ui.dashboard import get_font, get_dashboard_font, speedometer, display_tyres, draw_controls, draw_track_limits_warning, draw_drs_alert, draw_pitstop_alert, draw_pitstop_screen
from ui.screens import viewstats, savestats
from domain.leaderboard import add_player, update_leaderboard, get_sorted_leaderboard, leaderboard_positions, clear_leaderboard
from gameplay.player_controls import apply_track_limits, update_player_movement, apply_track_limits, update_DRS, update_pitstop
pygame.init()
pygame.font.init()

# screen variables - map regulation
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),  pygame.RESIZABLE)
BG = pygame.image.load("assets/final_background.png")
OPTIONS = pygame.image.load("assets/info_screen.png")  # info screen
STATSBG = pygame.image.load("assets/stats_screen.png")    # stats background
MAPS_SELECTION = pygame.image.load("assets/maps_screen.png")
PITSTOP_screen = pygame.image.load("assets/PITSTOP_GUI.png")
RESULTS_SCREEN = pygame.image.load("assets/results_screen.png")
T3_intro = pygame.image.load("assets/tutorial_3.0.png")
T3_intro = pygame.transform.scale(T3_intro,(200, 350))
T3_results = pygame.image.load("assets/tutorial_three_results.png")     # tutorial 3's separate results GUI background, as tutorial_three() does not have its own subroutine
DRS_ALERT_IMAGE = pygame.image.load("assets/DRS_Alert.png")
PITSTOP_ALERT_IMAGE = pygame.image.load("assets/PITSTOP_Alert.png")  
PITSTOP_SCREEN_IMAGE = pygame.image.load("assets/PITSTOP_GUI.png")  
    
# car functionality regulation
user_car_image = pygame.image.load("assets/user_car.png").convert_alpha()
user_car_image = pygame.transform.scale(user_car_image, (CAR_WIDTH, CAR_HEIGHT))
current_generation:int = 0

# user-car variables & constants 
user_start = True   # used to check whether it is the first lap for user-controlled car, keep its separate from simulated cars
last_checkpoint:int = 1   # condition checking variable for lap progression()



def display_leaderboard():
    LEADERBD_TEXT = get_dashboard_font(20).render(" ", True, (38,38,38))
    if update_leaderboard:
        sorted_leaderboard = get_sorted_leaderboard()
        #print("Leaderboard: ")
        for i, (player, lap) in enumerate(sorted_leaderboard):
            #print(f"{i+1}. {player}:{lap}")
            LEADERBD_TEXT = get_dashboard_font(18).render(player+ " - "+str(lap), True, (38,38,38))
            SCREEN.blit(LEADERBD_TEXT, (1022,120 + (26*i)))                                                         
    else:
        print("leaderboard is empty")

# end of leaderboard functions


def results_summary(position_based_score, all_time_score, sorted_leaderboard, circuit):
    pygame.display.set_caption("Results")

    while True:
        RESULTS_MOUSE_POS = pygame.mouse.get_pos()
        
        # different results window for tutorial 3
        if circuit == "Tutorial3":
            SCREEN.blit(T3_results, (0,0))
            score_text_position = (613, 390)
        else:
            SCREEN.blit(RESULTS_SCREEN, (0,0))
            score_text_position = (535, 320)
            for i, (player,lap) in enumerate(sorted_leaderboard):
                LEADERBD_TEXT = get_dashboard_font(18).render(player, True, (175,171,171))
                SCREEN.blit(LEADERBD_TEXT, (915,100 + (26*i)))

        RESULTS_BACK = Button(image=None, pos = (143, 139),
                           text_input="BACK <-", font=get_font(22), base_color = "white", hovering_color = "Green")
        RESULTS_BACK.changeColor(RESULTS_MOUSE_POS)
        RESULTS_BACK.update(SCREEN)

        SCORE_TEXT = get_dashboard_font(30).render(str(position_based_score), True, (175,171,171))
        SCREEN.blit(SCORE_TEXT, (score_text_position))

        ALLTIMESCORE_TEXT = get_dashboard_font(30).render(str(all_time_score), True, (175,171,171))
        SCREEN.blit(ALLTIMESCORE_TEXT, (score_text_position[0],score_text_position[1]+40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESULTS_BACK.checkForInput(RESULTS_MOUSE_POS):
                    clear_leaderboard()  # clear leaderboard
                    choose_map()
        pygame.display.update()
    





def tutorial_one(circuit):
    global all_time_score
    pygame.display.set_caption("Tutorial One")
    game_map = pygame.image.load(maps[circuit]).convert()
    T1_toptip = pygame.image.load("assets/tutorial_1.1.png")
    T1_racedistance = pygame.image.load("assets/tutorial_1.2.png")
    T1_funfact = pygame.image.load("assets/tutorial_1.3.png")
    T1_results = pygame.image.load("assets/tutorial_one_results.png")

    user_angle = 0
    user_speed = 0
    checkpoint_flags = [False] * len(lap_checkpoints[circuit])
    x = starting_coords[circuit][0]
    y = starting_coords[circuit][1]
    lap_count = 1
    rotated_user_car = user_car_image
    all_time_score += 10

    clock = pygame.time.Clock()
    while True:

        T1_MOUSE_POS = pygame.mouse.get_pos()
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if T1_BACK.checkForInput(T1_MOUSE_POS):
                    choose_map()

        SCREEN.blit(game_map, (0,0))
        rotated_user_car = pygame.transform.rotate(user_car_image,user_angle)
        rotated_user_rect = rotated_user_car.get_rect(center=(x,y)) 
        SCREEN.blit(rotated_user_car, rotated_user_rect.topleft)

        T1_BACK = Button(image=None, pos = (998, 40),
                           text_input="<- BACK", font=get_font(20), base_color = "Black", hovering_color = "Green")
        T1_BACK.changeColor(T1_MOUSE_POS)
        T1_BACK.update(SCREEN)

        keys = pygame.key.get_pressed()
        # user controls & movement
        user_angle, user_speed, x, y, controls= update_player_movement(x,y, user_angle, user_speed, acceleration, keys)
        draw_controls(SCREEN, circuit, controls)
        # track limits
        user_speed,track_limits_hit = apply_track_limits(game_map, x, y, user_speed)
        draw_track_limits_warning(SCREEN, circuit, track_limits_hit)
        speedometer(SCREEN,user_speed, (1100,170))

        # lap progression
        for i, checkpoint in enumerate(lap_checkpoints[circuit]):
            dist_to_checkpoint = math.sqrt((x - checkpoint[0])**2 + (y - checkpoint[1])**2)

            if dist_to_checkpoint < CHECKPOINT_RADIUS and not checkpoint_flags[i]:
                checkpoint_flags[i] = True

                if i == last_checkpoint:
                    lap_count += 1
                    print(lap_count)
    
            elif dist_to_checkpoint >= CHECKPOINT_RADIUS:
                checkpoint_flags[i] = False
            
        LAPS_TEXT = get_dashboard_font(30).render(str(lap_count) + "/" + str(laps_to_win[circuit]), True, (0,0,0))
        LAPS_RECT = LAPS_TEXT.get_rect(center=(82,105))
        SCREEN.blit(LAPS_TEXT, LAPS_RECT)

        # tutorial one guidance
        if lap_count <= 3:
            T1POINTS_TEXT = get_dashboard_font(30).render("You have 8 laps to go. Use WASD or ARROWS to steer, accelerate and brake.", True, ("Black"))
            SCREEN.blit(T1POINTS_TEXT, (20,550))
            T1POINTS_TEXT = get_dashboard_font(30).render("See INFORMATION in main menu for more options.", True, ("Black"))
            SCREEN.blit(T1POINTS_TEXT, (20,600))

        if lap_count <= 6 and lap_count > 3 :
            SCREEN.blit(T1_toptip, (20,550))

        if lap_count <= 8 and lap_count > 6 :
            SCREEN.blit(T1_racedistance, (20,550))
        
        if lap_count <= 8 and lap_count > 6 :
            SCREEN.blit(T1_funfact, (990,400))

        # condition to check if race tutorial one is complete
        elif lap_count == (laps_to_win[circuit]+1):
            SCREEN.blit(T1_results, (0,0))  # results screen
            T1POINTS_TEXT = get_dashboard_font(30).render("10", True, (175,171,171))   # user gets 10 points for entering tutorial one
            T1POINTS_RECT = T1POINTS_TEXT.get_rect(center=(630,405))
            SCREEN.blit(T1POINTS_TEXT, T1POINTS_RECT)                                  # displayed on the screen


            T1POINTS_TEXT = get_dashboard_font(30).render(str(all_time_score), True, (175,171,171))  # user score updated displayed
            T1POINTS_RECT = T1POINTS_TEXT.get_rect(center=(630,444))
            SCREEN.blit(T1POINTS_TEXT, T1POINTS_RECT)

            # create new BACK button for results summary screen
            T1_BACK = Button(image=None, pos = (180, 150),
                           text_input="<- BACK", font=get_font(30), base_color = (175,171,171), hovering_color = "Green")
            T1_BACK.changeColor(T1_MOUSE_POS)
            T1_BACK.update(SCREEN)

        
        pygame.display.flip() 
        clock.tick(90) # 60 fps
        pygame.display.update()

def tutorial_two(circuit):
    global all_time_score
    pygame.display.set_caption("Tutorial Two")
    game_map = pygame.image.load(maps[circuit]).convert()
    T2_intro = pygame.image.load("assets/tutorial_2.0.png")
    T2_pitstop = pygame.image.load("assets/tutorial_2.1.png")
    T2_funfact1 = pygame.image.load("assets/tutorial_2.2.png")
    T2_funfact2 = pygame.image.load("assets/tutorial_2.3.png")
    T2_funfact3 = pygame.image.load("assets/tutorial_2.4.png")
    T2_drs = pygame.image.load("assets/tutorial_2.5.png")
    T2_results = pygame.image.load("assets/tutorial_two_results.png")

    user_angle = 0
    user_speed = 0
    acceleration = 0.15
    DRS_on = False
    tyre_compound = "Medium"
    PITSTOP_screen_show = False

    checkpoint_flags = [False] * len(lap_checkpoints[circuit])
    x = starting_coords[circuit][0]
    y = starting_coords[circuit][1]
    lap_count = 1    
    rotated_user_car = user_car_image
    all_time_score += 10

    clock = pygame.time.Clock()
    while True:

        T2_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if T2_BACK.checkForInput(T2_MOUSE_POS):
                    choose_map()
        SCREEN.blit(game_map, (0,0))
        rotated_user_car = pygame.transform.rotate(user_car_image,user_angle)
        rotated_user_rect = rotated_user_car.get_rect(center=(x,y)) 
        SCREEN.blit(rotated_user_car, rotated_user_rect.topleft)

        T2_BACK = Button(image=None, pos = (998, 40),
                           text_input="<- BACK", font=get_font(20), base_color = "black", hovering_color = "green")
        T2_BACK.changeColor(T2_MOUSE_POS)
        T2_BACK.update(SCREEN)

        keys = pygame.key.get_pressed()
        user_angle, user_speed, x, y, controls= update_player_movement(x,y, user_angle, user_speed, acceleration, keys)
        draw_controls(SCREEN, circuit, controls)
        user_speed,track_limits_hit = apply_track_limits(game_map, x, y, user_speed)
        draw_track_limits_warning(SCREEN, circuit, track_limits_hit)
        # drs
        user_speed, DRS_on, DRS_available = update_DRS(circuit, x, y, user_speed, keys, DRS_on)
        draw_drs_alert(SCREEN, DRS_available, DRS_ALERT_IMAGE)
        # pitstop
        user_speed, acceleration, tyre_compound, PITSTOP_screen_show, pitstop_available = update_pitstop(circuit, x, y, user_speed, acceleration, keys, tyre_compound, PITSTOP_screen_show, lap_count)
        draw_pitstop_alert(SCREEN, pitstop_available, PITSTOP_ALERT_IMAGE)
        draw_pitstop_screen(SCREEN, PITSTOP_screen_show, PITSTOP_SCREEN_IMAGE)
        
        speedometer(SCREEN, user_speed, (1100,170))
        display_tyres(SCREEN,tyre_compound, acceleration, (1160,205))

        for i, checkpoint in enumerate(lap_checkpoints[circuit]):
            dist_to_checkpoint = math.sqrt((x - checkpoint[0])**2 + (y - checkpoint[1])**2)

            if dist_to_checkpoint < CHECKPOINT_RADIUS and not checkpoint_flags[i]:
                checkpoint_flags[i] = True

                if i == last_checkpoint:
                    lap_count += 1
                    print(lap_count)
    
            elif dist_to_checkpoint >= CHECKPOINT_RADIUS:
                checkpoint_flags[i] = False
            
        LAPS_TEXT = get_dashboard_font(30).render(str(lap_count) + "/" + str(laps_to_win[circuit]), True, (0,0,0))
        LAPS_RECT = LAPS_TEXT.get_rect(center=(82,105))
        SCREEN.blit(LAPS_TEXT, LAPS_RECT)

        if lap_count <= 2:
            SCREEN.blit(T2_intro, (20,550))

        if lap_count <= 4 and lap_count > 2 :
            SCREEN.blit(T2_pitstop, (20,550))
        
        if lap_count <= 8 and lap_count > 4 :
            SCREEN.blit(T2_drs, (20,550))

        if lap_count <= 3 and lap_count > 1 :
            SCREEN.blit(T2_funfact1, (990,400))
        
        if lap_count <= 5 and lap_count > 3 :
            SCREEN.blit(T2_funfact2, (990,400))
        
        if lap_count <= 8 and lap_count > 5 :
            SCREEN.blit(T2_funfact3, (990,400))


        elif lap_count == (laps_to_win[circuit]+1):
            SCREEN.blit(T2_results, (0,0))
            T2POINTS_TEXT = get_dashboard_font(30).render("10", True, (175,171,171))
            T2POINTS_RECT = T2POINTS_TEXT.get_rect(center=(630,405))
            SCREEN.blit(T2POINTS_TEXT, T2POINTS_RECT)


            T1POINTS_TEXT = get_dashboard_font(30).render(str(all_time_score), True, (175,171,171))
            T1POINTS_RECT = T1POINTS_TEXT.get_rect(center=(630,444))
            SCREEN.blit(T1POINTS_TEXT, T1POINTS_RECT)

            T2_BACK = Button(image=None, pos = (180, 150),
                           text_input="<- BACK", font=get_font(30), base_color = (175,171,171), hovering_color = "Green")
        
            T2_BACK.changeColor(T2_MOUSE_POS)
            T2_BACK.update(SCREEN)

        pygame.display.flip() 
        clock.tick(90) # 60 fps
        pygame.display.update()
    

def f1_map_wrapper(circuit):
    def f1_map(genomes, config):
        global user_angle
        global user_speed
        global user_start
        global x  # user position coordinates
        global y
        global lap_count
        global DRS_on
        global acceleration
        global PITSTOP_screen_show
        global tyre_compound
        global current_generation
        global checkpoint_flags
        global all_time_score
        global sim_success

        pygame.display.set_caption(circuit)
        current_generation += 1
        rotated_user_car = user_car_image
        game_map = pygame.image.load(maps[circuit]).convert()

        # this below is to navigate the issue of user_controlled car restarting after each generation in simulation
        if user_start == True:
            x = starting_coords[circuit][0]
            y = starting_coords[circuit][1]
            lap_count = 1
            DRS_on = False
            PITSTOP_screen_show = False
            tyre_compound = "Medium"
            checkpoint_flags = [False] * len(lap_checkpoints[circuit])   # flag to initialise all checkpoints to false
            sim_success = True
        else:
            x = x    
            y = y
            lap_count = lap_count
            DRS_on = DRS_on
            PITSTOP_screen_show = PITSTOP_screen_show
            tyre_compound = tyre_compound
            checkpoint_flags = checkpoint_flags
            sim_success = sim_success
        
        # empty collections for nets and cars in each new generation
        nets = []
        cars = []
 
        # update nets & cars based on NEAT function
        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)    
            nets.append(net)
            g.fitness = 0
            cars.append(SimCar(circuit))

        # clock settings & can limit time using counter
        clock = pygame.time.Clock()
        counter = 0   
        
        while True:

            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            pygame.time.delay(10) # makes user car move slower, at a more acceptable speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        clear_leaderboard()
                        cars.clear()
                        nets.clear()
                        current_generation = 0
                        user_start = True
                        choose_map()

            SCREEN.blit(game_map, (0,0))
            add_player(user_nickname, 1)
            
            if sim_success == False and current_generation == 3:
                print("ERROR: This map ("+maps[circuit]+") might not be valid, Press '<- Back' to Return.") # terminal message to check if invalid map

            rotated_user_car = pygame.transform.rotate(user_car_image,user_angle)
            rotated_user_rect = rotated_user_car.get_rect(center=(x,y)) 
            SCREEN.blit(rotated_user_car, rotated_user_rect.topleft)             # drawing object on screen which is rectangle here 

            PLAY_BACK = Button(image=None, pos = (998, 40),
                           text_input="<- BACK", font=get_font(20), base_color = "Black", hovering_color = "Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            # if tutorial 3, display intro
            if lap_count <=1 and circuit == 'Tutorial3':
                SCREEN.blit(T3_intro,(990,300))

            # user-centred features
            keys = pygame.key.get_pressed()
            user_angle, user_speed, x, y, controls= update_player_movement(x,y, user_angle, user_speed, acceleration, keys)
            draw_controls(SCREEN, circuit, controls)
            user_speed,track_limits_hit = apply_track_limits(game_map, x, y, user_speed)
            draw_track_limits_warning(SCREEN, circuit, track_limits_hit)
            # drs
            user_speed, DRS_on, DRS_available = update_DRS(circuit, x, y, user_speed, keys, DRS_on)
            draw_drs_alert(SCREEN, DRS_available, DRS_ALERT_IMAGE)
            # pitstop
            user_speed, acceleration, tyre_compound, PITSTOP_screen_show, pitstop_available = update_pitstop(circuit, x, y, user_speed, acceleration, keys, tyre_compound, PITSTOP_screen_show, lap_count)
            draw_pitstop_alert(SCREEN, pitstop_available, PITSTOP_ALERT_IMAGE)
            draw_pitstop_screen(SCREEN, PITSTOP_screen_show, PITSTOP_SCREEN_IMAGE)
            # displays for dashboard
            speedometer(SCREEN, user_speed,(435,630))
            display_tyres(SCREEN, tyre_compound, acceleration, (70,605))

            # lap progression - not its own function since errors are caused if it is.
            for i, checkpoint in enumerate(lap_checkpoints[circuit]):
                dist_to_checkpoint = math.sqrt((x - checkpoint[0])**2 + (y - checkpoint[1])**2)
                if dist_to_checkpoint < CHECKPOINT_RADIUS and not checkpoint_flags[i]:
                    checkpoint_flags[i] = True
                    if i == last_checkpoint:
                        lap_count += 1
                elif dist_to_checkpoint >= CHECKPOINT_RADIUS:
                    checkpoint_flags[i] = False
            LAPS_TEXT = get_dashboard_font(30).render(str(lap_count) + "/" + str(laps_to_win[circuit]), True, (0,0,0))
            LAPS_RECT = LAPS_TEXT.get_rect(center=(82,105))
            SCREEN.blit(LAPS_TEXT, LAPS_RECT)

            # leaderboard
            update_leaderboard(cars, circuit, lap_count, user_nickname)
            display_leaderboard()

            #print(max(leaderboard_positions.values())) - USE TO TRACE LEADERBOARD_POSITIONS
            # checks for winner
            if max(leaderboard_positions.values()) == (laps_to_win[circuit] + 1):
                sorted_leaderboard = get_sorted_leaderboard()
                leaderboard_list = []               # create a list of exact same thing in sorted_leaderboard dictionary
                for player in sorted_leaderboard:
                    leaderboard_list.append(player[0])
                
                # only scores points if user is in top 10 positions
                if str(leaderboard_list.index(user_nickname) + 1) in point_allocation:                          
                    position_based_score = point_allocation[str(leaderboard_list.index(user_nickname) + 1)]
                else:
                    position_based_score = 0

                all_time_score += position_based_score
                clear_leaderboard()
                cars.clear()
                nets.clear()
                current_generation = 0
                user_start = True
                results_summary(position_based_score, all_time_score, sorted_leaderboard, circuit)
   
            # simulation NEAT
            for i, car in enumerate(cars):
                output = nets[i].activate(car.get_data())
                choice = output.index(max(output))
                if choice == 0:
                    car.sim_angle += 10 # left
                elif choice == 1:
                    car.sim_angle -= 10 # right
                elif choice == 2:
                    if (car.sim_speed - 2 >= 12):    # min speed = 12
                        car.sim_speed -= 2 # slows down
                elif choice == 3:
                     car.sim_angle += 30 # extreme left - NEW
                elif choice == 4:
                     car.sim_angle -= 30 # extreme right - NEW
                else:
                    car.sim_speed += 3# speeds up
        

            # checks if car is still alive
            # increase fitness if yes 
            still_alive = 0
            for i, car in enumerate(cars):
                if car.is_alive():
                    still_alive += 1
                    car.update_sim_car(circuit,game_map)
                    genomes[i][1].fitness += car.get_reward()
            
            # conditions to check if a new generation should begin: still_alive = 0 & counter = 1200
            if still_alive == 0:
                user_start = False
                break

            counter += 1 
            if counter == 1200:  # about 80 seconds
                sim_success = False
                break      

            # draw all cars that are alive
            for car in cars:
                if car.is_alive():
                    car.draw(SCREEN)

            # display simulation algorithm info
            GEN_FONT = get_dashboard_font(30).render("Generation: " + str(current_generation), True, (38,38,38))
            GEN_RECT = GEN_FONT.get_rect(center=(645,590))
            SCREEN.blit(GEN_FONT, GEN_RECT)

            ALIVE_FONT = get_dashboard_font(20).render("Still Alive: " + str(still_alive), True, (38,38,38))
            ALIVE_RECT = ALIVE_FONT.get_rect(center=(645,630))
            SCREEN.blit(ALIVE_FONT, ALIVE_RECT)

            pygame.display.flip() 
            clock.tick(60) # 60 fps
            pygame.display.update()
        pass
    return f1_map







def choose_map():
    pygame.display.set_caption("Choose Map")
    config_path = "./neat_config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    while True:
        MAPS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(MAPS_SELECTION, (0,0))

        MAPS_TEXT = get_font(50).render("Choose Map:", True, "#3D3938")
        MAPS_RECT = MAPS_TEXT.get_rect(center = (640, 100))
        SCREEN.blit(MAPS_TEXT, MAPS_RECT)

        MAPS_BACK = Button(image=None, pos = (93, 45),
                           text_input="BACK", font=get_font(45), base_color = "white", hovering_color = "Yellow")

        T1_BUTTON = Button(image = None, pos=(280,195),
                             text_input="TUTORIAL ONE", font=get_font(35), base_color="white", hovering_color="Green")
        T2_BUTTON = Button(image = None, pos=(645,265),
                             text_input="TUTORIAL TWO", font=get_font(35), base_color="white", hovering_color="Yellow")
        T3_BUTTON = Button(image = None, pos=(1003,195),
                             text_input="TUTORIAL THREE", font=get_font(35), base_color="white", hovering_color="Red")

        SILVERSTONE_BUTTON = Button(image = None, pos=(280,480),
                             text_input="Silverstone", font=get_font(35), base_color="white", hovering_color="Yellow")
        MONACO_BUTTON = Button(image = None, pos=(645,530),
                             text_input="Circuit de Monaco", font=get_font(30), base_color="white", hovering_color="Yellow")
        REDBULL_BUTTON = Button(image = None, pos=(1003,480),
                             text_input="Red Bull Ring", font=get_font(38), base_color="white", hovering_color="Yellow")

        for button in [MAPS_BACK, T1_BUTTON, T2_BUTTON, T3_BUTTON, SILVERSTONE_BUTTON, MONACO_BUTTON, REDBULL_BUTTON]:
            button.changeColor(MAPS_MOUSE_POS)
            button.update(SCREEN)   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MAPS_BACK.checkForInput(MAPS_MOUSE_POS):
                    main_menu()
                elif T1_BUTTON.checkForInput(MAPS_MOUSE_POS):
                    tutorial_one("Tutorial1")
                elif T2_BUTTON.checkForInput(MAPS_MOUSE_POS):
                    tutorial_two("Tutorial2")
                elif T3_BUTTON.checkForInput(MAPS_MOUSE_POS):
                    population.run(f1_map_wrapper("Tutorial3"), 1000)
                elif SILVERSTONE_BUTTON.checkForInput(MAPS_MOUSE_POS):
                    population.run(f1_map_wrapper("Silverstone"), 1000)
                elif MONACO_BUTTON.checkForInput(MAPS_MOUSE_POS):
                    population.run(f1_map_wrapper("Monaco"), 1000)
                elif REDBULL_BUTTON.checkForInput(MAPS_MOUSE_POS):
                    population.run(f1_map_wrapper("RedBullRing"), 1000) #maintainable
        pygame.display.update()

def options(): # Information Options screen
    pygame.display.set_caption("Information Options")

    while True:
        SCREEN.blit(OPTIONS, (0,0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_BACK = Button(image=None, pos = (80, 70),
                           text_input="<- BACK", font=get_font(24), base_color = "Green", hovering_color = "White")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            choose_map() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def main_menu(): # Main Menu Screen
    pygame.display.set_caption("Menu")

    while True:
        SCREEN.blit(BG, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(110).render("Silver Zim", True, "#3D3938")
        MENU_RECT = MENU_TEXT.get_rect(center=(640,100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = Button(image = pygame.image.load("assets/Play Rect.png"), pos=(640, 200),
                             text_input="PLAY", font=get_font(60), base_color="#b68f40", hovering_color="White")
        OPTIONS_BUTTON = Button(image = pygame.image.load("assets/Options Rect.png"), pos=(640,295),
                             text_input="INFORMATION", font=get_font(50), base_color="#b68f40", hovering_color="White")
        VIEWSTATS_BUTTON = Button(image = pygame.image.load("assets/Options Rect.png"), pos=(640,485),
                             text_input="VIEW STATS", font=get_font(50), base_color="#b68f40", hovering_color="White")
        SAVESTATS_BUTTON = Button(image = pygame.image.load("assets/Options Rect.png"), pos=(640,390),
                             text_input="SAVE STATS", font=get_font(50), base_color="#b68f40", hovering_color="White")
        QUIT_BUTTON = Button(image = pygame.image.load("assets/Play Rect.png"), pos=(640,580),
                             text_input="QUIT", font=get_font(60), base_color="#b68f40", hovering_color="White")


        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, VIEWSTATS_BUTTON, SAVESTATS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    choose_map() 
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if VIEWSTATS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    viewstats(SCREEN, STATSBG, user_nickname, main_menu)
                if SAVESTATS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    savestats(SCREEN, STATSBG, user_nickname, all_time_score, main_menu)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()


# ------ MAIN PROGRAM -------------
if __name__ == "__main__":
    print("\n\n-------WELCOME TO SILVER ZIM-------\n")
    user_nickname = str(input("Please enter a nickname to continue (Must be under 15 charcters): "))
    while len(user_nickname) > 15 or len(user_nickname) ==0:  #validation
        user_nickname = str(input("Invalid: Please enter a nickname under 15 characters: "))
    print("USERNAME SELECTION SUCCESSFUL \n beep beep silver zim loading...")

    all_user_records = load_records()                              # creates variable for all dictionaries in json file - to be used in return_user_score()
    if get_user_score(user_nickname, all_user_records) is None:
        print(f"No score found for the nickname: {user_nickname}")    # returning info if record does not contain information about the user-entered nickname - does not leave user confused
        all_time_score = 100
    else:
        all_time_score = get_user_score(user_nickname, all_user_records)

    main_menu()
