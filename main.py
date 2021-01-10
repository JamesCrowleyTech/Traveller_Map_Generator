import pygame
from math import ceil, sqrt
from hex_class import Hex


class Subsector:
    def __init__(self, subsector_height, subsector_width, hex_edge_length):
        self.systems = []
        self.apothem = sqrt(3) / 2
        self.subsector_height = subsector_height
        self.subsector_width = subsector_width
        self.total_cells = subsector_height * subsector_width + ceil(subsector_width // 2)
        self.hex_edge_length = hex_edge_length
        self.outline_width = 6
        self.display_height = 960
        self.display_width = 1800
        self.mid_height = self.display_height // 2
        self.mid_width = self.display_width // 2
        self.true_height = self.get_true_height()
        self.true_width = self.get_true_width()
        self.top = self.mid_height - self.true_height // 2
        self.left = self.mid_width - self.true_width // 2
        self.bottom = self.top + self.get_true_height() - 3
        self.index_generator_object = self.index_generator()
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        self.map_button_to_index = {}
        self.map_index_to_system = {}
        self.clock = None

    def get_true_width(self):
        return 3 / 2 * self.hex_edge_length * self.subsector_width + 1 / 2 * self.hex_edge_length

    def get_true_height(self):
        return sqrt(3) * self.hex_edge_length * self.subsector_height + self.apothem * self.hex_edge_length

    def get_systems(self):
        return self.systems

    def get_position_of_hex(self, index):
        ycoord = int((index[2] if int(index[2]) else "") + (index[3]))
        xcoord = int((index[0] if int(index[0]) else "") + (index[1]))
        x = self.left + self.hex_edge_length * xcoord * 3 / 2 - self.hex_edge_length * 1 / 2
        y = self.top + self.hex_edge_length * ycoord * sqrt(3) - self.hex_edge_length + \
            (self.apothem * self.hex_edge_length if not xcoord % 2 else 0)
        return [x, y]

    def index_generator(self):
        for i in range(1, self.subsector_width + 1):
            for j in range(1, self.subsector_height + 2):
                if not i % 2 and j == self.subsector_height + 1:
                    continue
                yield f"{''.join(['0' for _ in range(2 - len(str(i)))])}{i}{''.join(['0' for _ in range(2 - len(str(j)))])}{j}"

    def make(self):
        for _ in range(self.total_cells):
            self.systems.append(Hex(self.true_width, self.true_height, self.mid_width, self.mid_height,
                                    self.subsector_width, self.subsector_height, self.top, self.left,
                                    self.hex_edge_length, next(self.index_generator_object), self.display))

    def draw_individual_hex(self, system, colour=(211, 211, 211), index_only=False, replace=None):
        x, y = self.get_position_of_hex(system.index)
        system.draw(x, y, colour, index_only)

    def input_to_change_info(self, system):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                response = input('What do you wish to change? (Name/Starport/Gas Giant) >>> ').lower().strip()
                if response != 'name' and response != 'starport' and response != 'gas giant':
                    if response == 'cancel':
                        continue
                    print('Enter a valid choice')
                    continue
                else:
                    if response == 'name':
                        change = input("Enter name change or 'cancel' >>> ").title()
                        if len(change) >= 15:
                            print('System name must not exceed 14 characters')
                        system.name = change if change != 'cancel' else system.name
                    elif response == 'starport':
                        change = input("Enter new starport (e.g. 'A', 'C' etc.) or 'cancel' >>> ")
                        system.starport = ' ' + change + ' ' \
                            if change != 'cancel' and change in ['A', 'B', 'C', 'D', 'E', 'X'] else system.starport
                    elif response == 'gas giant':
                        change = input("Enter new gas giant setting or 'cancel' >>> ")
                        system.gas_giant = True if change == 'True' else False if change == 'False' else system.gas_giant
                    self.draw_individual_hex(system, colour=(255, 255, 255), replace=True)
                    self.display_popup_info(system)
                    break
        self.main_loop()

    def display_popup_info(self, system):
        black = (0, 0, 0)
        white = (255, 255, 255)
        y_increment = 0
        font = pygame.font.SysFont('arial', int(self.hex_edge_length))

        pygame.draw.rect(self.display, white,
                         (0, 0, self.display_width - self.left - self.true_width - 10, self.display_height))
        for i, j in (('Name: ', str(system.name).strip()), ('Index: ', system.index), ('Gas Giant: ', system.gas_giant),
                     ('Starport: ', str(system.starport).strip())):
            text = font.render(f'{i}{j}', True, black)
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 5, self.display_height // 3 + y_increment)
            self.display.blit(text, text_rect)
            font = pygame.font.SysFont('arial', int(self.hex_edge_length / 2))
            y_increment += 60
        text = font.render("Press 'F' to alter system info", True, black)
        text_rect = text.get_rect()
        text_rect.center = (self.display_width // 5, self.display_height // 3 + y_increment + 50)
        self.display.blit(text, text_rect)
        pygame.display.update()
        self.input_to_change_info(system)

    def draw(self):
        def draw_outline():
            pygame.draw.rect(self.display, b,
                             (self.left, self.top - self.outline_width - 2
                              , self.true_width, self.true_height), self.outline_width)

        def draw_main_hexes():
            for system in self.systems:
                x, y = self.get_position_of_hex(system.index)
                button = system.draw(x, y)
                self.map_index_to_system[system.index] = system
                self.map_button_to_index[button] = system.index

        def clean_bottom_rect():
            pygame.draw.rect(self.display, w, (self.left - 10, self.bottom, 1000, 1000))

        w = (255, 255, 255)
        b = (0, 0, 0)
        clock = pygame.time.Clock()

        pygame.display.set_caption("Traveller Map Generator & Display")

        self.clock = pygame.time.Clock()

        self.display.fill(w)

        draw_outline()

        draw_main_hexes()

        clean_bottom_rect()

        #  self.display_popup_info(self.map_index_to_system['0101'])

        pygame.display.update()

        self.main_loop()

    def main_loop(self):
        while True:
            grey = (211, 211, 211)
            white = (255, 255, 255)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEMOTION:
                    mouse = pygame.mouse.get_pos()
                    for i, j in self.map_button_to_index.items():
                        if i[0] <= mouse[0] <= i[1] and i[2] <= mouse[1] <= i[3]:
                            self.draw_individual_hex(self.map_index_to_system[self.map_button_to_index[i]], grey, True)
                            pygame.display.update()
                            while i[0] <= mouse[0] <= i[1] and i[2] <= mouse[1] <= i[3]:
                                for e in pygame.event.get():
                                    if e.type == pygame.MOUSEBUTTONDOWN:
                                        self.display_popup_info(self.map_index_to_system[self.map_button_to_index[i]])
                                mouse = pygame.mouse.get_pos()
                                self.clock.tick(25)
                            self.draw_individual_hex(self.map_index_to_system[j], white, True)
                            pygame.display.update()
                            break


if __name__ == "__main__":
    pygame.init()  # input("Random or predetermined? (r/p) >>> ").lower()
    Main = Subsector(10, 8, 50)
    Main.make()
    Main.draw()
    pygame.quit()
