import pygame, sys
from PIL import Image

pygame.init()

class SelectImage:
    def __init__(self, input_image):
        self.px = pygame.image.load(input_image)
        self.screen = pygame.display.set_mode( self.px.get_rect()[2:] )
        self.screen.blit(self.px, self.px.get_rect())

    def __displayImage__(self, screen, px, topleft, prior):
        # ensure that the rect always has positive width, height
        x, y = topleft
        width =  pygame.mouse.get_pos()[0] - topleft[0]
        height = pygame.mouse.get_pos()[1] - topleft[1]
        if width < 0:
            x += width
            width = abs(width)
        if height < 0:
            y += height
            height = abs(height)

        # eliminate redundant drawing cycles (when mouse isn't moving)
        current = x, y, width, height
        if not (width and height):
            return current
        if current == prior:
            return current

        # draw transparent box and blit it onto canvas
        screen.blit(px, px.get_rect())
        im = pygame.Surface((width, height))
        im.fill((128, 128, 128))
        pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
        im.set_alpha(128)
        screen.blit(im, (x, y))
        pygame.display.flip()

        # return current box extents
        return (x, y, width, height)

    def cropSelection(self):
        pygame.display.flip()
        topleft = bottomright = prior = None
        n=0
        while n!=1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if not topleft:
                        topleft = event.pos
                    else:
                        bottomright = event.pos
                        n=1
            if topleft:
                prior = self.__displayImage__(self.screen, self.px, topleft, prior)
        pygame.display.quit()
        return ( topleft + bottomright )
