import random
from config import laps_to_win, player_names

leaderboard_positions = {}

# leaderboard functions
def add_player(player_name, lap_count):
    leaderboard_positions[player_name] = lap_count

def update_player(player_name, new_lap_count):
    if player_name in leaderboard_positions:
        leaderboard_positions[player_name] = new_lap_count

def update_leaderboard(cars, circuit, lap_count, user_nickname):  
    for car in cars:
        #print(car.sim_lap_count)
        if car.sim_lap_count > 1:   # leaderboard for sim cars generated after first run through the entire circuit
            #if car.sim_lap_count < 3:
            if leaderboard_positions and max(leaderboard_positions.values()) < (laps_to_win[circuit]+1):
                sim_player_name = random.choice(player_names)

                if sim_player_name not in leaderboard_positions:
                    fake_lap_count = random.randint(1,2)
                    add_player(sim_player_name, fake_lap_count)

                if car.sim_lap_count > 7 and car.sim_lap_count < 11:
                    fake_lap_count_add_1 = random.randint(1,2)
                    total_fake_lap = fake_lap_count_add_1 + leaderboard_positions[sim_player_name]
                    if (total_fake_lap) <= (laps_to_win[circuit]+1):
                        update_player(sim_player_name, total_fake_lap)
    # user
    update_player(user_nickname,lap_count)


def get_sorted_leaderboard():
    return sorted(leaderboard_positions.items(), key=lambda x: x[1], reverse=True)

def clear_leaderboard():
    leaderboard_positions.clear()
