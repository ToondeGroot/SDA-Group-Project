import random, SDAmath, math, pygame, navSystem

class Robot:
    def __init__(self, renderingContext, simContext):
        #self.pos = [random.uniform(0, parent.displaysize[0]), random.uniform(0, parent.displaysize[1])]
        self.pos = [100, 100]
        self.mass = 1
        self.rot = 0
        maxvel = 0.3
        #self.vel = [random.uniform(-maxvel, maxvel), random.uniform(-maxvel, maxvel)]
        self.vel = [0, 0]
        self.size = 20
        self.simContext = simContext
        self.renderingContext = renderingContext
        self.navigation = navSystem.navigationSystem(renderingContext, self.simContext, self)

    def collisionCheck(self):
        #Collision checks
        #if you hit a wall it flips all the velocity vectors:
        if self.navigation.pointCollides(self.pos):
            self.vel[0] = -1*self.vel[0] + random.uniform(-self.vel[0]/2, self.vel[0]/2)
            self.vel[1] = -1*self.vel[1] + random.uniform(-self.vel[1]/2, self.vel[1]/2)

    def applyForce(self, forceX, forceY):
        self.vel[0] += forceX / self.mass
        self.vel[1] += forceY / self.mass

    def update(self):
        self.navigation.update()
        self.pos[0] += self.vel[0] * self.renderingContext.dt
        self.pos[1] += self.vel[1] * self.renderingContext.dt
        self.rot = SDAmath.math.atan2(self.vel[1], self.vel[0]) if SDAmath.length(self.vel) != 0 else 0

        if SDAmath.length(self.vel) > 1:
            self.vel = [0.0, 0.0]

        self.collisionCheck()

    def draw(self):
        self.navigation.draw()
        pygame.draw.circle(self.renderingContext.screen, (0, 0, 255), self.pos, self.size)

        #draw eyes
        eyeAngle = 45
        eye1Pos = [self.pos[0] + math.cos(self.rot + math.radians(eyeAngle)) * self.size/1.5, self.pos[1] + math.sin(self.rot + math.radians(eyeAngle)) * self.size/1.5]
        eye2Pos = [self.pos[0] + math.cos(self.rot - math.radians(eyeAngle)) * self.size/1.5, self.pos[1] + math.sin(self.rot - math.radians(eyeAngle)) * self.size/1.5]
        pygame.draw.circle(self.renderingContext.screen, (250, 250, 250), eye1Pos, self.size/4)
        pygame.draw.circle(self.renderingContext.screen, (250, 250, 250), eye2Pos, self.size/4)

        