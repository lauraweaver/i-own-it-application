# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#
from copy import deepcopy


class Node(object):
    def __init__(self, name):
        self.name = str(name)

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __deepcopy__(self, memo):
        return Node(self.name)


class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dest

    def __str__(self):
        return str(self.src) + '->' + str(self.dest)


class WeightedEdge(Edge):
    def __init__(self, src, dest, total_distance, outdoor_distance):
        super(WeightedEdge, self).__init__(src, dest)
        self.total_distance = total_distance
        self.outdoor_distance = outdoor_distance


class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        self.nodes = set([])
        self.edges = {}

    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []

    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)

    def childrenOf(self, node):
        return self.edges[node]

    def hasNode(self, node):
        return node in self.nodes

    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]


class WeightedEdgeDigraph(Digraph):
    """
    Create a WeightedEdgeDigraph subclass of Digraph that stores
    WeightedEdge objects instead of just implying the edges.
    You should be able to ask your class for all the
    edges leading out of a given node.
    """

    def addEdge(self, weighted_edge):
        if not isinstance(weighted_edge, WeightedEdge):
            raise TypeError('Edge must be an instance of WeightedEdge')
        src = weighted_edge.getSource()
        dest = weighted_edge.getDestination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(weighted_edge)

    def childrenOf(self, node):
        dests = []
        for edge in self.edges[node]:
            dests.append(edge.getDestination())
        return dests

    def getEdges(self, node):
        return self.edges[node]

    def __str__(self):
        res = ''
        for node in self.edges:
            for weighted_edge in self.edges[node]:
                res += '{}\t-->\t{}\ttotal: {}, outdoor: {}\n'.format(
                    node,
                    weighted_edge.getDestination(),
                    weighted_edge.total_distance,
                    weighted_edge.outdoor_distance,
                )
        return res[:-1]


class Path(object):
    """
    Create a Path class to encapsulate a path along weighted edges.
    """
    def __init__(self, nodes=[], total_distance=0, outdoor_distance=0):
        self.nodes = nodes
        self.total_distance = total_distance
        self.outdoor_distance = outdoor_distance

    def __deepcopy__(self, memo):
        return Path(
            deepcopy(self.nodes, memo),
            self.total_distance,
            self.outdoor_distance,
        )

    def __add__(self, edge):
        new_path = deepcopy(self)
        if new_path.get_end() != edge.getSource():
            raise ValueError('This is not a usable path')
        new_path.nodes.append(edge.getDestination())
        new_path.total_distance += edge.total_distance
        new_path.outdoor_distance += edge.outdoor_distance
        return new_path

    def contains_node(self, node):
        return node in self.nodes

    def get_end(self):
        return self.nodes[-1]

    def to_list(self):
        return [node.name for node in self.nodes]
