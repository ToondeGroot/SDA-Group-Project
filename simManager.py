

import random, simManager, SDAmath, math, pygame, robot, collisionGen

class simulationManager:
    def __init__(self, renderingContext):
        self.robots = []
        self.robots.append(robot.Robot(renderingContext))

        self.collisionGenInstances = []
        self.collisionGenInstances.append(collisionGen.CollisionGen())

    def update(self, renderingContext):
            for robot in self.robots:
                robot.update(renderingContext)
                robot.draw(renderingContext)

                #robot.applyForce([random.uniform(-1, 1), random.uniform(-1, 1)])

            for collisionGen in self.collisionGenInstances:
                collisionGen.draw(renderingContext)


