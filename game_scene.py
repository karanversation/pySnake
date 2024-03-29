import time
import pygame
import random

from scene_base import SceneBase
from end_scene import EndScene
import constants as c

sz = 10
S_COLOR = (255,0,0)
P_COLOR = (0,0,255)

G_U = 0
G_D = 1
G_L = 2
G_R = 3

def get_rand(limit):
    return random.randrange(0, limit, sz)

class Snake:
    def __init__(self):
        self.cells = [(get_rand(c.SCREEN_L), get_rand(c.SCREEN_B))]
        self.direction = G_R
        self.LEN = 5
        self.birth()

    def birth(self):
        for idx in range(1, self.LEN):
            prev_cell = self.cells[-1]
            self.cells.append((prev_cell[0]-sz, prev_cell[1]))

class Prey:
    def __init__(self):
        self.cell = (get_rand(c.SCREEN_L), get_rand(c.SCREEN_B))

class GameScene(SceneBase):

    def __init__(self):
        SceneBase.__init__(self)
        self.snake = Snake()
        self.prey = Prey()
    
    def ProcessInput(self, events, pressed_keys):
        if events:
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if self.snake.direction in (G_U, G_D) :
                        print e
                        if e.key == pygame.K_LEFT:
                            self.snake.direction = G_L
                            break
                        elif e.key == pygame.K_RIGHT:
                            self.snake.direction = G_R
                            break
                    elif self.snake.direction in (G_L, G_R):
                        print e
                        if e.key == pygame.K_UP:
                            self.snake.direction = G_U
                            break
                        elif e.key == pygame.K_DOWN:
                            self.snake.direction = G_D
                            break
        
    def Update(self):
        time.sleep(0.01)
        # update the cells
        head = self.snake.cells[0]
        new_cell = head
        if self.snake.direction == G_U:
            new_cell = (head[0], (head[1]-sz)%c.SCREEN_B)
        elif self.snake.direction == G_D:
            new_cell = (head[0], (head[1]+sz)%c.SCREEN_B)
        elif self.snake.direction == G_L:
            new_cell = ((head[0]-sz)%c.SCREEN_L, head[1])
        elif self.snake.direction == G_R:
            new_cell = ((head[0]+sz)%c.SCREEN_L, head[1])

        if new_cell in self.snake.cells:
            self.SwitchToScene(EndScene())
        
        self.snake.cells.insert(0, new_cell)
        if self.prey.cell in self.snake.cells:
            self.prey = Prey()
        else:
            self.snake.cells.pop()
        
    def Render(self, screen):
        screen.fill((0, 0, 0))
        for cell in self.snake.cells:
            pygame.draw.rect(screen, S_COLOR, (cell[0], cell[1], sz, sz))

        pygame.draw.rect(screen, P_COLOR, (self.prey.cell[0], self.prey.cell[1], sz, sz))
