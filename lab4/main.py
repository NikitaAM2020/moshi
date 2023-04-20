import random
import math

# Генерація випадкових даних для карти маршрутів
n_cities = random.randint(25, 35)
cities = [i for i in range(1, n_cities+1)]
distances = {}
for i in range(1, n_cities+1):
    for j in range(i+1, n_cities+1):
        distances[(i,j)] = distances[(j,i)] = random.randint(10, 100)

# Збереження даних у файл
with open("route_map.txt", "w") as f:
    f.write(f"{n_cities}\n")
    for i, city in enumerate(cities):
        f.write(f"{i+1} 0 0\n")
    for (i,j), distance in distances.items():
        f.write(f"{i} {j} {distance}\n")



# Зчитування даних про карту маршрутів з файлу
with open("route_map.txt", "r") as f:
    n_cities = int(f.readline().strip())
    cities = [tuple(map(int, f.readline().strip().split())) for _ in range(n_cities)]
    distances = {(int(i), int(j)): int(d) for i, j, d in [line.strip().split() for line in f]}


class Ant:
    def __init__(self, start_city):
        self.visited_cities = [start_city]
        self.distance_travelled = 0

    def select_next_city(self, pheromone, alpha, beta):
        current_city = self.visited_cities[-1]
        unvisited_cities = set(cities) - set(self.visited_cities)
        probabilities = []
        for city in unvisited_cities:
            pheromone_level = pheromone.get((current_city, city), 0.1)
            visibility = distances.get((current_city, city), 0.1)
            probability = math.pow(pheromone_level, alpha) * math.pow(1 / visibility, beta)
            probabilities.append((city, probability))
        total_probability = sum(prob for _, prob in probabilities)
        probabilities = [(city, prob / total_probability) for city, prob in probabilities]
        selected_city = random.choices(population=[city for city, _ in probabilities],
                                       weights=[prob for _, prob in probabilities])[0]
        self.visited_cities.append(selected_city)
        self.distance_travelled += distances.get((current_city, selected_city), 0)

    def __str__(self):
        return f"{self.visited_cities}, distance = {self.distance_travelled}"


class AntColony:
    def __init__(self, n_ants, n_iterations, evaporation_rate, alpha, beta):
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.pheromone = {(i, j): 1 for i in cities for j in cities if i != j}

    def update_pheromone(self, ants):
        for i, j in self.pheromone.keys():
            evaporation = (1 - self.evaporation_rate) * self.pheromone[(i, j)]
            self.pheromone[(i, j)] = evaporation
            for ant in ants:
                if (i, j) in ant.path():
                    self.pheromone[(i, j)] += ant.pheromone_delta(i, j, self.alpha)

    def run(self):
        best_ant = None
        for iteration in range(self.n_iterations):
            ants = [Ant(random.choice(cities)) for _ in range(self.n_ants)]
            for ant in ants:
                for _ in range(len(cities) - 1):
                    ant.select_next_city(self.pheromone, self.alpha, self.beta)
                ant.distance_travelled += distances.get((ant.visited_cities[-1], ant.visited_cities[0]), 0)
                if best_ant is None or ant.distance_travelled < best_ant.distance_travelled:
                    best_ant = ant
            self.update_pheromone(ants)
        return best_ant
