# pylibs

###astar: Python Tile-based A* basics

#####Pathfinding as a generator
######Optimizations
- We use a heap-based priority queue to provide O(log N) to Insert and removeMax operations (worst case)
- We store search states into nodes to remove the Closed list. 

######Blocking search pattern 
```
    +         + + +       + +
A0: S S S S S P P P P P P P G
A1: P P P P P P G S S S S P P
```
######Interlaced pattern 
(i.e. reasoning to use a generator)
```
    + + + + + + + + + + + + +
A0: S S S S S P P P P P P G .
A1: P P P P P P G S S S S P P
A2: P P P P P P P G . . . S S
```

#####Parallel pathfinding using multiprocessing
#####Concurrent pathfinding using a worker pool
(TODO)

###raycats: Tile-based Ray casting
