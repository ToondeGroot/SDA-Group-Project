import robot, collisionGen, random

class simulationManager: # responsible for keeping track of the simulated robot and colliders
    def __init__(self, renderingContext):
        self.collisionGenInstances = []
        self.collisionGenInstances.append(collisionGen.CollisionGen(renderingContext))

        self.robots = []
        self.robots.append(robot.Robot(renderingContext, self))

    def update(self):
        for robot in self.robots:
            robot.update()
            # robot.applyForce([random.uniform(-50, 50), random.uniform(-50, 50)])

    def draw(self):
        for collisionGen in self.collisionGenInstances:
            collisionGen.draw()

        for robot in self.robots:
            robot.draw()



