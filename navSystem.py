import random, pygame

class navigationSystem:
    def __init__(self, renderingContext, simContext, nodeCount=50, radius=5):
        self.networkNodes = []
        self.radius = radius

        for _ in range(nodeCount):
            pos = [
                random.uniform(0, renderingContext.displaysize[0]),
                random.uniform(0, renderingContext.displaysize[1])
            ]

            if not self.pointCollides(pos, simContext):
                self.networkNodes.append(navigationNode(pos))

    def pointCollides(self, pos, simContext):
        r = self.radius
        for gen in simContext.collisionGenInstances:
            for obj in gen.collisionObjects:
                if (
                    pos[0] + r > obj.pos[0] and
                    pos[0] - r < obj.pos[0] + obj.size[0] and
                    pos[1] + r > obj.pos[1] and
                    pos[1] - r < obj.pos[1] + obj.size[1]
                ):
                    return True
        return False
    
    def lineCollides(self, a, b, simContext):
        r = self.radius
        dx = b[0] - a[0]
        dy = b[1] - a[1]

        for gen in simContext.collisionGenInstances:
            for obj in gen.collisionObjects:
                xmin = obj.pos[0] - r
                xmax = obj.pos[0] + obj.size[0] + r
                ymin = obj.pos[1] - r
                ymax = obj.pos[1] + obj.size[1] + r

                t0, t1 = 0.0, 1.0

                for p, q in (
                    (-dx, a[0] - xmin),
                    ( dx, xmax - a[0]),
                    (-dy, a[1] - ymin),
                    ( dy, ymax - a[1]),
                ):
                    if p == 0:
                        if q <= 0:
                            break
                    else:
                        t = q / p
                        if p < 0:
                            if t > t1:
                                break
                            t0 = max(t0, t)
                        else:
                            if t < t0:
                                break
                            t1 = min(t1, t)
                else:
                    return True

        return False
    
    def draw(self, renderingContext):
        for node in self.networkNodes:
            pygame.draw.circle(renderingContext.screen, (0, 255, 0), node.pos, self.radius)

            for connectingNode in self.networkNodes:
                if not self.lineCollides(node.pos, connectingNode.pos, renderingContext.simManager):
                    pygame.draw.line(renderingContext.screen, (0, 255, 0), node.pos, connectingNode.pos)




class navigationNode:
    def __init__(self, pos):
        self.name = "Empty"
        self.pos = pos
        self.ConnectingNodes = {}
