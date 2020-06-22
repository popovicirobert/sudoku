
import sys, json
import pygame
from grid import Grid
from colors import Colors
from random import randint
from button import Button

class Sudoku:

    def __init__(self):
        pygame.init()

        self.SCREEN_HEIGHT = 552
        self.SCREEN_WIDTH = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.fill(Colors.BLACK)

        pygame.display.set_caption('Sudoku')

        self.BLOCK_SIZE = 60
        self.grid = Grid(self.BLOCK_SIZE, self.screen)

        self.mouse_pressed = False
        self.mouse_position = (None, None)

        self.game_active = False

        self.GRID_WIDTH = self.BLOCK_SIZE * 9 + 9 + 2 * 2
        right_edge_rect = pygame.Rect(self.GRID_WIDTH, 0,
                                      self.SCREEN_WIDTH - self.GRID_WIDTH, self.SCREEN_HEIGHT)
        self.screen.fill(Colors.GREY, right_edge_rect)

        self.start_button = Button(self.screen, 'Start', 575, 20)
        self.restart_button = Button(self.screen, 'Restart', 575, 90)
        self.solve_button = Button(self.screen, 'Solve', 575, 160)

        self.get_patterns()

    def get_patterns(self):
        with open('patterns.json', 'r') as fd:
            self.patterns = json.load(fd)
            self.PATTERN_COUNT = len(self.patterns)

    def update_screen(self):

        self.grid.show_grid()
        self.start_button.draw_button()
        self.solve_button.draw_button()
        self.restart_button.draw_button()

        pygame.display.update()

    def color_cells(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for x in range(9):
            for y in range(9):
                current_cell = self.grid.cell[x][y]
                if current_cell.collidepoint(mouse_x, mouse_y) == True:
                    self.grid.color[x][y] = Colors.LIGHT_GREY
                else:
                    self.grid.color[x][y] = Colors.WHITE

    def get_mouse_cell(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for x in range(9):
            for y in range(9):
                current_cell = self.grid.cell[x][y]
                if current_cell.collidepoint(mouse_x, mouse_y) == True:
                    return (x, y)
        return (None, None)

    def check_start_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.start_button.rect.collidepoint(mouse_x, mouse_y) == True:
            self.game_active = True
            self.grid.build_grid(randint(0, self.PATTERN_COUNT - 1))

    def check_restart_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.restart_button.rect.collidepoint(mouse_x, mouse_y) == True:
            self.grid.build_grid(randint(0, self.PATTERN_COUNT - 1))

    def check_solve_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.solve_button.rect.collidepoint(mouse_x, mouse_y) == True:
            answer = self.grid.solve_grid()
            for x in range(9):
                for y in range(9):
                    if self.grid.digit[x][y] != answer[1].digit[x][y]:
                        self.grid.add_digit(x, y,
                                            pygame.key.key_code(str(answer[1].digit[x][y])))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.game_active == True:
                    (x, y) = self.get_mouse_cell()

                    if x != None:
                        self.grid.color[x][y] = Colors.LIGHT_GREY

                        if self.mouse_pressed == True:
                            self.grid.color[self.mouse_position[0]][self.mouse_position[1]] = Colors.WHITE

                        if self.grid.color[x][y] == Colors.LIGHT_GREY:
                            # not the same cell
                            self.mouse_pressed = True
                            self.mouse_position = (x, y)
                        else:
                            # double click on same cell unselects it
                            self.mouse_pressed = False
                            self.mouse_position = (None, None)

                    self.check_restart_button()
                    self.check_solve_button()

                else:
                    self.check_start_button()

            elif event.type == pygame.KEYDOWN:

                if self.mouse_pressed == True:
                    x, y = self.mouse_position
                    self.grid.add_digit(x, y, event.key)
                    self.mouse_position = (None, None)
                    self.mouse_pressed = False



        if self.mouse_pressed == False and self.game_active == True:
            self.color_cells()


    def start(self):

        while True:
            self.update_screen()
            self.check_events()



sudoku = Sudoku()
sudoku.start()

