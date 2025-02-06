# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wilson's algorithm maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from random import randint, choice
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator


class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """
	
    def generateMaze(self, maze:Maze3D):
        # TODO: Implement this method for task A.

        # make sure we start the maze with all walls there
        maze.initCells(True)

        # select starting cell 
		# random floor
        startLevel = randint(0, maze.levelNum()-1)
        startCoord : Coordinates3D = Coordinates3D(startLevel, randint(0, maze.rowNum(startLevel)-1), randint(0, maze.colNum(startLevel)-1))
        
        #initialise 
        finalised : set[Coordinates3D] = set([startCoord])
        unvisited: set = set(maze.allCells())
        unvisited= set([cell for cell in unvisited if cell.getRow() >= 0 and cell.getRow() < maze.rowNum(cell.getLevel()) and\
												cell.getCol() >= 0 and cell.getCol() < maze.colNum(cell.getLevel())])
        unvisited.remove(startCoord)
        #
        while unvisited:
            #find path
            curr = choice(tuple(unvisited))
            passage ={}
            passage_final = {}
            while curr not in finalised:
                neighbours_curr = maze.neighbours(curr)
                nb_inbound = [neigh for neigh in neighbours_curr if neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and\
												neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel())]
                next = choice(tuple(nb_inbound))
                #update direction using dictionary
                passage[curr] = next
                curr = next
            ## manage passage!
            ## add code to backtrack 
            # Filter passage to include only paths leading to a finalised cell
            passage_final = {}
            prev = list(passage.keys())[0]
            while prev not in finalised:
                next_cell = passage[prev]
                passage_final[prev] = next_cell
                prev = next_cell

            finalised.update(passage_final.keys())
            for cell1,cell2 in passage_final.items():
                maze.removeWall(cell1,cell2)
            unvisited.difference_update(passage_final.keys())
        
        self.m_mazeGenerated = True 
        

		
        
        
		