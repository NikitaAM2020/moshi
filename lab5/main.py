import random

# Параметри задачі
NUM_LESSONS = 25
NUM_TEACHERS = 4
NUM_CLASSES = 3
MAX_LESSONS_PER_DAY = 5
NUM_SPECIAL_ROOMS = 1

# Задання назв предметів, вчителів та класів
subjects = {
    (1, 1): "Математика",
    (2, 1): "Українська мова",
    (3, 1): "Англійська мова",
    (4, 1): "Музичне мистецтво",
    (1, 2): "Інформатика",
    (2, 2): "Я досліджую світ",
    (3, 2): "Образотворче мистецтво",
    (4, 2): "Фізкультура",
    (1, 3): "Математика",
    (2, 3): "Українська мова",
    (3, 3): "Фізкультура",
    (4, 3): "Інформатика",
}

teachers = {
    (1, 1): "Василенко",
    (2, 1): "Шевченко",
    (3, 1): "Мельникук",
    (4, 1): "Омельчук",
    (1, 2): "Інші вчителі",
    (2, 2): "Інші вчителі",
    (3, 2): "Інші вчителі",
    (4, 2): "Інші вчителі",
    (1, 3): "Інші вчителі",
    (2, 3): "Інші вчителі",
    (3, 3): "Інші вчителі",
    (4, 3): "Інші вчителі"
}

classes = {
    1: "1A",
    2: "2A",
    3: "3A",
    4: "Інші класи",
    5: "Інші класи",
    6: "Інші класи"
}

# Задання назв днів тижня
days_of_week = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]


# Генерація початкової популяції
def generate_schedule():
    schedule = []
    for _ in range(NUM_LESSONS):
        teacher = random.randint(1, NUM_TEACHERS)
        time_slot = random.randint(1, MAX_LESSONS_PER_DAY)
        schedule.append((teacher, time_slot))
    return schedule


# Функція придатності
def fitness(schedule):
    # Розрахунок функції придатності (наприклад, кількість "вікон")
    fitness_score = 0
    # Додаткові перевірки можуть бути виконані для оцінки якості розкладу
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
    # Реалізація оператора мутації (напририкладу)
    mutated_schedule = schedule[:]
    gene_index = random.randint(0, NUM_LESSONS - 1)
    gene = random.randint(0, NUM_LESSONS - 1)
    mutated_schedule[gene] = (random.randint(1, NUM_TEACHERS), random.randint(1, MAX_LESSONS_PER_DAY))
    return mutated_schedule


def selection(population):
    # Реалізація функції вибору найкращих особин (наприклад, турнірний відбір)
    selected = random.sample(population, 2)
    fitness_scores = [fitness(individual) for individual in selected]
    best_individual = selected[fitness_scores.index(max(fitness_scores))]
    return best_individual


def genetic_algorithm():
    # Генерація початкової популяції
    population = {class_name: [generate_schedule() for _ in range(NUM_LESSONS)] for class_name in classes.values()}

    # Цикл оптимізації
    for _ in range(100):
        # Створення нового покоління
        new_population = {class_name: [] for class_name in classes.values()}
        for class_name in classes.values():
            # Вибір найкращих особин
            parent1 = selection(population[class_name])
            parent2 = selection(population[class_name])

            # Схрещування
            child1, child2 = crossover(parent1, parent2)

            # Мутація
            mutated_child1 = mutate(child1)
            mutated_child2 = mutate(child2)

            # Додавання дитини в нову популяцію
            new_population[class_name].append(mutated_child1)
            new_population[class_name].append(mutated_child2)

        # Заміна попередньої популяції новою
        population = new_population

    # Об'єднання розкладів для кожного класу
    best_schedule = []
    for class_name in classes.values():
        best_schedule.extend(population[class_name])

    return best_schedule


best_schedule = genetic_algorithm()

# Створення словника для зберігання уроків за класами
class_schedule = {class_name: [] for class_name in classes.values()}

# Додавання уроків до відповідних класів
for lesson in best_schedule:
    teacher = teachers[lesson[0]]
    time_slot = lesson[1]
    day_of_week = random.choice(days_of_week)  # Випадковий день тижня
    lesson_class = classes[lesson[1]]

    subject = subjects[(lesson[0], lesson[2])]
    class_schedule[lesson_class].append((subject, teacher, day_of_week, time_slot))

# Виведення розкладу за класами
for class_name, lessons in class_schedule.items():
    print(f"Клас: {class_name}")
    for lesson in lessons:
        subject = lesson[0]
        teacher = lesson[1]
        day_of_week = lesson[2]
        time_slot = lesson[3]
        print(f"Предмет: {subject}, Вчитель: {teacher}, День тижня: {day_of_week}, Час: {time_slot}")
    print()
