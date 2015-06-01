# 6.00 Problem Set 11
#
# ps11.py
#
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
import sys
from graph import Digraph, Edge, Node, WeightedEdge, WeightedEdgeDigraph, Path
from time import time

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
# The nodes will be the buildings, and the edges will be the paths from the source building to the destination building. 
# The edges will have two weights. The first is the total distance; the second will be the the distance outside.

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    #TODO
    print "Loading map from file..."

    mit_graph = WeightedEdgeDigraph()
    with open(mapFilename) as mit_edge_file:
    #Doing this so I don't leak memory
        for line in mit_edge_file:
            src, dest, total_dist, outdoors_dist = line.split()
            src_node = Node(src)
            dest_node = Node(dest)
            edge = WeightedEdge(src_node, dest_node, int(total_dist), int(outdoors_dist))
            if not mit_graph.hasNode(src_node):
                mit_graph.addNode(src_node)
            if not mit_graph.hasNode(dest_node):
                mit_graph.addNode(dest_node)
            mit_graph.addEdge(edge)

    print mit_graph
    return mit_graph


def DFS(digraph, start, end, maxTotalDist, maxOutdoorDist, searchFunction):
    start_node = Node(start)
    end_node = Node(end)

    # 1: find all paths from start to end
    paths = searchFunction(digraph, Path([start_node]), end_node)

    # 2: remove paths that do not satisfy the distance constraints, raise an
    # error if none satisfy constraints
    filtered_paths = []
    for path in paths:
        if path.total_distance <= maxTotalDist and path.outdoor_distance <= maxOutdoorDist:
            filtered_paths.append(path)
    if len(filtered_paths) == 0:
        raise ValueError('No paths exist that satisfy the distance constraints')

    # 3: return the shortest (by total distance) of the remaining paths
    shortest_path = min(filtered_paths, key=lambda p: p.total_distance)

    return shortest_path.to_list()


#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints


def bruteDFS(digraph, path, end):
    """
    Parameters:
        digraph: instance of class Digraph or its subclass
        end: desired end Node object
        path: a Path object, the path travelled "so far"

    Returns:
        A list of complete paths beginning with `path`, ending with `end`
    """
    complete_paths = []

    for edge in digraph.getEdges(path.get_end()):
        if not path.contains_node(edge.getDestination()):
            new_path = path + edge
            if new_path.get_end() == end:
                complete_paths.append(new_path)
            else:
                complete_paths += bruteDFS(digraph, new_path, end)

    return complete_paths


def bruteForceSearch(digraph, start, end, maxTotalDist, maxOutdoorDist):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxOutdoorDist: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxOutdoorDist constraints, then raises a ValueError.
    """
    return DFS(digraph, start, end, maxTotalDist, maxOutdoorDist, bruteDFS)


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#

def optimizedDFS(digraph, path, end):
    complete_paths = []
    shortest_path = None

    current_node = path.get_end()

    for edge in digraph.getEdges(current_node):
        if not path.contains_node(edge.getDestination()):
            new_path = path + edge

            if new_path.get_end() == end:
                if shortest_path is None or new_path.total_distance < shortest_path.total_distance:
                    shortest_path = new_path
                complete_paths.append(new_path)
            elif shortest_path is not None and new_path.total_distance > shortest_path.total_distance:
                continue
            else:
                complete_paths += optimizedDFS(digraph, new_path, end)

    return complete_paths


def directedDFS(digraph, start, end, maxTotalDist, maxOutdoorDist):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxOutdoorDist: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxOutdoorDist constraints, then raises a ValueError.
    """
    return DFS(digraph, start, end, maxTotalDist, maxOutdoorDist, optimizedDFS)


def time_this(func, *args, **kwargs):
    begin = time()
    result = func(*args, **kwargs)
    delta = time() - begin
    return result, delta


# Uncomment below when ready to test
if __name__ == '__main__':
    # Test cases
    digraph = load_map("mit_map.txt")

    LARGE_DIST = 1000000

    # Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    print "Expected: ", expectedPath1
    brutePath1, bruteTime1 = time_this(bruteForceSearch, digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Brute-force: {} ({} s)".format(brutePath1, bruteTime1)
    dfsPath1, directedTime1 = time_this(directedDFS, digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print "DFS: {} ({} s)".format(dfsPath1, directedTime1)

    # Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2, bruteTime2 = time_this(bruteForceSearch, digraph, '32', '56', LARGE_DIST, 0)
    dfsPath2, directedTime2 = time_this(directedDFS, digraph, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: {} ({} s)".format(brutePath2, bruteTime2)
    print "DFS: {} ({} s)".format(dfsPath2, directedTime2)

    # Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3

    # Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4

    # Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5

    # Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6

    # Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'

    try:
        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'

    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    # Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'

    try:
        directedDFS(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'

    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

