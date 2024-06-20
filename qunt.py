import random
import pygame

pygame.init()
rectanglepertical=True

# Screen dimensions
WIDTH, HEIGHT = 1300, 1000
MOLAR_MASS_NaOH = 40
MOLAR_MASS_KOH = 57
MOLAR_MASS_CaOH = 58
MOLAR_MASS_NH4OH = 36
MOLAR_MASS_HCL = 37
MOLAR_MASS_HNO3 = 65
MOLAR_MASS_H2SO4 = 98
CONC_HCL = 0.1
CONC_HNO3 = 0.1
CONC_NaOH = 0.1
CONC_CaOH = 0.1
CONC_NH4OH = 0.1
CONC_KOH = 0.1
CONC_H2SO4 = 0.1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chemical Reactions and Liquid Simulations")
clock = pygame.time.Clock()

class Chemicals(pygame.sprite.Sprite):
    def __init__(self, pos, color, amount, concentration, name,window):
        super().__init__()
        self.pos = list(pos)
        self.color = color
        self.window=window
        self.name = name
        self.amount = amount
        self.concentration = concentration
        self.gravity = 0.1
        self.dragging = False
        self.vel = [random.uniform(-0.5, 0.5), random.uniform(-2, -1)]
        self.size = random.randint(2, 4)
        self.image = pygame.Surface([6, 12], pygame.SRCALPHA)
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
    def __init__(self, pos, width, height, color, name ,window,image_path,fixHeightP,fixWidthP,scaleWidth,scaleHeight):
        super().__init__()
        self.pos = list(pos)

        self.window=window
        self.color = color
        self.name = name
        self.window=window
        self.dragging = False
        self.image = pygame.Surface([100, 90], pygame.SRCALPHA)
        self.height=height
        self.width=width
        self.fixHeightP=fixHeightP
        self.fixWidthP=fixWidthP
        self.scaleAdditionHeight=scaleHeight
        self.scaleAdditionWidth=scaleWidth
        font = pygame.font.Font(None, 24)
        label = font.render(name, True, (255, 0, 0))
        collector_image = pygame.image.load(image_path).convert_alpha()
        collector_image = pygame.transform.scale(collector_image, (self.width+self.scaleAdditionWidth, self.height+self.scaleAdditionHeight))
        self.image.blit(collector_image, (self.fixWidthP,self.fixHeightP))
        self.image.blit(label, (5, 5))
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self):
        self.rect.center = self.pos
        self.window.blit(self.image, self.rect.topleft)
        
    def release_particle(self):
        if rectanglepertical==True:
           return Chemicals(self.rect.center, self.color, 1, 0.1, self.name,self.window)
        else:
           return  (self.rect.center, self.color, 1, 0.1, self.name,self.window)
 
class WaterParticle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = list(pos)
        self.dragging = False
        imageOfWaterContainer = pygame.image.load("1.png").convert_alpha()
        self.texture = pygame.transform.scale(imageOfWaterContainer, (200, 200))
        self.rect = self.texture.get_rect(center=self.pos)
      
    def update(self):
        self.rect.center = self.pos
        screen.blit(self.texture, self.rect.topleft)

class LiquidIndicator(pygame.sprite.Sprite):
    def __init__(self, pos, color,image, label,width,height,window):
        
        super().__init__()
        self.pos = list(pos)
        self.height=height
        self.width=width
        self.window=window
        self.color = color
        self.window=window
        self.label = label
        self.dragging = False
        self.image = pygame.Surface([90, 120], pygame.SRCALPHA)
        # pygame.draw.rect(self.image,(255,255,255), [0, 0, 50, 50])
        font = pygame.font.Font(None, 24)
        cover_image = pygame.image.load(image).convert_alpha()
        cover_image = pygame.transform.scale(cover_image, (self.width+70, self.height+85))
        label = font.render(self.label, True, (255, 0, 0))
        
        self.image.blit(cover_image, (-25, -5))
        self.image.blit(label, (0, 0))
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos
        self.window.blit(self.image, self.rect.topleft)

    def release_particle(self):
        return Chemicals(self.rect.center, self.color, 1, 0.1, self.label,self.window)

class LiquidCollector(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, capacity, image_path,window,fixHeightP,fixWidthP,scaleWidth,scaleHeight):
        super().__init__()
        self.pos = list(pos)
        self.width = width
        self.window=window
        self.fixHeightP=fixHeightP
        self.fixWidthP=fixWidthP
        self.scaleAdditionHeight=scaleHeight
        self.scaleAdditionWidth=scaleWidth
        self.height = height
        self.capacity = capacity
        self.current_liquid_level = 0
        self.hcl_volume = 0
        self.h2so4_volume = 0
        self.hno3_volume = 0
        self.naoh_volume = 0
        self.koh_volume = 0
        self.caoh_volume = 0
        self.nh4oh_volume = 0
        self.has_indicator = False
        self.indicator_color = (0, 0, 0)
        self.color = (200, 200, 200)
        self.liquid_color = (0, 0, 255)
        self.dragging = False
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 100))
        collector_image = pygame.image.load(image_path).convert_alpha()
        collector_image = pygame.transform.scale(collector_image, (self.width+self.scaleAdditionWidth, self.height+self.scaleAdditionHeight))
        self.image.blit(collector_image, (self.fixWidthP,self.fixHeightP))
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self):
        self.rect.topleft = self.pos
        self.window.blit(self.image, self.rect.topleft)
        if self.current_liquid_level > 0:
            liquid_rect = pygame.Rect(self.rect.left, self.rect.bottom - (self.height * self.current_liquid_level / self.capacity), self.width, self.height * self.current_liquid_level / self.capacity)
            pygame.draw.rect(self.window, self.liquid_color, liquid_rect)
            font = pygame.font.Font(None, 18)
            volume_text = font.render(f"{self.current_liquid_level:.1f} ml", True, (255, 0, 0))
            self.window.blit(volume_text, (self.rect.left, self.rect.top -30))

    def add_liquid(self, chemical):
        self.current_liquid_level += chemical.amount * 0.1
        if chemical.name == "HCL":
            self.hcl_volume += chemical.amount * 0.1
        elif chemical.name == "HNO3":
            self.hno3_volume += chemical.amount * 0.1
        elif chemical.name == "H2SO4":
            self.h2so4_volume += chemical.amount * 0.1
        elif chemical.name == "NaOH":
            self.naoh_volume += chemical.amount * 0.1
        elif chemical.name == "KOH":
            self.koh_volume += chemical.amount * 0.1
        elif chemical.name == "NH4OH":
            self.nh4oh_volume += chemical.amount * 0.1
        elif chemical.name == "CaOH":
            self.caoh_volume += chemical.amount * 0.1
        self.check_neutralization()

        if self.current_liquid_level > self.capacity:
            self.current_liquid_level = self.capacity

    def add_indicator(self, indicator):
        if not self.has_indicator:
            self.has_indicator = True
            self.indicator_color = indicator.color
            self.update_indicator_color()

    def update_indicator_color(self):
        if (self.naoh_volume > 0 or self.koh_volume > 0 or self.caoh_volume > 0 or self.nh4oh_volume > 0 ) and self.has_indicator:
            if self.indicator_color == (255, 0, 255):  # Phenolphthalein
                self.liquid_color = (255, 0, 255)  # Pink in base
            elif self.indicator_color == (176, 0, 0):  # Methyl orange
                self.liquid_color = (255, 165, 0)  # Orange in base

    def check_neutralization(self):
        # Check neutralization for HCl with NaOH, KOH, CaOH, NH4OH
        acid_needed_for_base_hcl_naoh = self.calculate_acid_needed(self.naoh_volume, "HCL")
        acid_needed_for_base_hcl_koh = self.calculate_acid_needed(self.koh_volume, "HCL")
        acid_needed_for_base_hcl_caoh = self.calculate_acid_needed(self.caoh_volume, "HCL")
        acid_needed_for_base_hcl_nh4oh = self.calculate_acid_needed(self.nh4oh_volume, "HCL")
        
        # Check neutralization for H2SO4 with NaOH, KOH, CaOH, NH4OH
        acid_needed_for_base_h2so4_naoh = self.calculate_acid_needed(self.naoh_volume, "H2SO4")
        acid_needed_for_base_h2so4_koh = self.calculate_acid_needed(self.koh_volume, "H2SO4")
        acid_needed_for_base_h2so4_caoh = self.calculate_acid_needed(self.caoh_volume, "H2SO4")
        acid_needed_for_base_h2so4_nh4oh = self.calculate_acid_needed(self.nh4oh_volume, "H2SO4")

        # Check neutralization for HNO3 with NaOH, KOH, CaOH, NH4OH
        acid_needed_for_base_hno3_naoh = self.calculate_acid_needed(self.naoh_volume, "HNO3")
        acid_needed_for_base_hno3_koh = self.calculate_acid_needed(self.koh_volume, "HNO3")
        acid_needed_for_base_hno3_caoh = self.calculate_acid_needed(self.caoh_volume, "HNO3")
        acid_needed_for_base_hno3_nh4oh = self.calculate_acid_needed(self.nh4oh_volume, "HNO3")
        
        
        # Check if any acid volume is greater than 0 and within the defined range for neutralization
        if (self.hcl_volume > 0 and 
            (self.hcl_volume <= acid_needed_for_base_hcl_naoh or 
            self.hcl_volume <= acid_needed_for_base_hcl_koh or 
            self.hcl_volume <= acid_needed_for_base_hcl_caoh or 
            self.hcl_volume <= acid_needed_for_base_hcl_nh4oh)):
            self.liquid_color = (0, 255, 0)  # Green if neutralized
        elif (self.h2so4_volume > 0 and 
            (self.h2so4_volume <= acid_needed_for_base_h2so4_naoh or 
            self.h2so4_volume <= acid_needed_for_base_h2so4_koh or 
            self.h2so4_volume <= acid_needed_for_base_h2so4_caoh or 
            self.h2so4_volume <= acid_needed_for_base_h2so4_nh4oh)):
            self.liquid_color = (0, 255, 0)  # Green if neutralized
        elif (self.hno3_volume > 0 and (
            self.hno3_volume <= acid_needed_for_base_hno3_naoh or 
            self.hno3_volume <= acid_needed_for_base_hno3_koh or 
            self.hno3_volume <= acid_needed_for_base_hno3_caoh or 
            self.hno3_volume <= acid_needed_for_base_hno3_nh4oh )):
            self.liquid_color = (0, 255, 0)  # Green if neutralized
        else:
            self.update_indicator_color()

    def calculate_acid_needed(self, base_volume, acid_type):
        if acid_type == "HCL":
            # Use the defined range logic here for HCl
            if base_volume <= 5:
                return 5 * (base_volume / 5)
            elif base_volume <= 10:
                return 10 * (base_volume / 10)
            elif base_volume <= 15:
                return 15 * (base_volume / 15)
            elif base_volume <= 20:
                return 20 * (base_volume / 20)
            elif base_volume <= 25:
                return 25 * (base_volume / 25)
            else:
                return base_volume  # Default to a 1:1 ratio for simplicity
        elif acid_type == "HNO3":
            # Use the defined range logic here for HCl
            if base_volume <= 5:
                return 5 * (base_volume / 5)
            elif base_volume <= 10:
                return 10 * (base_volume / 10)
            elif base_volume <= 15:
                return 15 * (base_volume / 15)
            elif base_volume <= 20:
                return 20 * (base_volume / 20)
            elif base_volume <= 25:
                return 25 * (base_volume / 25)
            else:
                return base_volume
        elif acid_type == "H2SO4":
            # Use the defined range logic here for H2SO4
            if base_volume <= 5:
                return 2.5 * (base_volume / 5)
            elif base_volume <= 10:
                return 5 * (base_volume / 10)
            elif base_volume <= 15:
                return 7.5 * (base_volume / 15)
            elif base_volume <= 20:
                return 10 * (base_volume / 20)
            elif base_volume <= 25:
                return 12.5 * (base_volume / 25)
            else:
                return base_volume / 2  # Default to a 1:2 ratio for simplicity

    def reset(self):
        self.hcl_volume = 0
        self.h2so4_volume = 0
        self.hno3_volume = 0
        self.naoh_volume = 0
        self.koh_volume = 0
        self.caoh_volume = 0
        self.nh4oh_volume = 0
        self.current_liquid_level = 0
        self.has_indicator = False
        self.liquid_color = (0, 0, 255)

class SolidIndicator(pygame.sprite.Sprite):
    def __init__(self, pos, name,window):
        super().__init__()
        self.name = name
        self.window=window
        self.pos = list(pos)
        self.dragging = False
        self.original_image = pygame.Surface([90, 100], pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 0, 0) if name == "redLitmus" else (0, 0, 255), [0, 0, 30, 100])
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos
        self.window.blit(self.image, self.rect.topleft)

    def change_color(self, new_color):
        self.image = pygame.Surface([50, 110], pygame.SRCALPHA)
        pygame.draw.rect(self.image, new_color, [0, 0, 30, 100])

    def reset(self):
        self.image = self.original_image.copy()

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
