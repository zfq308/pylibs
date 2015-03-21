# pylibs

###astar: Python Tile-based A* basics

#####Pathfinding as a generator
######Optimizations
- I used a heap-based priority queue to provide O(log N) to Insert and removeMax operations (worst case)
- I stored search intermediary results into tiles (Node class) to remove the Closed list. Note: this has the important consequence to constrain concurrency among a set of agents acting in the same world. Below is the study of various patterns working around that constraint.

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
(i.e. reasoning to use a generator)
for example with a very simple state machine:
```
    def move(self):
        if self.state == 0:
             goal = self.world.getSomeLocation()
             self.astar.initSearch(self.location, goal, [obstacles])
             self.state = 1
        elif self.state == 1:
            self.path = self.astar.search()
            if self.path:
                self.state = 2
        elif self.state == 2:
            self.location = self.path.pop(0)
            if not self.path:
                self.state = 0
```
Note: that example doesn't include synchronization between searches.
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
