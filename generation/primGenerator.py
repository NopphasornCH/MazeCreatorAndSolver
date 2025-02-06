# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Prim's maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

from random import randint, choice
from collections import deque

class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator.  
    TODO: Complete the implementation (Task A)
    """
	

    def generateMaze(self, maze:Maze3D):
        # TODO: Implement this method for task A.

        #start with all walls
        maze.initCells(True)

        # select starting cell 
		# random floor
        startLevel = randint(0, maze.levelNum()-1)
        startCoord : Coordinates3D = Coordinates3D(startLevel, randint(0, maze.rowNum(startLevel)-1), randint(0, maze.colNum(startLevel)-1))

        totalCells = sum([maze.rowNum(l) * maze.colNum(l) for l in range(maze.levelNum())])
        
        ####
        visited : set[Coordinates3D] = set([startCoord])
        frontier_set = set()
        nb_inmaze = []
			
        while len(visited)<totalCells:
            for cell in visited:
                neighbours : list[Coordinates3D] = maze.neighbours(cell)
                nb_inbound = [neigh for neigh in neighbours if neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and\
												neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel())]
                frontier_set.update(nb_inbound)
            for cell in list(frontier_set):
                if cell in visited:      
                    frontier_set.remove(cell)
            new_vertex = choice(tuple(frontier_set))
            visited.add(new_vertex)
            frontier_set.remove(new_vertex)
            nb_of_newV = list(maze.neighbours(new_vertex))
            nb_of_newV_inbound = [neigh for neigh in nb_of_newV if neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and\
												neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel())]
            for c in nb_of_newV_inbound:
                if c in visited:
                    nb_inmaze.append(c)
            if len(nb_inmaze)>1:
                curr = choice(nb_inmaze)
            else:
                curr = nb_inmaze[0]
            maze.removeWall(new_vertex,curr)
            #restet frontier and nb_inmaze every time that we add new vertex
            nb_inmaze=[]

        self.m_mazeGenerated = True    


        