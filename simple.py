
'''
    Author: Kyle McLaughlin

    Description: Given an input file containing elements (pipe, sink, source) and there visual coordinates on a grid, 
                 we find all connected sinks to the source and return them as a string in alphabetical order.
'''


'''
    Get connectable directions for a given element.
 
    Parameters
    ----------
    identifier : str
        The character identifier for the element in the grid.
 
    Returns
    -------
    list of str
        List of direction names. L = left, R = right, U = up, D = down.
'''
def get_directions(identifier: str) -> list[str]:
    # Elements with all directions. Source or Sink
    if identifier == '*' or identifier.isalpha():
        return { 'L', 'R', 'U', 'D' }

    # Elements with only specific directions. Pipes
    directions = {
        '═': {'L', 'R'},
        '║': {'U', 'D'},
        '╔': {'D', 'R'},
        '╗': {'D', 'L'},
        '╚': {'U', 'R'},
        '╝': {'U', 'L'},
        '╠': {'U', 'D', 'R'},
        '╣': {'U', 'D', 'L'},
        '╦': {'D', 'L', 'R'},
        '╩': {'U', 'L', 'R'}
    }
    return directions[identifier]

'''
    Check if an element is connected to another element.
 
    Parameters
    ----------
    first : str
        The character identifier for the first element to check.
    second : str
        The character identifier for the first element to check.
 
    Returns
    -------
    bool
        True when the first is connected to the second.
'''
def is_connected_to(first: str, second: str, direction: str) -> bool:
    # Define the opposite directions.
    opposites = { 
        'L': 'R', 
        'R': 'L',
        'U': 'D', 
        'D': 'U'
    }
    return direction in get_directions(first) and opposites[direction] in get_directions(second)

'''
    Find nearby connected elements in the grid.
    Checks 1 position in each direction.
 
    Parameters
    ----------
    x : int
        The x position of the element we are starting at.
    y : int
        The y position of the element we are starting at.
    grid : list of lists of strs
        The grid of all elements.
 
    Returns
    -------
    list of tuples of (int, int)
        The list of positions of the connected elements.
'''
def get_connected_elements(x: int, y: int, grid: list[list[str]]) -> list[tuple[int, int]]:
    connected = []

    # Grid movement for determining position in given direction.
    directions = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }

    for direction, (dx, dy) in directions.items():
        # Position to check.
        nx, ny = x + dx, y + dy

        # Check that the new position is in the grid bounds.
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            # Ensure new position is not empty space, 
            # and that the element at that new position is connected to element at original position.
            if grid[nx][ny] != ' ' and is_connected_to(grid[x][y], grid[nx][ny], direction):
                connected.append( (nx, ny) )
    
    return connected

'''
    Find all connected sinks.
 
    Parameters
    ----------
    grid : list of lists of strs
        The grid of all elements.
 
    Returns
    -------
    list of strs
        List of sink characters found to be connected to the source.
        Will be empty if the source is not found in the grid.
'''
def bfs_for_connected_sinks(grid: list[list[str]]):
    source_position = None  # Only 1 source per grid. Represented as an asterisk.
    sink_positions = []     # Sinks in the grid. Represented as alphabetical characters.

    # Parse the grid to find the source and sinks.
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '*': # Found the source.
                source_position = (i, j)
            elif grid[i][j].isalpha(): # Found a sink.
                sink_positions.append((i, j))

    # If no source found, return empty list as there cannot be any connected sinks.
    if not source_position:
        return []

    # BFS
    visited = [ source_position ]
    queue = [ source_position ]
    while queue:
        x, y = queue.pop(0)
        for nx, ny in get_connected_elements(x, y, grid):
            if (nx, ny) not in visited:
                visited.append((nx, ny))
                queue.append((nx, ny))

    # Return a list of connected sinks characters
    # Loop through all sink_positions, and if it has been visited, that sink's character (from: grid[x][y]) will be included in the list.
    return [ grid[x][y] for (x, y) in sink_positions if (x, y) in visited ]

'''
    Parse a line from the input file.
 
    Parameters
    ----------
    line : str
        The text line to be parsed.
 
    Returns
    -------
    tuple of (str, int, int)
        A tuple containing the final information of the element for the grid. (identifier, x, y)
    None
        Will return None if error parsing line occurs.
'''
def parse_line(line: str, max_y: int) -> tuple[str, int, int]:
    # If the given line is empty.
    if not line.strip():
        return None

    # Split each character, delimited by ' ' 
    vars = line.strip().split()

    # Incorrect amount of data describing the element.
    if len(vars) != 3:
        return None

    identifier = vars[0]
    x_visual = int(vars[1])
    y_visual = int(vars[2])

    # Convert the positions from the input line to indexes in the grid.
    x = abs(y_visual - max_y)
    y = x_visual

    return identifier, x, y

'''
    Returns all connected sinks.
 
    Parameters
    ----------
    file_path : str
        The path to the input file containing information for where each element will be in the grid.
 
    Returns
    -------
    str
        Alphabetically sorted string of the connected sinks.
'''
def get_connected_sinks(file_path: str) -> str:
    inputs: list[str] = []
    max_x, max_y = 0, 0

    # Read the file, collect all lines, and determine the grid's max dimensions.
    with open(file_path, 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            vars = line.strip().split()
            if len(vars) == 3: # Ensure correct amount of data.
                x_visual = int(vars[1])
                y_visual = int(vars[2])
                max_x = max(max_x, x_visual)
                max_y = max(max_y, y_visual)
                inputs.append(line)

    # Create a grid with empty spaces to size calculated.
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Insert elements parsed from the input lines into the grid.
    for line in inputs:
        parsed = parse_line(line, max_y)
        if parsed:
            identifier, x, y = parsed
            grid[x][y] = identifier

    # BFS search for connected sinks.
    connected_sinks = bfs_for_connected_sinks(grid)
    # Sort alphabetically.
    connected_sinks.sort()

    # Return the resulting string.
    return ''.join(connected_sinks)

# Test
print(get_connected_sinks("input.txt"))