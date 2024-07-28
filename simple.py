

def get_directions(identifier) -> list[str]:
    # Elements with all directions
    if identifier == '*' or identifier.isalpha():
        return { "left", "right", "up", "down" }

    # Elements with only specific directions
    directions = {
        '═': {"left", "right"},
        '║': {"up", "down"},
        '╔': {"down", "right"},
        '╗': {"down", "left"},
        '╚': {"up", "right"},
        '╝': {"up", "left"},
        '╠': {"up", "down", "right"},
        '╣': {"up", "down", "left"},
        '╦': {"down", "left", "right"},
        '╩': {"up", "left", "right"}
    }
    return directions[identifier]

# Returns true if the second is connected to the first
def is_connected_to(first, second, direction) -> bool:
    # Define the opposite directions
    opposites = { 
        "up": "down", 
        "down": "up", 
        "left": "right", 
        "right": "left"
    }
    return direction in get_directions(first) and opposites[direction] in get_directions(second)

def get_neighbors(x, y, grid):
    neighbors = []
    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    for direction, (dx, dy) in directions.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] != ' ' and is_connected_to(grid[x][y], grid[nx][ny], direction):
                neighbors.append((nx, ny))
    
    return neighbors

def find_connected_sinks(grid):
    source = None
    sinks = []

    # Parse the grid to find the source and sinks
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '*':
                source = (i, j)
            elif grid[i][j].isalpha():
                sinks.append((i, j))

    if not source:
        return []

    # BFS to find all reachable cells
    visited = []
    queue = [ source ]
    visited.append(source)

    while queue:
        x, y = queue.pop(0)
        for nx, ny in get_neighbors(x, y, grid):
            if (nx, ny) not in visited:
                visited.append((nx, ny))
                queue.append((nx, ny))

    # Determine which sinks are connected
    connected_sinks = [grid[x][y] for x, y in sinks if (x, y) in visited]
    return connected_sinks

# Given a line of text from the input file,
# parse the line and return the:
#   identifier str, x, y for given grid element
def parse_line(line: str, max_y: int) -> tuple[str, int, int]:
    vars = line.rstrip().split(' ')
    identifier  = str(vars[0])
    x_visual     = int(vars[1])
    y_visual     = int(vars[2])

    # invert the coordinates from the input file 
    # to programmatic x and y for the 2D array
    x = int(abs(y_visual - max_y))
    y = int(x_visual)

    return identifier, x, y

# Returns string of all connected sinks in alphabetical order
# @param file_path string is the file path of the input file
def get_connected_sinks(file_path: str) -> str:
    # get all lines in the input file and get max grid size
    inputs = []
    max_x, max_y = 0, 0
    with open(file_path, 'r', encoding='UTF-8') as file:
        while line := file.readline():
            vars = line.rstrip().split(' ')
            max_x = max(max_x, int(vars[1]))
            max_y = max(max_y, int(vars[2]))
            inputs.append(line)
    
    # fill the grid with empty spaces
    grid = []
    for i in range(max_y + 1):
        grid.append([])
        for j in range(max_x + 1):
            grid[i].append(' ')

    for line in inputs:
        identifier, x, y = parse_line(str(line), max_y)
        # Insert the identifier into the grid
        # at given coordinates after parsing from the input file
        grid[int(x)][int(y)] = str(identifier)

    connected_sinks = find_connected_sinks(grid)
    connected_sinks.sort()
    return ''.join(connected_sinks)

print(get_connected_sinks("input.txt"))