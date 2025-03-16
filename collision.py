import curses
import random
import time
import math


# Explosion effect function
def explosion(stdscr, x, y, letters="BOOM", duration=1.5):
    curses.start_color()

    # Define some color pairs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    max_y, max_x = stdscr.getmaxyx()
    particles = []

    # Initialize particles with random directions
    for letter in letters:
        angle = random.uniform(0, 2 * math.pi)  # Random angle
        speed = random.uniform(1, 3)  # Random speed factor
        particles.append(
            {"char": letter, "x": x, "y": y, "dx": math.cos(angle) * speed, "dy": -abs(math.sin(angle) * speed),
             "color": 1})

    start_time = time.time()

    while time.time() - start_time < duration:
        stdscr.clear()

        new_particles = []
        for p in particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["dy"] += 0.1  # Gravity effect

            # Change colors over time
            if time.time() - start_time > duration * 0.5:
                p["color"] = 2
            if time.time() - start_time > duration * 0.7:
                p["color"] = 3
            if time.time() - start_time > duration * 0.9:
                p["color"] = 4

            if 0 < int(p["x"]) < max_x - 1 and 0 < int(p["y"]) < max_y - 1:
                new_particles.append(p)
                stdscr.addch(int(p["y"]), int(p["x"]), p["char"], curses.color_pair(p["color"]))

        particles = new_particles
        stdscr.refresh()
        time.sleep(0.05)

    stdscr.clear()
    stdscr.refresh()


# Main function
def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getch non-blocking
    stdscr.timeout(100)

    max_y, max_x = stdscr.getmaxyx()
    x, y = max_x // 2, max_y // 2

    stdscr.addstr(y, x, "Press SPACE to trigger explosion", curses.A_BOLD)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord("q"):  # Quit
            break
        elif key == ord(" "):  # Space triggers explosion
            explosion(stdscr, x, y)
            stdscr.addstr(y, x, "Press SPACE to trigger explosion", curses.A_BOLD)
            stdscr.refresh()


curses.wrapper(main)


