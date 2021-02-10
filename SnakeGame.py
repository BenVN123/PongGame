import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# The cube objects are the individual squares that make up the snake
class cube:
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    # Moves the cube
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # Draws the cube
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))

        # Draws the eyes on the cube where eyes=True
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i*dis+center-radius, j*dis+8)
            circleMiddle2 =  (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

# The snake object is the combination of the cube objects to make a complete snake
class snake:
    body = [] # A list containing the cubes of the snake
    turns = {} # The turns of the snake

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            keys = pygame.key.get_pressed() # Dictionary of all keys and wether or not they are pressed

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    # Adds element to the turns dictionary (key is current position and value is the newdirection)
                    # We don't keep this code outside of the if and elifs because player may not always press a key
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # Turns for all of the following cubes in the snake's body
        for i, c in enumerate(self.body):
            p =  c.pos[:] # Grabs position of each cube
            if p in self.turns: # If p is in the turns dictionary...
                turn = self.turns[p] # turn is the value in turns where the key is p
                c.move(turn[0], turn[1]) # Gives move method the dirnx and dirny from the turn variable
                if i == len(self.body) - 1: # If we are on the last cube of the snake...
                    self.turns.pop(p) # Removes turn since if we don't, we will always turn at that position no matter what
            else:
                # If the snake is at the edge of the screen, appear at the opposite side
                # Else, just continue to move
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0],c.rows-1)
                else:
                    c.move(c.dirnx,c.dirny)

    def reset(self, pos):
        self.body = []
        self.turns = {}
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0 :
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        # Draws each cube of the snake
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True) # True says that the first cube has eyes
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows # Finds size of each row in grid by dividing the width by the number of rows
    x = 0
    y = 0

    # Creates the grid
    for i in range(rows):
        x += sizeBtwn # Changes x-value to compensate for size of each block
        y += sizeBtwn # Changes y-value to compensate for size of each block
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) # Vertical line (starts at (x, 0) and ends (x,w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y)) # Horizontal line (starts at (0, y) and ends (w,y))

# Redraws window to show change in snake/snack position
def redrawWindow(surface):
    global rows, width, s
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    # Keeps changing the position until the snack doesn't spawn on the snake
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except Exception:
        pass

def main():
    # Sets sizes for the game window
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width)) # Creates the window
    s = snake((255,0,0), (10, 10)) # Creates the snake object
    snack = cube(randomSnack(rows, s), color=(0,255,0)) # Creates object for the snack cube
    flag = True
    clock = pygame.time.Clock()

    # Updates the window after a certain amount of time
    while flag:
        pygame.event.get()
        pygame.time.delay(50) # Delays by 50 milliseconds
        clock.tick(10) # Keeps the game at 10 fps or lower
        s.move() # Everytime this loop runs, run the move() method in the snake class
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Died!', 'Play again...')
                s.reset((10,10))
                break
        
        redrawWindow(win) # Redraws window

main()