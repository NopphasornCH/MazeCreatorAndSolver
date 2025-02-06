# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wall following maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from random import seed

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation. You'll need to complete its implementation for task B.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"
        

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        currCell = entrance

        visited = []
        self.solverPathAppend(currCell, False)
        
        dir_from_index = {'north': 0, 'north-east': 1, 'east': 2, 'south': 3, 'south-west': 4, 'west': 5}

        currLevel = currCell.getLevel()
        currRow = currCell.getRow()
        currCol = currCell.getCol()

        # Determine the direction we came from based on the initial position
        if currRow < 0:
            comefrom = 'north'
        elif currLevel == maze.levelNum():
            comefrom = 'north-east'
        elif currCol < 0:
            comefrom = 'east'      
        elif currRow == maze.rowNum():
            comefrom = 'south'        
        elif currLevel < 0:
            comefrom = 'south-west'
        elif currCol == maze.colNum():
            comefrom = 'west'

        index = dir_from_index[comefrom]

        while currCell not in maze.getExits():
            # Reset cells to None to indicate they haven't been set yet
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
            next = (index + 1) % 6  # Ensure 'next' wraps around properly

            while m:
                wall = True
                if next == 0:
                    if Ncell is not None:
                        wall = maze.hasWall(currCell, Ncell)
                    if not wall:
                        currCell = Ncell
                        if currCell not in visited:
                            visited.append(currCell)
                            self.solverPathAppend(currCell, False)
                        else:
                            self.solverPathAppend(currCell, True)
                        index = 3  # South
                        m = False
                    else:
                        next = (next + 1) % 6
                elif next == 1:
                    if NEcell is not None:
                        wall = maze.hasWall(currCell, NEcell)
                    if not wall:
                        currCell = NEcell
                        if currCell not in visited:
                            visited.append(currCell)
                            self.solverPathAppend(currCell, False)
                        else:
                            self.solverPathAppend(currCell, True)
                        index = 4  # South-West
                        m = False
                    else:
                        next = (next + 1) % 6
                elif next == 2:
                    if Ecell is not None:
                        wall = maze.hasWall(currCell, Ecell)
                    if not wall:
                        currCell = Ecell
                        if currCell not in visited:
                            visited.append(currCell)
                            self.solverPathAppend(currCell, False)
                        else:
                            self.solverPathAppend(currCell, True)
                        index = 5  # West
                        m = False
                    else:
                        next = (next + 1) % 6
                elif next == 3:
                    if Scell is not None:
                        wall = maze.hasWall(currCell, Scell)
                    if not wall:
                        currCell = Scell
                        if currCell not in visited:
                            visited.append(currCell)
                            self.solverPathAppend(currCell, False)
                        else:
                            self.solverPathAppend(currCell, True)
                        index = 0  # North
                        m = False
                    else:
                        next = (next + 1) % 6
                elif next == 4:
                    if SWcell is not None:
                        wall = maze.hasWall(currCell, SWcell)
                    if not wall:
                        currCell = SWcell
                        if currCell not in visited:
                            visited.append(currCell)
                            self.solverPathAppend(currCell, False)
                        else:
                            self.solverPathAppend(currCell, True)
                        index = 1  # North-East
                        m = False
                    else:
                        next = (next + 1) % 6
                elif next == 5:
                    if Wcell is not None:
                        wall = maze.hasWall(currCell, Wcell)
                    if not wall:
                        currCell = Wcell
                        if currCell not in visited:
                            visited.append(currCell)
                            self.solverPathAppend(currCell, False)
                        else:
                            self.solverPathAppend(currCell, True)
                        index = 2  # East
                        m = False
                    else:
                        next = (next + 1) % 6

        if currCell in maze.getExits():
            self.solved(entrance, currCell)
            print(f"Exit found at: {currCell}")
        else:
            print("No exit found.")
                
                



                    


                               




                
        
           

        
            


        
        
                
            
    
        