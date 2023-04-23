import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

# Генерація тестової послідовності
N = np.random.randint(1000, 2001)
X = np.random.rand(N, 2)
print(f"Кількість N = ", N)


# Обчислення міри відстані
def distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


# Реалізація методу К-середніх
def k_means(X, K, max_iters=100):
    centroids = X[np.random.choice(N, K, replace=False)]
    for i in range(max_iters):
        clusters = [[] for _ in range(K)]
        for x in X:
            distances = [distance(x, c) for c in centroids]
            cluster_idx = np.argmin(distances)
            clusters[cluster_idx].append(x)
        prev_centroids = centroids
        centroids = [np.mean(cluster, axis=0) for cluster in clusters if len(cluster) > 0]
        if len(centroids) < K:
            break
        if np.allclose(prev_centroids, centroids):
            break
    return clusters


# Реалізація іншого методу кластеризації
def other_clustering(X, K1):
    clustering = AgglomerativeClustering(n_clusters=K1)
    clustering.fit(X)
    labels = clustering.labels_
    clusters = [[] for _ in range(K1)]
    for i, x in enumerate(X):
        clusters[labels[i]].append(x)
    return clusters


# Виконання кластеризації методом К-середніх
# Генерація кількості кластерів
K = random.randint(2, 10)
K1 = random.randint(2, 10)

kmeans_clusters = k_means(X, K)

# Виконання кластеризації іншим методом
other_clusters = other_clustering(X, K1)

# Порівняння результатів кластеризації
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].set_title('Метод К-середніх')
axs[1].set_title('Інший метод кластеризації (ієрархічний)')

for i in range(K):
    cluster = np.array(kmeans_clusters[i])
    axs[0].scatter(cluster[:, 0], cluster[:, 1], label=f'Кластер {i + 1}')
for i, cluster in enumerate(other_clusters):
    cluster = np.array(cluster)
    axs[1].scatter(cluster[:, 0], cluster[:, 1], label=f'Кластер {i + 1}')
axs[0].legend()
axs[1].legend()

plt.show()

# Оцінка кількості кластерів та якості кластеризації
print(f'Кількість кластерів (метод К-середніх): {len(kmeans_clusters)}')
kmeans_inertia = sum(np.sum((np.array(kmeans_clusters[i]) - np.mean(np.array(kmeans_clusters[i]), axis=0)) ** 2)
                     for i in range(len(kmeans_clusters)))
print(f'Функціонал якості (метод К-середніх): {kmeans_inertia}')

other_clusters = other_clustering(X, K1)
print(f'Кількість кластерів (ієрархічний метод): {len(other_clusters)}')
other_inertia = sum(np.sum((np.array(other_clusters[i]) - np.mean(np.array(other_clusters[i]), axis=0)) ** 2)
                    for i in range(len(other_clusters)))
print(f'Функціонал якості (ієрархічний метод): {other_inertia}')
