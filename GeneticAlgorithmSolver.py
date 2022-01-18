import random
from RouteManager import RouteManager
from Route import Route


class GeneticAlgorithmSolver:
    def __init__(self, cities, population_size=50, mutation_rate=0.2, tournament_size=10, elitism=False):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def evolve(self, routes):

        elitism = 0
        tournament_parent1 = self.tournament(routes)
        tournament_parent2 = self.tournament(routes)

        tournament_child = self.crossover(tournament_parent1, tournament_parent2)
        for i in range(elitism, len(routes)):
            routes.set_route(i, tournament_child)

        for route in routes.routes:
            for i in range(int(len(routes)*self.mutation_rate)):
                self.mutate(route)

        routes.find_best_route()

        return routes

    def crossover(self, route_1, route_2):
        child = Route(self.cities)

        for i in range(0, len(child.route)):
            child.route[i] = None

        start = random.randint(0, len(route_1.route))
        end = random.randint(0, len(route_1.route))

        if start < end:
            for i in range(start, end):
                child.route[i] = route_1.route[i]

        elif start > end:
            for i in range(end , start):
                child.route[i] = route_1.route[i]

        for i in range(len(route_2.route)):
            if not route_2.route[i] in child.route:
                for j in range(len(child.route)):
                    if child.route[j] is None:
                        child.route[j] = route_2.route[i]
                        break

        child.calc_route_distance()
        return child

    def mutate(self, route):

        mutation_pos1 = random.randint(0, len(route.route) - 1)
        mutation_pos2 = random.randint(0, len(route.route) - 1)

        if mutation_pos1 == mutation_pos2:
            return route

        city1 = route.route[mutation_pos1]
        city2 = route.route[mutation_pos2]

        route.route[mutation_pos2] = city1
        route.route[mutation_pos1] = city2

        route.calc_route_distance()

        return route

    def tournament(self, routes):

        tour = RouteManager(self.cities, self.tournament_size)


        for i in range(0,self.tournament_size - 1):
            id= int(random.random()*self.population_size)
            tour.set_route(i,routes.get_route(id))



        return tour.find_best_route()
