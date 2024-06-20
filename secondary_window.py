
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GAS_COLOR = (200, 200, 200)
ORIGINALBOX_SMELL = False

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bunsen Burner Simulation")

# Load images
burner_images = [pygame.image.load("burnenburner.png"), pygame.image.load("fired.png")]
metal_images = {
    'Na': pygame.image.load("11.png"),
    'Fe': pygame.image.load("12.png"),
    'Cu': pygame.image.load("13.png")
}

class Qualitative:
    def __init__(self, mainWindow):
        self.window = mainWindow.new_window_qul
        self.beaker = LiquidCollectorQ((600, 400), 200, 300, 50, "beekerr.png",  self.window, -90, -105, 190, 170)
        self.particles = mainWindow.particles
        self.HCLContainer = ChemicalContainerQ((30, 50), 94, 56, (255, 0, 0), "HCL", self.window, "h2so4.png", 3, 7, 43, 89, "acid")
        self.KmnO4Container = ChemicalContainerQ((30, 100), 94, 56, (255, 0, 0), "kmo4", self.window, "h2so4.png", 3, 7, 43, 89, "NOTacid")
        self.mainWindow = mainWindow
        self.feedback_text = mainWindow.feedback_text
        self.window.fill((0, 0, 0))
        self.dragging_sprite = None
        self.gas_particles = pygame.sprite.Group()  # Group to manage gas particles

    def check_collision(self, burner, metal):
        if burner.rect.collidepoint(metal.rect.center):
            if burner.image_index != 0:  # Burner is on fire
                if metal.metal_type == 'Na':
                    return YELLOW
                elif metal.metal_type == 'Fe':
                    return GREEN
                elif metal.metal_type == 'Cu':
                    return BLUE
        return None

    def handle_smell(self):
        self.font = pygame.font.Font(None, 36)
        self.chlorine_smell_button = pygame.Rect(500, 20, 150, 50)
        if not ORIGINALBOX_SMELL:
            pygame.draw.rect(self.window, (0, 0, 0), self.chlorine_smell_button)
            self.chlorine_smell_text = self.font.render("Smell", True, (255, 255, 255))
            self.window.blit(self.chlorine_smell_text, (self.chlorine_smell_button.x + 20, self.chlorine_smell_button.y + 10))
        else:
            pygame.draw.rect(self.window, (255, 255, 0), self.chlorine_smell_button)
            self.chlorine_smell_text = self.font.render("irritant", True, (255, 255, 255))
            self.window.blit(self.chlorine_smell_text, (self.chlorine_smell_button.x + 20, self.chlorine_smell_button.y + 10))

    def main(self):
        clock = pygame.time.Clock()
        burner = BunsenBurner(100, 70)
        metals = [
            Metal((5, 150), 100, 100, 'Na',"NaCl"),
            Metal((5, 270), 100, 100, 'Fe',"FeSo4"),
            Metal((5, 400), 100, 100, 'Cu',"CuSO4")
        ]
        selected_metal = None
        dragging = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if burner.rect.collidepoint(event.pos):
                            burner.toggle_fire()
                        elif self.HCLContainer.rect.collidepoint(event.pos):
                            self.HCLContainer.dragging = True
                        elif self.KmnO4Container.rect.collidepoint(event.pos):
                            self.KmnO4Container.dragging = True
                        elif self.beaker.rect.collidepoint(event.pos):
                            self.beaker.dragging = True
                        else:
                            for metal in metals:
                                if metal.rect.collidepoint(event.pos):
                                    selected_metal = metal
                                    selected_metal.dragging = True
                                    offset_x = selected_metal.rect.x - event.pos[0]
                                    offset_y = selected_metal.rect.y - event.pos[1]
                                    break
                    elif event.button == 3:
                        if self.HCLContainer.rect.collidepoint(event.pos):
                            particle = self.HCLContainer.release_particle()
                            self.particles.add(particle)
                        elif self.KmnO4Container.rect.collidepoint(event.pos):
                            particle = self.KmnO4Container.release_particle()
                            self.particles.add(particle)
                elif event.type == pygame.MOUSEMOTION:
                    if self.beaker.dragging:
                        self.beaker.pos = list(event.pos)
                    elif self.HCLContainer.dragging:
                        self.HCLContainer.pos = list(event.pos)
                    elif self.KmnO4Container.dragging:
                        self.KmnO4Container.pos = list(event.pos)
                    elif selected_metal and selected_metal.dragging:
                        selected_metal.rect.x = event.pos[0] + offset_x
                        selected_metal.rect.y = event.pos[1] + offset_y
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                    self.beaker.dragging = False
                    self.HCLContainer.dragging = False
                    self.KmnO4Container.dragging = False
                    if selected_metal:
                        selected_metal.dragging = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.feedback_text = self.feedback_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.feedback_text += "\n"
                    elif event.unicode.isprintable():
                        self.feedback_text += event.unicode

            if dragging and selected_metal:
                selected_metal.rect.center = pygame.mouse.get_pos()

            flame_color = None
            for particle in self.particles:
                if pygame.sprite.collide_rect(self.beaker, particle):
                    self.beaker.add_liquid(particle)
                    self.particles.remove(particle)
                    if isinstance(particle, PotPermangernate) and any(isinstance(p, ChemicalsQ) for p in self.beaker.liquid_particles):
                        gas_particle = GasParticle(particle.pos, self.mainWindow, self.window)
                        self.gas_particles.add(gas_particle)
                        global ORIGINALBOX_SMELL
                        ORIGINALBOX_SMELL = True

            for metal in metals:
                flame_color = self.check_collision(burner, metal)
                if flame_color:
                    break

            self.window.fill(WHITE)
            self.handle_smell()
            burner.draw(self.window)
            self.particles.update()
            self.gas_particles.update()  # Update gas particles
            self.gas_particles.draw(self.window)  # Draw gas particles
            self.beaker.update()
            for metal in metals:
                metal.draw(self.window)
            self.mainWindow.draw_feedback_area(self.window, self.window.get_width() - 400, 50, 350, self.window.get_height() - 100, "qulitative")
            if flame_color:
                pygame.draw.rect(self.window, flame_color, (350, 200, 100, 50))  # Draw the colored flame
            self.beaker.update()
            self.HCLContainer.update()
            self.KmnO4Container.update()

            pygame.display.flip()
            clock.tick(30)

class BunsenBurner(Qualitative):
    def __init__(self, x, y):
        self.images = burner_images
        self.image_index = 0  # Start with no fire
        self.rect = self.images[self.image_index].get_rect(topleft=(290, 380))

    def toggle_fire(self):
        self.image_index = 1 - self.image_index  # Toggle between 0 and 1

    def draw(self, screen):
        screen.blit(self.images[self.image_index], (290, 380))


class Metal(Qualitative):
    def __init__(self, pos, width, height, metal_type,name):
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.Metal_image = metal_images[metal_type]
        self.image = pygame.transform.scale(self.Metal_image, (width, height))
        font = pygame.font.Font(None, 24)
        self.label = font.render(name, True, (255, 0, 0))
        self.image.blit(self.image, (width,height))
        self.image.blit(self.label, (5, 5))
        self.rect = self.image.get_rect(topleft=pos)
        self.metal_type = metal_type
        self.dragging = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class PotPermangernate(pygame.sprite.Sprite):
    def __init__(self, pos,window):
        super().__init__() 
        self.screen=window
        self.pos = list(pos)
        self.color = PURPLE
        self.name = "kmno4"
        self.amount = 1
        self.gravity = 0.1
        self.dragging = False
        self.vel = [random.uniform(-0.5, 0.5), random.uniform(-2, -1)]
        self.size = random.randint(2, 4)
        self.image = pygame.Surface([self.size, self.size], pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), self.size // 2)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if not self.dragging:
            self.move()
        self.rect.center = self.pos
        self.screen.blit(self.image, self.rect.topleft)

    def move(self):
        self.vel[1] -= self.gravity
        self.pos[0] -= self.vel[0]
        self.pos[1] -= self.vel[1]


class GasParticle(pygame.sprite.Sprite):
    def __init__(self, pos, main_window, window):
        super().__init__()
        self.main_window = main_window
        self.window = window
        self.color = GAS_COLOR
        self.size = 5
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = [random.uniform(-0.5, 0.5), random.uniform(-2, -1)]

    def update(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        if self.rect.y < 0:  # Gas particles move upward, remove if out of screen
            self.kill()



class ChemicalsQ(pygame.sprite.Sprite):
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


class ChemicalContainerQ(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, color, name ,window,image_path,fixHeightP,fixWidthP,scaleWidth,scaleHeight,chemicalCartegory):
        super().__init__()
        self.pos = list(pos)
        self.type=chemicalCartegory
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
        self.label = font.render(name, True, (255, 0, 0))
        collector_image = pygame.image.load(image_path).convert_alpha()
        collector_image = pygame.transform.scale(collector_image, (self.width+self.scaleAdditionWidth, self.height+self.scaleAdditionHeight))
        self.image.blit(collector_image, (self.fixWidthP,self.fixHeightP))
        self.image.blit(self.label, (5, 5))
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self):
        self.rect.center = self.pos
        self.window.blit(self.image, self.rect.topleft)
        
    def release_particle(self):
       if self.type=="acid":
           return  PotPermangernate(self.rect.center,self.window)
       else:
           return  ChemicalsQ(self.rect.center, self.color, 1, 0.1, self.label,self.window)

class LiquidCollectorQ(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, capacity, image_path, window, fixHeightP, fixWidthP, scaleWidth, scaleHeight):
        super().__init__()
        self.pos = list(pos)
        self.width = width
        self.window = window
        self.fixHeightP = fixHeightP
        self.fixWidthP = fixWidthP
        self.scaleAdditionHeight = scaleHeight
        self.scaleAdditionWidth = scaleWidth
        self.height = height
        self.capacity = capacity
        self.current_liquid_level = 0
        self.hcl_volume = 0
        self.h2so4_volume = 0
        self.naoh_volume = 0
        self.color = (200, 200, 200)
        self.liquid_color = (0, 0, 255)
        self.dragging = False
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 100))
        collector_image = pygame.image.load(image_path).convert_alpha()
        collector_image = pygame.transform.scale(collector_image, (self.width + self.scaleAdditionWidth, self.height + self.scaleAdditionHeight))
        self.image.blit(collector_image, (self.fixWidthP, self.fixHeightP))
        self.rect = self.image.get_rect(topleft=self.pos)
        self.liquid_particles = []  # Add this line

    def update(self):
        self.rect.topleft = self.pos
        self.window.blit(self.image, self.rect.topleft)
        if self.current_liquid_level > 0:
            liquid_rect = pygame.Rect(self.rect.left, self.rect.bottom - (self.height * self.current_liquid_level / self.capacity), self.width, self.height * self.current_liquid_level / self.capacity)
            pygame.draw.rect(self.window, self.liquid_color, liquid_rect)
            font = pygame.font.Font(None, 18)
            volume_text = font.render(f"{self.current_liquid_level:.1f} ml", True, (255, 0, 0))
            self.window.blit(volume_text, (self.rect.left, self.rect.top - 30))

    def add_liquid(self, chemical):
        self.current_liquid_level += chemical.amount * 0.1
        self.liquid_particles.append(chemical)  # Add this line to keep track of particles
        if chemical.name == "HCL":
            self.hcl_volume += chemical.amount * 0.1
        elif chemical.name == "kmo4":
            self.h2so4_volume += chemical.amount * 0.1
        elif chemical.name == "NaOH":
            self.naoh_volume += chemical.amount * 0.1
      
        if self.current_liquid_level > self.capacity:
            self.current_liquid_level = self.capacity


