import robot, collisionGen

class simulationManager:
    def __init__(self, renderingContext):
        self.collisionGenInstances = []
        self.collisionGenInstances.append(collisionGen.CollisionGen())

        self.robots = []
        self.robots.append(robot.Robot(renderingContext, self))

    def update(self, renderingContext):
            for robot in self.robots:
                robot.update(renderingContext)
                #robot.applyForce([random.uniform(-1, 1), random.uniform(-1, 1)])

    def draw(self, renderingContext):
        for collisionGen in self.collisionGenInstances:
            collisionGen.draw(renderingContext)

        for robot in self.robots:
            robot.draw(renderingContext)



