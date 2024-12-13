import turtle
import math
from tkinter import Button, Tk



class Robot:
    def __init__(self, name, base, color):
        self.name = name
        self.base = base
        self.color = color
        self.turtle = turtle.Turtle()
        self.turtle.shape("turtle")
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.goto(base.x, base.y)
        self.task_radius = None
        self.is_busy = False
        self.target_x = None
        self.target_y = None
        self.drawing_angle = 0
        self.returning = False

    def take_task(self):
        """Робот берет новое задание, если оно есть."""
        if not self.is_busy and not self.returning and self.base.tasks:
            self.task_radius = self.base.tasks.pop(0)
            # Устанавливаем начальную точку круга
            self.target_x = self.base.x + self.task_radius
            self.target_y = self.base.y
            self.is_busy = True
            self.drawing_angle = 0  # Сброс угла рисования
            #print(f"{self.name} взял задание: круг радиуса {self.task_radius}")

    def move_to_target(self):
        """Движение к целевой точке."""
        if self.target_x is not None and self.target_y is not None:
            dx = self.target_x - self.turtle.xcor()
            dy = self.target_y - self.turtle.ycor()
            distance = (dx**2 + dy**2)**0.5
            if distance > 2:
                step = 2
                self.turtle.setheading(self.turtle.towards(self.target_x, self.target_y))
                self.turtle.forward(min(step, distance))
            else:
                self.turtle.goto(self.target_x, self.target_y)
                #print(f"{self.name} достиг точки начала рисования.")
                self.target_x = None
                self.target_y = None

    def draw_circle_step(self):
        """Рисует круг пошагово."""
        if self.drawing_angle < 360:
            angle_rad = math.radians(self.drawing_angle)
            x = self.base.x + self.task_radius * math.cos(angle_rad)
            y = self.base.y + self.task_radius * math.sin(angle_rad)
            self.turtle.goto(x, y)
            self.turtle.pendown()
            self.drawing_angle += 5
        else:
            #print(f"{self.name} завершил рисование круга радиуса {self.task_radius}.")
            self.task_radius = None
            self.drawing_angle = 0
            self.turtle.penup()
            self.target_x = self.base.x
            self.target_y = self.base.y
            self.returning = True

    def update(self):
        """Обновление состояния робота."""
        if self.returning:
            self.move_to_target()
            if self.target_x is None and self.target_y is None:
                print(f"{self.name} вернулся на базу.")
                self.returning = False
                self.is_busy = False
        elif not self.is_busy and not self.returning:
            self.take_task()
        elif self.task_radius is not None and self.target_x is not None:
            self.move_to_target()
        elif self.task_radius is not None:
            self.draw_circle_step()

    def explode(self):
        """Удаляет черепашку с экрана."""
        print(f"{self.name} взорвалась!")
        self.turtle.hideturtle()

class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.color("red")
        self.turtle.shapesize(2)
        self.tasks = []

    def add_task(self, radius):
        """Добавляет задание на рисование круга."""
        self.tasks.append(radius)
       # print(f"Добавлено задание: круг радиуса {radius}")

def rgb_to_hex(rgb):
    """Преобразует RGB кортеж в строку HEX."""
    return f"#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}"

def main(robot_send_number, robot_send_color):
    # Инициализация экрана
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.tracer(0)

    base = Base(0, 0)

    # Ввод количества кругов от пользователя
    num_circles = int(screen.textinput("Количество кругов", "Введите количество кругов:"))
    radius_step = 10
    print("Robots=",robot_send_number, robot_send_color)
    # Добавляем задания
    for i in range(num_circles):
        base.add_task((i + 1) * radius_step)

    # Создаем роботов
    robots = [
        Robot(f"Robot {i + 1}", base, robot_send_color[i])
        for i in range(robot_send_number)
    ]

    # Создание кнопок для взрыва роботов
    def create_buttons():
        root = Tk()
        root.title("Управление роботами")

        for i, robot in enumerate(robots):
            Button(
                root,
                text=f"Взорвать {robot.name}",
                command=lambda r=robot: (r.explode(), robots.remove(r)),
                fg=rgb_to_hex(robot.color)
            ).pack()

        root.mainloop()

    # Обновление движения и рисования
    def update():
        for robot in robots:
            robot.update()
        screen.update()
        screen.ontimer(update, 50)

    # Запускаем параллельно кнопки и обновление
    import threading
    threading.Thread(target=create_buttons).start()
    update()

    screen.mainloop()

if __name__ == "__main__":
    robot_send_number = 0
    robot_send_color = []
    main(robot_send_number, robot_send_color)

