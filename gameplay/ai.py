import neat
def create_ai_population(genomes, config, circuit):
    nets = []
    cars = []

    # for _, genome in genomes:
    #     net = neat.nn.FeedForwardNetwork.create(genome, config)
    #     nets.append(net)
    #     genome.fitness = 0
    #     cars.append(SimCar(circuit))

    return nets, cars


# for every simulated car, get information on surroundings, feed into the neural network, get output and then update the car's angle and speed based on the output
def update_ai_actions(cars, nets):
    for i, car in enumerate(cars):
        output = nets[i].activate(car.get_data()) # should return an output list from neural netwrok like [0.2, 0.8, -0.1, 0.3, 0.1, 0.5]
        choice = output.index(max(output)) # get the index of the highest value in the output list, which corresponds to the action to take

        if choice == 0:  # reactove cpntrol, the networks that make better choices survivce longer and get higher fitness
            car.sim_angle += 10
        elif choice == 1:
            car.sim_angle -= 10
        elif choice == 2:
            if car.sim_speed - 2 >= 12:
                car.sim_speed -= 2
        elif choice == 3:
            car.sim_angle += 30
        elif choice == 4:
            car.sim_angle -= 30
        else:
            car.sim_speed += 3

def update_ai_cars(cars, genomes, game_map, circuit):
    still_alive = 0

    for i, car in enumerate(cars):
        if car.is_alive():
            still_alive += 1
            car.update_sim_car(circuit, game_map)
            genomes[i][1].fitness += car.get_reward()

    return still_alive