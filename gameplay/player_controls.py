import math, pygame
from config import *

# user controls and movement
def update_player_movement(x, y, angle, speed, acceleration, keys):
    controls = {
        "left": keys[pygame.K_LEFT] or keys[pygame.K_a],
        "right": keys[pygame.K_RIGHT] or keys[pygame.K_d],
        "gas": keys[pygame.K_UP] or keys[pygame.K_w],
        "brake": keys[pygame.K_DOWN] or keys[pygame.K_s],
    }

    if controls["left"]:
        angle += 3
    if controls["right"]:
        angle -= 3
    if controls["gas"] and speed < MAX_VELOCITY:
        speed += acceleration
    if controls["brake"]:
        if speed > 0:
            speed -= DECELERATION
        if speed < 0:
            speed = 0

    # section below: user_controlled_car cannot escape the game_map
    # x & y denotes user x and y
    half_car_width = CAR_WIDTH / 2   # half car_width or car_height as position is denoted by centre of car
    half_car_height = CAR_HEIGHT / 2

    x = max(x, 23 + half_car_width)
    x = min(x, 943 - half_car_width)
    y = max(y, 25 + half_car_height)
    y = min(y, 535 - half_car_height)

    x += speed * math.cos(math.radians(angle))
    y -= speed * math.sin(math.radians(angle))

    return angle, speed, x, y, controls # controls communicates with gui.py - dashboard to show which controls are being pressed


def apply_track_limits(game_map, x, y, user_speed):
    track_limits_hit = game_map.get_at((int(x), int(y))) == BORDER_COLOR

    if track_limits_hit:
        if user_speed > 0:
            user_speed *= TRACK_LIMITS_DECELERATION
        if user_speed < 0:
            user_speed = 0

    return user_speed, track_limits_hit # returns whether track limits have been hit to display "track limits!" on the screen in gui.py



def update_DRS(circuit, x, y, user_speed, keys, DRS_on):
    DRS_available = False

    distance_to_DRS_start_list = []
    distance_to_DRS_end_list = []

    for i in range(0, len(DRS_checkpoints[circuit]), 2):
        dist = math.sqrt((x - DRS_checkpoints[circuit][i][0])**2 + (y - DRS_checkpoints[circuit][i][1])**2)
        distance_to_DRS_start_list.append(dist)

    for i in range(1, len(DRS_checkpoints[circuit]), 2):
        dist = math.sqrt((x - DRS_checkpoints[circuit][i][0])**2 + (y - DRS_checkpoints[circuit][i][1])**2)
        distance_to_DRS_end_list.append(dist)

    if distance_to_DRS_start_list and min(distance_to_DRS_start_list) < DRS_RADIUS:
        DRS_available = True
    elif distance_to_DRS_end_list and min(distance_to_DRS_end_list) < DRS_RADIUS and DRS_on:
        user_speed = 2
        DRS_on = False

    if DRS_available and (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]):
        DRS_on = True
        user_speed = 8
        # could refine selection statement to see if any AI cars are also within the DRS radius and then you return that
    

    return user_speed, DRS_on, DRS_available



def update_pitstop(circuit, x, y, user_speed, acceleration, keys, tyre_compound, pitstop_screen_show, lap_count):
    pitstop_available = False
     # if true, user can pit
    PITSTOP_completed = False   # future maintenance - one pitstop is required or race is invalid

    distance_to_pitlane = math.sqrt(
        (x - PITSTOP_checkpoint[circuit][0])**2 + (y - PITSTOP_checkpoint[circuit][1])**2
    )

    if lap_count % 2 == 0 and distance_to_pitlane < PITSTOP_RADIUS: # opportunity to pit isnt always possible, drivers dont do this every lap so it will show up 50% of the time
        pitstop_available = True
 
    if pitstop_available and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):  # PITSTOP controlled by shift
        user_speed = 0
        pitstop_screen_show = True

    if pitstop_screen_show:
        if keys[pygame.K_1]:
            acceleration = 0.3
            tyre_compound = "Soft"
            pitstop_screen_show = False # SOFTS: 1.3x faster
        elif keys[pygame.K_2]:
            acceleration = 0.15
            tyre_compound = "Medium"
            pitstop_screen_show = False # MEDIUMS: 1.15x faster
        elif keys[pygame.K_3]:
            acceleration = 0.1
            tyre_compound = "Hard"
            pitstop_screen_show = False # HARDS: 1.1x faster
        elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            pitstop_screen_show = False

    return user_speed, acceleration, tyre_compound, pitstop_screen_show, pitstop_available