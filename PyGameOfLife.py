import random
import sys
import pygame
from pygame.locals import *


class LifeGame:

    def __init__(self, screen_width=1024, screen_height=768, cell_size=10, alive_color=(0, 255, 255),
                 dead_color=(0, 0, 0), max_fps=10):
        """
        Initialize grid, set default game state, initialize screen
        :param screen_width: Game window width
        :param screen_height: Game window height
        :param cell_size: Diameter of circles.
        :param alive_color: RGB tuple e.g. (255,255,255) for cells
        :param dead_color: RGB tuple e.g. (255,255,255)
        :param max_fps: Framerate cap to limit game speed
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()

        self.last_update_completed = 0
        self.desired_milliseconds_between_updates = (1.0 / max_fps) * 1000.0

        self.active_grid = 0

        self.num_cols = int(self.screen_width / self.cell_size)
        self.num_rows = int(self.screen_height / self.cell_size)
        self.grids = []
        self.init_grids()
        self.set_grid(0, self.active_grid)

        self.closeWelcomeWindow = False
        self.paused = False
        self.game_over = False

    def init_grids(self):
        """
        Create and stores the default active and inactive grid
        :return: None
        """
        def create_grid():
            """
            Generate 2 empty grids
            :return:
            """
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows
        self.grids.append(create_grid())
        self.grids.append(create_grid())

#    def set_gridpoint(self, grid=0, x, y, value):
#        self.grids[grid][x][y] = value

    def set_grid(self, value=None, gr=0):
        """
        Set an entire grid at once. Set to a single value or random 0/1.
        Examples:
          set_grid(0) # all dead
          set_grid(1) # all alive
          set_grid() # random
          set_grid(None) # random
        :param grid: Index of grid, for active/inactive (0 or 1)
        :param value: Value to set the cell to (0 or 1)
        :return:
        """
        
        #if value == None:
        #    cell_value = 0
        #else:
        #    cell_value = value

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value
                self.grids[gr][r][c] = cell_value

    def draw_grid(self):
        """
        Given the grid and cell states, draw the cells on the screen
        :return:
        """
        self.clear_screen()
        for c in range(self.num_cols + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (c * self.cell_size, 0), (c * self.cell_size, self.screen_height))
        for r in range(self.num_rows + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (0, r * self.cell_size), (self.screen_width, r * self.cell_size))
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grid][r][c] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                pygame.draw.circle(self.screen,
                                   color,
                                   (int(c * self.cell_size + (self.cell_size / 2)),
                                    int(r * self.cell_size + (self.cell_size / 2))),
                                   int(self.cell_size / 2 - 1),
                                   0)
        pygame.display.flip()

    def clear_screen(self):
        """
        Fill whole screen with dead color
        :return:
        """
        self.screen.fill(self.dead_color)

    def get_cell(self, row_num, col_num):
        """
        Get the alive/dead (0/1) state of a specific cell in active grid
        :param row_num:
        :param col_num:
        :return: 0 or 1 depending on state of cell. Defaults to 0 (dead)
        """

        r = row_num #-1 - num_rows
        c = col_num #-1 - num_cols

        if r == -1:
            r = self.num_rows - 1
        if r == self.num_rows:
            r = 0
        if c == -1:
            c = self.num_cols - 1
        if c == self.num_cols:
            c = 0
        
        cell_value = self.grids[self.active_grid][r][c]
        return cell_value

        #try:
        #    cell_value = self.grids[self.active_grid][row_num][col_num]
        #except:
        #    cell_value = 0
        #return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        """
        Get the number of alive neighbor cells, and determine the state of the cell
        for the next generation. Determine whether it lives, dies, survives, or is born.
        :param row_index: Row number of cell to check
        :param col_index: Column number of cell to check
        :return: The state the cell should be in next generation (0 or 1)
        """
        num_alive_neighbors = 0
        
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        # Rules for life and death
        if self.grids[self.active_grid][row_index][col_index] == 1:  # alive
            if num_alive_neighbors > 3:  # Overpopulation
                return 0
            if num_alive_neighbors < 2:  # Underpopulation
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0:  # dead
            if num_alive_neighbors == 3:
                return 1  # come to life

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        """
        Inspect current generation state, prepare next generation
        :return:
        """
        self.set_grid(0, self.inactive_grid())
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                next_gen_state = self.check_cell_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        """
        Simple helper function to get the index of the inactive grid
        If active grid is 0 will return 1 and vice-versa.
        :return:
        """
        return (self.active_grid + 1) % 2

    def handle_events(self):
        """
        Handle any keypresses
        s - start drawing nad start evoluving (when drawing is finished)
        p - pause the game
        o . start Over
        r - randomize grid
        q - quit
        :return:
        """
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                print("key pressed")
                self.closeWelcomeWindow = True
                if event.unicode == 'p':
                    print("Toggling pause.")
                    if self.closeWelcomeWindow:
                        if self.paused:
                            self.paused = False
                        else:
                            self.paused = True
                elif event.unicode == 's':
                    self.grids = []
                    self.init_grids()
                    self.set_grid(0, self.active_grid)
                    self.closeWelcomeWindow = True
                    self.grid_maker()
                elif event.unicode == 'o':
                    self.grids = []
                    self.init_grids()
                    self.set_grid(0, self.active_grid)
                    self.closeWelcomeWindow = False
                    self.welcome()
                elif event.unicode == 'r':
                    print("Randomizing grid.")
                    self.paused = False
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)  # randomize
                    self.set_grid(0, self.inactive_grid())  # set to 0
                    self.draw_grid()
                elif event.unicode == 'q':
                    print("Exiting.")
                    self.game_over = True
                    return self.game_over
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def cap_frame_rate(self):
        """
        If game is running too fast and updating frames too frequently,
        just wait to maintain stable framerate
        :return:
        """
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now

    def grid_maker(self):

        ready = False
        
        self.draw_grid()

        while not ready:

            for event in pygame.event.get():

                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                if mouse_click[0] == 1:

                    y = int(mouse_x / self.cell_size)
                    x = int(mouse_y / self.cell_size)

                    print(mouse_x, mouse_y)
                    print(x, y)

                    if mouse_x < self.screen_width - self.cell_size and mouse_y < self.screen_height - self.cell_size:
                        if self.grids[self.active_grid][x][y] == 0:
                            self.grids[self.active_grid][x][y] = 1
                            print(self.grids[self.active_grid][x][y])
                        else:
                            self.grids[self.active_grid][x][y] = 0
                            print(self.grids[self.active_grid][x][y])

                        self.draw_grid()
            
                if event.type == pygame.QUIT:
                    ready = True
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    ready = True

        return self.grids

    def welcome(self):

        if not self.closeWelcomeWindow:

            fontobject=pygame.font.SysFont('Arial', 18)
            
            text1 = "Welcome to Conway's Game of Life!"
            text2 = "Use keys as follows:"
            text3 = "'S' - Start drawing, Start evolving (when drawing is finished)"
            text4 = "'P' - Pause / unPause"
            text5 = "'R' - start a Random grid"
            text6 = "'O' - start Over"
            text7 = "'Q' - QUIT"
            textPane1 = fontobject.render(text1, 1, (255, 255, 255))
            textPane2 = fontobject.render(text2, 1, (255, 255, 255))
            textPane3 = fontobject.render(text3, 1, (255, 255, 255))
            textPane4 = fontobject.render(text4, 1, (255, 255, 255))
            textPane5 = fontobject.render(text5, 1, (255, 255, 255))
            textPane6 = fontobject.render(text6, 1, (255, 255, 255))
            textPane7 = fontobject.render(text7, 1, (255, 255, 255))
            
            self.clear_screen()
            
            self.screen.blit(textPane1, (int ((self.screen.get_width() - textPane1.get_size()[0]) / 2), int (self.screen.get_height() / 2) - 20))
            self.screen.blit(textPane2, (int ((self.screen.get_width() - textPane2.get_size()[0]) / 2), int (self.screen.get_height() / 2)))
            self.screen.blit(textPane3, (int ((self.screen.get_width() - textPane3.get_size()[0]) / 2), int (self.screen.get_height() / 2) + 40))
            self.screen.blit(textPane4, (int ((self.screen.get_width() - textPane4.get_size()[0]) / 2), int (self.screen.get_height() / 2) + 60))
            self.screen.blit(textPane5, (int ((self.screen.get_width() - textPane5.get_size()[0]) / 2), int (self.screen.get_height() / 2) + 80))
            self.screen.blit(textPane6, (int ((self.screen.get_width() - textPane6.get_size()[0]) / 2), int (self.screen.get_height() / 2) + 100))
            self.screen.blit(textPane7, (int ((self.screen.get_width() - textPane7.get_size()[0]) / 2), int (self.screen.get_height() / 2) + 120))
            
            pygame.display.flip()

            while not self.closeWelcomeWindow:
                self.handle_events()
        
    def run(self):
        
        self.welcome()
        
        while not self.game_over:
            if not self.paused:
                self.update_generation()
                self.draw_grid()
                self.handle_events()
                self.cap_frame_rate()
            else: 
                self.handle_events()

if __name__ == "__main__":
    
    gol = LifeGame()
    gol.run()

    pygame.quit()
    quit()
    sys.exit()

    

