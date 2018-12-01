from sense_hat import SenseHat

from random import randint

sense = SenseHat()

bricks = []
selectedBrick = None

black = (0, 0, 0)
white = (255, 255, 255)
cyan = (0, 255, 255)
blue = (0, 0, 255)
orange = (255, 100, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
magenta = (255, 0, 255)
red = (255, 0, 0)

pixels = [black for i in range(64)]
occupied = [[False for x in range(8)] for y in range(8)]

types = [
    [
        [[cyan, cyan, cyan, cyan]],

        [[cyan],
        [cyan],
        [cyan],
        [cyan]],

        [[cyan, cyan, cyan, cyan]],


        [[cyan],
        [cyan],
        [cyan],
        [cyan]]
    ],
    [
        [[blue, 0, 0],
        [blue, blue, blue]],
        
        [[blue, blue],
        [blue, 0],
        [blue, 0]],
        
        [[blue, blue, blue],
        [0, 0, blue]],
        
        [[0, blue],
        [0, blue],
        [blue, blue]]
    ],
    [
        [[0, 0, orange],
        [orange, orange, orange]],

        [[orange, 0],
        [orange, 0],
        [orange, orange]],

        [[orange, orange, orange],
        [orange, 0, 0]],

        [[orange, orange],
        [0, orange],
        [0, orange]]
    ],
    [
        [[yellow, yellow],
        [yellow, yellow]],
        
        [[yellow, yellow],
        [yellow, yellow]],
        
        [[yellow, yellow],
        [yellow, yellow]],
        
        [[yellow, yellow],
        [yellow, yellow]]
    ],
    [
        [[0, green, green],
        [green, green, 0]],

        [[green, 0],
        [green, green],
        [0, green]],

        [[0, green, green],
        [green, green, 0]],

        [[green, 0],
        [green, green],
        [0, green]]
    ],
    [
        [[0, magenta, 0],
        [magenta, magenta, magenta]],

        [[magenta, 0],
        [magenta, magenta],
        [magenta, 0]],

        [[magenta, magenta, magenta],
        [0, magenta, 0]],

        [[0, magenta],
        [magenta, magenta],
        [0, magenta]]
    ],
    [
        [[red, red, 0],
        [0,   red, red]],

        [[0, red],
        [red, red],
        [red, 0]],

        [[red, red, 0],
        [0,   red, red]],

        [[0, red],
        [red, red],
        [red, 0]]
    ]
]

def clearPixels():
    global pixels
    for x in range(8):
        for y in range(8):
            if not occupied[x][y]:
                pixels[x + y * 8] = black

def setPixel(x, y, c):
    if x < 8 and not occupied[x][y]:
        pixels[x + y * 8] = c

def addBrick(b):
    bricks.append(b)

class Brick:
    def __init__(self, type, rotation, xpos, ypos):
        self.type = type
        self.rotation = rotation
        self.xpos = xpos
        self.ypos = ypos
    
    def render(self):
        for y in range(len(types[self.type][self.rotation])):
            for x in range(len(types[self.type][self.rotation][y])):
                if types[self.type][self.rotation][y][x] != 0:
                    setPixel(self.xpos + x, self.ypos + y, types[self.type][self.rotation][y][x])


    def dropped(self):
        if self.ypos + len(types[self.type][self.rotation]) - 1 >= 7:
            return True
        
        dropped = False
        for i in range(len(types[self.type][self.rotation][0])):
            if occupied[self.xpos + i][self.ypos + len(types[self.type][self.rotation]) - 1]:
                dropped = True
        return dropped

    def markActives(self):
        for y in range(len(types[self.type][self.rotation])):
            for x in range(len(types[self.type][self.rotation][y])):
                if types[self.type][self.rotation][y][x] != 0:
                    occupied[self.xpos + x][self.ypos + y] = True

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
    
    def right(self):
        if self.xpos < 8 - len(types[self.type][self.rotation][0]):
            self.xpos += 1
    
    def left(self):
        if self.xpos > 0:
            self.xpos -= 1

    def down(self):
        self.ypos += 1

    def drop(self):
        while not self.dropped():
            self.down()

def newBrick():
    return Brick(randint(0, 6), 0, 3, 0)
    

def gameLoop():
    global selectedBrick

    if selectedBrick.dropped():
         
        selectedBrick.markActives()
        selectedBrick = newBrick()

    for i in range(len(occupied)):
        if all(cell[i] for cell in occupied):
            print('Yay')
            for j in range(i - 1, 0):
                occupied[j + 1] = occupied[j]
    
    for event in sense.stick.get_events():
        if event.direction == 'up' and event.action == 'pressed':
            selectedBrick.rotate();
        if event.direction == 'right' and event.action != 'released':
            selectedBrick.right();
        if event.direction == 'left' and event.action != 'released':
            selectedBrick.left();
        if event.direction == 'down' and event.action != 'released':
            selectedBrick.down();
        if event.direction == 'middle' and event.action == 'released':
            selectedBrick.drop();
    
    clearPixels()
    
    selectedBrick.render()
    sense.set_pixels(pixels)


selectedBrick = newBrick()

while True:
    gameLoop()
