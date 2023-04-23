import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate


# тестова функція
def test_function(x):
    return x ** 3 - 1


# головна функція
def main_function(x):
    return np.exp(- x ** 2)


# функція для роботи з режимами
def exct_value(x, mode='test'):
    if mode == 'test':
        return test_function(x)
    elif mode == 'main':
        return main_function(x)
    else:
        raise ValueError("Помилка")


# функція для знаходження макс значення на заданому інтервалі
def find_max_func_value(func, start, end, mode):
    return max(func(np.array([start, end]), mode=mode))


# функція для генерації випадкових точок
def generate_random_point(start, end, func, mode):
    return random.uniform(start, end), \
        random.uniform(0, find_max_func_value(func, start, end, mode))


# метод монте-карло
def monte_carlo(func, start, end, points_amount=10000, mode='main'):
    points_in = []
    all_points = []
    for i in range(points_amount):
        x, y = generate_random_point(start, end, func, mode)
        if y <= func(x, mode):
            points_in.append((x, y))
        all_points.append((x, y))
    total_area = (end - start) * find_max_func_value(func, start, end, mode)
    integral = total_area * (len(points_in) / points_amount)
    return integral, all_points


# функція для обчислення інтегралів
def calculate_integral(fuck, start, end, mode):
    return integrate.quad(fuck, start, end, args=mode)


# функція для обчислення абсолютної та відносної похибки
def calculate_error(real_value, approx_value):
    print(f"Значення інтегралу обчислене за допомогою методу Монте-Карло: {round(approx_value, 6)}")
    print(f"Істенне значення інтегралу: {round(real_value, 6)}")
    error_abs = abs(real_value - approx_value)
    print(f"Абсолютна похибка: {round(error_abs, 6)}")
    if real_value != 0:
        error_real = (error_abs * 100) / abs(real_value)
        print(f"Відносна похибка: {round(error_real, 6)}%")
    else:
        print(f"Обчислення відносної похибки неможливо")


# функція для виводу графіків
def plot_function(fuck, mode, points, range_start, range_end):
    fig1, ax1 = plt.subplots(1, 1, figsize=(10, 10))
    ax1.set_title("Графік функції y = x^3 - 1" if mode == 'test' else "Графік функції e^(-x^2)",
                  fontsize=16)
    plt.grid(True)
    x_1 = np.linspace(range_start, range_end, num=1000)
    plt.plot(x_1, fuck(x_1, mode), linewidth=4)
    for point in points[:5000]:
        plt.plot(point[0], point[1], 'ro-' if (point[1] > fuck(point[0], mode)) else 'go-', alpha=0.3)
    plt.show()


def main():
    stat = 1
    end = 2
    num_samples = 10000

    print("Для тестової функції y = x^3 - 1")
    integral, all_points = monte_carlo(exct_value, stat, end, points_amount=num_samples, mode='test')
    plot_function(exct_value, 'test', all_points, stat, end)
    calculate_error(calculate_integral(exct_value, stat, end, 'test')[0], integral)

    print("\nДля основної функції y = e^(x^2)")
    integral, all_points = monte_carlo(exct_value, stat, end, points_amount=num_samples, mode='main')
    plot_function(exct_value, 'main', all_points, stat, end)
    calculate_error(calculate_integral(exct_value, stat, end, 'main')[0], integral)


if __name__ == "__main__":
    main()
