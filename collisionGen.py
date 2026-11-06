import pygame

class CollisionGen:
    def __init__(self, renderingContext):
        self.RenderingContext = renderingContext
        self.collisionObjects = [
            # Outside walls
            CollisionObject(self.RenderingContext, [0, 0], [10, 1080]),
            CollisionObject(self.RenderingContext, [0, 0], [1920, 10]),
            CollisionObject(self.RenderingContext, [0, 1070], [1920, 10]),
            CollisionObject(self.RenderingContext, [1910, 0], [10, 1080]),

            # Original internal walls
            CollisionObject(self.RenderingContext, [500, 0], [20, 400]),
            CollisionObject(self.RenderingContext, [1000, 400], [20, 800]),
            CollisionObject(self.RenderingContext, [500, 680], [20, 400]),
            CollisionObject(self.RenderingContext, [1000, 400], [500, 20]),

            # Upper-left section
            CollisionObject(self.RenderingContext, [150, 200], [250, 20]),
            CollisionObject(self.RenderingContext, [150, 200], [20, 200]),
            CollisionObject(self.RenderingContext, [250, 400], [250, 20]),

            # Upper-middle section
            CollisionObject(self.RenderingContext, [650, 150], [250, 20]),
            CollisionObject(self.RenderingContext, [650, 150], [20, 150]),
            CollisionObject(self.RenderingContext, [800, 300], [200, 20]),

            # Upper-right section
            CollisionObject(self.RenderingContext, [1200, 150], [400, 20]),
            CollisionObject(self.RenderingContext, [1200, 150], [20, 150]),
            CollisionObject(self.RenderingContext, [1450, 300], [20, 100]),

            # Middle section
            CollisionObject(self.RenderingContext, [100, 550], [300, 20]),
            CollisionObject(self.RenderingContext, [250, 550], [20, 100]),
            CollisionObject(self.RenderingContext, [650, 500], [200, 20]),
            CollisionObject(self.RenderingContext, [800, 500], [20, 150]),
            CollisionObject(self.RenderingContext, [1200, 550], [300, 20]),

            # Lower-left section
            CollisionObject(self.RenderingContext, [150, 850], [250, 20]),
            CollisionObject(self.RenderingContext, [150, 850], [20, 150]),
            CollisionObject(self.RenderingContext, [350, 900], [20, 100]),

            # Lower-middle section
            CollisionObject(self.RenderingContext, [650, 800], [250, 20]),
            CollisionObject(self.RenderingContext, [650, 800], [20, 150]),
            CollisionObject(self.RenderingContext, [800, 950], [200, 20]),

            # Lower-right section
            CollisionObject(self.RenderingContext, [1200, 800], [300, 20]),
            CollisionObject(self.RenderingContext, [1200, 800], [20, 150]),
            CollisionObject(self.RenderingContext, [1500, 900], [20, 100]),
        ]

    def draw(self):
        for collisionObject in self.collisionObjects:
            collisionObject.draw()

class CollisionObject: #aka wall
    def __init__(self, RenderingContext, pos, size):
        self.RenderingContext = RenderingContext
        self.pos = pos
        self.size = size

    def draw(self):
        pygame.draw.rect(self.RenderingContext.screen, (255, 0, 0), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        
        # for i in self.networkNodes:
        #     pygame.draw.circle(parent.screen, (0, 255, 0), i.pos, 5)