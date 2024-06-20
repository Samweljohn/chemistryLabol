import pygame
import sys

class LiquidCollector(pygame.sprite.Sprite):
    def __init__(self, position, width, height, scaleAdditionWidth, scaleAdditionHeight, image_path):
        super().__init__()
        self.width = width
        self.height = height
        self.scaleAdditionWidth = scaleAdditionWidth
        self.scaleAdditionHeight = scaleAdditionHeight
        self.fixWidthP = position[0]
        self.fixHeightP = position[1]
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.maskSurface = pygame.Surface([self.width, self.height], pygame.SRCALPHA)  # Create a separate surface for the mask
        self.image.fill((255, 255, 255, 100))
        collector_image = pygame.image.load(image_path).convert_alpha()
        self.maskCollector = pygame.mask.from_surface(collector_image)
        collector_image = pygame.transform.scale(collector_image, (self.width + self.scaleAdditionWidth, self.height + self.scaleAdditionHeight))
        self.image.blit(collector_image, (self.fixWidthP, self.fixHeightP))

    def update(self):
        pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Liquid Collector Test")

    liquid_collector = LiquidCollector((100, 100), 100, 200, 25, 25, "con.png")
    all_sprites = pygame.sprite.Group(liquid_collector)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
