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
# grid = [[7,6,0, 5,0,0, 2,0,0],
#         [1,0,2, 0,4,0, 0,7,8],
#         [0,0,4, 0,0,8, 5,1,0],
#         [0,0,0, 0,0,3, 0,0,0],
#         [0,0,7, 1,0,2, 0,0,0],
#         [9,0,0, 0,8,7, 6,0,0],
#         [0,0,6, 0,0,0, 0,3,0],
#         [0,1,0, 7,0,0, 8,0,0],
#         [0,4,3, 0,0,9, 0,0,0]]
        
def debug(_grid):
    print '  0 1 2 3 4 5 6 7 8  '
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

def get_row(y):
    return list(set(range(1,10))-set(grid[y]))

def get_col(x):
    return list(set(range(1,10))-set([row[x] for row in grid]))

def get_3x3(x,y):
    return list(set(range(1,10))-set(sum([row[x/3*3:x/3*3+3] for row in grid[y/3*3:y/3*3+3]],[])))

change=True
# loop until nothign changes
while(change):
    change = False
    for y in xrange(0,9):
        for x in xrange(0,9):
            if grid[y][x] == 0:
                # merge all possible values together
                possible_values = list(set(get_row(y)) & set(get_col(x)) & set(get_3x3(x,y)))
                # if inly one value is possible for the field, fill it in, and set the flag for another run
                if(len(possible_values)==1):
                    grid[y][x] = possible_values[0]
                    change = True

debug(grid)