import pygame
import random
import sys
import os

W_S = 1000
COLORS = [(40, 40, 40), (37, 213, 0), (246, 0, 24)]

with open('config.txt', 'r', encoding='cp1251') as f:
    RANDOM = f.readline()
    RULE = str(f.readline())[:-1].replace('B', '').replace('S', '')
    NUMHUNTERS = int(f.readline())
    NUMVICTIMS = int(f.readline())
    TIMEHUNTERS = int(f.readline())
    TIMEVICTIMS = int(f.readline())
    RADHUNTER = int(f.readline())
    RADVICTIMS = int(f.readline())
    HUNGRY = int(f.readline())
    DELAY = int(f.readline())
    C_S = int(f.readline())


class Window:
    W_S = W_S
    C_S = C_S

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.W_S, self.W_S))

    def draw_cells(self, cells):
        for i in range(len(cells)):
            if cells[i].status:
                col = COLORS[cells[i].status]
                pygame.draw.rect(self.surface, col,
                                 (cells[i].x * self.C_S, cells[i].y * self.C_S, self.C_S, self.C_S))

    def check_events(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    return ['Start/Stop']
            elif i.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = (pos[0] // self.C_S, pos[1] // self.C_S)
                return ['Changing', pos]
        return ['']


class Cell:
    x: int
    y: int
    status: int
    neighbors_count: list
    birthtime: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0
        self.neighbors_count = [0] * 3
        self.birthtime = 0


class CellularAutomaton:
    W_S = W_S
    C_S = C_S
    WIDTH = W_S // C_S
    cells: dict

    def __init__(self):
        self.cells = {j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}
        if "True" in RANDOM:
            self.random_stats()

    def random_stats(self):
        for k in range(3):
            for i in range(len(self.cells) // 4):
                random_id = random.randint(0, len(self.cells) - 1)
                self.cells[random_id].status = k
                # if k>0:
                #     self.cells[random_id].birthtime = 1
        self.update_neighbors()

    def update_neighbors(self):
        for curr_cell in self.cells.keys():
            count = [0] * 3
            for i in range(self.cells[curr_cell].x - 1, self.cells[curr_cell].x + 2):
                for j in range(self.cells[curr_cell].y - 1, self.cells[curr_cell].y + 2):
                    if (i == self.cells[curr_cell].x) and (j == self.cells[curr_cell].y):
                        pass
                    else:
                        if i < 0:
                            i = self.WIDTH - 1
                        elif i > self.WIDTH:
                            i = 0
                        if j < 0:
                            j = self.WIDTH - 1
                        elif j > self.WIDTH:
                            j = 0
                        curr_id = j + self.WIDTH * i
                        try:
                            for k in range(3):
                                if self.cells[curr_id].status == k:
                                    count[k] += 1
                        except:
                            pass
            for k in range(3):
                self.cells[curr_cell].neighbors_count[k] = count[k]

    def update_cells(self, time):
        for key, item in self.cells.items():
            if self.cells[key].status == 0:
                if self.cells[key].neighbors_count[1] > 2:
                    self.cells[key].status = 1
                    self.cells[key].birthtime = time
                # else:
                #     newchance = random.randint(0, 50)
                #     if newchance == 0:
                #         self.cells[key].status = 1
            else:
                if time - self.cells[key].birthtime > 1000:
                    self.cells[key].status = 0
                    self.cells[key].birthtime = 0
                else:
                    if self.cells[key].status == 1:
                        if self.cells[key].neighbors_count[2] > 2:
                            self.cells[key].status = 2
                            self.cells[key].birthtime = time



    def random_green(self):
        for i in range(len(self.cells) // 16):
            random_id = random.randint(0, len(self.cells) - 1)
            self.cells[random_id].status = 1
        self.update_neighbors()


def main():
    PLAY = 0
    frst = 0
    d = 0
    Game = Window()
    Automaton = CellularAutomaton()
    while True:
        if PLAY:
            Automaton.update_cells(pygame.time.get_ticks())
            Automaton.update_neighbors()
            if pygame.time.get_ticks() % 600 == 0:
                Automaton.random_green()
        pygame.display.update()
        Game.surface.fill((40, 40, 40))
        Game.draw_cells(Automaton.cells)
        result = Game.check_events()
        if result[0] == 'Start/Stop':
            PLAY = not PLAY
            if frst == 0:
                d = pygame.time.get_ticks()
                frst = 1
        elif result[0] == 'Changing':
            Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status = (Automaton.cells[
                                                                                         result[1][1] + result[1][
                                                                                             0] * Automaton.WIDTH].status + 1) % 3
            Automaton.update_neighbors()
        pygame.time.wait(DELAY)


if __name__ == "__main__":
    main()
