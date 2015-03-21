# pylibs

###astar: Python Tile-based A* basics

#####Pathfinding as a generator
######Optimizations
- I used a heap-based priority queue to provide O(log N) to Insert and removeMax operations (worst case)
- I stored search states into nodes to remove the Closed list. Note: this has the important consequence to constrain concurrency among a set of agents acting in the same world. Below is the study of various patterns working around that constraint.

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
The resut is that it is often the case that a Search operation takes time, and then it stalls a frame. Below is a diagram showing how that approach is slow (assuming pathing is O(1), and worst: doesn't guarantee a constant framerate.
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
             goal = self.world.getRandomFreeLocation()
             self.findPath(self.location, goal, [1])
             self.state = 1
        elif self.state == 1:
            self.path = self.getPath()
            if self.path:
                self.state = 2
        elif self.state == 2:
            self.location = self.path.pop(0)
            if not self.path:
                self.state = 0
```

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
