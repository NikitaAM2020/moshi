import random

# Константи та параметри
DAYS_OF_WEEK = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]
NUM_LESSONS = 25  # Кількість уроків на тиждень
MAX_LESSONS_PER_DAY = 5  # Максимальна кількість уроків у день

# Предмети
subjects = ['Математика', 'Українська мова', 'Англійська мова', 'Фізкультура', 'Музика', 'Малювання',
            'Трудове навчання', 'Природознавство', 'Географія', 'Історія', 'Математика', 'Українська мова',
            'Англійська мова', 'Фізкультура', 'Музика', 'Малювання',
            'Трудове навчання', 'Природознавство', 'Географія', 'Історія', 'Математика', 'Українська мова',
            'Англійська мова', 'Фізкультура', 'Музика']


# Функція генерації початкової популяції
def generate_schedule():
    schedule = []
    for _ in range(NUM_LESSONS):
        day_of_week = random.choice(DAYS_OF_WEEK)
        schedule.append(day_of_week)
    return schedule


# Функція обчислення функції придатності
def fitness(schedule):
    # Розрахунок функції придатності (наприклад, кількість уроків у день та "вікон")
    fitness_score = 0
    for day in DAYS_OF_WEEK:
        lessons = schedule.count(day)
        if lessons > MAX_LESSONS_PER_DAY:
            fitness_score -= (lessons - MAX_LESSONS_PER_DAY)
        if lessons < MAX_LESSONS_PER_DAY:
            fitness_score -= (MAX_LESSONS_PER_DAY - lessons)
    return fitness_score


# Оператор схрещування
def crossover(parent1, parent2):
    # Реалізація оператора схрещування (наприклад, одноточкове схрещування)
    crossover_point = random.randint(1, NUM_LESSONS - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# Оператор мутації
def mutate(schedule):
    # Реалізація оператора мутації (наприкладу, заміна дня)
    mutated_schedule = schedule[:]
    gene_index = random.randint(0, NUM_LESSONS - 1)
    mutated_schedule[gene_index] = random.choice(DAYS_OF_WEEK)
    return mutated_schedule


def selection(population):
    # Реалізація оператора відбору (наприклад, турнірний відбір)
    tournament_size = 2
    selected_population = []
    while len(selected_population) < len(population):
        tournament = random.sample(population, tournament_size)
        best_schedule = max(tournament, key=fitness)
        selected_population.append(best_schedule)
    return selected_population


def genetic_algorithm():
    # Генерація початкової популяції
    population_size = 10
    population = [generate_schedule() for _ in range(population_size)]

    # Еволюція популяції
    num_generations = 50
    for generation in range(num_generations):
        # print(f"Покоління {generation + 1}")

        # Вибір найкращих особин
        selected_population = selection(population)

        # Схрещування
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)

        # Мутація
        mutated_offspring = [mutate(schedule) for schedule in offspring]

        # Оновлення популяції
        population = mutated_offspring

    # Виведення результатів
    for i, schedule in enumerate(population, 1):
        print(f"Розклад для класу {i}:")
        for day in DAYS_OF_WEEK:
            lessons = [subjects[index] for index, lesson in enumerate(schedule) if lesson == day]
            print(f"{day}: {', '.join(lessons)}")
        print()


# Запуск генетичного алгоритму
genetic_algorithm()
