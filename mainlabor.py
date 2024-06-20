
import pygame
from qunt import *
from secondary_window import *
import sys

pygame.init()

# Function to open a new window with the specified header
class mainWindow:
    def __init__(self):
        self.new_window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        simWindow = self.new_window
        self.Chemicals = Chemicals

        self.HCLContainer = ChemicalContainer((45, 50), 94, 56, (255, 0, 0), "HCL", simWindow, "h2so4.png", 3, 7, 43, 89)
        self.HNO3Container = ChemicalContainer((105, 50), 94, 56, (255, 0, 0), "HNO3", simWindow, "h2so4.png", 3, 7, 43, 89)
        self.H2SO4Container = ChemicalContainer((175, 50), 94, 56, (0, 255, 0), "H2SO4", simWindow, "h2so4.png", 3, 7, 43, 89)
        self.NaOHContainer = ChemicalContainer((70, 200), 94, 56, (0, 0, 255), "NaOH", simWindow, "h2so4.png", 3, 7, 43, 89)
        self.KOHContainer = ChemicalContainer((130, 200), 94, 56, (0, 0, 255), "KOH", simWindow, "h2so4.png", 3, 7, 43, 89)
        self.CaOHContainer = ChemicalContainer((190, 200), 94, 56, (0, 0, 255), "CaOH", simWindow, "h2so4.png", 3, 7, 43, 89)
        self.NH4OHContainer = ChemicalContainer((250, 200), 94, 56, (0, 0, 255), "NH4OH", simWindow, "h2so4.png", 3, 7, 43, 89)
        self.chemicalContainers = pygame.sprite.Group()
        self.chemicalContainers.add(self.NaOHContainer, self.KOHContainer, self.CaOHContainer, self.NH4OHContainer, self.HCLContainer, self.HNO3Container, self.H2SO4Container)

        self.water = WaterParticle((30, 250))
        # def __init__(self, pos, width, height, capacity, image_path,window,fixHeightP,fixWidthP,scaleWidth,scaleHeight):

        self.pipette = LiquidCollector((10, 220), 27, 200, 25, "musure.png", simWindow, 0, -60, 120, 26)
        self.burette = LiquidCollector((50, 220), 27, 120, 50, "musure.png", simWindow, 0, -60, 120, 14)
        self.beaker = LiquidCollector((600, 400), 200, 300, 50, "beekerr.png", simWindow, -90, -105, 190, 170)
        self.mesuringCylinder = LiquidCollector((400, 500), 140, 200, 50, "beekerr.png", simWindow, -90, -75, 150, 140)
       
        self.allCollectors = pygame.sprite.Group()
        self.allCollectors.add(self.pipette, self.burette, self.beaker,self.mesuringCylinder)

        self.POP = LiquidIndicator((30, 600), (255, 0, 255), "indicatorimage.png", "POP", 54, 67, simWindow)
        self.MO = LiquidIndicator((90, 600), (176, 0, 0), "indicatorimage.png", "MO", 54, 67, simWindow)
        self.allLiquidIndicators = pygame.sprite.Group()
        self.allLiquidIndicators.add(self.POP, self.MO)

        self.litmusPaper = pygame.sprite.Group()
        self.blueLitmusPaper = SolidIndicator((50, 500), "blueLitmus", simWindow)
        self.redLitmusPaper = SolidIndicator((110, 500), "redLitmus", simWindow)
        self.litmusPaper.add(self.blueLitmusPaper, self.redLitmusPaper)

        self.particles = pygame.sprite.Group()

        # Clear button
        self.font = pygame.font.Font(None, 36)
        self.clear_button = pygame.Rect(700, 20, 150, 50)
        self.clear_text = self.font.render("Clear", True, (255, 255, 255))

        # Smell of Chlorine button
        self.chlorine_smell_button = pygame.Rect(500, 20, 150, 50)
        self.chlorine_smell_text = self.font.render("Smell", True, (255, 255, 255))

        self.dragging_sprite = None

        # Feedback area
        self.feedback_text = ""  # Initialize feedback text storage
        self.feedback_textQ=""
        self.new_window_qul= pygame.display.set_mode((900, 800), pygame.RESIZABLE)
        self.qunt=Qualitative(self)
       
    def open_new_qualy(self, header, menus=None):
        # Set up the new window
    
        pygame.display.set_caption(header)
      
        self.qunt.main()
        

    def open_new_window(self, header, menus=None):
        # Set up the new window
        self.new_window = pygame.display.set_mode((900, 800), pygame.RESIZABLE)
        pygame.display.set_caption(header)

        

        # Main loop for the new window
        running = True
        while running:
            self.new_window.fill((255, 255, 255))

           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.clear_button.collidepoint(event.pos):
                            # Clear all liquids and particles
                            self.pipette.reset()
                            self.burette.reset()
                            self.beaker.reset()
                            self.mesuringCylinder.reset()
                            self.particles.empty()
                            for litmus in self.litmusPaper:
                                litmus.reset()
                        elif self.chlorine_smell_button.collidepoint(event.pos):
                            # Display chlorine smell on the screen
                            font = pygame.font.Font(None, 24)
                            smell_text = font.render("Smell of Chlorine: Irritating, pungent, and suffocating", True, (0, 0, 255))
                            screen.blit(smell_text, (500, 70))
                        else:
                            for sprite in self.chemicalContainers.sprites() + self.allCollectors.sprites() + self.allLiquidIndicators.sprites() + self.litmusPaper.sprites():
                                if sprite.rect.collidepoint(event.pos):
                                    sprite.dragging = True
                                    self.dragging_sprite = sprite
                    elif event.button == 3:
                        for container in self.chemicalContainers.sprites():
                            if container.rect.collidepoint(event.pos):
                                particle = container.release_particle()
                                self.particles.add(particle)
                        for indicator in self.allLiquidIndicators.sprites():
                            if indicator.rect.collidepoint(event.pos):
                                particle = indicator.release_particle()
                                self.particles.add(particle)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.dragging_sprite:
                            self.dragging_sprite.dragging = False
                            self.dragging_sprite = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_sprite:
                        self.dragging_sprite.pos = list(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.feedback_text = self.feedback_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.feedback_text += "\n"
                    elif event.unicode.isprintable():
                        self.feedback_text += event.unicode

            self.particles.update()
            self.chemicalContainers.update()
            self.litmusPaper.update()
            self.allCollectors.update()
            self.allLiquidIndicators.update()

            for collector in self.allCollectors:
                collector.update()
                for particle in self.particles:
                    if pygame.sprite.collide_rect(collector, particle):
                        if isinstance(particle, self.Chemicals) and particle.name in ["POP", "MO"]:
                            collector.add_indicator(particle)
                        else:
                            collector.add_liquid(particle)
                        self.particles.remove(particle)

            for indicator in self.allLiquidIndicators:
                indicator.update()

            for litmus in self.litmusPaper:
                for particle in self.particles:
                    if pygame.sprite.collide_rect(litmus, particle):
                        if litmus.name == "blueLitmus" and particle.name in ["HCL", "HNO3", "H2SO4"]:
                            litmus.change_color((255, 0, 0))  # Change to red in acid
                        elif litmus.name == "redLitmus" and particle.name in ["NaOH", "KOH", "CaOH", "NH4OH"]:
                            litmus.change_color((0, 0, 255))  # Change to blue in base

            pygame.draw.rect(screen, (0, 0, 0), self.clear_button)
            screen.blit(self.clear_text, (self.clear_button.x + 20, self.clear_button.y + 10))

            pygame.draw.rect(screen, (0, 0, 0), self.chlorine_smell_button)
            screen.blit(self.chlorine_smell_text, (self.chlorine_smell_button.x + 20, self.chlorine_smell_button.y + 10))

            self.draw_feedback_area(self.new_window, self.new_window.get_width() - 400, 50, 350, self.new_window.get_height() - 100,"quntitative")
            pygame.display.flip()
            clock.tick(60)

    def draw_menus(self, window, x, y, menus):
        current_x = x
        for menu in menus:
            self.draw_dropdown_menu(window, current_x, y, menu['label'], menu['items'], menu['open'])
            current_x += 120

    def draw_dropdown_menu(self, window, x, y, label, items, menu_open):
        font = pygame.font.SysFont(None, 24)
        label_surface = font.render(str(label), True, (0, 0, 0))  # Convert label to string
        window.blit(label_surface, (x, y))

        if menu_open:
            item_height = 25
            for i, item in enumerate(items):
                item_y = y + (i + 1) * item_height
                item_surface = font.render(item, True, (0, 0, 0))
                window.blit(item_surface, (x, item_y))

    def draw_feedback_area(self, window, x, y, width, height,type_feedback):
        if type_feedback=="qulitative":
            self.feedback_text=self.feedback_textQ
        pygame.draw.rect(window, (200, 200, 200), (x, y, width, height))
        pygame.draw.rect(window, (0, 0, 0), (x, y, width, height), 2)
        font = pygame.font.SysFont(None, 20)
        text_surface = font.render("Feedback Area", True, (0, 0, 0))
        window.blit(text_surface, (x + 10, y + 10))

        input_rect = pygame.Rect(x + 10, y + 40, width - 20, height - 100)
        pygame.draw.rect(window, (255, 255, 255), input_rect)
        pygame.draw.rect(window, (0, 0, 0), input_rect, 2)

        font = pygame.font.SysFont(None, 25)
        feedback_lines = []
        words = self.feedback_text.split(' ')  
        line = ""

        for word in words:
            if '\n' in word:
                parts = word.split('\n')
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:
                        test_line = line + part
                        if font.size(test_line)[0] > input_rect.width:
                            line = test_line + " "
                        else:
                            feedback_lines.append(line)
                            line = part + " "
                    else:
                        test_line = line + part
                        if font.size(test_line)[0] < input_rect.width:
                            feedback_lines.append(test_line)
                        else:
                            feedback_lines.append(line)
                            feedback_lines.append(part)
                        line = ""
            else:
                test_line = line + word + " "
                if font.size(test_line)[0] < input_rect.width:
                    line = test_line
                else:
                    feedback_lines.append(line)
                    line = word + " "
        feedback_lines.append(line)

        y_offset = input_rect.y + 5
        for line in feedback_lines:
            line_surface = font.render(line, True, (0, 0, 0))
            window.blit(line_surface, (input_rect.x + 5, y_offset))
            y_offset += font.get_height()
            if y_offset >= input_rect.bottom:
                break

        font = pygame.font.SysFont(None, 24)
        print_button = font.render("Print", True, (0, 0, 0))
        submit_button = font.render("take note", True, (0, 0, 0))
        print_button_rect = print_button.get_rect(topleft=(x + 10, input_rect.bottom + 20))
        submit_button_rect = submit_button.get_rect(topleft=(print_button_rect.right + 20, input_rect.bottom + 20))
        # window.blit(print_button, print_button_rect)
        window.blit(submit_button, submit_button_rect)

# Screen dimensions
WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chemistry Lab Simulator")
clock = pygame.time.Clock()


# Load background image
background_image = pygame.image.load("Bg.jpg")  
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
menuQuary = pygame.Rect(500, 20, 150, 50)


#-------------------box  for quaritative-------------
font = pygame.font.Font(None, 24)
qlBox= pygame.Surface([200, 50], pygame.SRCALPHA)
rectQnt=qlBox.get_rect()

# screen.blit(rectQnt,(300,400))

textQ=font.render("Quantitative analysis", True, (255, 255, 255))



#-------------------box for quantitative--------------
font = pygame.font.Font(None, 24)
textL=font .render("Qualitative analysis", True, (255, 255, 255))
qNBox= pygame.Surface([200, 50], pygame.SRCALPHA)
rectQl=qlBox.get_rect()



# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font settings
font = pygame.font.SysFont(None, 24)

# Dropdown menu items
files_menu_items = ["Home", "New", "Open", "Info", "Save", "Save As", "Close", "Feedback", "Options"]
settings_menu_items = ["Language", "Privacy", "Security", "Display", "Text Format"]
updates_menu_items = ["Check for Updates", "Download Updates", "Install Updates"]
help_menu_items = ["Links", "Contact Support", "Tutorials"]


# Dropdown menu state
files_menu_open = False
settings_menu_open = False
updates_menu_open = False
help_menu_open = False
practicals_menu_open = False

current_menu = None
winMain = mainWindow()

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Blit background image
    screen.blit(background_image, (0, 0))
    qlBox.fill((0,0,0))
    screen.blit(qlBox, (600, 380))
    screen.blit(textQ, (620, 400))
    qNBox.fill((0,0,0))
    screen.blit(qNBox,(600, 290))
    screen.blit(textL, (620, 300))

   
  

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
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
                elif 600 <= event.pos[0] <= 600+200 and 380<= event.pos[1] <= 380+100:
                        winMain.open_new_window("Welcome to Quantitative practicals simulations")
                elif 600 <= event.pos[0] <= 600+200 and 250<= event.pos[1] <= 250+100:
                         winMain.open_new_qualy("Welcome to Qualitative practicals simulations")
                         
                       

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 30))
    winMain.draw_menus(screen, 100, 50, [
        # {"label": "Files", "items": files_menu_items, "open": files_menu_open},
        # {"label": "Settings", "items": settings_menu_items, "open": settings_menu_open},
        # {"label": "Updates", "items": updates_menu_items, "open": updates_menu_open},
        # {"label": "Help", "items": help_menu_items, "open": help_menu_open},

    ])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()





