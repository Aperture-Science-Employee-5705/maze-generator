import ILib, random
#need my PNG image writer to run


import numpy, cv2
#these are only used for the fun debug thing and the threshold function
#i could have used cv2 to write images too instead of my own library for that but whatever


class stack:# a stack
    def __init__(self):
        self.__stack = []
    def push(self, item):
        self.__stack.append(item)
        return True
    def pop(self):
        l = len(self.__stack)
        if l == 0:
            return
        return self.__stack.pop(l-1)
    def top(self):
        return self.__stack[len(self.__stack)-1]
    def size(self):
        return len(self.__stack)
    def __repr__(self):
        return f'<stack of {self.size()} items>'

class node:
    def __init__(self, Id, x, y, n=False, e=False, s=False, w=False):
        self.id = Id
        self.x, self.y = x, y#id, position and connection info
        self.n = (False if n in [False, 0, -1] else True)
        self.e = (False if e in [False, 0, -1] else True)
        self.s = (False if s in [False, 0, -1] else True)
        self.w = (False if w in [False, 0, -1] else True)
        self.visited = False
        self.draw = True
    def __repr__(self):
        n = (1 if self.n else 0)
        e = (1 if self.e else 0)
        s = (1 if self.s else 0)
        w = (1 if self.w else 0)
        return f'<node {self.id} [{self.x},{self.y}] {n} {e} {s} {w}>'

class Maze:
    def __init__(self, nodes):
        self.start = None#set stuff up
        self.end = None
        self.nodes = nodes
        self.size = len(nodes), len(nodes[0])
    def setStart(self, startx, starty):#add start position
        self.start = startx, starty
    def setEnd(self, endx, endy):#add end position
        self.end = endx, endy
    def __repr__(self):
        start = (self.start if self.start != None else '(undefined)')
        end = (self.end if self.end != None else '(undefined)')
        return f'<maze {self.size[0]}x{self.size[1]} start{start} end{end}>'
    def __str__(self):
        return '\n'.join(['\t'.join([str(n) for n in y]) for y in self.nodes])#return all nodes (string format)
    
def renderMaze(maze, wall=(0,)*3, space=(255,)*3, Start=(255, 0, 0), End=(0, 255, 0)):
    '''renders the maze as an image in the format of a three dimensional array
       renders the maze with thin paths
       maze - maze object input
       wall, space, Start, End - the colour pallet to be used in the image'''
    img = [[wall for x in range(maze.size[1]*3)] for y in range(maze.size[0]*3)]#generate blank image
    for row in maze.nodes:
        for Node in row:#loop over node array
            if Node == None:
                continue
            if not Node.draw:
                continue
            xcoord, ycoord = Node.x*3 + 1, Node.y*3 + 1#get coords in image
            img[ycoord][xcoord] = space
            if Node.n == 1:#link stuff up
                img[ycoord][xcoord - 1] = space
            if Node.s == 1:
                img[ycoord][xcoord + 1] = space
            if Node.e == 1:
                img[ycoord + 1][xcoord] = space
            if Node.w == 1:
                img[ycoord - 1][xcoord] = space
    start, end = maze.start, maze.end
    if start != None:#add start and end pixel
        img[start[1]*3+1][start[0]*3+1] = Start
    if end != None:
        img[end[1]*3+1][end[0]*3+1] = End
    return img

def renderMaze2(maze, wall=(0,)*3, space=(255,)*3, Start=(255, 0, 0), End=(0, 255, 0)):
    '''renders the maze as an image in the format of a three dimensional array
       renders the maze with thin walls and a thick path
       maze - maze object input
       wall, space, Start, End - the colour pallet to be used in the image'''
    img = [[wall for x in range(maze.size[1]*5)] for y in range(maze.size[0]*5)]#generate blank image
    for row in maze.nodes:
        for Node in row:#loop over node array
            if Node == None:
                continue
            if not Node.draw:
                continue
            xcoord, ycoord = Node.x*5 + 2, Node.y*5 + 2#get coords in image
            for x in range(-1, 2):
                for y in range(-1, 2):
                    img[ycoord+y][xcoord+x] = space
            if Node.n == 1:#link stuff up
                img[ycoord + 1][xcoord - 2] = space
                img[ycoord    ][xcoord - 2] = space
                img[ycoord - 1][xcoord - 2] = space
            if Node.s == 1:
                img[ycoord + 1][xcoord + 2] = space
                img[ycoord    ][xcoord + 2] = space
                img[ycoord - 1][xcoord + 2] = space
            if Node.e == 1:
                img[ycoord + 2][xcoord + 1] = space
                img[ycoord + 2][xcoord    ] = space
                img[ycoord + 2][xcoord - 1] = space
            if Node.w == 1:
                img[ycoord - 2][xcoord + 1] = space
                img[ycoord - 2][xcoord    ] = space
                img[ycoord - 2][xcoord - 1] = space
    start, end = maze.start, maze.end
    if start != None:#add start and end pixel
            for x in range(-1, 2):
                for y in range(-1, 2):
                    img[start[1]*5+2+y][start[0]*5+2+x] = Start
    if end != None:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    img[end[1]*5+2+y][end[0]*5+2+x] = End
    return img

#small = Maze([[node(0,  0, 0, -1,  1,  4, -1), node(1,  1, 0, -1,  2,  5,  0), node(2,  2, 0, -1,  1, -1,  1), node(3,  3, 0, -1, -1,  1,  1)],
#              [node(4,  0, 1,  1, -1,  8, -1), node(5,  1, 1,  1,  6,  9,  1), node(6,  2, 1, -1, -1,  1,  1), node(7,  3, 1,  1, -1,  1, -1)],
#              [node(8,  0, 2,  4,  9, -1, -1), node(9,  1, 2,  1, -1,  1,  1), node(10, 2, 2,  1,  1, -1, -1), node(11, 3, 2,  1, -1,  1, -1)],
#              [node(12, 0, 3, -1, 13, -1, -1), node(13, 1, 3,  1, -1, -1,  1), node(14, 2, 3, -1,  1, -1, -1), node(15, 3, 3,  1, -1, -1,  1)]])


#img = renderMaze(small)
#ILib.write(img, 'maze')
#print(small)

def generateMaze(width, height, interlinkProbablility=.0, maxInterlinks=-1, mask=None, longRunProbability=0.01, longRunMinMax=(10,20), maxLongRuns=-1):
    '''generates a maze of height x width
       interlinkProbablility, a float between 0, 1 - determines the probability of genetrating interlinks that can form loops, normally 0.0 (should be kept low)
       mask, a 2D array of 1's and 0's determining where the maze path should be generated (1 = generate, 0 = do not generate)'''
    
    assert width  > 0 ,f'width must be greater than 0!\n not {width}!'
    assert height > 0 ,f'height must be greater than 0!\n not {height}!'

    assert interlinkProbablility <= 1 and interlinkProbablility >= 0, 'the interlinkProbablility must be a float between 0, 1'
    assert longRunProbability <= 1 and longRunProbability >= 0, 'the longRunProbability must be a float between 0, 1'
    longRunMinMax = min(longRunMinMax), max(longRunMinMax)#ensure they are in order
    if mask != None:
        assert (len(mask) == height) and (len(mask[0]) == width), 'error! mask dimensions must be the same as maze'

    
    maze = [[node(height*y+x, x, y) for x in range(width)] for y in range(height)]
    positions = stack()#create the maze and the stack
    total, done = width*height, 0

    if mask != None:
        for y, row in enumerate(mask):
            for x, item in enumerate(row):#mark all 0'ed out elements in mask as visited and done
                if item == 0:
                    maze[y][x].visited = True
                    maze[y][x].draw = False#also mark them to not be drawn
                    done += 1

    def findNextUnvisited():
        for y, row in enumerate(maze):
            for x, item in enumerate(row):#search through entire maze to find unvisited points
                if not maze[y][x].visited:
                    return y, x
        return current

    current = findNextUnvisited()#set start point
    
    backtracking = False
    interlinkCount = 0
    LRcount = 0
    LRsteps = 0
    prevDirection = (0, 0)
    
    while done != total:#while there are still nodes to link up to
        
        avaliable = []
        avaliableInterlink = []
        for p in [[0, 1], [1, 0], [0, -1], [-1, 0]]:#all next possible moves to be checked
            
            nx, ny = current[0]+p[0], current[1]+p[1]#calculate new coordinates
            if (nx < 0 or nx > height-1) or (ny < 0 or ny > width-1):#check if coordinates are in bounds
                continue
            if maze[nx][ny].visited:#if already visited normal movement is invalid, roll for possible interlink and skip normal movement
                if (random.uniform(0,1) < interlinkProbablility) and (interlinkCount != maxInterlinks) and (not backtracking):#never interlink during backtracks - it messes everything up
                    avaliableInterlink.append([nx, ny])
                continue
            avaliable += [[nx, ny],]#add the move to avaliable moves list

        if random.uniform(0, 1) < longRunProbability and (LRcount < maxLongRuns or maxLongRuns == -1) and LRsteps == 0:
            LRsteps = random.randint(longRunMinMax[0], longRunMinMax[1])#if a long run is started, set the step counter to a random number of moves in range
            LRcount += 1#increase the long run count
         
        if LRsteps > 0:#if during a long run and the current move is valid
            new = [prevDirection[0]+current[0], prevDirection[1]+current[1]]
            if list(prevDirection) != (0, 0) and not backtracking and new in avaliable:
                avaliable = [new,]#if the previous move is possible, ensure it repeats
                LRsteps -= 1
            elif random.randint(0,1) == 1:#50% chance of a long run cancelling on invalid
                LRsteps = 0
        
        if len(avaliableInterlink) > 0:
            link = random.choice(avaliableInterlink)#all of this is the same as the stuff below, check those comments down there instead
            move = link[0]-current[0], link[1]-current[1]
            #interlinker logic
            if move == (0, -1):#link north
                maze[current[0]][current[1]].n = 1
                maze[link[0]][link[1]].s = 1
            elif move == (1, 0):#link east
                maze[current[0]][current[1]].e = 1
                maze[link[0]][link[1]].w = 1
            elif move == (0, 1):#link south
                maze[current[0]][current[1]].s = 1
                maze[link[0]][link[1]].n = 1
            else:#               link west
                maze[current[0]][current[1]].w = 1
                maze[link[0]][link[1]].e = 1
            interlinkCount += 1#increase interlink counter
        
        if len(avaliable) > 0:#if there are possible moves
            new = random.choice(avaliable)#select a move
            move = new[0]-current[0], new[1]-current[1]#basically get back what p was
            #could have just added p to the avaliable list instead but oh well
            
            #linker logic
            if move == (0, -1):#link north
                #print('north')
                maze[current[0]][current[1]].n = 1
                maze[new[0]][new[1]].s = 1
            elif move == (1, 0):#link east
                #print('east')
                maze[current[0]][current[1]].e = 1
                maze[new[0]][new[1]].w = 1
            elif move == (0, 1):#link south
                #print('south')
                maze[current[0]][current[1]].s = 1
                maze[new[0]][new[1]].n = 1
            else:#               link west
                #print('west')
                maze[current[0]][current[1]].w = 1
                maze[new[0]][new[1]].e = 1
            
            maze[new[0]][new[1]].visited = True#mark next node as visited
            positions.push(current)#            and push to the stack
            backtracking = False#if we were already backtracking - stop that
            done += 1
            current = new#move to new node
            prevDirection = move
        else:#if there were no avaliable moves - backtrack or find the next unvisited if possible
            prevDirection = (0, 0)#dont allow long runs directly after
            if positions.size() > 0:
                prev = current
                current = positions.pop()
                backtracking = True
            else:
                new = findNextUnvisited()
                if new == current:
                    break
                current = new

        
        #       FUN DEBUG ANIMATION THINGY (NEEDS cv2, numpy)
        #
        #pathCol = (((1.0, 1.0, 0.0) if LRsteps > 0 else (1. ,)*3) if not backtracking else (0.0, 1.0, 1.0))
        #M = Maze(maze)
        #if backtracking:
        #    print(f'backtracking at {current}')
        #    M.setStart(current[1], current[0])
        #if LRsteps > 0:
        #    print(f'long run #{LRcount+1} step : {LRsteps}')
        #    M.setStart(current[1], current[0])
        #cv2.imshow('maze generation debug', cv2.resize(numpy.array(renderMaze(M, (0.,)*3, pathCol, (0.0, 0.0, 1.0))), (width*20, height*20), interpolation=cv2.INTER_NEAREST))
        #cv2.waitKey(2)
    return Maze(maze)

def generateCircleMaze(radius=100, hollow=False, hollowThickness=10, interlinkProbablility=.0, maxInterlinks=5, longRunProbability=0.01, longRunMinMax=(10,20), maxLongRuns=-1):
    if not hollow:
        mask = [[(1 if ((x-(radius-1))*(x-(radius-1)) + (y-(radius-1))*(y-(radius-1)))**0.5 <= radius else 0) for x in range(radius*2)] for y in range(radius*2)]
    else:
        mask = [[(1 if ((((x-(radius-1))*(x-(radius-1)) + (y-(radius-1))*(y-(radius-1)))**0.5 <= radius) and not (((x-(radius-1))*(x-(radius-1)) + (y-(radius-1))*(y-(radius-1)))**0.5 <= radius-hollowThickness)) else 0) for x in range(radius*2)] for y in range(radius*2)]
    return generateMaze(radius*2, radius*2, interlinkProbablility, maxInterlinks, mask, longRunProbability, longRunMinMax, maxLongRuns)

def mazeFromImage(img, binaryThreshold=128, interlinkProbablility=.0, maxInterlinks=5, longRunProbability=0.01, longRunMinMax=(10,20), maxLongRuns=-1):
    timg = cv2.threshold(img, binaryThreshold, 255, cv2.THRESH_BINARY)
    mask = [[int(x[0]*255) for x in y] for y in timg[1]]
    
    return generateMaze(timg[1].shape[1], timg[1].shape[0], interlinkProbablility, maxInterlinks, mask, longRunProbability, longRunMinMax, maxLongRuns)

if __name__ == "__main__":#if being run directly and not imported
    #mask = [[(1 if (x < 20 and x > 10) or (x < 40 and x > 30) else 0) for x in  range(50)] for y in range(50)]
    
    m = generateMaze(200, 200, 0.05)#CircleMaze(100, True, 90, longRunProbability=0.005, longRunMinMax=(20, 150))#(50, 50, 0.15, 5)#, mask)
    m.setStart(99,0)
    m.setEnd(9,199)
    
    img = renderMaze2(m)
    ILib.write(img, 'maze')
    img = renderMaze(m)
    ILib.write(img, 'maze - thin')




#wow - i actually commented my code for once
#lol
