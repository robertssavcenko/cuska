from tkinter import *
import random


GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 100

SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#800080"  #violets
FOOD_COLOR = "#FF0000"   #sarkans
BAD_FOOD_COLOR = "#FFFF00" #dzeltens
BACKGROUND_COLOR = "#000000" #melns

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, color):
        self.color = color
        self.coordinates = self._generate_coordinates()
        self.create_food()

    def _generate_coordinates(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        return [x, y]

    def create_food(self):
        x, y = self.coordinates
        if self.color == FOOD_COLOR:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="food")
        elif self.color == BAD_FOOD_COLOR:
            canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="bad_food")

def next_turn(snake, food, bad_food):
    global score


    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    
    if x < 0:
        x = GAME_WIDTH - SPACE_SIZE
    elif x >= GAME_WIDTH:
        x = 0
    if y < 0:
        y = GAME_HEIGHT - SPACE_SIZE
    elif y >= GAME_HEIGHT:
        y = 0

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)


    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food(FOOD_COLOR)
    elif x == bad_food.coordinates[0] and y == bad_food.coordinates[1]:
        score -= 1
        label.config(text="Score:{}".format(score))
        canvas.delete("bad_food")
        bad_food = Food(BAD_FOOD_COLOR)

        
        if len(snake.coordinates) > 1:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food, bad_food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.bind("<Button-1>", restart_game)

def restart_game(event):
    global score, direction, snake, food, bad_food

    score = 0
    direction = 'down'

    canvas.delete(ALL)
    canvas.unbind("<Button-1>")

    label.config(text="Score:{}".format(score))

    snake = Snake()
    food = Food(FOOD_COLOR)
    bad_food = Food(BAD_FOOD_COLOR)

    next_turn(snake, food, bad_food)

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food(FOOD_COLOR)
bad_food = Food(BAD_FOOD_COLOR)

next_turn(snake, food, bad_food)

window.mainloop()
