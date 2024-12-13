import turtle
import random
import math
import tkinter as tk
import time
import draw_circles  # Импортировать модуль



# Глобальная переменная для скорости
speed_factor = 1
robot_send_number = 0
robot_send_color = []
robots = []
def close_buttons_and_window(root):
    """Закрывает все кнопки и окно."""
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()  # Удаляем кнопки из интерфейса
    root.destroy()  # Полностью закрывает окно

# Класс для роботов
class Robot:
    def __init__(self, name, x, y, detection_radius, base, robot_number):
        self.name = name
        self.start_x = x  # Начальная позиция робота
        self.start_y = y
        self.x = x  # Текущая позиция робота
        self.y = y
        self.detection_radius = detection_radius
        self.detected_robots = [self]  # Список обнаруженных роботов (начиная с себя)
        self.turtle = turtle.Turtle()
        self.turtle.shape("turtle")
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.color = self.random_color()
        self.turtle.color(self.color)
        self.radius = 10  # Начальный радиус окружности
        self.angle = random.randint(0, 360)  # Случайный начальный угол
        self.base_detected = False  # Флаг, указывает, обнаружена ли база
        self.base = base
        self.robot_number = robot_number  # Номер робота

        # Отображение номера робота рядом с черепашкой

    def show_number(self):
        """Отображает номер робота рядом с ним."""
        self.number_turtle = turtle.Turtle()  # Отдельная черепашка для текста
        self.number_turtle.hideturtle()
        self.number_turtle.penup()
        self.number_turtle.goto(self.x, self.y + 20)  # Позиция текста чуть выше робота
        self.number_turtle.write(
            f"{self.robot_number}", align="center", font=("Arial", 12, "normal")
        )

    def hide_number(self):
        """Скрывает номер робота."""
        if hasattr(self, 'number_turtle'):
            self.number_turtle.clear()


    def random_color(self):
        r = random.random()
        g = random.random()
        b = random.random()
        return r, g, b

    def update_position(self):
        """Обновить координаты робота по текущей позиции черепашки."""
        self.x, self.y = self.turtle.position()

    def detect_robots_and_base(self, robots):
        """Проверить и обновить список обнаруженных роботов и проверить базу."""
        # Проверка на базу
        if not self.base_detected:
            distance_to_base = math.sqrt((self.x - self.base.x) ** 2 + (self.y - self.base.y) ** 2)
            if distance_to_base <= self.detection_radius:
                self.base_detected = True
                print(f"{self.name} обнаружил базу!")

        # Проверка других роботов
        if not self.base_detected:  # Если база ещё не найдена, ищем других роботов
            for robot in robots:
                if robot not in self.detected_robots:  # Проверяем только не обнаруженных
                    distance = math.sqrt((self.x - robot.x) ** 2 + (self.y - robot.y) ** 2)
                    if distance <= self.detection_radius:
                        self.detected_robots.extend(robot.detected_robots)  # Объединяем группы
                        for r in self.detected_robots:
                            r.detected_robots = self.detected_robots  # Синхронизируем списки

    def move_in_circle(self):
        """Движение по увеличивающейся окружности относительно начальной точки."""
        self.angle += 20 * speed_factor  # Увеличиваем шаг угла в зависимости от скорости
        if self.angle >= 360:
            self.angle -= 360
            self.radius += 10  # Увеличить радиус после полного круга

        # Вычислить новую позицию относительно начальной точки
        new_x = self.start_x + self.radius * math.cos(math.radians(self.angle))
        new_y = self.start_y + self.radius * math.sin(math.radians(self.angle))
        self.turtle.goto(new_x, new_y)
        self.update_position()

    def move_to_base(self):
        """Движение к базе."""
        self.turtle.goto(self.base.x, self.base.y)
        self.update_position()

    def move_with_group(self):
        """Двигаться вместе с обнаруженной группой или к базе."""
        if self.base_detected:  # Если база найдена, двигаться к ней
            self.move_to_base()
        elif len(self.detected_robots) > 1:  # Если робот в группе, двигаться синхронно
            leader = self.detected_robots[0]  # Первый робот в группе - лидер
            self.start_x, self.start_y = leader.start_x, leader.start_y
            self.radius = leader.radius
            self.angle = leader.angle
            self.move_in_circle()
        else:  # Если один, продолжать двигаться по окружности
            self.move_in_circle()

    def print_info(self):
        """Выводит информацию о роботе в консоль."""
        print(f"Информация о роботе {self.name}:")
        print(f"Позиция: ({self.x}, {self.y})")
        print(f"Обнаружена база: {self.base_detected}")
        print(f"Обнаруженные роботы: {[robot.name for robot in self.detected_robots]}")
        print("-" * 20)


# Класс базы
class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.color("red")
        self.turtle.shapesize(2)  # Увеличиваем размер базы


# Функция для паузы и возобновления
running = True

def show_and_hide_numbers(robots):
    for robot in robots:
        robot.show_number()  # Показываем номер
    time.sleep(2)  # Задержка 2 секунды
    for robot in robots:
        robot.hide_number()  # Скрываем номер

def move_all_to_base(robots):
    for robot in robots:
        robot.move_to_base()
    print("Все роботы перемещены на базу!")

def toggle_running(pause_button, resume_button):
    global running
    running = not running
    if running:
        resume_button.config(state=tk.DISABLED)
        pause_button.config(state=tk.NORMAL)
    else:
        resume_button.config(state=tk.NORMAL)
        pause_button.config(state=tk.DISABLED)

# Функция для ускорения
def speed_up():
    global speed_factor
    speed_factor *= 1.2  # Увеличиваем скорость на 20%

# Функция для замедления
def slow_down():
    global speed_factor
    speed_factor *= 0.8  # Уменьшаем скорость на 20%




def launch_scan_by_circles():
    print("Запуск программы...")
    draw_circles.main(num_robots, robot_send_color)

def launch_scan_by_blocks():
    print("Запуск сканирования по блокам.")
    # Вставьте сюда код для сканирования по блокам.

def launch_synchronous_scan():
    print("Запуск синхронного сканирования.")
    # Вставьте сюда код для синхронного сканирования.

def launch_fourth_option():
    print("Запуск четвёртого варианта.")
    # Вставьте сюда код для четвёртого варианта.

def show_dialog_window():
    # Создаём главное окно
    dialog = tk.Tk()
    dialog.title("Выбор режима сканирования")

    # Добавляем текст-инструкцию
    instruction = tk.Label(dialog, text="Выберите режим сканирования:", font=("Arial", 14))
    instruction.pack(pady=10)

    # Кнопка для первого варианта
    option1_button = tk.Button(dialog, text="Сканирование по окружностям", command=lambda: [launch_scan_by_circles(), dialog.destroy()])
    option1_button.pack(pady=5)

    # Кнопка для второго варианта
    option2_button = tk.Button(dialog, text="Сканирование по блокам", command=lambda: [launch_scan_by_blocks(), dialog.destroy()])
    option2_button.pack(pady=5)

    # Кнопка для третьего варианта
    option3_button = tk.Button(dialog, text="Синхронное сканирование", command=lambda: [launch_synchronous_scan(), dialog.destroy()])
    option3_button.pack(pady=5)

    # Кнопка для четвёртого варианта
    option4_button = tk.Button(dialog, text="Четвёртый вариант (в разработке)", command=lambda: [launch_fourth_option(), dialog.destroy()])
    option4_button.pack(pady=5)

    # Запускаем цикл окна
    dialog.mainloop()

# Основной цикл
def main():
    global running, speed_factor,num_robots

    # Настройки
    num_robots = int(input("Сколько роботов вы хотите создать? "))
    detection_radius = 100  # Радиус обнаружения роботов и базы
    # Настроить экран
    screen = turtle.Screen()
    screen.colormode(1.0)
    screen.title("Роботы объединяются")
    screen.setup(width=800, height=800)

    # Создать базу
    base = Base(0, 0)

    # Создать роботов с случайными координатами

    for i in range(num_robots):
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        robot = Robot(f"Robot-{i+1}", x, y, detection_radius, base, i+1)
        robots.append(robot)
        robot_send_color.append(robot.color)



    # Создание интерфейса для кнопок
    root = tk.Tk()
    root.title("Управление роботом")

    pause_button = tk.Button(root, text="Пауза", command=lambda: toggle_running(pause_button, resume_button))
    pause_button.pack(pady=10)

    resume_button = tk.Button(root, text="Возобновить", command=lambda: toggle_running(pause_button, resume_button), state=tk.DISABLED)
    resume_button.pack(pady=10)

    speed_up_button = tk.Button(root, text="Ускорить", command=speed_up)
    speed_up_button.pack(pady=10)

    slow_down_button = tk.Button(root, text="Замедлить", command=slow_down)
    slow_down_button.pack(pady=10)

    show_numbers_button = tk.Button(root, text="Показать номера роботов", command=lambda: show_and_hide_numbers(robots))
    show_numbers_button.pack(pady=10)

    move_to_base_button = tk.Button(root, text="Переместить всех на базу", command=lambda: move_all_to_base(robots))
    move_to_base_button.pack(pady=10)
    # Кнопки для каждого робота
    for robot in robots:
        robot_button = tk.Button(root, text=f"Информация о {robot.name}", command=lambda r=robot: r.print_info())
        robot_button.pack(pady=5)

    # Основной цикл
    while not all(robot.base_detected for robot in robots):  # Пока не все нашли базу
        if running:
            for robot in robots:
                robot.detect_robots_and_base(robots)  # Проверяет на наличие других роботов и базы
                robot.move_with_group()  # Робот движется либо по своей окружности, либо с группой, либо к базе
        root.update()

    # Когда все роботы достигли базы
    print("Все роботы достигли базы!")
    close_buttons_and_window(root)
    show_dialog_window()


    turtle.done()

if __name__ == "__main__":
    main()
