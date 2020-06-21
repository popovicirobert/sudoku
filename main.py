
import sys
import pygame
from grid import Grid
from colors import Colors


class Sudoku:

    def __init__(self):
        pygame.init()

        self.SCREEN_HEIGHT = 600
        self.SCREEN_WIDTH = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.fill(Colors.BLACK)

        pygame.display.set_caption('Sudoku')

        self.BLOCK_SIZE = 60
        self.grid = Grid(self.BLOCK_SIZE)

        self.mouse_pressed = False
        self.mouse_position = (None, None)

    def update_screen(self):
        self.grid.show_grid(self.screen)
        pygame.display.update()

    def color_cells(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for x in range(9):
            for y in range(9):
                current_cell = self.grid.cell[x][y]
                if current_cell.collidepoint(mouse_x, mouse_y) == True:
                    self.grid.color[x][y] = Colors.GREY
                else:
                    self.grid.color[x][y] = Colors.WHITE

    def get_mouse_cell(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for x in range(9):
            for y in range(9):
                current_cell = self.grid.cell[x][y]
                if current_cell.collidepoint(mouse_x, mouse_y) == True:
                    return (x, y)
        return None

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_position = self.get_mouse_cell()

                if self.mouse_position[0] != None:
                    x, y = self.mouse_position

                    self.grid.color[x][y] = Colors.GREY
                    self.mouse_pressed = True

            elif event.type == pygame.KEYDOWN:
                if self.mouse_pressed == True:
                    x, y = self.mouse_position
                    self.grid.add_digit(x, y, pygame.key.name(event.key))
                    self.mouse_position = (None, None)
                    self.mouse_pressed = False

        if self.mouse_pressed == False:
            self.color_cells()


    def start(self):
        self.grid.build_grid()

        while True:
            self.update_screen()
            self.check_events()



sudoku = Sudoku()
sudoku.start()
