
# wall don’t include
# locked door	don’t include
# door w/key	include
# land	include
from collections import deque

STOP_POSITION = '+'
START_POSITION = '@'
WALL = '|'


def find_shortest_path(grid):
    row_length = len(grid)
    col_length = len(grid[0])

    start_row, start_col = find_starting_position(grid, row_length, col_length)

    # we need this variables to build the path from our backref object
    stop_row, stop_col, stop_key_ring = False, False, False

    # initialize all values of the grid with empty sets in the dictionary
    seen = {(row, col): set() for row in range(row_length) for col in range(col_length)}
    seen[(start_row, start_col)].add(0)

    # we will use this to rebuild the shortest path
    backref = {(start_row, start_col, 0): None}

    # add the starting point and starting keyring into the queue and seen objects
    q = deque()
    q.append((start_row, start_col, 0))

    while q:
        cur_row, cur_col, key_ring = q.popleft()

        # We found the node we are looking for
        if grid[cur_row][cur_col] == STOP_POSITION:
            stop_row, stop_col, stop_key_ring = cur_row, cur_col, key_ring
            break

        for new_row, new_col, new_key_ring in get_neighbors(grid, cur_row, cur_col, key_ring):
            if not is_visited(new_row, new_col, new_key_ring, seen):
                q.append((new_row, new_col, new_key_ring))
                backref[(new_row, new_col, new_key_ring)] = cur_row, cur_col, key_ring
                seen[(new_row, new_col)].add(new_key_ring)

    path = []

    if all([stop_row, stop_col, stop_key_ring]):
        current = stop_row, stop_col, stop_key_ring

        while current:
            row, column, key_ring = current
            path.append((row, column))
            current = backref[current]

        path.reverse()

    return path


def find_starting_position(grid, row_length, col_length):
    r, c = None, None

    for i in range(row_length):
        for j in range(col_length):
            if grid[i][j] == START_POSITION:
                r, c = i, j
                break
    return r, c


def is_visited(new_row, new_col, new_key_ring, seen):
    for key in seen[(new_row, new_col)]:
        if new_key_ring == key:
            return True
    return False


def get_neighbors(grid, row, col, key_ring):
    DIRECTIONS = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    row_length = len(grid)
    col_length = len(grid[0])
    available_neighbors = []

    for direction_row, direction_col in DIRECTIONS:
        new_row, new_col = row + direction_row, col + direction_col

        if not (0 <= new_row < row_length and 0 <= new_col < col_length):
            continue

        pos_val = grid[new_row][new_col]

        if pos_val == WALL:
            continue

        if pos_val in 'ABCDEFGHIJ':
            if key_ring & (1 << (ord(pos_val) - ord('A'))) == 0:
                continue

        if pos_val in 'abcdefghij':
            # we found a key. Let's make sure it's in our keyring
            new_key_ring = key_ring | (1 << (ord(pos_val) - ord('a')))
        else:
            new_key_ring = key_ring

        available_neighbors.append((new_row, new_col, new_key_ring))

    for i in available_neighbors:
        print(available_neighbors)
    return available_neighbors


