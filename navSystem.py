import random, pygame, SDAmath

class Planner: # responsible for calculating a route from a to b
    def __init__(self, renderingContext):
        self.renderingContext = renderingContext
        self.StartingNode = None
        self.EndingNode = None
        self.path = []


    def calculatePath(self, start, end, networkNodes):  #find closest start and endnodes, then run dijkstra's algorithm
        if not networkNodes:
            self.path = []
            return self.path

        # find closest nodes to the start and end positions
        self.StartingNode = min(networkNodes, key=lambda n: SDAmath.distance(n.pos, start))
        self.EndingNode = min(networkNodes, key=lambda n: SDAmath.distance(n.pos, end))

        self.path = self.dijkstra(self.StartingNode, self.EndingNode, networkNodes)
        return self.path

    def dijkstra(self, startNode, endNode, networkNodes): # use dijkstra's algorithm to claculate a route from startNode to endNode
        unvisited = {node: float('inf') for node in networkNodes}
        unvisited[startNode] = 0
        previous_nodes = {node: None for node in networkNodes}

        while unvisited:
            current_node = min(unvisited, key=unvisited.get)
            if current_node == endNode:
                break

            for neighbor in current_node.ConnectingNodes:
                if neighbor in unvisited:
                    new_distance = unvisited[current_node] + SDAmath.distance(current_node.pos, neighbor.pos)
                    if new_distance < unvisited[neighbor]:
                        unvisited[neighbor] = new_distance
                        previous_nodes[neighbor] = current_node

            unvisited.pop(current_node)

        path, current_node = [], endNode
        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]
        return path[::-1]

    def draw(self):
        if self.StartingNode is None or self.EndingNode is None:
            return
        screen = self.renderingContext.screen

        for i in range(len(self.path) - 1):
            pygame.draw.line(screen, (255, 0, 255), self.path[i].pos, self.path[i + 1].pos, 3)

        pygame.draw.circle(screen, (255, 0, 255), self.StartingNode.pos, 10)
        pygame.draw.circle(screen, (255, 0, 255), self.EndingNode.pos, 10)

class navigationSystem:  # responsible for guiding the robot and determining what to do
    def __init__(self, renderingContext, simContext, robot, nodeCount=500, radius=5):
        self.networkNodes = []
        self.connectionPaths = []
        self.robot = robot
        self.radius = radius
        self.simContext = simContext
        self.renderingContext = renderingContext
        self.currentPathNode = 0
        self.currentTargetPos = [self.renderingContext.displaysize[0] - 100, self.renderingContext.displaysize[1] - 100]
        self.checkpoints = ["1", "2", "3", "4", "5", "6", "7"]
        self.path = []

        for CurrentNode in range(nodeCount):
            pos = [
                random.uniform(0, self.renderingContext.displaysize[0]),
                random.uniform(0, self.renderingContext.displaysize[1])
            ]

            if not self.pointCollides(pos):
                # im lazy
                name = "Empty"
                for i in self.checkpoints:
                    if CurrentNode == self.checkpoints.index(i):
                        name = i


                self.networkNodes.append(navigationNode(pos, name))

        for i, node in enumerate(self.networkNodes):
            for connectingNode in self.networkNodes[i + 1:]:

                if not self.lineCollides(node.pos, connectingNode.pos):

                    self.connectionPaths.append((node, connectingNode))
                    node.ConnectingNodes.append(connectingNode)
                    connectingNode.ConnectingNodes.append(node)

        self.planner = Planner(self.renderingContext)
        
    def recalculateRoute(self): # call the planner to recaclulate a path with the targetPos
        self.path = self.planner.calculatePath(self.robot.pos, self.currentTargetPos, self.networkNodes)

    def update(self): # main cycling loop for navigation logic
        multiplier = -300#tuning parameter

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False
                elif event.type == pygame.KEYDOWN:
                    for node in self.networkNodes:
                        if node.name.lower() == pygame.key.name(event.key):
                            self.currentPathNode = 0
                            self.currentTargetPos = node.pos
                            self.recalculateRoute()

        if self.currentPathNode < len(self.path):
            deltaDistance = SDAmath.distance(self.robot.pos, self.path[self.currentPathNode].pos)
            self.robot.applyForce(((self.robot.pos[0] - self.path[self.currentPathNode].pos[0])/deltaDistance) * multiplier, ((self.robot.pos[1] - self.path[self.currentPathNode].pos[1])/deltaDistance) * multiplier)
            if deltaDistance < 10:
                self.currentPathNode += 1

    def pointCollides(self, pos): # check if point collides with a collider
        r = self.radius
        for gen in self.simContext.collisionGenInstances:
            for obj in gen.collisionObjects:
                if (
                    pos[0] + r > obj.pos[0] and
                    pos[0] - r < obj.pos[0] + obj.size[0] and
                    pos[1] + r > obj.pos[1] and
                    pos[1] - r < obj.pos[1] + obj.size[1]
                ):
                    return True
        return False
    
    def lineCollides(self, a, b): # check if line collides with a collider
        r = self.radius
        dx = b[0] - a[0]
        dy = b[1] - a[1]

        for gen in self.simContext.collisionGenInstances:
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
    
    def draw(self):
        for path in self.connectionPaths:
            pygame.draw.line(self.renderingContext.screen, (3, 105, 0), path[0].pos, path[1].pos, 1)

        self.planner.draw()
        for node in self.networkNodes:
            pygame.draw.circle(self.renderingContext.screen, (0, 255, 0), node.pos, self.radius)

            if node.name in self.checkpoints:
                font = pygame.font.SysFont(None, 32)
                pygame.draw.rect(self.renderingContext.screen, (255, 0, 255), pygame.Rect(node.pos[0] - 5, node.pos[1] - 5, 20, 20))
                self.renderingContext.screen.blit(font.render(node.name, True, (255, 255, 255)), (node.pos[0] - 5, node.pos[1] - 5))
        

class navigationNode: # one node instance, with data for position name and connecting node references
    def __init__(self, pos, *args):
        self.name = "Empty"
        if args:
            self.name = args[0]
        self.pos = pos
        self.ConnectingNodes = []
