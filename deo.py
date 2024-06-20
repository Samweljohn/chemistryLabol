
import pygame
from neutralization import *
import sys

pygame.init()
background_image = pygame.image.load("Bg.jpg")  # Replace "background.jpg" with your image file path

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chemistry Lab Simulator")
clock = pygame.time.Clock()


            # Load background image

            # Font settings
font = pygame.font.SysFont(None, 24)

            # Dropdown menu items
files_menu_items = ["Home", "New", "Open", "Info", "Save", "Save As", "Close", "Feedback", "Options"]
settings_menu_items = ["Language", "Privacy", "Security", "Display", "Text Format"]
updates_menu_items = ["Check for Updates", "Download Updates", "Install Updates"]
help_menu_items = ["Links", "Contact Support", "Tutorials"]
practicals_menu_items = ["Qualitative", "Quantitative"]

            # Dropdown menu state
files_menu_open = False
settings_menu_open = False
updates_menu_open = False
help_menu_open = False
practicals_menu_open = False

current_menu = None



# Function to open a new window with the specified header
class mainWindow:
            def __init__(self):
            
                self.new_window= pygame.display.set_mode((WIDTH, 1000), pygame.RESIZABLE)
             
                self.HCLContainer = ChemicalContainer((5, 5), (255, 0, 0), "HCL",self.new_window)
                self.H2SO4Container = ChemicalContainer((300, 300), (0, 255, 0), "H2SO4",self.new_window)
                self.NaOHContainer = ChemicalContainer((500, 300), (0, 0, 255), "NaOH",self.new_window)
                self.baseGroup = pygame.sprite.Group()
                self.baseGroup.add(self.NaOHContainer)
                self.acidGroup = pygame.sprite.Group()
                self.acidGroup.add(self.HCLContainer,self.H2SO4Container)
                self.chemicalContainers = pygame.sprite.Group()
                self.chemicalContainers.add(self.HCLContainer, self.H2SO4Container, self.NaOHContainer)

                self.water = WaterParticle((350, 260),self)
                self.pipette = LiquidCollector((1, 230), 20, 80, 25,"concoflask.jpeg",self)
                self.burette = LiquidCollector((1, 280), 20, 80, 50,"secondbeeker.jpg",self)
                self.beaker = LiquidCollector((1, 280), 250, 300, 50,"secondbeeker.jpg",self)
                self.allCollectors = pygame.sprite.Group()
                self.allCollectors.add(self.pipette, self.burette, self.beaker)

                self.POP = LiquidIndicator((950, 450), (255, 0, 255), "POP",self.new_window)
                self.MO = LiquidIndicator((650, 350), (176, 0, 0), "MO",self.new_window)
                self.allLiquidIndicators = pygame.sprite.Group()
                self.allLiquidIndicators.add(self.POP, self.MO)

                self.litmusPaper = pygame.sprite.Group()
                self.blueLitmusPaper = SolidIndicator((150, 500), "blueLitmus",self.new_window)
                self.redLitmusPaper = SolidIndicator((200, 500), "redLitmus",self.new_window)
                self.litmusPaper.add(self.blueLitmusPaper, self.redLitmusPaper)

                self.particles = pygame.sprite.Group()

                self.dragging_sprite = None
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

     
            def draw_dropdown_menu(self,x, y, label, items, menu_open):
                global current_menu
                
                # Draw menu label
                label_surface = font.render(label, True, BLACK)
                screen.blit(label_surface, (x, y))

                # Draw menu items if menu is open
                if menu_open:
                    item_height = 25
                    for i, item in enumerate(items):
                        item_y = y + (i + 1) * item_height
                        item_surface = font.render(item, True, BLACK)
                        screen.blit(item_surface, (x, item_y))
                    
                    current_menu = label

                # # Highlight the selected menu
                # if current_menu == label:
                #     pygame.draw.rect(screen, GRAY, (x, y, 100, 25), 2)  # Highlight the selected menu label

            def draw_feedback_area(self,window, x, y, width, height):
                    pygame.draw.rect(window, GRAY, (x, y, width, height))
                    pygame.draw.rect(window, BLACK, (x, y, width, height), 2)
                    font = pygame.font.SysFont(None, 20)
                    text_surface = font.render("Feedback Area", True, BLACK)
                    window.blit(text_surface, (x + 10, y + 10))

                    # Make feedback area writable
                    input_rect = pygame.Rect(x + 10, y + 40, width - 20, height - 100)
                    pygame.draw.rect(window, WHITE, input_rect)
                    pygame.draw.rect(window, BLACK, input_rect, 2)

                    # Draw text input
                    input_text = ''  # Initialize input text
                    font = pygame.font.Font(None, 32)
                    text_surface = font.render(input_text, True, BLACK)
                    window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

                    # Draw print and submit buttons
                    print_button = font.render("Print", True, BLACK)
                    submit_button = font.render("Submit", True, BLACK)
                    print_button_rect = print_button.get_rect(topleft=(x + 10, input_rect.bottom + 20))
                    submit_button_rect = submit_button.get_rect(topleft=(print_button_rect.right + 20, input_rect.bottom + 20))
                    window.blit(print_button, print_button_rect)
                    window.blit(submit_button, submit_button_rect)

                    # Capture user input
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                input_text = input_text[:-1]
                            elif event.key == pygame.K_RETURN:
                                print("User Feedback:", input_text)
                                input_text = ''
                                
            def open_new_window(self,header):
                # Set up the new window
                
                pygame.display.set_caption(header)

                # Main loop for the new window
                running = True
                while running:
                    screen.fill((0, 255, 255))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                for sprite in self.chemicalContainers.sprites() + self.allCollectors.sprites() + self.allLiquidIndicators.sprites() + self.litmusPaper.sprites():
                                    if sprite.rect.collidepoint(event.pos):
                                        sprite.dragging = True
                                        self.dragging_sprite = sprite
                            elif event.button == 3:
                                for container in self.chemicalContainers.sprites():
                                    if container.rect.collidepoint(event.pos):
                                        particle = container.release_particle()
                                        self.particles.add(particle)
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                if self.dragging_sprite:
                                    self.dragging_sprite.dragging = False
                                    self.dragging_sprite = None
                        elif event.type == pygame.MOUSEMOTION:
                            if self.dragging_sprite:
                                self.dragging_sprite.pos = list(event.pos)

                    self.particles.update()
                    self.chemicalContainers.update()
                    self.litmusPaper.update()
                    self.allCollectors.update()
                    self.allLiquidIndicators.update()

                    for collector in self.allCollectors:
                        collector.update()
                        for particle in self.particles:
                            if pygame.sprite.collide_rect(collector, particle):
                                
                                collector.add_liquid(particle)
                                self.particles.remove(particle)

                    for indicator in self.allLiquidIndicators:
                        indicator.update()
                        
                    for litmus in self.litmusPaper:
                        for particle in self.particles:
                            if pygame.sprite.collide_rect(litmus, particle):
                                if litmus.name == "blueLitmus" and particle.name in ["HCL", "H2SO4"]:
                                    litmus.change_color((255, 0, 0))  # Change to red in acid
                                elif litmus.name == "redLitmus" and particle.name == "NaOH":
                                    litmus.change_color((0, 0, 255))  # Change to blue in base

                  
                    clock.tick(60)
                    # self.neutralization.part.draw()
                    self.draw_feedback_area(self.new_window, self.new_window.get_width() - 400, 50, 350, self.new_window.get_height() - 100)
                    # self.draw_feedback_area(new_window, new_window.get_width() - 400, 50, 350, new_window.get_height() - 150)

                    pygame.display.flip()

                pygame.quit()
                sys.exit()

            # Screen dimensions


winMain=mainWindow()
        # Main loop
running = True
while running:
    screen.fill(WHITE)

    # Blit background image
    screen.blit(background_image, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if dropdown menus are clicked to toggle their state
                if 100 <= event.pos[0] <= 200 and 50 <= event.pos[1] <= 75:
                    files_menu_open = not files_menu_open
                    settings_menu_open = False
                    updates_menu_open = False
                    help_menu_open = False
                    practicals_menu_open = False
                elif 220 <= event.pos[0] <= 320 and 50 <= event.pos[1] <= 75:
                    settings_menu_open = not settings_menu_open
                    files_menu_open = False
                    updates_menu_open = False
                    help_menu_open = False
                    practicals_menu_open = False
                elif 340 <= event.pos[0] <= 440 and 50 <= event.pos[1] <= 75:
                    updates_menu_open = not updates_menu_open
                    files_menu_open = False
                    settings_menu_open = False
                    help_menu_open = False
                    practicals_menu_open = False
                elif 460 <= event.pos[0] <= 560 and 50 <= event.pos[1] <= 75:
                    help_menu_open = not help_menu_open
                    files_menu_open = False
                    settings_menu_open = False
                    updates_menu_open = False
                    practicals_menu_open = False
                elif 580 <= event.pos[0] <= 700 and 50 <= event.pos[1] <= 75:
                    practicals_menu_open = not practicals_menu_open
                    files_menu_open = False
                    settings_menu_open = False
                    updates_menu_open = False
                    help_menu_open = False
                # Check if "Qualitative" or "Quantitative" is clicked to open new window
                elif 580 <= event.pos[0] <= 700 and 100 <= event.pos[1] <= 125:
                    if event.pos[1] <= 112.5:
                        winMain.open_new_window("Welcome to Qualitative Window")
                    else:
                        winMain.open_new_window("Welcome to Quantitative Window")

    # Draw header and dropdown menus
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 30))
    winMain.draw_dropdown_menu(100, 50, "Files", files_menu_items, files_menu_open)
    winMain.draw_dropdown_menu(220, 50, "Settings", settings_menu_items, settings_menu_open)
    winMain.draw_dropdown_menu(340, 50, "Updates", updates_menu_items, updates_menu_open)
    winMain.draw_dropdown_menu(460, 50, "Help", help_menu_items, help_menu_open)
    winMain.draw_dropdown_menu(580, 50, "Types of Practicals", practicals_menu_items, practicals_menu_open)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
