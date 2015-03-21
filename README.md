# pylibs

###astar: Python Tile-based A* basics

#####Pathfinding as a generator
######Optimizations
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
