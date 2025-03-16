import random
import curses

WIDTH, HEIGHT = 60, 20
SNAKE_CHAR = 'O'
food_char = '1'

def main(stdscr):
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(1)   # non - blocking input
    stdscr.timeout(100) # speed control

    #initial snake position
    snake = [(10,30), (10,29), (10,28)] #head and body
    direction = (0,1)
    food_xy = (random.randint(1, HEIGHT-2), random.randint(1,WIDTH-2))
    food_value = random.randint(1,9)
    food_list = [(food_xy[0], food_xy[1], food_value)]
    food_timer = 15

    while True:
        stdscr.clear()

        #Draw Walls
        for i in range(HEIGHT):
            stdscr.addch(i,0,'#')
            stdscr.addch(i, WIDTH-1,'#')
        for j in range(WIDTH):
            stdscr.addch(0, j, '#')
            stdscr.addch(HEIGHT-1, j,
                '#')
        # Draw food - test timer
        if food_timer == 0:
            food_char = str(random.randint(1,9))
            new_foodx = random.randint(1,WIDTH-2)
            new_foody = random.randint(1, HEIGHT-2)

            new_food = (new_foody,new_foodx, food_char)
            food_list.append(new_food)
            food_timer = 15
        else:
            food_timer -= 1

        # Draw food - put food on table

        for foodchars in food_list:
            stdscr.addch(foodchars[0],foodchars[1], foodchars[2])

        # Draw snake
        for y,x in snake:
            stdscr.addch(y,x,SNAKE_CHAR)

        # Get user input
        key = stdscr.getch()
        if key == curses.KEY_UP and direction != (1,0):
            direction = (-1,0)
        elif key == curses.KEY_DOWN and direction != (-1,0):
            direction = (1,0)
        elif key == curses.KEY_LEFT and direction != (0,1):
            direction = (0,-1)
        elif key == curses.KEY_RIGHT and direction != (0, -1):
            direction = (0, 1)

        # move the Snake
        new_head = (snake[0][0]+direction[0], snake[0][1]+direction[1])

        # collision detection
        if new_head in snake or new_head[0] in [0,HEIGHT-1] or new_head[1] in [0, WIDTH-1]:
            break

        snake.insert(0,new_head)

        if new_head in food_list:
        #    food = (random.randint(1,HEIGHT-2), random.randint(1, WIDTH-2))
            food_timer = 0
        else: snake.pop() # remove tail

        stdscr.refresh()

curses.wrapper(main)
