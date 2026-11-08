import pygame, simManager, UI

class RenderingContext: # responisble for the pygame context and display parameters
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
        while self.Active: # root running loop
            self.screen.fill("black") # draw black

            self.dt = self.clock.tick(self.FrameRate) / 1000 #calc frametime

            self.simManager.update() #calculate current frame
            self.simManager.draw() #draw current frame
            #self.UI.update(self)

            pygame.display.flip()
        pygame.quit()

#instance the rendering context and run the code
renderingContext = RenderingContext()
renderingContext.main()