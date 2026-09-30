import pygame
import random
import math


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

class Robot:
    def __init__(self, parent):
        self.pos = [random.uniform(0, parent.displaysize[0]), random.uniform(0, parent.displaysize[1])]
        #self.pos = [0, 0]
        self.rot = 0
        self.vel = [0, 0]
        self.size = 1
        
    def update(self, parent):
        self.pos = [self.pos[0] + self.vel[0]/parent.dt, self.pos[1] + self.vel[1]/parent.dt]
        self.rot = -angle([0, 1], self.vel) if length(self.vel) != 0 else 0

        pass

    def draw(self, parent):
        pygame.draw.circle(parent.screen, (0, 0, 255), self.pos, self.size)
        eye1Pos = [self.pos[0] + math.cos(self.rot + math.radians(15)) * self.size/2, self.pos[1] + math.sin(self.rot + math.radians(15)) * self.size/2]
        eye2Pos = [self.pos[0] - math.cos(self.rot - math.radians(15)) * self.size/2, self.pos[1] - math.sin(self.rot - math.radians(15)) * self.size/2]
        pygame.draw.circle(parent.screen, (250, 250, 250), eye1Pos, self.size/4)
        pygame.draw.circle(parent.screen, (250, 250, 250), eye2Pos, self.size/4)
        pass

class Main:
    def __init__(self):
        self.Active = True
        self.displaysize = (1920, 1080)
        self.clock = pygame.time.Clock()
        self.dt = 0 
        self.FrameRate = 60
        pygame.init()
        self.screen = pygame.display.set_mode(self.displaysize)

        self.robots = []
        for i in range(10):
            self.robots.append(Robot(self))


    def main(self):
        while self.Active:
            self.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False

            self.dt = self.clock.tick(self.FrameRate) / 1000

            for robot in self.robots:
                robot.update(self)
                robot.draw(self)

            pygame.display.flip()
        pygame.quit()

main = Main()
main.main()