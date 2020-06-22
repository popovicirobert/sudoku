
from colors import Colors
import pygame
import pygame.font
import json

class Grid:

    def __init__(self, BLOCK_SIZE, screen):
        self.color = [[None for y in range(9)] for x in range(9)]
        self.cell = [[None for y in range(9)] for x in range(9)]
        self.digit = [[None for y in range(9)] for x in range(9)]
        self.fixed = [[False for y in range(9)] for x in range(9)]

        self.BLOCK_SIZE = BLOCK_SIZE
        self.DIGIT_OFFSET = self.BLOCK_SIZE // 3

        self.get_patterns()
        # -1 stands for empty grid
        self.build_grid(-1)

        self.font = pygame.font.SysFont('Arial', 20)
        self.screen = screen

    def get_patterns(self):
        with open('patterns.json', 'r') as fd:
            self.patterns = json.load(fd)
            self.PATTERN_COUNT = len(self.patterns)

    def show_grid(self):
        for x in range(9):
            for y in range(9):
                pygame.draw.rect(self.screen, self.color[x][y], self.cell[x][y])

                if self.digit[x][y] != None:
                    self.show_digit(self.screen, x, y)

    def build_grid(self, grid_index):
        for x in range(9):
            for y in range(9):
                self.cell[x][y] = pygame.Rect(
                    x * self.BLOCK_SIZE + x - 1 + 2 * (x // 3), y * self.BLOCK_SIZE + y - 1 + 2 * (y // 3),
                    self.BLOCK_SIZE, self.BLOCK_SIZE)

                self.color[x][y] = Colors.WHITE
                self.fixed[x][y] = False
                self.digit[x][y] = None

                if grid_index != -1 and self.patterns[grid_index][x][y] != None:
                    self.digit[x][y] = self.patterns[grid_index][x][y]
                    self.fixed[x][y] = True



    def show_digit(self, screen, x, y):
        digit = self.digit[x][y]
        digit_image = self.font.render(f'{digit}', True, (0, 0, 0))
        screen.blit(digit_image, (x * self.BLOCK_SIZE + self.DIGIT_OFFSET + 2 * (x // 3) + x - 1,
                                  y * self.BLOCK_SIZE + self.DIGIT_OFFSET + 2 * (y // 3) + y - 1))

    def add_digit(self, x, y, key):
        if self.fixed[x][y] == False:
            digit = pygame.key.name(key)
            if digit.isdigit() and digit != '0':
                self.digit[x][y] = digit
                if self.check_grid(x, y) == False:
                    self.digit[x][y] = None

                return self.digit[x][y] != None

            elif key == pygame.K_BACKSPACE:
                self.digit[x][y] = None
                return None

        return False

    def check_grid(self, x, y):
        if self.check_x(x) and self.check_y(y) and self.check_square(x, y):
            return True
        return False

    def check_square(self, X, Y):
        frequence = {index: 0 for index in range(1, 10)}
        for x in range(3 * (X // 3), 3 * (X // 3) + 3):
            for y in range(3 * (Y // 3), 3 * (Y // 3) + 3):
                digit = self.digit[x][y]
                if digit != None:
                    digit = int(digit)
                    frequence[digit] += 1
                    if frequence[digit] > 1:
                        return False
        return True

    def check_x(self, x):
        frequence = {index: 0 for index in range(1, 10)}
        for y in range(9):
            digit = self.digit[x][y]
            if digit != None:
                digit = int(digit)
                frequence[digit] += 1
                if frequence[digit] > 1:
                    return False
        return True

    def check_y(self, y):
        frequence = {index: 0 for index in range(1, 10)}
        for x in range(9):
            digit = self.digit[x][y]
            if digit != None:
                digit = int(digit)
                frequence[digit] += 1
                if frequence[digit] > 1:
                    return False
        return True

    def solve_grid(self, x = 0, y = 0):
        self.show_grid()
        pygame.display.update()

        if x == 0 and y == 9:
            return [True, self]
        else:

            next_x, next_y = x + 1, y
            if x == 8:
                next_x, next_y = 0, y + 1

            answer = [False, self]

            if self.digit[x][y] != None:
                answer = self.solve_grid(next_x, next_y)
            else:
                for value in range(1, 10):
                    if (answer[0] == False and
                        self.add_digit(x, y, pygame.key.key_code(str(value))) == True):
                        answer = self.solve_grid(next_x, next_y)

                if answer[0] == False and self.fixed[x][y] == False:
                    self.digit[x][y] = None

            for x in range(9):
                for y in range(9):
                    if self.digit[x][y] != answer[1].digit[x][y]:
                        self.add_digit(x, y, pygame.key.key_code(str(answer[1].digit[x][y])))

            return [answer[0], self]