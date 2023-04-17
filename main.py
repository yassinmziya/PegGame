from tkinter import *
from math import trunc

GAME_WIDTH = 600.0
GAME_HEIGHT = 600.0
HOLE_RADIUS = 50.0
PEG_COLOR = 'red'
HOLE_COLOR = 'black'
BACKGROUND_COLOR = '#f5f5f4'

class Application:
    def __init__(self):
        # setup window
        self.window = Tk()
        self.window.title('Peg Game')
        self.window.resizable(False, False)

        self.label = Label(self.window, text= 'Hello, Yassin!', font= ('Arial', 40))
        self.pack()

        # setup canvas
        self.canvas = Canvas(self.window, width= GAME_WIDTH, height= GAME_HEIGHT, bg= BACKGROUND_COLOR)
        self.canvas.pack()

    def start(self):
        board = Board(self.canvas)
        self.window.mainloop()

class Board:

    # SETUP

    def __init__(self, canvas):
        # 1 => Draw a peg on canvas
        # -1 => Draw empty hole on canvas
        # 0 => Do not draw anything on cavas
        self.canvas = canvas
        self.model = [
            [0, 0, -1, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
        ]
        self.draw_board()
        self.setup_interactions()
    
    def draw_board(self):
        for y in range(len(self.model)):
            row = self.model[y]
            for x in range (len(row)):
                if not (self.model[y][x] == 0):
                    self.draw_circle(x, y, self.model[y][x] == -1)

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
        self.toggle_peg(x, y)
                
    
    def draw_circle(self, x, y, is_empty):
        column_width = GAME_WIDTH/len(self.model[0])
        column_height = GAME_HEIGHT/len(self.model)
        x0 = x * column_width + (column_width - HOLE_RADIUS)/2
        y0 = y * column_height + (column_height- HOLE_RADIUS)/2
        x1 = x0 + HOLE_RADIUS
        y1 = y0 + HOLE_RADIUS
        if is_empty:
            self.canvas.create_oval(x0, y0, x1, y1, fill=HOLE_COLOR)
        else:
            self.canvas.create_oval(x0, y0, x1, y1, fill=PEG_COLOR)


    def toggle_peg(self, x, y):
        if self.model[y][x] == 0:
            return
        self.model[y][x] *= -1
        self.draw_circle(x, y, self.model[y][x] == - 1)



if __name__ == '__main__':
    app = Application()
    app.start()