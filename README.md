<header>

<!--
  <<< Author notes: Course header >>>
  Include a 1280×640 image, course title in sentence case, and a concise description in emphasis.
  In your repository settings: enable template repository, add your 1280×640 social image, auto delete head branches.
  Add your open source license, GitHub uses MIT license.
-->

# Algorithm and Analysis: Maze Generator and Maze Solver Project

_An assignment of Algorithm and Analysis to implement a number of basic data structures for developing
 a maze generation program and evaluate their performance to determine what would be
 the best data structure in different situations._

</header>

## Maze Generator 
I implement a maze generator using Prim's and Wilson's algorithm

**Prim's Core Logic**

*1.  Initialization*
Starts with all walls intact `(initCells(True))`
Randomly selects a starting cell across maze levels

*2.  Frontier Expansion*
Maintains two sets: `visited` (completed cells) and `frontier_set` (boundary cells)
Iteratively finds all valid neighbors (`nb_inbound`) of visited cells to populate frontier

*3.  Maze Growth*
Randomly selects new cell from frontier `(choice(tuple(frontier_set)))`
Identifies existing maze neighbors (`nb_inmaze`) of newly added cell
Breaks wall between new cell and randomly chosen neighbor (`removeWall()`)

*4.  Termination*
Continues until all cells are visited `(while len(visited)<totalCells)`

**Wilson's Core Logic**

*1.  Initialization*
Starts with all walls intact `(initCells(True))`
Randomly selects starting cell and initializes two sets:
`finalised` (completed cells)
`unvisited` (all other valid cells)

*2.  Random Walk Phase*
Selects random cell from unvisited as path start
Performs random walk until reaching finalised cells:
Tracks path through passage dictionary
Selects random valid neighbors at each step

*3.  Path Integration*
Backtracks from first finalised cell to path start
Preserves valid path segment in `passage_final`
Removes walls between consecutive cells in path

*4.  Set Updates*
Adds path cells to finalised set
Removes path cells from unvisited
Repeats until unvisited is empty
