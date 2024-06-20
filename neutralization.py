import pygame
import random
class Chemicals(pygame.sprite.Sprite):
    def __init__(self, pos, color, acidAmmount, conceTration, name,window):
        super().__init__()
        self.pos = list(pos)
        self.window=window
        self.color = color
        self.name = name
        self.amount = acidAmmount
        self.conc = conceTration
        self.gravity = 0.1
        self.dragging = False
        self.vel = [random.uniform(-0.5, 0.5), random.uniform(-2, -1)]
        self.size = random.randint(2, 4)
        self.image = pygame.Surface([6, 12], pygame.SRCALPHA)  # smaller size
        pygame.draw.rect(self.image, self.color, [0, 0, 6, 12])
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self):
        if not self.dragging:
            self.move()
        self.rect.center = self.pos
        self.window.blit(self.image, self.rect.topleft)
        
    def move(self):
        self.vel[1] += self.gravity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

class ChemicalContainer(pygame.sprite.Sprite):
    def __init__(self, pos, color, name,window):
        super().__init__()
        self.pos = list(pos)
        self.window=window
        self.color = color
        self.name = name
        self.dragging = False
        self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, [0, 0, 50, 50])
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self):
        self.rect.center = self.pos
        self.window.blit(self.image, self.rect.topleft)
        
    def release_particle(self):
        return Chemicals(self.rect.center, self.color, 1, 0.1, self.name,self.window)  # smaller amount

class WaterParticle(pygame.sprite.Sprite):
    def __init__(self, pos,window):
        super().__init__()
        self.pos = list(pos)
        self.window=window
        self.dragging = False
        imageOfWaterContainer = pygame.image.load("1.png").convert_alpha()
        self.texture = pygame.transform.scale(imageOfWaterContainer, (200, 200))
        self.rect = self.texture.get_rect(center=self.pos)
        
    def update(self):
        self.rect.center = self.pos
        self.window.blit(self.texture, self.rect.topleft)

class LiquidIndicator(pygame.sprite.Sprite):
    def __init__(self, pos, color, label,window):
        super().__init__()
        self.radius = 10
        self.label = label
        self.window=window
        self.pos = list(pos)
        self.color = color
        self.dragging = False
        self.image = pygame.Surface([12, 23], pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, [0, 0, 12, 23])
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos
        self.window.blit(self.image, self.rect.topleft)

class LiquidCollector(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, capacity,imagApp,inportInfo):
        super().__init__()
        self.pos = list(pos)
        print(inportInfo)
        self.window=inportInfo.new_window
        self.acidGroup=inportInfo.acidGroup 
        self.baseGroup=inportInfo.baseGroup
        self.imgApp=imagApp
        self.width = width
        self.height = height
        self.capacity = capacity
        self.current_liquid_level = 0
        self.color = (200, 200, 200)
        self.liquid_color = (0, 0, 255)
        self.dragging = False
        self.permeable = False
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 100))  # Transparent background
        collector_image = pygame.image.load(self.imgApp).convert_alpha()  # Load collector image
        collector_image = pygame.transform.scale(collector_image, (width, height))  # Scale image to collector size
        self.image.blit(collector_image, (0, 0))  # Blit image onto collector surface
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self):
        self.rect.topleft = self.pos
        self.window.blit(self.image, self.rect.topleft)
        if self.current_liquid_level > 0:
            liquid_rect = pygame.Rect(self.rect.left, self.rect.bottom - (self.height * self.current_liquid_level / self.capacity), self.width, self.height * self.current_liquid_level / self.capacity)
            pygame.draw.rect(self.window, self.liquid_color, liquid_rect)

    def add_liquid(self, chemical):
        
        self.current_liquid_level += 1  # Increment proportional to particle size
        if chemical.name == "H2SO4" or chemical.name == "HCL" or chemical.name == "NaOH":
            self.liquid_color = chemical.color
        if self.current_liquid_level > self.capacity:
            self.current_liquid_level = self.capacity
                
    def mix_chemicals(self, chemical):
        # Handle mixing logic here
              
                if chemical.name =="H2SO4":
                    for base in self.baseGroup:
                        if pygame.sprite.collide_rect(chemical.name, base):
                            
                            self.neutralize(base)
                if chemical.name == "NaOH":
                    for acid in self.acidGroup:
                        if pygame.sprite.collide_rect(self, acid):
                            self.neutralize(chemical)
            
    def neutralize(self, chemical):
                if chemical.name == "NaOH":
                    needed_acid_volume = self.neutralization("H2SO4", chemical.amount, chemical.conc, self.current_liquid_level)
                    if self.current_liquid_level >= needed_acid_volume:
                        self.current_liquid_level -= needed_acid_volume
                    else:
                        self.current_liquid_level = 0
   
    def dilution(originalVol, volumeOfWater):
                C1 = 0.1
                V1 = originalVol
                V2 = V1 + volumeOfWater
                C2 = (C1 * V1) / V2
                return C2

    def neutralization(nameAcid, vBase, concentrationBase, concentrationOfAcid):
                if nameAcid == "H2SO4":
                    nBase = 2
                    nAcid = 1
                    VA = (concentrationBase * vBase * nAcid) / (concentrationOfAcid * nBase)
                    return VA
                elif nameAcid == "HCL":
                    nBase = 1
                    nAcid = 1
                    VA = (concentrationBase * vBase * nAcid) / (concentrationOfAcid * nBase)
                    return VA

class SolidIndicator(pygame.sprite.Sprite):
    def __init__(self, pos, name,window):
        super().__init__()
        self.name = name
        self.window=window
        self.pos = list(pos)
        self.dragging = False
        self.original_image = pygame.Surface([20, 20], pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 0, 0) if name == "redLitmus" else (0, 0, 255), [0, 0, 20, 20])
        self.image = self.original_image.copy()  # Start with original color
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos
        self.window.blit(self.image, self.rect.topleft)

    def change_color(self, new_color):
        self.image = pygame.Surface([20, 20], pygame.SRCALPHA)
        pygame.draw.rect(self.image, new_color, [0, 0, 20, 20])




