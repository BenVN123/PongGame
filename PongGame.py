import random
import pygame
import tkinter as tk
from tkinter import messagebox

class paddle:
    def __init__(self, start, color=(255,255,255)):
        self.pos = start
        self.color = color

    def move(self, dirn):
        self.dirn = dirn
        self.pos = (self.pos[0], self.pos[1] + self.dirn)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos[0], self.pos[1], 20, 100))

class ball:
    def __init__(self, color=(255,255,255)):
        self.color = color
        self.pos = (width/2, height/2)
        self.dirnx = random.choice([1, -1])
        self.dirny = random.choice([1,-1])
        self.dirn = random.choice([0.3,0.35,0.4,0.45,0.5,0.55,0.6])
        self.dirn = (self.dirn, 0.6-self.dirn)

    def draw(self, surface):
        self.pos = (self.pos[0]+self.dirnx*self.dirn[0], self.pos[1]+self.dirny*self.dirn[1])
        if self.pos[1] <= 0 or self.pos[1] >= height:
            self.dirny *= -1
        if self.pos[0] > 39 and self.pos[0] < 41 and self.pos[1] > (p1.pos[1]-10) and self.pos[1] < (p1.pos[1]+110):
            self.dirn = random.choice([0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6])
            self.dirn = (self.dirn, 0.6-self.dirn)
            self.dirnx = 1
            if (self.pos[1] > (p1.pos[1]-10) and self.pos[1] < (p1.pos[1]+40)) or (self.pos[1] > (p1.pos[1]+60) and self.pos[1] < (p1.pos[1]+110)):
                self.dirny *= -1
        elif self.pos[0] < width-55 and self.pos[0] > width-57 and self.pos[1] > (p2.pos[1]-10) and self.pos[1] < (p2.pos[1]+109):
            self.dirn = random.choice([0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6])
            self.dirn = (self.dirn, 0.6-self.dirn)
            self.dirnx = -1
            if (self.pos[1] > (p2.pos[1]-10) and self.pos[1] < (p2.pos[1]+40)) or (self.pos[1] > (p2.pos[1]+60) and self.pos[1] < (p2.pos[1]+110)):
                self.dirny *= -1
        elif self.pos[0] < 0 or self.pos[0] > width:
            state = 'HELP'
            window.fill((0,0,0))
            font = pygame.font.SysFont(None, 50)
            if self.pos[0]<0:
                text = font.render("Player two wins!", True, (255,255,255))
                window.blit(text,[width/6 + 30, height/5 + 70])
            else: 
                text = font.render("Player one wins!", True, (255,255,255))
                window.blit(text,[width/6 + 30, height/5 + 70])
            font = pygame.font.SysFont(None, 30)
            text = font.render("Press the 'b' key to return", True, (255,255,255))
            window.blit(text,[width-300, height-50])
            pygame.display.update()
            while True:
                pygame.event.get()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_b]:
                    start()
        
        pygame.draw.ellipse(surface, self.color, (self.pos[0], self.pos[1], 20, 20))

def keyboard():
    global current_option, state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()
    if state == 'START':
        if keys[pygame.K_RETURN] and current_option == 'Start':
            play()
            return
        elif keys[pygame.K_RETURN] and current_option == 'Help':
            state = 'HELP'
            window.fill((0,0,0))
            font = pygame.font.SysFont(None, 50)
            text = font.render("Player one uses the 'w' and 'a' keys to move", True, (255,255,255))
            window.blit(text,[width/6 + 30, height/5 + 70])
            text = font.render("Player two uses the arrow keys to move", True, (255,255,255))
            window.blit(text,[width/6 + 50, height/5+2*70])
            text = font.render('Use your paddles to block the ball', True, (255,255,255))
            window.blit(text,[width/6 + 90, height/5+3*70])
            text = font.render("Get the ball past your opponent's paddle to win", True, (255,255,255))
            window.blit(text,[width/6, height/5+4*70])
            font = pygame.font.SysFont(None, 30)
            text = font.render("Press the 'b' key to return", True, (255,255,255))
            window.blit(text,[width-300, height-50])
            pygame.display.update()
            while True:
                pygame.event.get()
                keyboard()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
        elif keys[pygame.K_RETURN] and current_option == 'Exit':
            pygame.quit()
        elif keys[pygame.K_UP] and (current_option == options_list[2][2:] or current_option == options_list[1][2:]):
            index = options_list.index('* '+current_option)
            options_list[index] = current_option
            current_option = options_list[index-1]
            options_list[index-1] = '* '+options_list[index-1]
            pygame.time.delay(125)
        elif keys[pygame.K_DOWN] and (current_option == options_list[0][2:] or current_option == options_list[1][2:]):
            index = options_list.index('* '+current_option)
            options_list[index] = current_option
            current_option = options_list[index+1]
            options_list[index+1] = '* '+options_list[index+1]
            pygame.time.delay(125)    
    elif state == 'PLAY':
        if keys[pygame.K_UP] and p2.pos[1] >= 0 and state == 'PLAY':
            p2.move(-0.4) 
        if keys[pygame.K_DOWN] and p2.pos[1] <= (height - 100) and state == 'PLAY':
            p2.move(0.4)
        if keys[pygame.K_w] and p1.pos[1] >= 0 and state == 'PLAY':
            p1.move(-0.4)
        if keys[pygame.K_s] and p1.pos[1] <= (height - 100) and state == 'PLAY':
            p1.move(0.4)
    elif state == 'HELP':
        if keys[pygame.K_b]:
            start()
            return

def redrawWindow(s):
    s.fill((0, 0, 0))
    p1.draw(s)
    p2.draw(s)
    pongball.draw(s)
    pygame.display.update()

def play():
    global p1, p2, state, pongball
    p1 = paddle((20, 270))
    p2 = paddle((width-40, 270))
    pongball = ball()
    state = 'PLAY'
    for i in ['3','2','1']:
        window.fill((0,0,0))
        font = pygame.font.SysFont(None, 300)
        text = font.render(i, True, (255,255,255))
        window.blit(text,[width/2 -50, height/2 - 125])
        pygame.display.update()
        pygame.time.delay(1000)

    while True:
        pygame.event.get()
        redrawWindow(window)
        keyboard()

def start():
    pygame.init()
    global width, height, window, state, start_text, help_text, exit_text, current_option, options_list
    width = 1200
    height = 700
    state = 'START'
    window = pygame.display.set_mode((width, height))
    current_option = 'Start'
    options_list = ['* Start', 'Help', 'Exit']

    while True: 
        keyboard()
        window.fill((0,0,0))
        font = pygame.font.SysFont(None, 125)
        text = font.render('Pong: The Game', True, (255,255,255))
        window.blit(text,[width/2-340, height/6])
        font = pygame.font.SysFont(None, 90)
        text = font.render(options_list[0], True, (255,255,255))
        window.blit(text,[width/2 - 50, height/2.5])
        text = font.render(options_list[1], True, (255,255,255))
        window.blit(text,[width/2 - 45, height/2.5+(height/7)])
        text = font.render(options_list[2], True, (255,255,255))
        window.blit(text,[width/2 - 45, height/2.5+2*(height/7)])
        pygame.display.update()

start()