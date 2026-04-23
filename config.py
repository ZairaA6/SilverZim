# data structures
maps = {"Silverstone":"assets/silverstone_map.png", "Monaco":"assets/monaco_map.png", "RedBullRing":"assets/redbullring_map.png", "Suzuka":"assets/suzuka_map.png","Tutorial1":"assets/tutorial_one_map.png", 
        "Tutorial2":"assets/tutorial_two_map.png", "Tutorial3":"assets/tutorial_three_map.png"}
starting_coords = {"Silverstone": (355,90),"Monaco":(107,207),"RedBullRing":(716,332), "Tutorial1":(372,122), "Tutorial2":(372,122), "Tutorial3":(372,122)}
finish_line_coords = {"Silverstone": (310,50),"Monaco":(102,293),"RedBullRing":(662,381), "Tutorial3": (250,100)}

lap_checkpoints = {"Silverstone": [(135,275), (321, 68)],"Monaco": [(365,160), (115, 277)], "RedBullRing":[(263,326),(676,178)], "Tutorial1":[(795,223), (259,98)], "Tutorial2":[(795,223), (259,98)],
                     "Tutorial3":[(795,223), (259,98)]}
DRS_checkpoints = {"Monaco": [(843, 360), (325, 327)], "Silverstone": [(565, 393), (726, 174), (435,480), (105,245)], "RedBullRing": [(500, 467), (207, 295), (113,194), (469,84)],
                    "Tutorial2": [(315,415), (130, 210)], "Tutorial3": [(315,415), (130, 210)]}
PITSTOP_checkpoint = {"Silverstone": (807,110), "Monaco": (162, 329),"RedBullRing":(784,142), "Tutorial2": (793, 208),  "Tutorial3": (793, 208)}
laps_to_win = {"Monaco": 14, "Silverstone": 10, "RedBullRing":13,"Suzuka": 11, "Tutorial1": 8, "Tutorial2": 8, "Tutorial3":8}
steer_text = {"Silverstone":[(800,600),(840,575),(880,600),(840,630)], "Monaco":[(800,600),(840,575),(880,600),(840,630)], "RedBullRing":[(800,600),(840,575),(880,600),(840,630)], 
                "Tutorial1": [(1060,330),(1100,305),(1140,330),(1100,360)], "Tutorial2": [(1060,330),(1100,305),(1140,330),(1100,360)], "Tutorial3": [(800,600),(840,575),(880,600),(840,630)]}
point_allocation = {"1": 25,"2":18,"3": 15,"4":12,"5":10,"6":8,"7":6,"8":4,"9":2,"10":1}
player_names = ["formula_one_pro", "ai_24","silverZim11","simulated_player22","hamilton_8","sebastian_vettel","lewis_hamilton","leclerc_ai_16","charles_leclerc","lando_norris","vertappen_ai",
                "8x_world_champ", "michael_shumacher", "artyon_senna","senna_ai", "susie_wolff", "martin_brundle","jenson_button","natalie_pinkham"]
coloured_cars = ["assets/car1.png", "assets/car2.png","assets/car3.png","assets/car4.png","assets/car5.png","assets/car6.png"]

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 700
BORDER_COLOR = (255,255,255,255)

# car functionality regulation
CAR_WIDTH:float = 35
CAR_HEIGHT:float = 35
DRS_RADIUS:float = 50  
PITSTOP_RADIUS:float = 50
CHECKPOINT_RADIUS:float = 30

# user-car variables & constants
user_angle:float = 0
user_speed:float = 0
acceleration:float = 0.15    # acceleration is not a CONSTANT  
DECELERATION:float = 0.05
TRACK_LIMITS_DECELERATION:float = 0.8     
MAX_VELOCITY:int = 10 
