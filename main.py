from tkinter import *
from math import trunc

GAME_WIDTH = 600.0
GAME_HEIGHT = 600.0
HOLE_RADIUS = 50.0
SELECTED_PEG_COLOR = 'yellow'
PEG_COLOR = 'red'
HOLE_COLOR = 'black'
BACKGROUND_COLOR = '#f5f5f4'

class Application:
    def __init__(self):
        # setup window
        self.window = Tk()
        self.window.title('Peg Game')
        self.window.resizable(False, False)

        self.label = Label(self.window, text= 'Pegging Game', font= ('Arial', 40))
        self.label.pack()

        # setup canvas
        self.canvas = Canvas(self.window, width= GAME_WIDTH, height= GAME_HEIGHT, bg= BACKGROUND_COLOR)
        self.canvas.pack()

    def start(self):
        board = Board(self.canvas)
        self.window.mainloop()

class Board:

    # SETUP

    def __init__(self, canvas):
        # 2 => Peg is selected
        # 1 => Draw a peg on canvas
        # -1 => Draw empty hole on canvas
        # 0 => Do not draw anything on cavas
        self.canvas = canvas
        self.model = [
            [0, 0, 0, 0, -1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1]
        ]
        self.selected_peg = None

        self.draw_board()
        self.setup_interactions()
    
    def draw_board(self):
        for y in range(len(self.model)):
            row = self.model[y]
            for x in range (len(row)):
                if not (self.model[y][x] == 0):
                    self.draw_circle(x, y)

    def setup_interactions(self):
        self.canvas.bind('<Button>', self.did_click_canvas)

    # HELPERS

    def did_click_canvas(self, event):
        num_rows = len(self.model[0])
        num_cols = len(self.model)
        column_width = GAME_WIDTH/num_rows
        column_height = GAME_HEIGHT/num_cols
        x =  trunc(event.x * num_rows / GAME_WIDTH)
        y = trunc(event.y * num_cols / GAME_HEIGHT)
        # print(x, y)
        if self.selected_peg == None:
            # if not peg is selected, select (x,y) and highlight
            self.select_peg(x, y)
        else:
            # @ SALUM
            if (x == self.selected_peg[0]) and (y == self.selected_peg[1]):
                self.selected_peg = None
                self.model[y][x] = 1
                self.draw_circle(x, y)
                return
            # select a hole to fill (pause) with the selected peg
            self.fill_hole(x, y)
                
    # Draws a circle at (x, y) representing the value of model[y][x]
    def draw_circle(self, x, y):
        column_width = GAME_WIDTH/len(self.model[0])
        column_height = GAME_HEIGHT/len(self.model)
        x0 = x * column_width + (column_width - HOLE_RADIUS)/2
        y0 = y * column_height + (column_height- HOLE_RADIUS)/2
        x1 = x0 + HOLE_RADIUS
        y1 = y0 + HOLE_RADIUS
        if self.model[y][x] == -1:
            self.canvas.create_oval(x0, y0, x1, y1, fill=HOLE_COLOR)
        elif self.model[y][x] == 1:
            self.canvas.create_oval(x0, y0, x1, y1, fill=PEG_COLOR)
        elif self.model[y][x] == 2:
            self.canvas.create_oval(x0, y0, x1, y1, fill=SELECTED_PEG_COLOR)

    # Selects peg (x, y) and updates model
    def select_peg(self, peg_x, peg_y):
        if self.model[peg_y][peg_x] != 1:
            return
        self.model[peg_y][peg_x] = 2
        self.selected_peg = [peg_x, peg_y]
        self.draw_circle(peg_x, peg_y)
        

    # Fills hole (x, y) with the selcted peg and updates model
    def fill_hole(self, hole_x, hole_y):
        # Is the move legal?
        if not self.is_valid_move(hole_x, hole_y):
            print("Move is invalid my boi!")
            return 
        
        # Fill the hole
        self.model[hole_y][hole_x] = 1
        self.draw_circle(hole_x, hole_y)

        # @ SALUM: Remove the peg we just skipped over
        selected_x = self.selected_peg[0]
        selected_y = self.selected_peg[1]
        skipped_peg_x = trunc((hole_x + selected_x) / 2)
        skipped_peg_y = trunc((hole_y + selected_y) / 2)
        self.model[skipped_peg_y][skipped_peg_x] = -1
        self.draw_circle(skipped_peg_x, skipped_peg_y)


        # Clear the old selected peg
        self.model[self.selected_peg[1]][self.selected_peg[0]] = -1
        self.draw_circle(self.selected_peg[0], self.selected_peg[1])
        self.selected_peg = None

    # @ SALUM
    # Returns True only if move from selected peg to given (x, y) is valid. False otherwise
    def is_valid_move(self, hole_x, hole_y):
        # Do we have a peg selected?
        if self.select_peg == None:
            print('selected peg is None')
            return False
        
        # Is our destination a hole?
        if self.model[hole_y][hole_x] != -1:
            print('not a hole')
            return False
        
        # Is our destination within 2
        selected_x = self.selected_peg[0]
        selected_y = self.selected_peg[1]
        return abs(selected_x - hole_x) == 2 and abs(selected_y - hole_y) == 2
        


if __name__ == '__main__':
    app = Application()
    app.start()