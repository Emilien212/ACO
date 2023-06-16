import numpy as np
import matplotlib.pyplot as plt
import time

n = 50
ants = 5
iterations = 100

alpha = 0.5
beta = 5
gamma = 0
phi = 0.9
Q = 10



## INITIALISATION
cities = np.random.uniform(0, 100, size=(n,2))

plt.plot(cities[0, 0], cities[0, 1], '.', markersize=15, color="red")
plt.plot(cities[1:, 0], cities[1:, 1], ".", markersize=15)

distances = np.zeros((n, n))
for i, city1 in enumerate(cities):
    for j, city2 in enumerate(cities):
        distances[i, j] = ((cities[i][0]-cities[j][0])**2 + (cities[i][1]-cities[j][1])**2)**(1/2)

pheromones = np.ones((n, n))/10000

def probability(start, cities, pheromones):
    probability = []
    for city in cities:
        i = (gamma + (pheromones[start, city]**alpha)*((1/distances[start, city])**beta))
        probability.append(i)

    probability /=  np.sum(probability)
    return probability


def choose_city(path, pheromones):
    avaible_cities = np.setdiff1d(np.arange(0, n, 1), path["cities"])
    proba = probability(path["cities"][-1], avaible_cities, pheromones)
    selected = np.random.choice(avaible_cities, 1, p=proba)
    return int(selected)

def update_pheromones(paths, pheromones):
    pheromones *= (1-phi)
    for path in paths:
        l = path["length"]
        for i in range(len(path["cities"])-1):
            pheromones[path["cities"][i], path["cities"][i+1]] = pheromones[path["cities"][i-1], path["cities"][i]] = Q/l
    return pheromones

def best_path(start, pheromones):
    path = [start]
    l = 0
    for i in range(n-1):
        new = np.argmax(pheromones[path[i]])
        l += distances[path[i], new]
        path.append(new)
    print(l)
    return path


s = time.time()

# ALGO
for iteration in range(iterations):
    paths = []
    for ant in range(ants):
        path = {"length" :0, "cities": [0]}
        for _ in range(n-1):
            new_city = choose_city(path, pheromones)
            path["length"] += distances[path["cities"][-1], new_city]
            path["cities"].append(new_city)
        paths.append(path)
    pheromones = update_pheromones(paths, pheromones)

opti = best_path(0, pheromones)
route = np.zeros((n, 2))

for i, city in enumerate(opti):
    route[i] = cities[city]

print(f"Elapsed time : {time.time()-s}")

plt.plot(route[:, 0], route[:, 1])

plt.show()
