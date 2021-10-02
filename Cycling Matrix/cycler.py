#!/usr/bin/python3.8

## Objective get all the unique permutation for all class
"""
example  
class A [A1,A2,A3]
class B [B1,B2,B3]
class C [C1,C2,C3]
result 
day one
A1,B1,C1
A2,B2,C2
A3,B3,C3
day two
A1,B3,C2
A2,B1,C3
A3,B2,C1
day three
A1,B2,C3
A2,B3,C1
A3,B1,C2
stop
"""


from itertools import combinations
from copy import deepcopy
from typing import List, Set, Optional, Iterable, Union


def build_complete_graph(vertex_count: int) -> List[Set[int]]:
    adjacency_list = list([set() for _ in range(vertex_count)])
    for i, j in combinations(range(vertex_count), 2):
        adjacency_list[i].add(j)
        adjacency_list[j].add(i)
    return adjacency_list


def increase_clique_size(adjacency_list: List[Set[int]], clique_size: int, current_clique: List[int],
                         remaining_vertices: Set[int]) -> Iterable[List[int]]:
    remaining_vertices_to_add = clique_size - len(current_clique)
    if remaining_vertices_to_add <= 0:
        yield current_clique
    elif remaining_vertices_to_add == len(remaining_vertices):
        yield current_clique + list(remaining_vertices)
    elif remaining_vertices_to_add <= len(remaining_vertices):
        for candidate_vertex in remaining_vertices:
            # Reduce the remaining vertices by the intersection of the adjacent vertices
            # to the candidate
            candidate_remaining_vertices = remaining_vertices.intersection(adjacency_list[candidate_vertex])
            yield from increase_clique_size(adjacency_list, clique_size, current_clique + [candidate_vertex],
                                            candidate_remaining_vertices)


def greedy_extract_clique(adjacency_list: List[Set[int]], clique_size: int,
                          remaining_vertices: Optional[Set[int]] = None, enumerate_all: bool = False) -> \
        Union[Iterable[List[int]], List[int]]:
    if remaining_vertices is None:
        remaining_vertices = set([i for i in range(len(adjacency_list)) if len(adjacency_list[i]) > 0])
    for clique in increase_clique_size(adjacency_list, clique_size, list(), remaining_vertices):
        if enumerate_all:
            yield clique
        else:
            return clique


def get_edge_count(adjacency_list: List[Set[int]]) -> int:
    return sum([
        len(list(filter(lambda j: j > i, adjacent_vertices)))
        for i, adjacent_vertices in enumerate(adjacency_list)
    ])


def remove_clique(adjacency_list: List[Set[int]], clique: List[int]) -> List[Set[int]]:
    for i in clique:
        adjacency_list[i].difference_update(clique)
    return adjacency_list


def enumerate_clique_partitions(adjacency_list: List[Set[int]], clique_size: int, number_of_cliques: int,
                                previous_cliques: Optional[List[List[int]]] = None) -> Iterable[List[List[int]]]:
    if previous_cliques is None:
        previous_cliques = list()
    if get_edge_count(adjacency_list) == 0:
        yield previous_cliques
    else:
        remaining_vertices = set([i for i in range(len(adjacency_list)) if len(adjacency_list[i]) > 0])
        if (num_cliques_to_forbid := len(previous_cliques) % number_of_cliques) > 0:
            for clique in previous_cliques[-num_cliques_to_forbid:]:
                remaining_vertices.difference_update(clique)
        for clique in greedy_extract_clique(adjacency_list, clique_size, remaining_vertices, enumerate_all=True):
            adjacency_list_without_clique = remove_clique(deepcopy(adjacency_list), clique)
            yield from enumerate_clique_partitions(adjacency_list_without_clique, clique_size, number_of_cliques,
                                                   previous_cliques + [clique])


def verify_clique_partition_optimality(vertex_count: int, cliques: List[List[int]], number_of_cliques: int):
    adjacency_list = build_complete_graph(vertex_count)
    clique_cluster = set()
    for clique_idx, clique in enumerate(cliques):
        if clique_idx % number_of_cliques == 0:
            clique_cluster = set(clique)
        else:
            clique_cluster.update(clique)
        if clique_idx % number_of_cliques == number_of_cliques - 1:
            if len(clique_cluster) != vertex_count:
                return False
        for i, j in combinations(clique, 2):
            if j not in adjacency_list[i] or i not in adjacency_list[j]:
                return False
        remove_clique(adjacency_list, clique)
    return True


def _full_enumeration():
    adjacency_list = build_complete_graph(16)
    for cliques in enumerate_clique_partitions(adjacency_list, 4, 4, list()):
        optimum: bool = verify_clique_partition_optimality(16, cliques, 4)
        if optimum:
            print('Found optimum solution.')
        else:
            print('Found a solution, but it is either incorrect or not optimal')
        for i, clique in enumerate(cliques):
            if i % 4 == 0:
                print('')
            print(clique)
        if optimum:
            return
    print('It is not possible to partition K16 into blocks of disjoint 4-cliques.')


if __name__ == '__main__':
    _full_enumeration()