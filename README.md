# pylibs

###astar: Python Tile-based A* basics

#####Pathfinding as a generator
######Optimizations
- I used a heap-based priority queue to provide O(log N) to Insert and removeMax operations (worst case)
- I stored search intermediary results into tiles (Node class) to remove the Closed list. 

Note: storing intermediary states has the important consequence to constrain concurrency among a set of agents acting in the same world. Below is the study of various patterns working around that constraint.

######Blocking search pattern 
The basic usage of A* is to do a blocking search of a solution (path) in a frame. This is exactly what we do here:
```
iterSearch = astar.search()
while True:
    try:
        path = iterSearch.next()
    except StopIteration:
        break
```
The resut is that it is often the case that a Search operation takes time, and then it stalls a frame. Below is a diagram showing how that approach is slow - assuming search time is constant and pathing is O(1). In reality it is worst since search time is variable and then that approach doesn't guarantee a constant framerate.
```
    +     + + + +     + + + +     + + + + 
A0: S S S P P P G . . . . . . . . . . . S 
A1: . . . . . . S S S P P P G . . . . . .
A2: . . . . . . . . . . . . S S S P P P G
```
(Legend: '+': frame; 'Ax':agent x; 'S':Search operation; 'P':pathing operation; 'G':goal found; '.':stalling)
######Interlaced pattern 
It is not true we need to execute search at every frame. To simulate human-like behaviours it is reasonnable to accept a latency that emulates the thinking process. However the motions of an agent shouldn't be blocked by the search operations of other agents. 
The generator approach allows us not to wait a search is completed to execute behaviours of other agents. Granularity of the search operation is reduced to neighborhood examination which is exactly 8 fast operations in a tile-based world. However since results are stored in the shared world object, searches cannot be concurrent and must be synchronised. 
Below is an example with a very simple state machine:
```
def move(self):
    if self.state == 0 and not Busy:
        Busy = True
        goal = self.world.getSomeLocation()
        self.astar.initSearch(self.location, goal, [obstacles])
        self.state = 1
    elif self.state == 1:
        self.path = self.astar.search()
        if self.path:
            Busy = False
            self.state = 2
    elif self.state == 2:
        self.location = self.path.pop(0)
        if not self.path:
            self.state = 0
```
Note: Busy is a global variable showing example of search synchronization.

Below is another example of diagram showing reduced latencies and constant framerate thanks to generators:
```
    + + + + + + + + + + + + + + + +
A0: S S S P P P G . . S S S P P G .
A1: . . . S S S P P P G . . S S S P
A2: . . . . . . S S S P P P G . . S
```
(Legend: '+': frame; 'Ax':agent x; 'S':Search operation; 'P':pathing operation; 'G':goal found; '.':stalling)
#####Parallel pathfinding using multiprocessing
#####Concurrent pathfinding using a worker pool
(TODO)

###raycats: Tile-based Ray casting
