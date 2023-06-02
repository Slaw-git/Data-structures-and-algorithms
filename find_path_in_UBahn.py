
# source of info about U-Bahn lines- https://de.wikipedia.org/wiki/U-Bahn_M%C3%BCnchen
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


NO_PARENT = -1


class GraphAdjacencyMatrix:
    def __init__(self, verticies):
        self.matrix = []
        for i in range(verticies + 1):
            self.matrix.append([0] * (verticies + 1))

    def add_edge(self, edge):
        fr, to = edge
        self.matrix[fr][to] = 1

    def print_all_edges(self):
        for fr in range(len(self.matrix)):
            for to in range(len(self.matrix[0])):
                if self.matrix[fr][to] == 1:
                    print(f'Edge {fr}->{to}')

    def print_structure(self, nodelist=None):
        node_labels = name_set
        # Define the adjacency matrix as a 2D numpy array
        adj_matrix = np.array(self.matrix)
        # Create a graph object from the adjacency matrix
        G = nx.Graph(adj_matrix)
        pos = nx.spring_layout(G, k=.9)
        options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_nodes(G, pos, nodelist=nodelist, node_color="tab:red", **options)
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.6)
        nx.draw_networkx_labels(G, pos, node_labels, font_size=9, font_color="black")

        plt.tight_layout()
        plt.axis("off")
        plt.show()


    def check_if_edge_exists(self, fr, to):
        return False if self.matrix[fr][to] == 0 else True


def make_name_set(stations):
    name_set = {}
    for line, station in stations.items():
        for num, data in station.items():
            if num not in name_set.keys():
                name_set[num] = data['name']

    return name_set


def get_name(key):
    if key in name_set.keys():
        return name_set[key]
    if key in name_set.values():
        inverted_dict = {v: k for k, v in name_set.items()}
        val = inverted_dict[key]
        return val


def dijkstra(adjacency_matrix, start_vertex, end_vertex=None):
    n_vertices = len(adjacency_matrix[0])

    # shortest_distances[i] will hold the
    # shortest distance from start_vertex to i
    shortest_distances = [sys.maxsize] * n_vertices

    # added[i] will true if vertex i is
    # included in shortest path tree
    # or shortest distance from start_vertex to
    # i is finalized
    added = [False] * n_vertices

    # Initialize all distances as
    # INFINITE and added[] as false
    shortest_distances[0] = 0
    for vertex_index in range(1, n_vertices):
        shortest_distances[vertex_index] = sys.maxsize
        added[vertex_index] = False

    # Distance of source vertex from
    # itself is always 0
    shortest_distances[start_vertex] = 0

    # Parent array to store shortest
    # path tree
    parents = [-1] * n_vertices

    # The starting vertex does not
    # have a parent
    # parents[start_vertex] = NO_PARENT

    # Find the shortest path for all
    # vertices
    for i in range(1, n_vertices):
        # Pick the minimum distance vertex
        # from the set of vertices not yet
        # processed. nearest_vertex is
        # always equal to start_vertex in
        # first iteration.
        nearest_vertex = -1
        shortest_distance = sys.maxsize
        for vertex_index in range(n_vertices):
            if not added[vertex_index] and shortest_distances[vertex_index] < shortest_distance:
                nearest_vertex = vertex_index
                shortest_distance = shortest_distances[vertex_index]

        # Mark the picked vertex as
        # processed
        added[nearest_vertex] = True

        # Update dist value of the
        # adjacent vertices of the
        # picked vertex.
        for vertex_index in range(1, n_vertices):
            edge_distance = adjacency_matrix[nearest_vertex][vertex_index]

            if edge_distance > 0 and shortest_distance + edge_distance < shortest_distances[vertex_index]:
                parents[vertex_index] = nearest_vertex
                shortest_distances[vertex_index] = shortest_distance + edge_distance

    print_solution(start_vertex, shortest_distances, parents, end_vertex)


# A utility function to print
# the constructed distances
# array and shortest paths
def print_solution(start_vertex, distances, parents, end_vertex):
    n_vertices = len(distances)
    print("Vertex".ljust(60), "Stations".ljust(26), "Path")

    if end_vertex is not None:
        if end_vertex != start_vertex:
            print("\n", get_name(start_vertex), "->", get_name(end_vertex).ljust(30), "\t\t",
                  str(distances[end_vertex]).ljust(20), "\t\t",
                  end="")
            print_path(end_vertex, parents)
    else:
        for vertex_index in range(1, n_vertices):
            if vertex_index != start_vertex:
                print("\n", get_name(start_vertex), "->", get_name(vertex_index).ljust(20), "\t\t",
                      str(distances[vertex_index]).ljust(10), "\t\t",
                      end="")
                print_path(vertex_index, parents)


# Function to print shortest path
# from source to current_vertex
# using parents array
def print_path(current_vertex, parents):
    # Base case : Source node has
    # been processed
    if current_vertex == NO_PARENT:
        return
    print_path(parents[current_vertex], parents)
    if parents[current_vertex] != NO_PARENT:
        print(f'-> {get_name(current_vertex)}', end=" ")
        nodelist.append(current_vertex)
    else:
        print(f'{get_name(current_vertex)}', end=" ")
        nodelist.append(current_vertex)





if __name__ == '__main__':
    stations = {
        'U1': {
            1: {'name': 'Olympia_Einkaufszentrum', 'coord': [], 'prev': None, 'next': 2},
            2: {'name': 'Westfriedhof', 'coord': [], 'prev': 1, 'next': 4},
            4: {'name': 'Hauptbahnhof', 'coord': [], 'prev': 2, 'next': 5},
            5: {'name': 'Sendlinger_Tor', 'coord': [], 'prev': 4, 'next': 6},
            6: {'name': 'Kolumbusplatz', 'coord': [], 'prev': 5, 'next': 7},
            7: {'name': 'Mangfallplatz', 'coord': [], 'prev': 6, 'next': None},
        },

        'U2': {
            8:  {'name': 'Feldmoching', 'coord': [], 'prev': None, 'next': 9},
            9:  {'name': 'Scheidplatz', 'coord': [], 'prev': 8, 'next': 4},
            4:  {'name': 'Hauptbahnhof', 'coord': [], 'prev': 9, 'next': 5},
            5:  {'name': 'Sendlinger_Tor', 'coord': [], 'prev': 4, 'next': 6},
            6:  {'name': 'Kolumbusplatz', 'coord': [], 'prev': 5, 'next': 10},
            10: {'name': 'Innsbrucker_Ring', 'coord': [], 'prev': 6, 'next': 11},
            11: {'name': 'Messestadt_Ost', 'coord': [], 'prev': 10, 'next': None},
        },

        'U3': {
            12: {'name': 'Moosach', 'coord': [], 'prev': None, 'next': 1},
            1:  {'name': 'Olympia_Einkaufszentrum', 'coord': [], 'prev': 12, 'next': 3},
            3:  {'name': 'Olympiazentrum', 'coord': [], 'prev': 1, 'next': 9},
            9:  {'name': 'Scheidplatz', 'coord': [], 'prev': 3, 'next': 13},
            13: {'name': 'Münchner_Freiheit', 'coord': [], 'prev': 9, 'next': 14},
            14: {'name': 'Odeonsplatz', 'coord': [], 'prev': 13, 'next': 5},
            5:  {'name': 'Sendlinger_Tor', 'coord': [], 'prev': 14, 'next': 15},
            15: {'name': 'Implerstraße', 'coord': [], 'prev': 5, 'next': 16},
            16: {'name': 'Fürstenried_West', 'coord': [], 'prev': 15, 'next': None},
        },

        'U4': {
            17: {'name': 'Westendstraße', 'coord': [], 'prev': None, 'next': 4},
            4:  {'name': 'Hauptbahnhof', 'coord': [], 'prev': 17, 'next': 14},
            14: {'name': 'Odeonsplatz', 'coord': [], 'prev': 4, 'next': 18},
            18: {'name': 'Max_Weber_Platz', 'coord': [], 'prev': 14, 'next': 19},
            19: {'name': 'Arabellapark', 'coord': [], 'prev': 18, 'next': None},
        },

        'U5': {
            20: {'name': 'Laimer_Platz', 'coord': [], 'prev': None, 'next': 17},
            17: {'name': 'Westendstraße', 'coord': [], 'prev': 20, 'next': 4},
            4:  {'name': 'Hauptbahnhof', 'coord': [], 'prev': 17, 'next': 14},
            14: {'name': 'Odeonsplatz', 'coord': [], 'prev': 4, 'next': 18},
            18: {'name': 'Max_Weber_Platz', 'coord': [], 'prev': 14, 'next': 10},
            10: {'name': 'Innsbrucker_Ring', 'coord': [], 'prev': 18, 'next': 21},
            21: {'name': 'Neuperlach_Zentrum', 'coord': [], 'prev': 10, 'next': 22},
            22: {'name': 'Neuperlach_Süd', 'coord': [], 'prev': 21, 'next': None},
        },

        'U6': {
            24: {'name': 'Garching_Forschungszentrum', 'coord': [], 'prev': None, 'next': 25},
            25: {'name': 'Fröttmaning', 'coord': [], 'prev': 24, 'next': 13},
            13: {'name': 'Münchner_Freiheit', 'coord': [], 'prev': 25, 'next': 14},
            14: {'name': 'Odeonsplatz', 'coord': [], 'prev': 13, 'next': 5},
            5:  {'name': 'Sendlinger_Tor', 'coord': [], 'prev': 14, 'next': 15},
            15: {'name': 'Implerstraße', 'coord': [], 'prev': 5, 'next': 23},
            23: {'name': 'Klinikum_Großhadern', 'coord': [], 'prev': 15, 'next': None}
        },

        'U7': {
            1:  {'name': 'Olympia_Einkaufszentrum', 'coord': [], 'prev': None, 'next': 2},
            2:  {'name': 'Westfriedhof', 'prev': 1, 'next': 4},
            4:  {'name': 'Hauptbahnhof', 'coord': [], 'prev': 2, 'next': 5},
            5:  {'name': 'Sendlinger_Tor', 'coord': [], 'prev': 4, 'next': 6},
            6:  {'name': 'Kolumbusplatz', 'coord': [], 'prev': 5, 'next': 10},
            10: {'name': 'Innsbrucker_Ring', 'coord': [], 'prev': 6, 'next': 21},
            21: {'name': 'Neuperlach_Zentrum', 'coord': [], 'prev': 10, 'next': None}
        },

        'U8': {
            3:  {'name': 'Olympiazentrum', 'coord': [], 'prev': None, 'next': 9},
            9:  {'name': 'Scheidplatz', 'coord': [], 'prev': 3, 'next': 4},
            4:  {'name': 'Hauptbahnhof', 'coord': [], 'prev': 9, 'next': 5},
            5:  {'name': 'Sendlinger_Tor', 'coord': [], 'prev': 4, 'next': 21},
            21: {'name': 'Neuperlach_Zentrum', 'coord': [], 'prev': 5, 'next': None}
        },

    }

    name_set = make_name_set(stations)
    max_stations = max(name_set.keys())
    nodelist = []
    # Making Graph structure
    graph = GraphAdjacencyMatrix(max_stations)

    stations_set = []
    for line, station in stations.items():
        for num, data in station.items():
            # stations_set.append(Station(data['coord'], ))
            # print(num, data['prev'], data['next'])
            if data['next'] is not None:
                fr, to = num, data['next']
                # print(f"inserting {fr}->{to}")
                if not graph.check_if_edge_exists(fr, to):
                    graph.add_edge((fr, to))
                    graph.add_edge((to, fr))

    # graph.print_all_edges()
    # print(graph.check_if_edge_exists(4, 17))
    # use 'from_station' as station from where You want to go
    from_station = 'Garching_Forschungszentrum'

    # use 'to_station' as station where You want to go to
    # use None if You don't know where to go

    to_station = 'Neuperlach_Zentrum'
    # to_station = None

    dijkstra(graph.matrix, get_name(from_station), get_name(to_station))

    graph.print_structure(nodelist)
