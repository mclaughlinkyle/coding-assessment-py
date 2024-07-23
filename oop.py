

class Coordinate:
    def __init__(self, x: int, y: int):
        self.__x: int = x
        self.__y: int = y

    # Returns the x
    def get_x(self) -> int:
        return self.__x
    
    # Returns the y
    def get_y(self)-> int:
        return self.__y
    
    def set_x(self, x: int) -> None:
        self.__x = x

    def set_y(self, y: int) -> None:
        self.__y = y

    # Returns the x and y
    def get_coordinates(self)-> tuple[int, int]:
        return int(self.__x), int(self.__y)

    def __eq__(self, coordinate: object) -> bool:
        return self.get_coordinates() == coordinate.get_coordinates()

    def __repr__(self) -> str:
        return "Coordinate({}, {})".format(self.__x, self.__y)

# Node in our graph
class Node:
    """ 
    @parameters string identifier: the character symbol representing the node
                int x: the x coordinate of the node
                int y: the y coordinate of the node
    """
    def __init__(self, identifier: str, coordinate: Coordinate):
        self.__identifier = identifier
        self.__coordinate = coordinate

    # Returns the directions of this node
    def get_directions(self):
        # Nodes with all directions
        if self.__identifier == '*' or self.__identifier.isalpha():
            return { "left", "right", "up", "down" }

        # Nodes with only specific directions
        node_directions = {
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
        return node_directions[self.__identifier]

    # Returns true if the other_node is connected to this node
    def is_connected_to(self, other_node, direction):
        # Define the opposite direction
        opposites = { 
            "up": "down", 
            "down": "up", 
            "left": "right", 
            "right": "left"
        }
        return direction in self.get_directions() and opposites[direction] in other_node.get_directions()
    
    # Returns the identifier
    def get_identifier(self):
        return self.__identifier
    
    # Returns the x and y
    def get_coordinates(self) -> tuple[int, int]:
        return self.__coordinate.get_coordinates()
    
    def get_coordinate(self) -> Coordinate:
        return self.__coordinate
    
    # Converts the coordinates given in the input file of the visual placement of the node
    # to the coordinates used in the Graph
    def convert_coordinates(self, max_coordinate: Coordinate):
        mx, my = max_coordinate.get_coordinates()
        x, y = self.__coordinate.get_coordinates()
        self.__coordinate.set_x(abs(y - my))
        self.__coordinate.set_y(x)
    
    def __repr__(self):
        return "Node '{}' at {}".format(self.__identifier, self.get_coordinate())
    
# Graph / grid of the nodes and edges
# 2 Dimensional
class Graph2D:
    def __init__(self, nodes: list):
        self.__nodes = nodes
        max_x, max_y = 0, 0
        
        for node in nodes:
            x, y = node.get_coordinates()
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        
        for node in nodes:
            node.convert_coordinates(Coordinate(max_x, max_y))

    def get_node_at_coordinate(self, coordinate: Coordinate) -> Node:
        for node in self.__nodes:
            if node.get_coordinate() == coordinate:
                return node
        return None

    def get_connecting_nodes(self, node: Node):
        # List / array of connecting nodes
        connecting_nodes = []

        # Direction and cooresponding grid position change
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        # Check all directions for connecting node
        for direction, (dx, dy) in directions.items():
            # Node we are checking for edges on
            x, y = node.get_coordinates()

            # Get node in the direction we are checking
            other_node = self.get_node_at_coordinate(Coordinate(x + dx, y + dy))

            # other_node will be None if not found
            # ex: if the coordinates we are checking are out the grid bounds    
            if not other_node:
                continue

            # Node is not empty and the node is connected
            if other_node.get_identifier() != ' ' and node.is_connected_to(other_node, direction):
                connecting_nodes.append(other_node)
        
        return connecting_nodes
    
    def get_nodes(self):
        return self.__nodes
    
    def get_connected_sinks(self):
        source = None
        sinks = set()

        for node in self.__nodes:
            if node.get_identifier() == '*':
                source = node
            elif node.get_identifier().isalpha():
                sinks.add(node)

        if not source:
            return []

        # BFS to find all reachable cells
        visited = set()
        queue = [source]
        visited.add(source)

        while queue:
            for node in self.get_connecting_nodes(queue.pop(0)):
                if node not in visited:
                    visited.add(node)
                    queue.append(node)

        # Determine which sinks are connected
        connected_sinks = []
        for node in sinks:
            if node in visited:
                connected_sinks.append(node)

        return connected_sinks

def get_connected_sinks(file_path: str) -> str:
    nodes = []

    with open(file_path, 'r', encoding='UTF-8') as file:
        while line := file.readline():
            vars = line.rstrip().split(' ')
            nodes.append(Node(vars[0], Coordinate(vars[1], vars[2])))

    graph = Graph2D(nodes)

    sinks = ""
    for node in graph.get_connected_sinks():
        sinks += str(node.get_identifier())

    return ''.join(sorted(sinks))

if __name__ == "__main__":
    print(get_connected_sinks("C:/Users/klye/Documents/Code/coding-assessment-py/input.txt"))
