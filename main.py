from tkinter import *

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

        label = Label(self.window, text= 'Hello, Yassin!', font= ('Arial', 40))
        label.pack()

        # setup canvas
        self.canvas = Canvas(self.window, width= GAME_WIDTH, height= GAME_HEIGHT, bg= BACKGROUND_COLOR)
        self.canvas.pack()

    def start(self):
        board = Board(self.canvas)
        self.window.mainloop()

class Board:
    def __init__(self, canvas):
        # 2 => Draw a peg on canvas
        # 1 => Draw empty hole on canvas
        # 0 => Do not draw anything on cavas
        self.canvas = canvas
        self.board = [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 2, 0, 2, 0, 0],
            [0, 2, 0, 2, 0, 2, 0],
            [2, 0, 2, 0, 2, 0, 2],
        ]
        self.draw_board()
        self.setup_interactions()
    
    def draw_board(self):
        for y in range(len(self.board)):
            row = self.board[y]
            for x in range (len(row)):
                column_width = GAME_WIDTH/len(row)
                column_height = GAME_HEIGHT/len(self.board)
                x0 = x * column_width + (column_width - HOLE_RADIUS)/2
                y0 = y * column_height+ (column_height- HOLE_RADIUS)/2
                x1 = x0 + HOLE_RADIUS
                y1 = y0 + HOLE_RADIUS
                if row[x] == 2:
                    self.canvas.create_oval(x0, y0, x1, y1, fill=PEG_COLOR)
                elif row[x] == 1:
                    self.canvas.create_oval(x0, y0, x1, y1, fill=HOLE_COLOR)
    
    def setup_interactions(self):
        self.canvas.bind('<Button>', self.did_click_canvas)

    def did_click_canvas(self, event):
        print('(yassini)', event.x, event.y)
        # convert event coordinates to self.board index


if __name__ == '__main__':
    app = Application()
    app.start()