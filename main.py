import pygame
import random
import math

#extra math for rotating the lil guy
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def distance(v1, v2):
    return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)

class navigationSystem:
    def __init__(self, parent):
        pass

class CollisionObject: #aka wall
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def draw(self, parent):
        pygame.draw.rect(parent.screen, (255, 0, 0), (self.pos[0], self.pos[1], self.size[0], self.size[1]))


class Robot:
    def __init__(self, parent):
        self.pos = [random.uniform(0, parent.displaysize[0]), random.uniform(0, parent.displaysize[1])]
        #self.pos = [0, 0]
        self.mass = 100
        self.rot = 0
        maxvel = 0.3
        #self.vel = [random.uniform(-maxvel, maxvel), random.uniform(-maxvel, maxvel)]
        self.vel = [-0.5, 0.5]
        self.size = 10

    def collisionCheck(self, parent):

        #Collision checks
        #if you hit a wall it flips all the velocity vectors
        for i in parent.collisionObjects:
            if (self.pos[0] + self.size > i.pos[0] and self.pos[0] - self.size < i.pos[0] + i.size[0]) and (self.pos[1] + self.size > i.pos[1] and self.pos[1] - self.size < i.pos[1] + i.size[1]):
                self.vel[0] = -1*self.vel[0] + random.uniform(-self.vel[0]/2, self.vel[0]/2)
                self.vel[1] = -1*self.vel[1] + random.uniform(-self.vel[1]/2, self.vel[1]/2)

        for i in parent.robots:
            if distance(self.pos, i.pos) < self.size + i.size and i != self:
                self.vel[0] = -1*self.vel[0] + random.uniform(-self.vel[0]/2, self.vel[0]/2)
                self.vel[1] = -1*self.vel[1] + random.uniform(-self.vel[1]/2, self.vel[1]/2)


    def applyForce(self, force):
        self.vel[0] += force[0] / self.mass
        self.vel[1] += force[1] / self.mass
    
    def update(self, parent):
        self.pos[0] += self.vel[0] / parent.dt
        self.pos[1] += self.vel[1] / parent.dt
        self.rot = math.atan2(self.vel[1], self.vel[0]) if length(self.vel) != 0 else 0

        if length(self.vel) > 1:
            self.vel = [0.0, 0.0]

        self.collisionCheck(parent)

    def draw(self, parent):
        pygame.draw.circle(parent.screen, (0, 0, 255), self.pos, self.size)

        #pygame.draw.line(parent.screen, (0, 255, 0), self.pos, [self.pos[0] + math.cos(self.rot)*100, self.pos[1] + math.sin(self.rot)*100])
        
        #draw eyes
        eyeAngle = 45
        eye1Pos = [self.pos[0] + math.cos(self.rot + math.radians(eyeAngle)) * self.size/1.5, self.pos[1] + math.sin(self.rot + math.radians(eyeAngle)) * self.size/1.5]
        eye2Pos = [self.pos[0] + math.cos(self.rot - math.radians(eyeAngle)) * self.size/1.5, self.pos[1] + math.sin(self.rot - math.radians(eyeAngle)) * self.size/1.5]
        pygame.draw.circle(parent.screen, (250, 250, 250), eye1Pos, self.size/4)
        pygame.draw.circle(parent.screen, (250, 250, 250), eye2Pos, self.size/4)


class Main:
    def __init__(self):
        self.Active = True
        self.displaysize = (1920, 1080)
        self.clock = pygame.time.Clock()
        self.dt = 0 
        self.FrameRate = 60
        pygame.init()
        self.screen = pygame.display.set_mode(self.displaysize)
        
        self.collisionObjects = [
            #Outside walls
            CollisionObject([0, 0], [10, 1080]), CollisionObject([0, 0], [1920, 10]),
            CollisionObject([0, 1080-10], [1920, 10]), CollisionObject([1920-10, 0], [10, 1080]),

            CollisionObject([500, 0], [20, 400]), CollisionObject([1000, 400], [20, 800]),
        ]

        self.robots = []
        for i in range(1):
            self.robots.append(Robot(self))


    def main(self):
        while self.Active:
            self.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False

            self.dt = self.clock.tick(self.FrameRate) / 1000

            #draw queue
            for collisionObject in self.collisionObjects:
                collisionObject.draw(self)

            for robot in self.robots:
                robot.update(self)
                robot.draw(self)

                #robot.applyForce([random.uniform(-1, 1), random.uniform(-1, 1)])

            pygame.display.flip()
        pygame.quit()

main = Main()
main.main()