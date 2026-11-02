import random, SDAmath, math, pygame, navSystem

class Robot:
    def __init__(self, renderingContext, simContext):
        #self.pos = [random.uniform(0, parent.displaysize[0]), random.uniform(0, parent.displaysize[1])]
        self.pos = [100, 100]
        self.mass = 100
        self.rot = 0
        maxvel = 0.3
        #self.vel = [random.uniform(-maxvel, maxvel), random.uniform(-maxvel, maxvel)]
        self.vel = [0, 0]
        self.size = 20
        self.navigation = navSystem.navigationSystem(renderingContext, simContext)

    def collisionCheck(self):
        #Collision checks
        #if you hit a wall it flips all the velocity vectors
        for i in simContext.collisionObjects:
            if (self.pos[0] + self.size > i.pos[0] and self.pos[0] - self.size < i.pos[0] + i.size[0]) and (self.pos[1] + self.size > i.pos[1] and self.pos[1] - self.size < i.pos[1] + i.size[1]):
                self.vel[0] = -1*self.vel[0] + random.uniform(-self.vel[0]/2, self.vel[0]/2)
                self.vel[1] = -1*self.vel[1] + random.uniform(-self.vel[1]/2, self.vel[1]/2)

        for i in simContext.robots:
            if SDAmath.distance(self.pos, i.pos) < self.size + i.size and i != self:
                self.vel[0] = -1*self.vel[0] + random.uniform(-self.vel[0]/2, self.vel[0]/2)
                self.vel[1] = -1*self.vel[1] + random.uniform(-self.vel[1]/2, self.vel[1]/2)


    def applyForce(self, force):
        self.vel[0] += force[0] / self.mass
        self.vel[1] += force[1] / self.mass
    
    def update(self, renderingContext):
        self.pos[0] += self.vel[0] / renderingContext.dt
        self.pos[1] += self.vel[1] / renderingContext.dt
        self.rot = SDAmath.atan2(self.vel[1], self.vel[0]) if SDAmath.length(self.vel) != 0 else 0

        if SDAmath.length(self.vel) > 1:
            self.vel = [0.0, 0.0]

        #self.collisionCheck(renderingContext)

    def draw(self, renderingContext):
        pygame.draw.circle(renderingContext.screen, (0, 0, 255), self.pos, self.size)

        #draw eyes
        eyeAngle = 45
        eye1Pos = [self.pos[0] + math.cos(self.rot + math.radians(eyeAngle)) * self.size/1.5, self.pos[1] + math.sin(self.rot + math.radians(eyeAngle)) * self.size/1.5]
        eye2Pos = [self.pos[0] + math.cos(self.rot - math.radians(eyeAngle)) * self.size/1.5, self.pos[1] + math.sin(self.rot - math.radians(eyeAngle)) * self.size/1.5]
        pygame.draw.circle(renderingContext.screen, (250, 250, 250), eye1Pos, self.size/4)
        pygame.draw.circle(renderingContext.screen, (250, 250, 250), eye2Pos, self.size/4)

        self.navigation.draw(renderingContext)