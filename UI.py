import pygame

# not used

class UI: 
    def __init__(self):
        self.size = [500, 300]
        self.color = (100, 100, 100)
        self.font = pygame.font.SysFont(None, 48)
        self.HeaderIMG = self.font.render("SDA UI", True, (0, 0, 0))

    def update(self, renderingContext):
        pygame.draw.rect(renderingContext.screen, self.color, (renderingContext.displaysize[0] - self.size[0], renderingContext.displaysize[1] - self.size[1], self.size[0], self.size[1]))
        renderingContext.screen.blit(self.HeaderIMG, (renderingContext.displaysize[0] - (self.size[0]/2) - self.HeaderIMG.get_width()/2, renderingContext.displaysize[1] - self.size[1]))