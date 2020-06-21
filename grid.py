
from colors import Colors
import pygame
import pygame.font

class Grid:

    def __init__(self, BLOCK_SIZE):
        self.color = [[None for y in range(9)] for x in range(9)]
        self.cell = [[None for y in range(9)] for x in range(9)]
        self.digit = [[None for y in range(9)] for x in range(9)]

        self.BLOCK_SIZE = BLOCK_SIZE
        self.DIGIT_OFFSET = self.BLOCK_SIZE // 3
        self.build_grid()

        self.font = pygame.font.SysFont('Arial', 20)


    def show_grid(self, screen):
        for x in range(9):
            for y in range(9):
                pygame.draw.rect(screen, self.color[x][y], self.cell[x][y])

                if self.digit[x][y] != None:
                    self.show_digit(screen, x, y)

    def build_grid(self):
        for x in range(9):
            for y in range(9):
                self.cell[x][y] = pygame.Rect(
                    x * self.BLOCK_SIZE + x - 1, y * self.BLOCK_SIZE + y - 1, self.BLOCK_SIZE, self.BLOCK_SIZE)
                self.color[x][y] = Colors.WHITE

    def show_digit(self, screen, x, y):
        digit = self.digit[x][y]
        text = self.font.render(f'{digit}', True, (0, 0, 0))
        screen.blit(text, (x * self.BLOCK_SIZE + self.DIGIT_OFFSET, y * self.BLOCK_SIZE + self.DIGIT_OFFSET))

    def add_digit(self, x, y, digit):
        if digit.isdigit() and digit != '0':
            self.digit[x][y] = digit
            if not self.check_grid(x, y):
                self.digit[x][y] = None

    def check_grid(self, x, y):
        if self.check_x(x) and self.check_y(y) and self.check_square(x, y):
            return True
        return False

    def check_square(self, X, Y):
        frequence = [0 for value in range(10)]
        for x in range(X // 3, X // 3 + 3):
            for y in range(Y // 3, Y // 3 + 3):
                digit = self.digit[x][y]
                if digit != None:
                    digit = int(digit)
                    frequence[digit] += 1
                    if frequence[digit] > 1:
                        return False
        return True

    def check_x(self, x):
        frequence = [0 for value in range(10)]
        for y in range(9):
            digit = self.digit[x][y]
            if digit != None:
                digit = int(digit)
                frequence[digit] += 1
                if frequence[digit] > 1:
                    return False
        return True

    def check_y(self, y):
        frequence = [0 for value in range(10)]
        for x in range(9):
            digit = self.digit[x][y]
            if digit != None:
                digit = int(digit)
                frequence[digit] += 1
                if frequence[digit] > 1:
                    return False
        return True