import pygame

class CollisionGen:
    def __init__(self):
        self.collisionObjects = [
            #Outside walls
            CollisionObject([0, 0], [10, 1080]), CollisionObject([0, 0], [1920, 10]),
            CollisionObject([0, 1080-10], [1920, 10]), CollisionObject([1920-10, 0], [10, 1080]),

            CollisionObject([500, 0], [20, 400]), CollisionObject([1000, 400], [20, 800]),
        ]

    def draw(self, drawingContext):
        for collisionObject in self.collisionObjects:
            collisionObject.draw(drawingContext)

class CollisionObject: #aka wall
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def draw(self, drawingContext):
        pygame.draw.rect(drawingContext.screen, (255, 0, 0), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        
        # for i in self.networkNodes:
        #     pygame.draw.circle(parent.screen, (0, 255, 0), i.pos, 5)