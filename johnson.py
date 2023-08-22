import networkx as nx
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, key):
        self.key = key
        self.neighbours = {}

    def add_neighbour(self, neighbour, weight):
        self.neighbours[neighbour] = weight

    def get_neighbours(self):
        return self.neighbours.keys()

    def get_weight(self, neighbour):
        return self.neighbours[neighbour]

    def get_key(self):
        return self.key

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, key):
        self.vertices[key] = Vertex(key)

    def add_edge(self, src_key, dest_key, weight):
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)

    def does_edge_exist(self, src_key, dest_key):
        return self.vertices[dest_key] in self.vertices[src_key].get_neighbours()

    def __iter__(self):
        return iter(self.vertices.values())

    def __contains__(self, key):
        return key in self.vertices

def dijkstra(g, source):
    unvisited = set(g)
    distance = dict.fromkeys(g, float('inf'))
    distance[source] = 0

    while unvisited != set():
        closest = min(unvisited, key=lambda v: distance[v])
        unvisited.remove(closest)

        for neighbour in closest.get_neighbours():
            if neighbour in unvisited:
                new_distance = distance[closest] + closest.get_weight(neighbour)
                if distance[neighbour] > new_distance:
                    distance[neighbour] = new_distance

    return distance

def johnson(g):
    return {v.get_key(): dijkstra(g, v) for v in g}

def draw_graph(g):
    G = nx.DiGraph()  # Create a new directed graph G

    for v in g:  # Add nodes to the graph
        G.add_node(v.get_key())

    for v in g:  # Add edges to the graph
        for dest in v.get_neighbours():
            G.add_edge(v.get_key(), dest.get_key(), weight=v.get_weight(dest))

    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, width=2)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.axis("off")
    plt.show()

g = Graph()
print('Menu')
print('add vertex <key>')
print('add edge <src> <dest> <weight>')
print('johnson')
print('display')
print('quit')

while True:
    do = input('What would you like to do? ').split()

    operation = do[0]
    if operation == 'add':
        suboperation = do[1]
        if suboperation == 'vertex':
            key = int(do[2])
            if key not in g:
                g.add_vertex(key)
            else:
                print('Vertex already exists.')
        elif suboperation == 'edge':
            src = int(do[2])
            dest = int(do[3])
            weight = int(do[4])
            if src not in g:
                print('Vertex {} does not exist.'.format(src))
            elif dest not in g:
                print('Vertex {} does not exist.'.format(dest))
            else:
                if not g.does_edge_exist(src, dest):
                    g.add_edge(src, dest, weight)
                else:
                    print('Edge already exists.')

    elif operation == 'johnson':
        distances = johnson(g)
        print('Shortest distances:')
        for start in distances:
            for end, distance in distances[start].items():
                print('{} to {}'.format(start, end.get_key()), end=' ')
                print('distance {}'.format(distance))

    elif operation == 'display':
        draw_graph(g)

    elif operation == 'quit':
        break
