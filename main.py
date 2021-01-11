import pygame
from math import ceil, sqrt
from hex_class import Hex
from time import sleep
from random import randrange


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
        self.clock = pygame.time.Clock()
        self.rand = True

    def intro(self):
        def draw_title():
            white = (255, 255, 255)
            black = (0, 0, 0)
            self.display.fill(white)
            font = pygame.font.SysFont('arial', self.display_width // 22)
            text = font.render("Traveller Map Generator & Display", True, black, white)
            text_rect = text.get_rect()
            text_rect.center = (self.display_width // 2, self.display_height // 4)
            self.display.blit(text, text_rect)
            pygame.display.update()

        def get_random_generator_button_rect_points():
            p1 = (self.display_width / 12, (self.display_height / 2))
            p2 = (self.display_width / 9 * 4, (self.display_height / 2))
            p3 = (self.display_width / 9 * 4, (self.display_height * 5) / 8)
            p4 = (self.display_width / 12, (self.display_height * 5) / 8)
            return p1, p2, p3, p4

        def draw_random_generator_button():
            def draw_button_background():
                points = get_random_generator_button_rect_points()
                pygame.draw.polygon(self.display, red, points)

            def draw_button_text():
                font = pygame.font.SysFont('arial', self.display_width // 32)
                text = font.render("Generate Random Map", True, black, red)
                text_rect = text.get_rect()
                text_rect.center = (self.display_width * 19 / 72, self.display_height * 9 / 16)
                self.display.blit(text, text_rect)

            draw_button_background()
            draw_button_text()

        def get_preselected_map_button_rect_points():
            p1 = (self.display_width / 12 * 11, (self.display_height / 2))
            p2 = (self.display_width / 9 * 5, (self.display_height / 2))
            p3 = (self.display_width / 9 * 5, (self.display_height * 5) / 8)
            p4 = (self.display_width / 12 * 11, (self.display_height * 5) / 8)
            return p1, p2, p3, p4

        def draw_preselected_map_button():
            def draw_button_background():
                points = get_preselected_map_button_rect_points()
                pygame.draw.polygon(self.display, green, points)

            def draw_button_text():
                font = pygame.font.SysFont('arial', self.display_width // 32)
                text = font.render("Draw Preselected Map", True, black, green)
                text_rect = text.get_rect()
                text_rect.center = (self.display_width * 53 / 72, self.display_height * 9 / 16)
                self.display.blit(text, text_rect)

            draw_button_background()
            draw_button_text()

        black = (0, 0, 0)
        red = (255, 0, 0)
        green = (0, 255, 0)
        draw_title()
        draw_random_generator_button()
        draw_preselected_map_button()
        pygame.display.update()

        random_generator_button_rect_points = get_random_generator_button_rect_points()
        preselected_map_button_rect_points = get_preselected_map_button_rect_points()

        print(random_generator_button_rect_points)
        print(preselected_map_button_rect_points)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if random_generator_button_rect_points[0][0] <= mouse[0] <= random_generator_button_rect_points[2][0] \
                            and random_generator_button_rect_points[1][1] <= mouse[1] <= random_generator_button_rect_points[3][1]:
                        return
                    elif preselected_map_button_rect_points[2][0] <= mouse[0] <= preselected_map_button_rect_points[0][0] \
                            and preselected_map_button_rect_points[1][1] <= mouse[1] <= preselected_map_button_rect_points[3][1]:
                        self.rand = False
                        self.ask_for_csv_file()

    def write_to_display(self, message, coords, font_size, font_colour=(0, 0, 0), font_background_colour=(255, 255, 255)):
        font = pygame.font.SysFont('arial', font_size)
        text = font.render(message, True, font_colour, font_background_colour)
        text_rect = text.get_rect()
        text_rect.center = coords[0], coords[1]
        self.display.blit(text, text_rect)

    def ask_for_csv_file(self):
        white = (255, 255, 255)
        black = (0, 0, 0)
        self.display.fill(white)
        self.write_to_display("Enter a CSV file name", (self.display_width / 2, self.display_height * 1 / 3), font_size=self.display_width // 28)
        name = ""
        while True:
            self.write_to_display(name, (self.display_width / 2, self.display_height * 4 / 7), font_size=self.display_width // 32)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(name) < 1:
                            continue
                        name = name[:-1]
                        pygame.display.update()

                    elif event.key == pygame.K_DELETE:
                        name = ""

                    else:
                        name += event.unicode

                    #~print('backspace', randrange(1, 1000))
            #self.clock.tick(60)

    def get_true_width(self):
        return 3 / 2 * self.hex_edge_length * self.subsector_width + 1 / 2 * self.hex_edge_length

    def get_true_height(self):
        return sqrt(3) * self.hex_edge_length * self.subsector_height + self.apothem * self.hex_edge_length

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
                              , self.true_width, self.true_height + 2), self.outline_width)

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

        pygame.display.set_caption("Traveller Map Generator & Display")

        self.display.fill(w)

        draw_outline()

        draw_main_hexes()

        clean_bottom_rect()

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
    with open("Traveller_Test_CSV") as f:
        for l in f:
            print(l)
    pygame.init()  # input("Random or predetermined? (r/p) >>> ").lower()
    Main = Subsector(10, 8, 50)
    Main.intro()
    Main.make()
    Main.draw()
    pygame.quit()

