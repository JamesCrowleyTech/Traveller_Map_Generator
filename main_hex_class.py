from random import randrange, choice
import pygame
from math import sqrt


class Hex:
    def __init__(self, true_width, true_height, mid_width, mid_height, subsector_width,
                 subsector_height, top, left, hex_edge_length, index, display, random=True, starport=None, gas_giant=None):
        self.is_random = random
        self.left = left
        self.top = top
        self.true_width = true_width
        self.true_height = true_height
        self.mid_width = mid_width
        self.mid_height = mid_height
        self.hex_edge_length = hex_edge_length
        self.subsector_height = subsector_height
        self.subsector_width = subsector_width
        self.index = index
        self.is_valid = None
        self.gas_giant = None
        self.starport = None
        self.name = None
        self.button_parameters = None
        self.display = display
        self.apothem = sqrt(3) / 2
        self.dot_width = self.hex_edge_length // 6
        self.white = (255, 255, 255)
        self.b = (0, 0, 0)
        self.make()

    def make(self):
        def is_valid_generator():
            while True:
                yield choice((True, False))

        def gas_giant_generator():
            while True:
                yield randrange(1, 7) != 6

        def starport_generator():
            while True:
                roll = randrange(1, 7) + randrange(1, 7)
                if roll == 2:
                    yield "X"
                elif roll == 3 or roll == 4:
                    yield "E"
                elif roll == 5 or roll == 6:
                    yield "D"
                elif roll == 7 or roll == 8:
                    yield "C"
                elif roll == 9 or roll == 10:
                    yield "B"
                elif roll == 11 or roll == 12:
                    yield "A"

        def name_generator():
            capital_syllables = ['Es', 'Ran', 'Cal', 'Lag', 'Ren', 'Tel', 'Ag', 'Os', 'Loth', 'Hel', 'Bel', 'Pol',
                                 'Bal', 'Bes', 'Tran', 'Fan', 'Ho', 'Kan', 'Man', 'Tan', 'Lan',
                                 'Ar', 'Lin', 'Ban', 'Ben', 'Pan', 'Sen', 'Min', 'Tol', 'Hol']
            mid_syllables = ['la', 're', 'tre', 'res', 'bre', 'bul', 'tol', 'nur', 'par', 'parl', 'ian',
                             'lian', 'cre', 'gan', 'tral', 'ul', 'lan', 'il', 'tan', 'pon', 'lor',
                             'nas', 'fan', 'les', 'lat', 'lin', 'tam', 'tan', 'res', 'on', 'hin', 'gin']
            end_syllables = ['los', 'lax', 'tax', 'nax', 'di', 'ien', 'iem', 'las', 'mir', 'mor', 'bi',
                             'lin', 'dan', 'nir', 'fir', 'fur', 'ti', 'mur', 'far', 'lesh', 'len', 'don', 'fian',
                             'fin', 'fen', 'na', 'tem', 'anx', 'nen', 'reth', 'lan', 'dir', 'si', 'tir', 'nem', 'ni',
                             'fi', 'ni', 'ra', 'ga', 'ion']

            yield "".join([choice(capital_syllables)] + [choice(mid_syllables) if choice((True, False)) else ""]
                          + [choice(end_syllables)])

        gas_giant_generator_object = gas_giant_generator()
        is_valid_generator_object = is_valid_generator()
        starport_generator_object = starport_generator()
        name_generator_object = name_generator()

        self.is_valid = next(is_valid_generator_object)
        tmp_name = next(name_generator_object)
        tmp_starport = next(starport_generator_object)
        tmp_gas_giant = next(gas_giant_generator_object)
        if self.is_valid:
            self.name = tmp_name
            self.starport = tmp_starport
            self.gas_giant = tmp_gas_giant

    def draw(self, x, y, colour=(255, 255, 255,), index_only=False):
        def main_hex_outline(p1, p2, p3, p4, p5, p6):
            pygame.draw.polygon(self.display, self.b, (p1, p2, p3, p4, p5, p6), 2)

        def star():
            pygame.draw.circle(self.display, self.b, (x, y), self.dot_width)

        def display_name():
            font = pygame.font.SysFont('arial', int(self.hex_edge_length / 4))
            whitespaces = font.render("".join([' ' for _ in range(self.hex_edge_length // 3)]), True, (255, 255, 255), (255, 255, 255))
            white_rect = whitespaces.get_rect()
            white_rect.center = (x, y + int(self.hex_edge_length / 2))
            self.display.blit(whitespaces, white_rect)
            text = font.render(f'{str(self.name).strip()}', True, self.b, colour)
            text_rect = text.get_rect()
            text_rect.center = (x, y + int(self.hex_edge_length / 2))
            self.display.blit(text, text_rect)

        def display_index(dis_from_center=1.55, font_size=3.5):
            font = pygame.font.SysFont('arial', int(self.hex_edge_length / font_size))
            text = font.render(f'  {self.index}  ', True, self.b, colour)
            text_rect = text.get_rect()
            text_rect.center = (x, y - int(self.hex_edge_length / dis_from_center))
            self.display.blit(text, text_rect)
            return text_rect

        def display_starport():
            font = pygame.font.SysFont('arial', int(self.hex_edge_length / 3.5))
            text = font.render(f' {self.starport} ', True, self.b, colour)
            text_rect = text.get_rect()
            text_rect.center = (x, y - int(self.hex_edge_length / 3))
            self.display.blit(text, text_rect)

        def display_gas_giant():
            black = (0, 0, 0)
            white = (255, 255, 255)
            colour = black
            if self.index == '0405': print(x, y, colour)
            if not self.gas_giant: colour = white
            pygame.draw.circle(self.display, colour, (x + self.hex_edge_length / 3 * 2, y - self.hex_edge_length / 5),
                               self.hex_edge_length / 10)
            pygame.display.update()

        def get_hex_parameters():
            p1 = [x - self.hex_edge_length / 2, y - self.apothem * self.hex_edge_length]
            p2 = [x + self.hex_edge_length / 2, y - self.apothem * self.hex_edge_length]
            p3 = [x + self.hex_edge_length, y]
            p4 = [x + self.hex_edge_length / 2, y + self.apothem * self.hex_edge_length]
            p5 = [x - self.hex_edge_length / 2, y + self.apothem * self.hex_edge_length]
            p6 = [x - self.hex_edge_length, y]
            return [p1, p2, p3, p4, p5, p6]

        def get_button_parameters(text_rectangle):
            return tuple([text_rectangle.left, text_rectangle.right, text_rectangle.top, text_rectangle.bottom])

        if self.is_random:
            if index_only:
                display_index()
                return

            main_hex_outline(*get_hex_parameters())
            text_rect = display_index()
            if not self.is_valid: return get_button_parameters(text_rect)
            star()
            display_name()
            display_starport()
            display_gas_giant()
            return get_button_parameters(text_rect)
