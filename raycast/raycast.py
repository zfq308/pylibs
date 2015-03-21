'''
Raycast and visibility testing (in maps) functions 
Created on 2010-10-08
@author: Artsimboldo
'''

from math import copysign

#-----------------------------------------------------------------------------
def rayCast1((i0, j0), (i1, j1)):
    result = [(i0, j0)]
    di, dj = abs(i1 - i0), abs(j1 - j0)
    i, j = i0, j0
    n = 1 + di + dj
    inci, incj = int(copysign(1, i1 - i0)), int(copysign(1, j1 - j0))
    error = di - dj
    while n > 0:
        result.append((i,j))
        # compute next move
        if error > 0:
            i += inci
            error -= dj
        else:
            j += incj
            error += di
        n -= 1
    return result
    
#-----------------------------------------------------------------------------
# Exit with True if no obstacles has been found
def isVisible1((i0, j0), (i1, j1), map):
    di, dj = abs(i1 - i0), abs(j1 - j0)
    i, j = i0, j0
    n = 1 + di + dj
    inci, incj = int(copysign(1, i1 - i0)), int(copysign(1, j1 - j0))
    error = di - dj
    while n > 0:
        if map[j][i] is 1 and (i != i1 or j != j1):
            return False
        # compute next move
        if error > 0:
            i += inci
            error -= dj
        else:
            j += incj
            error += di
        n -= 1
    return True
    
#-----------------------------------------------------------------------------
def rayCast2((i0, j0), (i1, j1)):
    steep = abs(j1 - j0) > abs(i1 - i0)
    if steep:
        i0, j0 = j0, i0
        i1, j1 = j1, i1
    if i0 > i1:
        i0, i1 = i1, i0
        j0, j1 = j1, j0
    result = []
    deltai, deltaj = i1 - i0, abs(j1 - j0)
    error = 0
    jstep = -1
    j = j0
    if j0 < j1:
        jstep = 1
    for i in range(i0, i1 + 1):
        if steep:
            result.append((j,i))
        else:
            result.append((i,j))
        error += deltaj
        if (2 * error) >= deltai:
            j += jstep
            error -= deltai
    return result

#-----------------------------------------------------------------------------
# Exit with True if no obstacles has been found
def isVisible2((i0, j0), (i1, j1), map):
    steep = abs(j1 - j0) > abs(i1 - i0)
    if steep:
        i0, j0 = j0, i0
        i1, j1 = j1, i1
    if i0 > i1:
        i0, i1 = i1, i0
        j0, j1 = j1, j0
    deltai, deltaj = i1 - i0, abs(j1 - j0)
    error = 0
    jstep = -1
    j = j0
    if j0 < j1:
        jstep = 1
    for i in range(i0, i1 + 1):
        if not ((i == i1 and j == j1) or (i == i0 and j == j0)):
            if (steep is True) and map[j][i] == 1:
                return False
            elif (steep is False) and map[i][j] == 1:
                return False
        error += deltaj
        if (2 * error) >= deltai:
            j += jstep
            error -= deltai
    return True

#-----------------------------------------------------------------------------
import unittest

class TestRaycast(unittest.TestCase):
    def test1(self):
        width, height = 10, 10
        world = [['.' for j in range(height)] for i in range(width)]
        for n in range(5):
            world[n][4] = 1
        self.assertFalse(isVisible1((5, 5), (0, 0), world))
        self.assertTrue(isVisible1((5, 5), (0, 9), world))
        result = rayCast1((5, 5), (0, 0))
        result.extend(rayCast1((5, 5),(0, 9)))
        for (i, j) in result:
            world[i][j] = '*'
        world_str = ''
        for j in range(height):
            world_str += ''.join(str(world[i][j]) for i in range(width)) + '\n'
        print world_str

    def test2(self):
        width, height = 10, 10
        world = [['.' for j in range(height)] for i in range(width)]
        for n in range(5):
            world[n][4] = 1
        self.assertFalse(isVisible2((5, 5), (0, 0), world))
        self.assertTrue(isVisible2((5, 5), (0, 9), world))
        result = rayCast2((5, 5), (0, 0))
        result.extend(rayCast2((5, 5),(0, 9)))
        for (i, j) in result:
            world[i][j] = '*'
        world_str = ''
        for j in range(height):
            world_str += ''.join(str(world[i][j]) for i in range(width)) + '\n'
        print world_str

if __name__ == '__main__':
    unittest.main()