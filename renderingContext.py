import pygame, simManager, UI

class RenderingContext:
    def __init__(self):
        self.Active = True
        self.displaysize = (1000, 1000)
        self.clock = pygame.time.Clock()
        self.dt = 0 
        self.FrameRate = 120
        pygame.init()
        self.screen = pygame.display.set_mode(self.displaysize)
        self.simManager = simManager.simulationManager(self)
        self.UI = UI.UI()

    def main(self):
        while self.Active:
            self.screen.fill("black")

            self.dt = self.clock.tick(self.FrameRate) / 1000

            self.simManager.update()
            self.simManager.draw()
            #self.UI.update(self)

            pygame.display.flip()
        pygame.quit()

renderingContext = RenderingContext()
renderingContext.main()