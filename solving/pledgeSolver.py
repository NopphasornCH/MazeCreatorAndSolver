# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Pledge maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from random import seed


class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"
        self.turns = 0  # Turn counter

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        currCell = entrance
        self.visited = [currCell]

        dir_from_index = {0: 'north', 1: 'north-east', 2: 'east', 3: 'south', 4: 'south-west', 5: 'west'}

        currLevel = currCell.getLevel()
        currRow = currCell.getRow()
        currCol = currCell.getCol()

        # Determine the direction we came from based on the initial position
        if currRow < 0:
            currdir = 'north'
            index = 0
        elif currLevel == maze.levelNum():
            currdir = 'north-east'
            index = 1
        elif currCol < 0:
            currdir = 'east'
            index = 2
        elif currRow == maze.rowNum():
            currdir = 'south'
            index = 3
        elif currLevel < 0:
            currdir = 'south-west'
            index = 4
        elif currCol == maze.colNum():
            currdir = 'west'
            index = 5

        comefrom_index = (index + 3) % 6  # facing opposite from comefrom
        comefrom = dir_from_index[comefrom_index]
        preferdir = currdir

        while currCell not in maze.getExits():
            # Move straight ahead if possible
            hitwall,fwdcell = self.hit_wall(maze, currCell, preferdir)
            while hitwall == False:
                currCell =fwdcell
                if currCell not in self.visited:
                    self.visited.append(currCell)
                    self.solverPathAppend(currCell, False)
                else:
                    self.solverPathAppend(currCell, True)
                hitwall, fwdcell = self.hit_wall(maze, currCell, preferdir)
                if fwdcell is None:
                    fwdcell = currCell
                if currCell in maze.getExits():
                    self.solved(entrance, currCell)
                    break

            angle = self.check_turn_angle(currdir)
            comefrom_index,currCell = self.turn_direction(maze,currCell,comefrom_index)
            comefrom = dir_from_index[comefrom_index]
            currdir_index = (comefrom_index+3)%6
            currdir = dir_from_index[currdir_index]
            Turning = angle[currdir]
            self.turns += Turning
            while self.turns != 0:
                angle = self.check_turn_angle(currdir)
                comefrom_index, currCell = self.turn_direction(maze, currCell, comefrom_index)
                comefrom = dir_from_index[comefrom_index]
                currdir_index = (comefrom_index + 3) % 6
                currdir = dir_from_index[currdir_index]
                Turning = angle[currdir]
                self.turns += Turning
                hitwall, fwdcell = self.hit_wall(maze, currCell, currdir)     
                # in-case the exit found berfore prefer direction     
                if currCell in maze.getExits():
                    self.solved(entrance, currCell)
                    break
            self.turns = 0

        if currCell in maze.getExits():
            self.solved(entrance, currCell)
            print(f"Exit found at: {currCell}")
        else:
            print("No exit found.")

    def check_turn_angle(self,currdir):
        #using left-hand rule
        if currdir == 'north':
            angle = {'north':0,
                     'north-east':45,
                     'east':90,
                     'south':180,
                     'south-west':-135,
                     'west':-90}
        elif currdir == 'north-east':
            angle = {'north':-45,
                     'north-east':0,
                     'east':45,
                     'south':135,
                     'south-west':180,
                     'west':-135}
        elif currdir == 'east':
            angle = {'north':-90,
                     'north-east':-45,
                     'east':0,
                     'south':90,
                     'south-west':135,
                     'west':180}
        elif currdir == 'south':
            angle = {'north':180,
                     'north-east':-135,
                     'east':-90,
                     'south':0,
                     'south-west':45,
                     'west':90}
        elif currdir == 'south-west':
            angle = {'north':135,
                     'north-east':180,
                     'east':-135,
                     'south':-45,
                     'south-west':0,
                     'west':45}
        elif currdir == 'west':
            angle = {'north':90,
                     'north-east':135,
                     'east':180,
                     'south':-90,
                     'south-west':-45,
                     'west':0}    
        return angle
    
    def turn_direction(self,maze,currCell,comefrom_index):
        Ncell, NEcell, Ecell, Scell, SWcell, Wcell = None, None, None, None, None, None
        neighbours = maze.neighbours(currCell)
        for nb in neighbours:
            if currCell.getLevel() - nb.getLevel() == 1:
                SWcell = nb
            elif currCell.getCol() - nb.getCol() == 1:
                Wcell = nb
            elif nb.getCol() - currCell.getCol() == 1:
                Ecell  = nb
            elif nb.getRow() - currCell.getRow() == 1:
                Ncell = nb
            elif currCell.getRow() - nb.getRow() == 1:
                Scell = nb
            elif nb.getLevel() - currCell.getLevel() == 1:
                NEcell = nb
            
        m = True
        next = (comefrom_index + 1) % 6 
        while m:
            wall = True
            if next == 0:
                #print('Check North')
                if Ncell is not None:
                    wall = maze.hasWall(currCell, Ncell)
                if not wall:
                    currCell = Ncell
                    if currCell not in self.visited:
                        self.visited.append(currCell)
                        self.solverPathAppend(currCell, False)
                    else:
                        self.solverPathAppend(currCell, True)
                    comefrom_index = 3  # mean come from South
                    m = False
                else:
                    next = (next + 1) % 6
            elif next == 1:
                #print('Check North-East')
                if NEcell is not None:
                    wall = maze.hasWall(currCell, NEcell)
                if not wall:
                    currCell = NEcell
                    if currCell not in self.visited:
                        self.visited.append(currCell)
                        self.solverPathAppend(currCell, False)
                    else:
                        self.solverPathAppend(currCell, True)
                    comefrom_index = 4  # mean come from South-West
                    m = False
                else:
                    next = (next + 1) % 6
            elif next == 2:
                #print('Check East')
                if Ecell is not None:
                    wall = maze.hasWall(currCell, Ecell)
                if not wall:
                    currCell = Ecell
                    if currCell not in self.visited:
                        self.visited.append(currCell)
                        self.solverPathAppend(currCell, False)
                    else:
                        self.solverPathAppend(currCell, True)
                    comefrom_index = 5  # mean come from West
                    m = False
                else:
                    next = (next + 1) % 6
            elif next == 3:
                #print('Check South')
                if Scell is not None:
                    wall = maze.hasWall(currCell, Scell)
                if not wall:
                    currCell = Scell
                    if currCell not in self.visited:
                        self.visited.append(currCell)
                        self.solverPathAppend(currCell, False)
                    else:
                        self.solverPathAppend(currCell, True)
                    comefrom_index = 0  # mean come from North
                    m = False
                else:
                    next = (next + 1) % 6
            elif next == 4:
                #print('Check South-West')
                if SWcell is not None:
                    wall = maze.hasWall(currCell, SWcell)
                if not wall:
                    currCell = SWcell
                    if currCell not in self.visited:
                        self.visited.append(currCell)
                        self.solverPathAppend(currCell, False)
                    else:
                        self.solverPathAppend(currCell, True)
                    comefrom_index = 1  # mean come from North-East
                    m = False
                else:
                    next = (next + 1) % 6
            elif next == 5:
                #print('Check West')
                if Wcell is not None:
                    wall = maze.hasWall(currCell, Wcell)
                if not wall:
                    currCell = Wcell
                    if currCell not in self.visited:
                        self.visited.append(currCell)
                        self.solverPathAppend(currCell, False)
                    else:
                        self.solverPathAppend(currCell, True)
                    comefrom_index = 2  # mean come from East
                    m = False
                else:
                    next = (next + 1) % 6
        return comefrom_index,currCell

    def hit_wall(self, maze, currCell, currdir):
        Ncell, NEcell, Ecell, Scell, SWcell, Wcell = None, None, None, None, None, None
        neighbours = maze.neighbours(currCell)
        for nb in neighbours:
            if currCell.getLevel() - nb.getLevel() == 1:
                SWcell = nb
            elif currCell.getCol() - nb.getCol() == 1:
                Wcell = nb
            elif nb.getCol() - currCell.getCol() == 1:
                Ecell = nb
            elif nb.getRow() - currCell.getRow() == 1:
                Ncell = nb
            elif currCell.getRow() - nb.getRow() == 1:
                Scell = nb
            elif nb.getLevel() - currCell.getLevel() == 1:
                NEcell = nb

        if currdir == 'north':
            if Ncell is not None:
                wall = maze.hasWall(currCell, Ncell)
                fwdcell = Ncell
            else:
                wall = True
                fwdcell = None
        elif currdir == 'north-east':
            if NEcell is not None:
                wall = maze.hasWall(currCell, NEcell)
                fwdcell = NEcell
            else:
                wall = True
                fwdcell = None
        elif currdir == 'east':
            if Ecell is not None:
                wall = maze.hasWall(currCell, Ecell)
                fwdcell = Ecell
            else:
                wall = True
                fwdcell = None
        elif currdir == 'south':
            if Scell is not None:
                wall = maze.hasWall(currCell, Scell)
                fwdcell = Scell
            else:
                wall = True
                fwdcell = None
        elif currdir == 'south-west':
            if SWcell is not None:
                wall = maze.hasWall(currCell, SWcell)
                fwdcell = SWcell
            else:
                wall = True
                fwdcell = None
        elif currdir == 'west':
            if Wcell is not None:
                wall = maze.hasWall(currCell, Wcell)
                fwdcell = Wcell
            else:
                wall = True
                fwdcell = None
        return wall, fwdcell
                    

            





                







    



    




                    
                        

            









	
