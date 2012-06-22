import copy

# solveable
grid = [[3,0,0, 2,4,0, 0,6,0],
        [0,4,0, 0,0,0, 0,5,3],
        [1,8,9, 6,3,5, 4,0,0],
        [0,0,0, 0,8,0, 2,0,0],
        [0,0,7, 4,9,6, 8,0,1],
        [8,9,3, 1,5,0, 6,0,4],
        [0,0,1, 9,2,0, 5,0,0],
        [2,0,0, 3,0,0, 7,4,0],
        [9,6,0, 5,0,0, 3,0,2]]
        
# solveable        
grid = [[0,0,7, 0,1,0, 0,0,0],
        [0,0,3, 0,0,0, 4,7,0],
        [0,5,4, 0,0,7, 2,0,1],
        [0,0,0, 9,8,0, 0,4,6],
        [0,0,0, 4,6,2, 0,0,0],
        [4,6,1, 0,0,0, 0,8,2],
        [5,7,0, 0,0,3, 6,2,0],
        [9,0,0, 0,0,8, 0,1,0],
        [1,0,0, 0,0,9, 5,3,0]]
        
# not solveable
grid = [[7,6,0, 5,0,0, 2,0,0],
        [1,0,2, 0,4,0, 0,7,8],
        [0,0,4, 0,0,8, 5,1,0],
        [0,0,0, 0,0,3, 0,0,0],
        [0,0,7, 1,0,2, 0,0,0],
        [9,0,0, 0,8,7, 6,0,0],
        [0,0,6, 0,0,0, 0,3,0],
        [0,1,0, 7,0,0, 8,0,0],
        [0,4,3, 0,0,9, 0,0,0]]
        
def debug(_grid):
    print '---------------------'
    for line in _grid:
        print '|',
        for field in line:
            if field>0:
                print str(field),
            else:
                print ' ',
        print '|'
    print '---------------------'

debug(grid)

def get_row(y,_grid):
    return list(set(range(1,10))-set(_grid[y]))

def get_col(x,_grid):
    return list(set(range(1,10))-set([row[x] for row in _grid]))

def get_3x3(x,y,_grid):
    return list(set(range(1,10))-set(sum([row[x/3*3:x/3*3+3] for row in _grid[y/3*3:y/3*3+3]],[])))


def solve(_grid):
    #print " recursive call"
    debug(_grid)
    change=True
    error=False
    # loop until nothign changes
    while(change and not error):
        change = False
        for y in xrange(0,9):
            for x in xrange(0,9):
                if _grid[y][x] == 0:
                    # merge all possible values together
                    possible_values = list(set(get_row(y,_grid)) & set(get_col(x,_grid)) & set(get_3x3(x,y,_grid)))
                    # if inly one value is possible for the field, fill it in, and set the flag for another run
                    if(len(possible_values)==1):
                        _grid[y][x] = possible_values[0]
                        change = True
                    if(len(possible_values)==0):
                        #print "ERROR"
                        return False

    # recursive calls when undecidable
    for y in xrange(0,9):
        for x in xrange(0,9):
            if _grid[y][x] == 0:
                # merge all possible values together
                possible_values = list(set(get_row(y,_grid)) & set(get_col(x,_grid)) & set(get_3x3(x,y,_grid)))
                if(len(possible_values)>1):
                    # print x,y,possible_values
                    for value in possible_values:
                        tmp_grid = copy.deepcopy(_grid)
                        tmp_grid[y][x] = value
                        tmp_grid = solve(tmp_grid)
                        if tmp_grid: # recursion
                            return tmp_grid
                    change = True
                if(len(possible_values)==0):
                    #print "ERROR"
                    return False
    #print "ERROR"
    return _grid
    # easy number chosing stucks

debug(solve(grid))
