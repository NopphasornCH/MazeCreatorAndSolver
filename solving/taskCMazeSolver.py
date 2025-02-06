# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Task C solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

from queue import PriorityQueue
from random import seed

class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation.  You'll need to complete its implementation for task C.
    """


    def __init__(self):
        super().__init__()
        self.m_name = "taskC"
        seed(0)



    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        # we call the the solve maze call without the entrance.
        # DO NOT CHANGE THIS METHOD
        self.solveMazeTaskC(maze)



    def solveMazeTaskC(self, maze: Maze3D):
        """       
        solve the maze, used by Task C.
        This version of solveMaze does not provide a starting entrance, and as part of the solution, the method should
        to find the entrance and exit pair (see project specs for requirements of this task).
        TODO: Please complete this implementation for task C.  You should call maze.solved(...) to update which entrance
        and exit you used for task C.

        @param maze: Instance of maze to solve.

        """
        #explore shortest pair using BFS
        entrance,exit = self.find_shortest_pair(maze)
        startCoord: Coordinates3D = entrance
        exitCoord: Coordinates3D = exit
        allcell_inbound = [cell for cell in maze.allCells() if (cell.getRow() >= -1 and cell.getRow() <= maze.rowNum(cell.getLevel()) and 
                                                        cell.getCol() >= -1 and cell.getCol() <= maze.colNum(cell.getLevel()))]

        gScore = {cell:float('inf') for cell in allcell_inbound}
        gScore[startCoord] = 0
        fScore = {cell:float('inf') for cell in allcell_inbound}
        fScore[startCoord] = gScore[startCoord]+self.hScore(startCoord,exitCoord)

        Path = {}
        visited = [startCoord]
        
        PQ = PriorityQueue()
        PQ.put([fScore[startCoord],self.hScore(startCoord,exitCoord),startCoord])

        while not PQ.empty():
            CurrCell = PQ.get()[2]
            #print(CurrCell)
            if CurrCell == exitCoord:
                self.solved(entrance, CurrCell)
                break 
            neighbours = maze.neighbours(CurrCell)
            for neigh in neighbours:
                if not maze.hasWall(CurrCell,neigh):
                    temp_gScore = gScore[CurrCell]+1
                    temp_fScore = temp_gScore+self.hScore(neigh,exitCoord)
                    if temp_fScore < fScore[neigh]:
                        gScore[neigh] = temp_gScore
                        fScore[neigh] = temp_fScore
                        PQ.put([temp_fScore,self.hScore(neigh,exitCoord),neigh])
                        if CurrCell not in visited:
                            Path[neigh] = CurrCell
                            self.solverPathAppend(CurrCell, False)
                        else:
                            self.solverPathAppend(CurrCell, True)

                        
                        

    def hScore(self,cell1: Coordinates3D,exitcell:Coordinates3D):
        """       
        calculate manhattan distance from current cell to exit.
        """
        l,r,c = cell1.getLevel(),cell1.getRow(),cell1.getCol()
        le,re,ce = exitcell.getLevel(),exitcell.getRow(),exitcell.getCol()
        return abs(l-le)+abs(r-re)+abs(c-ce)

    #exploration phase using BFS       
    def find_shortest_pair(self, maze: Maze3D):
        """       
        find shortest pair of entrance and exit using BFS.
        """
        startCoord: list = maze.getEntrances()
        pairs = {}
        
        for start_cell in startCoord:
            X = 0
            frontier = [start_cell]
            visited = {start_cell}
            exits = []

            while frontier:
                CurrCell = frontier.pop(0)
                if (CurrCell.getRow() < 0 or CurrCell.getRow() == maze.rowNum(CurrCell.getLevel()) or \
                    CurrCell.getCol() < 0 or CurrCell.getCol() == maze.colNum(CurrCell.getLevel())) and (CurrCell not in startCoord):
                    exits.append(CurrCell)
                    break

                neighbours = maze.neighbours(CurrCell)
                for neigh in neighbours:
                    if neigh not in visited and not maze.hasWall(CurrCell,neigh):
                        frontier.append(neigh)
                        visited.add(neigh)

            X = len(visited)
            if start_cell not in pairs:
                pairs[start_cell] = {}
            for exit_cell in exits:
                pairs[start_cell][exit_cell] = X
        i = 0
        min_explored = float('inf')
        shortest_pair = None

        for pair, exit_cells in pairs.items():
            for exit_cell, number_explored in exit_cells.items():
                if number_explored < min_explored:
                    min_explored = number_explored
                    shortest_pair = (pair, exit_cell)
                    i += 1
                print(f"pair {i}: {pair} to {exit_cell} with {number_explored} cells explored")

        print(f"shortest pair is {shortest_pair[0]} to {shortest_pair[1]} with {min_explored} cells explored.")
        shortest_entrance = shortest_pair[0]
        shortest_exit = shortest_pair[1]
        return shortest_entrance,shortest_exit



        






    

