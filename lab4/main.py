import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class AntColonyOptimizer:
    def __init__(self, distances, num_ants, num_iterations, alpha=1.0, beta=2.0, evaporation_rate=0.5, Q=100):
        self.distances = distances
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q
        self.pheromone = np.ones_like(distances) / len(distances)
        self.best_tour = None
        self.best_distance = float('inf')

    def is_edge_in_tour(self, node1, node2, tour):
        return ((node1 in tour) and (node2 in tour)) and (
                np.abs(np.argwhere(np.array(tour) == node1) - np.argwhere(np.array(tour) == node2)) == 1)

    def calculate_probabilities(self, current_node, unvisited_nodes):
        pheromone = self.pheromone[current_node, unvisited_nodes]
        distances = self.distances[current_node, unvisited_nodes]
        probabilities = (pheromone ** self.alpha) * ((1.0 / distances) ** self.beta)
        probabilities = probabilities / np.sum(probabilities)
        return probabilities

    def run(self):
        for i in range(self.num_iterations):
            ants = [Ant(random.randint(0, len(self.distances) - 1), self) for j in range(self.num_ants)]
            for ant in ants:
                ant.run()
                if ant.distance < self.best_distance:
                    self.best_distance = ant.distance
                    self.best_tour = ant.tour
            self.pheromone *= self.evaporation_rate
            for ant in ants:
                ant.update_pheromone(self.evaporation_rate, self.Q)

    def get_best_tour(self):
        return self.best_tour, self.best_distance


class Ant:
    def __init__(self, start_node, optimizer):
        self.optimizer = optimizer
        self.tour = [start_node]
        self.unvisited_nodes = list(range(len(optimizer.distances)))
        self.unvisited_nodes.remove(start_node)
        self.distance = 0.0

    def run(self):
        while self.unvisited_nodes:
            probabilities = self.optimizer.calculate_probabilities(self.tour[-1], self.unvisited_nodes)
            next_node = np.random.choice(self.unvisited_nodes, p=probabilities)
            self.tour.append(next_node)
            self.unvisited_nodes.remove(next_node)
            self.distance += self.optimizer.distances[self.tour[-2], self.tour[-1]]
        self.distance += self.optimizer.distances[self.tour[-1], self.tour[0]]

    def update_pheromone(self, evaporation_rate, Q):
        for i in range(1, len(self.tour)):
            node1, node2 = self.tour[i - 1], self.tour[i]
            self.optimizer.pheromone[node1, node2] += (Q / self.distance)
            self.optimizer.pheromone[node2, node1] += (Q / self.distance)


# generate distances matrix
N = random.randint(25, 35)
distances = np.zeros((N, N))
for i in range(N):
    for j in range(i + 1, N):
        distances[i][j] = distances[j][i] = random.randint(10, 100)


# запис даних щодо згенерованої карти у файл
with open('map.txt', 'w') as f:
    f.write(f'{N}\n')
    for row in distances:
        f.write(' '.join(map(str, row)) + '\n')
# print(distances)

min_distance = np.min(distances)
max_distance = np.max(distances)

print("Minimum distance:", min_distance)
print("Maximum distance:", max_distance)

avg_distance = np.mean(distances)

print("Average distance:", avg_distance)
min_indices = np.unravel_index(np.argmin(distances), distances.shape)
print("Index of closest nodes:", min_indices)

max_indices = np.unravel_index(np.argmax(distances), distances.shape)
print("Index of farthest nodes:", max_indices)

sns.heatmap(distances, cmap="YlGnBu", annot=True, fmt=".0f")
plt.title("Distances Matrix")
plt.show()

aco = AntColonyOptimizer(distances, num_ants=10, num_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, Q=100)
aco.run()

best_tour, best_distance = aco.get_best_tour()

print("Best tour:", best_tour)
print("Best distance:", best_distance)