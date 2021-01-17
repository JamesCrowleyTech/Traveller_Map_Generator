import pygame
import csv
from math import ceil, sqrt
from hex_class import Hex
from time import sleep
from random import randrange, choice


class Subsector:
    def __init__(self, subsector_height, subsector_width, hex_edge_length):
        self.subsector_title = None
        self.systems = []
        self.apothem = sqrt(3) / 2
        self.subsector_height = subsector_height
        self.subsector_width = subsector_width
        self.total_cells = subsector_height * subsector_width + ceil(subsector_width // 2)
        self.hex_edge_length = hex_edge_length
        self.outline_width = 6
        self.display_height = 960
        self.display_width = 1800
        self.mid_height = self.display_height // 1.92
        self.mid_width = self.display_width // 2
        self.true_height = self.get_true_height()
        self.true_width = self.get_true_width()
        self.top = self.mid_height - self.true_height // 2
        self.left = self.mid_width - self.true_width // 2
        self.bottom = self.top + self.get_true_height() - 3
        self.index_generator_object = None
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        self.map_button_to_index = {}
        self.map_index_to_system = {}
        self.clock = pygame.time.Clock()
        self.save_a_copy_button_points = None
        self.save_button_points = None
        self.rand = None
        self.csv = None

    def save_a_copy(self):
        try:
            with open(f"{self.subsector_title}", "x"):
                pass
            with open(f"{self.subsector_title}", "a") as f:
                f.write("index,name,gas giant,starport\n")
                for system in self.systems:
                    if system.is_valid:
                        f.write(f"{system.index}, {system.name}, {system.gas_giant}, {system.starport}\n")
            with open(f"{self.subsector_title}") as f:
                print(f.read())
        except IOError:
            pass

    def save_to_original_file(self):
        try:
            with open(f"{self.subsector_title}", "x"):
                pass
            with open(f"{self.subsector_title}", "a"):
                pass
        except:
            pass

    def setup_system_from_csv(self, csv_file):
        self.systems = []
        total_indices = set()

        for i in range(1, self.subsector_width + 1):
            for j in range(1, self.subsector_height + 2):
                if not i % 2 and j == self.subsector_height + 1:
                    continue
                tmp = ""
                if len(str(i)) == 1:
                    tmp += "0"
                tmp += str(i)
                if len(str(j)) == 1:
                    tmp += "0"
                tmp += str(j)
                total_indices.add(tmp)

        with open(csv_file) as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                index = row[0]
                name = row[1]
                gas_giant = row[2]
                starport = row[3]
                total_indices.discard(index)
                self.systems.append((Hex(self.true_width, self.true_height, self.mid_width, self.mid_height,
                                         self.subsector_width, self.subsector_height, self.top, self.left,
                                         self.hex_edge_length, index, self.display, random=False, name=name,
                                         starport=starport, gas_giant=gas_giant, valid=True)))

        for index in total_indices:
            self.systems.append((Hex(self.true_width, self.true_height, self.mid_width, self.mid_height,
                                     self.subsector_width, self.subsector_height, self.top, self.left,
                                     self.hex_edge_length, index, self.display, random=False, valid=False)))

    def ask_for_csv_file(self):
        white = (255, 255, 255)
        self.display.fill(white)
        self.write_to_display("Enter a CSV file name", (self.display_width / 2, self.display_height * 1 / 3),
                              font_size=self.display_width // 28)
        name = ""
        while True:
            self.write_to_display(name, (self.display_width / 2, self.display_height * 4 / 7),
                                  font_size=self.display_width // 32)
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
                        pygame.draw.rect(self.display, white, (0, 480, 1800, 480))

                    elif event.key == pygame.K_ESCAPE:
                        self.rand = None
                        return self.intro()

                    elif event.key == pygame.K_RETURN:
                        self.csv = name
                        return self.setup_system_from_csv(self.csv)

                    else:
                        name += event.unicode

    def intro(self):
        def draw_title():
            self.display.fill((255, 255, 255))
            self.write_to_display("Traveller Map Generator & Display",
                                  (self.display_width // 2, self.display_height // 4), self.display_width // 22)

        def get_random_generator_button_rect_points():
            p1 = (self.display_width / 12, (self.display_height / 2))
            p2 = (self.display_width / 9 * 4, (self.display_height / 2))
            p3 = (self.display_width / 9 * 4, (self.display_height * 5) / 8)
            p4 = (self.display_width / 12, (self.display_height * 5) / 8)
            return p1, p2, p3, p4

        def draw_random_generator_button():
            def draw_button_background():
                points = get_random_generator_button_rect_points()
                pygame.draw.polygon(self.display, (255, 0, 0), points)

            def draw_button_text():
                self.write_to_display("Generate Random Map",
                                      (self.display_width * 19 / 72, self.display_height * 9 / 16),
                                      self.display_width // 32, font_background_colour=(255, 0, 0))

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
                pygame.draw.polygon(self.display, (0, 255, 0), points)

            def draw_button_text():
                self.write_to_display("Draw Preselected Map",
                                      (self.display_width * 53 / 72, self.display_height * 9 / 16),
                                      self.display_width // 32, font_background_colour=(0, 255, 0))

            draw_button_background()
            draw_button_text()

        draw_title()
        draw_random_generator_button()
        draw_preselected_map_button()

        pygame.display.update()

        random_generator_button_rect_points = get_random_generator_button_rect_points()
        preselected_map_button_rect_points = get_preselected_map_button_rect_points()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if random_generator_button_rect_points[0][0] <= mouse[0] <= random_generator_button_rect_points[2][
                        0] \
                            and random_generator_button_rect_points[1][1] <= mouse[1] <= \
                            random_generator_button_rect_points[3][1]:
                        self.rand = True
                        return
                    elif preselected_map_button_rect_points[2][0] <= mouse[0] <= preselected_map_button_rect_points[0][
                        0] \
                            and preselected_map_button_rect_points[1][1] <= mouse[1] <= \
                            preselected_map_button_rect_points[3][1]:
                        self.rand = False
                        return

    def write_to_display(self, message, coordinates, font_size, font_colour=(0, 0, 0),
                         font_background_colour=(255, 255, 255)):
        font = pygame.font.SysFont('arial', font_size)
        text = font.render(message, True, font_colour, font_background_colour)
        text_rect = text.get_rect()
        text_rect.center = coordinates[0], coordinates[1]
        self.display.blit(text, text_rect)
        return text_rect

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
        self.index_generator_object = self.index_generator()
        self.systems = []
        if self.rand:
            for _ in range(self.total_cells):
                self.systems.append(Hex(self.true_width, self.true_height, self.mid_width, self.mid_height,
                                        self.subsector_width, self.subsector_height, self.top, self.left,
                                        self.hex_edge_length, next(self.index_generator_object), self.display))
        else:
            pass

    def draw_individual_hex(self, system, colour=(211, 211, 211), index_only=False):
        x, y = self.get_position_of_hex(system.index)
        system.draw(x, y, colour, index_only)

    def new_input_to_change_info(self, system, press_f_text_rect_points):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.write_to_display("Press 'F' to alter system info", (
                (press_f_text_rect_points[0] * 2 + press_f_text_rect_points[2]) / 2,
                (press_f_text_rect_points[1] * 2 + press_f_text_rect_points[3]) / 2),
                                  self.hex_edge_length // 2)
            pygame.display.update()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                pygame.draw.rect(self.display, (255, 255, 255), press_f_text_rect_points)
                centerx = (press_f_text_rect_points[0] * 2 + press_f_text_rect_points[2]) / 2
                centery = (press_f_text_rect_points[1] * 2 + press_f_text_rect_points[3]) / 2
                line1_points = self.write_to_display("What do you wish to change?", (centerx, centery),
                                                     self.hex_edge_length // 2)
                line2_points = self.write_to_display("Name, Starport Class, Gas_Giant, Erase System",
                                                     (centerx, centery + press_f_text_rect_points[3]),
                                                     self.hex_edge_length // 2)

                replace_rect_points = (min(line1_points[0], line2_points[0]), min(line1_points[1], line2_points[1]),
                                       max(line1_points[2], line2_points[2]), (line1_points[3] + line2_points[3]) + 5)
                pygame.display.update()
                response = ""

                while True:
                    breakloop = False
                    self.write_to_display(response, ((replace_rect_points[0] * 2 + replace_rect_points[2]) / 2,
                                                     (replace_rect_points[1] * 2 + replace_rect_points[3]) / 2),
                                          font_size=self.display_width // 32)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif event.type == pygame.KEYDOWN:
                            pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)

                            if event.key == pygame.K_BACKSPACE:
                                if len(response) < 1:
                                    continue
                                response = response[:-1]
                                pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)

                            elif event.key == pygame.K_ESCAPE:
                                response = ""
                                pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)
                                self.write_to_display("Press 'F' to alter system info", (
                                    (press_f_text_rect_points[0] * 2 + press_f_text_rect_points[2]) / 2,
                                    (press_f_text_rect_points[1] * 2 + press_f_text_rect_points[3]) / 2),
                                                      self.hex_edge_length // 2)
                                breakloop = True
                                break

                            elif event.key == pygame.K_RETURN:
                                response = response.lower().strip()
                                if response in {"erase system", "name", "starport", "gas giant"}:
                                    self.change_attribute(system, response, replace_rect_points)
                                else:
                                    self.write_to_display("Invalid Type", (
                                        (press_f_text_rect_points[0] * 2 + press_f_text_rect_points[2]) / 2,
                                        (press_f_text_rect_points[1] * 2 + press_f_text_rect_points[3]) / 2),
                                                          self.hex_edge_length // 2)
                                    pygame.display.update()
                                    sleep(2)
                                breakloop = True
                                break

                            else:
                                response += event.unicode
                    if breakloop:
                        break

    def change_attribute(self, system, attribute, replace_rect_points):
        pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)
        response = ""
        if attribute == "erase system":
            system.name = None
            system.gas_giant = False
            system.starport = "X"
            system.is_valid = False
            return self.draw()

        while True:
            self.write_to_display(response, ((replace_rect_points[0] * 2 + replace_rect_points[2]) / 2,
                                             (replace_rect_points[1] * 2 + replace_rect_points[3]) / 2),
                                  font_size=self.display_width // 32)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)

                    if event.key == pygame.K_BACKSPACE:
                        if len(response) < 1:
                            continue
                        response = response[:-1]
                        pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)

                    elif event.key == pygame.K_ESCAPE:
                        return

                    elif event.key == pygame.K_RETURN:
                        response = response.lower().strip()

                        if not len(response):
                            continue
                        if attribute == "name":
                            system.is_valid = True
                            system.gas_giant = False
                            system.starport = "X"
                            system.name = response.title()
                        elif attribute == "starport":
                            if response in {"A", "B", "C", "D", "E", "X"}:
                                system.starport = response
                            else:
                                pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)
                                self.write_to_display("Starport class must be 'A', 'B', 'C', 'D', 'E', or 'X'",
                                                      ((replace_rect_points[0] * 2 + replace_rect_points[2]) / 2,
                                                       (replace_rect_points[1] * 2 + replace_rect_points[3]) / 2),
                                                      font_size=self.hex_edge_length // 2)
                                pygame.display.update()
                                pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)
                                sleep(2)
                                return
                        elif attribute == "gas giant":
                            if response in {"True", "False"}:
                                if response == "True":
                                    system.gas_giant = True
                                if response == "False":
                                    system.gas_giant = False
                            else:
                                pygame.draw.rect(self.display, (255, 255, 255), replace_rect_points)
                                self.write_to_display("Gas Giant setting must be 'True' or 'False'",
                                                      ((replace_rect_points[0] * 2 + replace_rect_points[2]) / 2,
                                                       (replace_rect_points[1] * 2 + replace_rect_points[3]) / 2),
                                                      font_size=self.hex_edge_length // 2)
                        return self.draw()
                    else:
                        response += event.unicode

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
            text_rect.center = (self.display_width // 6, self.display_height // 3 + y_increment)
            self.display.blit(text, text_rect)
            font = pygame.font.SysFont('arial', self.hex_edge_length // 2)
            y_increment += 60
        text = font.render("Press 'F' to alter system info", True, black)
        text_rect = text.get_rect()
        text_rect.center = (self.display_width // 6, self.display_height * 5 / 7)
        press_f_text_rect_points = (text_rect.left, text_rect.top, text_rect.width, text_rect.height)
        self.display.blit(text, text_rect)
        pygame.display.update()
        self.new_input_to_change_info(system, press_f_text_rect_points)

    def draw(self):
        def draw_save_as_button():
            points = self.write_to_display("Save A Copy", (self.display_width * 6 / 7, 90 // 1),
                                           int(self.hex_edge_length),
                                           font_colour=(255, 0, 0), font_background_colour=(30, 30, 30))
            enlargement = 20
            points[0] -= enlargement
            points[1] -= enlargement
            points[2] += enlargement * 2
            points[3] += enlargement * 2
            pygame.draw.rect(self.display, (0, 0, 0), points)
            self.write_to_display("Save A Copy", (self.display_width * 6 / 7, 90 // 1), int(self.hex_edge_length),
                                  font_colour=(255, 0, 0), font_background_colour=(0, 0, 0))
            self.save_a_copy_button_points = points

        def draw_save_button():
            self.write_to_display("Save", (self.display_width * 6 / 7, 200 // 1), int(self.hex_edge_length),
                                  font_colour=(255, 0, 0), font_background_colour=(30, 30, 30))
            self.save_button_points = [self.save_a_copy_button_points[0], self.save_a_copy_button_points[1] + 110,
                                       *self.save_a_copy_button_points[-2:]]
            pygame.draw.rect(self.display, (0, 0, 0), self.save_button_points)
            self.write_to_display("Save", (self.display_width * 6 / 7, 200 // 1), int(self.hex_edge_length),
                                  font_colour=(255, 0, 0), font_background_colour=(0, 0, 0))

        def generate_subsector_title():
            first_words = ["Fallen", "Distant", "Farthest", "Spinward", "Rimward", "Coreward"]
            second_words = ["Reaches", "Marches", "Extents", "Void", "Rifts"]
            return choice(first_words) + " " + choice(second_words)

        def draw_subsector_title():
            if self.rand:
                self.subsector_title = generate_subsector_title()
            else:
                self.subsector_title = self.csv
            self.write_to_display(self.subsector_title, (self.mid_width, self.top - 27), self.display_width // 70)

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
        draw_save_as_button()
        draw_save_button()
        clean_bottom_rect()

        draw_subsector_title()

        pygame.display.update()

        self.main_loop()

    def main_loop(self):
        while True:
            grey = (211, 211, 211)
            white = (255, 255, 255)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
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
                                    elif e.type == pygame.K_ESCAPE:
                                        pygame.quit()
                                        quit()
                                mouse = pygame.mouse.get_pos()
                                self.clock.tick(25)
                            self.draw_individual_hex(self.map_index_to_system[j], white, True)
                            pygame.display.update()
                            break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.save_a_copy_button_points[0] < mouse_pos[0] < self.save_a_copy_button_points[0] + \
                            self.save_a_copy_button_points[2] and \
                            self.save_a_copy_button_points[1] < mouse_pos[1] < self.save_a_copy_button_points[1] + \
                            self.save_a_copy_button_points[3]:
                        self.save_a_copy()
                    elif self.save_button_points[0] < mouse_pos[0] < self.save_button_points[0] + \
                            self.save_button_points[2] and self.save_button_points[1] < mouse_pos[1] < \
                            self.save_button_points[1] + self.save_button_points[3]:
                        self.save_to_original_file()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.rand = None
                        self.csv = None
                        return self.intro()
            self.clock.tick(30)


if __name__ == "__main__":
    pygame.init()
    Main = Subsector(10, 8, 50)
    Main.intro()
    while True:
        if Main.rand:
            Main.make()
            Main.draw()
            Main.save_a_copy()
        else:
            Main.ask_for_csv_file()
            if Main.csv:
                Main.draw()
