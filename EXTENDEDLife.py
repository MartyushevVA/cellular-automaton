import pygame
import random
import sys
from tkinter import *

W_S = 1000
C_S = 10
COLORS = [(40, 40, 40), (255, 100, 135), (255, 91, 16), (14, 220, 142), (142, 245, 16)]


def clicked():
    global RULE
    global NUM_OF_COND
    RULE = pravilo.get()
    NUM_OF_COND = int(sost.get())


window = Tk()
window.title("Настройка конфигурации")
window.geometry('320x100')
vopros = Label(window, text="Заполнить поле в случайном порядке?", font=("Arial Bold", 10))
vopros.grid(column=0, row=0)
chk_state = BooleanVar()
chk_state.set(True)
chk = Checkbutton(window, text='', var=chk_state)
chk.grid(column=1, row=0)
vvodpravila = Label(window, text="Введите правило:", font=("Arial Bold", 10))
vvodpravila.grid(column=0, row=2)
pravilo = Entry(window, width=10)
pravilo.grid(column=1, row=2)
vvodsost = Label(window, text="Введите количество состояний:", font=("Arial Bold", 10))
vvodsost.grid(column=0, row=1)
sost = Entry(window, width=10)
sost.grid(column=1, row=1)
btn = Button(window, text="Подтвердить", command=clicked)
btn.grid(column=0, row=3)
window.mainloop()
RANDOM = chk_state.get()


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

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0
        self.neighbors_count = [0] * NUM_OF_COND


class CellularAutomaton:
    W_S = W_S
    C_S = C_S
    WIDTH = W_S // C_S
    RULE = RULE
    cells: dict

    def __init__(self):
        self.cells = {j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}
        if RANDOM:
            self.random_stats()

    def random_stats(self):
        for k in range(NUM_OF_COND):
            for i in range(len(self.cells) // 2):
                random_id = random.randint(0, len(self.cells) - 1)
                self.cells[random_id].status = k
        self.update_neighbors()

    def update_neighbors(self):
        for curr_cell in self.cells.keys():
            count = [0] * NUM_OF_COND
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
                            for k in range(NUM_OF_COND):
                                if self.cells[curr_id].status == k:
                                    count[k] += 1
                        except:
                            pass
            for k in range(NUM_OF_COND):
                self.cells[curr_cell].neighbors_count[k] = count[k]

    def update_cells(self):
        RULE_sections = self.RULE.split('/')
        Laws = []
        for k in range(NUM_OF_COND):
            Laws.append(RULE_sections[k].split(','))
        for key, item in self.cells.items():
            for k in range(NUM_OF_COND):
                if self.cells[key].status == k:
                    if str(item.neighbors_count[abs(k - 1) % NUM_OF_COND]) in str(Laws[k]).replace("['", "").replace("']", ""):
                        self.cells[key].status = abs(k + 1) % NUM_OF_COND
                        break


def main():
    PLAY = 0
    Game = Window()
    Automaton = CellularAutomaton()
    while True:
        if PLAY:
            Automaton.update_cells()
            Automaton.update_neighbors()
        pygame.display.update()
        Game.surface.fill((40, 40, 40))
        Game.draw_cells(Automaton.cells)
        result = Game.check_events()
        if result[0] == 'Start/Stop':
            PLAY = not PLAY
        elif result[0] == 'Changing':
            if not Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status == 0:
                Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status = 0
            else:
                Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status = 1
            Automaton.update_neighbors()


if __name__ == "__main__":
    main()
