import pygame, math, random
from config import *

class SimCar():
    def  __init__(self, circuit):
        # Load Random coloured car file for AI_simulation
        random_car = random.choice(coloured_cars)

        # Load the image of each simulated car
        self.sim_car_image = pygame.image.load(random_car).convert() 
        self.sim_car_image = pygame.transform.scale(self.sim_car_image, (CAR_WIDTH, CAR_HEIGHT))
        
        # Rotated version of simulated car continously updated
        self.rotated_sim_car = self.sim_car_image 

        self.sim_position = list(starting_coords[circuit]) # Starting Position depending on Circuit
        self.sim_angle = 0
        self.sim_speed = 0
        self.sim_center = [self.sim_position[0] + CAR_WIDTH / 2, self.sim_position[1] + CAR_HEIGHT / 2] 
        self.sim_speed_set = False # Flag For Default Speed later on

        self.radars = [] # List For Radar lines
        self.alive = True # Boolean To Check If Sim Car has Crashed
        self.sim_distance = 0 # distance driven - used to calculate fitness using NEAT

        self.sim_lap_count = 1 # for Leaderboard

    def draw(self, SCREEN):
        SCREEN.blit(self.rotated_sim_car, self.sim_position)
    
    def __check_track_limits(self, game_map): 
        self.alive = True
        for point in self.corners:
            #if any corner touches the border colour, there is a crash
            #print(point, ":",game_map.get_at((int(point[0]), int(point[1])))) tracing
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break 
    
    def __check_radar(self, degree, game_map): 
        radar_length = 0
        # continously update simX and simY to find point where radar line meets track limits aka border colour
        simX = int(self.sim_center[0] + math.cos(math.radians(360 - (self.sim_angle + degree))) * radar_length)
        simY = int(self.sim_center[1] + math.sin(math.radians(360 - (self.sim_angle + degree))) * radar_length)
        
        while not game_map.get_at ((simX,simY)) == BORDER_COLOR: 
            radar_length += 1
            simX = int(self.sim_center[0] + math.cos(math.radians(360 - (self.sim_angle + degree))) * radar_length)
            simY = int(self.sim_center[1] + math.sin(math.radians(360 - (self.sim_angle + degree))) * radar_length)

        # calculate radar line length aka distance to border, append to radars
        dist_to_border = int(math.sqrt((simX - self.sim_center[0])** 2 + (simY - self.sim_center[1])** 2))
        self.radars.append([(simX, simY), dist_to_border])

    def update_sim_car(self, circuit, game_map):     # continously updated in f1_map game loop as the sim car moves
        # sets speed to 20 for first time for sim car
        if not self.sim_speed_set:
            self.sim_speed = 20
            self.sim_speed_set = True

        self.rotated_sim_car = self.__rotate_center(self.sim_car_image, self.sim_angle)

        # update x position based on sim_speed output
        self.sim_position[0] += self.sim_speed * math.cos(math.radians(360 - self.sim_angle))
        self.sim_position[0] = max(self.sim_position[0], 20)
        self.sim_position[0] = min(self.sim_position[0], SCREEN_WIDTH - 120)

        # same for move into y position
        self.sim_position[1] += self.sim_speed * math.sin(math.radians(360 - self.sim_angle)) 
        self.sim_position[1] = max(self.sim_position[1], 20)
        self.sim_position[1] = min(self.sim_position[1], SCREEN_WIDTH - 120)

        # calculate new center
        self.sim_center = [int(self.sim_position[0]) + CAR_WIDTH / 2, int(self.sim_position[1]) + CAR_HEIGHT / 2 ]

        # increase distance travelled for reward
        self.sim_distance += self.sim_speed

        # for leaderboard
        startX = finish_line_coords[circuit][0]
        startY = finish_line_coords[circuit][1]
        dist_to_start = int(math.sqrt((startX - self.sim_center[0])** 2 + (startY - self.sim_center[1])** 2))
        if dist_to_start < CHECKPOINT_RADIUS:
            self.sim_lap_count += 1

        # calculate corners
        self.corners = self.__update_corners()

        # check collisions with track limits and clear radars next update
        self.__check_track_limits(game_map)
        self.radars.clear()

        # from -90 to 120 with 45o steps , check radar
        for d in range(-90, 120, 45):
            self.__check_radar(d, game_map)

    def __calculate_corner(self, angle_offset, half_length):
        # create corners to be added to self.corners
        cornerX = self.sim_center[0] + math.cos(math.radians(360-(self.sim_angle + angle_offset))) * half_length
        cornerY = self.sim_center[1] + math.sin(math.radians(360-(self.sim_angle + angle_offset))) * half_length
        return [cornerX, cornerY]

    def __update_corners(self):
        half_length = 0.5 * CAR_WIDTH # (half car length)
        angle_offsets = [30, 150, 210, 330] # can change in future
        self.corners = [self.__calculate_corner(offset,half_length) for offset in angle_offsets]
        return self.corners

    def get_data(self):
        # get distances to border, create return values for NEAT function
        radars = self.radars
        return_values = [0,0,0,0,0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] /30)
        
        return return_values
    
    def is_alive(self):
        # checks if alive
        return self.alive
    
    def get_reward(self):
        # ai!
        # calculate reward, return self.distance /50
        return self.sim_distance / (CAR_WIDTH /2)
    
    def __rotate_center(self, image, sim_angle):
        # rotate rectangle image of the sim car
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image,sim_angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image
