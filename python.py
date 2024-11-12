from tkinter import *
import random

GAME_WIDTH=1000
GAME_HEIGHT=700
SPEED=100
SPACE_SIZE=50
BODY_PARTS=3

SNAKE_COLOR="#00FF00"
FOOD_COLOR="#FF0000"
BACKGROUND_COLOR="#000000"

window=Tk()
window.title("Snake Game")

score=0
direction='down'
current_speed=SPEED
foods=[]

label=Label(window,text="Score: {}".format(score),font=('arial',40))
label.pack()

canvas=Canvas(window,bg=BACKGROUND_COLOR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

window.update()

window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

x=int((screen_width/2)-(window_width/2))
y=int((screen_height/2)-(window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Snake
class Snake:
    def __init__(self):
        self.body_size=BODY_PARTS
        self.coordinantes=[]
        self.squares=[]
        for i in range(BODY_PARTS):
            self.coordinantes.append([0,0])
        for x,y in self.coordinantes:
            square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tag="snake")
            self.squares.append(square)

#Food
class Food:
    def __init__(self):
        x=random.randint(0,(GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y=random.randint(0,(GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE
        self.coordinantes=[x,y]
        self.food=canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=FOOD_COLOR,tag="food")

def create_food():
    food=Food()
    foods.append(food)

def next_turn(snake):
    global score, current_speed
    x, y = snake.coordinantes[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinantes.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    #Check if food was eaten
    food_eaten = False
    for food in foods[:]: 
        if x == food.coordinantes[0] and y == food.coordinantes[1]:
            score += 1
            label.config(text="Score: {}".format(score))
            canvas.delete(food.food)
            foods.remove(food)
            food_eaten = True

    #Levels
    if food_eaten:
        #Level 2               Score 5
        if score == 5:
            current_speed = 90
            canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="Level 2: Speed Increased!", font=('arial', 30), fill="yellow", tag="levelup")
            window.after(1000, lambda: canvas.delete("levelup"))
            snake.body_size = 1
            while len(foods) < 2:
                create_food()

        #Level 3              Score 10
        elif score == 10:
            current_speed = 80
            canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="Level 3: Difficult", font=('arial', 30), fill="yellow", tag="levelup")
            window.after(1000, lambda: canvas.delete("levelup"))
            while len(foods) < 3:
                create_food()

        #Level 4              Score 15
        elif score == 15:
            current_speed = 70
            canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="Level 4: Insane", font=('arial', 30), fill="yellow", tag="levelup")
            window.after(1000, lambda: canvas.delete("levelup"))
            while len(foods) < 4:
                create_food()

        #Level 5               Score 20
        elif score == 20:
            current_speed = 60
            canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="Level 5: EXTREME", font=('arial', 30), fill="yellow", tag="levelup")
            window.after(1000, lambda: canvas.delete("levelup"))
            while len(foods) < 5:
                create_food()

        #Level 6              Score 25
        elif score == 25:
            current_speed = 50
            canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="Level 4: DEMON", font=('arial', 30), fill="yellow", tag="levelup")
            window.after(1000, lambda: canvas.delete("levelup"))
            while len(foods) < 6:
                create_food()

        
            for _ in range(3):
                snake.coordinantes.append(snake.coordinantes[-1])
                square = canvas.create_rectangle(snake.coordinantes[-1][0], snake.coordinantes[-1][1], snake.coordinantes[-1][0] + SPACE_SIZE, snake.coordinantes[-1][1] + SPACE_SIZE, fill=SNAKE_COLOR)
                snake.squares.append(square)
        else:
            create_food()
    else:
        del snake.coordinantes[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(current_speed, next_turn, snake)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinantes[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinantes[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('arial', 70), text="GAME OVER", fill="red", tag="gameover")

#Key binds
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
create_food()

next_turn(snake)

window.mainloop()
