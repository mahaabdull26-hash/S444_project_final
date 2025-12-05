"""
Search Algorithms - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Implement the following search algorithms:
1. Breadth-First Search (BFS)
2. Uniform Cost Search (UCS)
3. A* Search

This is the CORE of Phase 1 (Week 1-2)
"""

from typing import Tuple, List, Optional
from collections import deque
import heapq


def bfs(env, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List], float, int]:
    """
    Breadth-First Search - Find shortest path in terms of number of steps.
    """
    
    # Create a queue for BFS (FIFO - First In First Out)
    queue = deque()
    queue.append(start)
    
    # Keep track of visited nodes
    visited = set()
    visited.add(start)
    
    # Store parent nodes to reconstruct path later
    parent = {}
    parent[start] = None
    
    # Count how many nodes we expand
    expanded = 0
    
    while queue:
        # Get the next node from the queue
        current = queue.popleft()
        expanded += 1
        
        # Check if we found the goal
        if current == goal:
            # Reconstruct the path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()  # Reverse to get start-to-goal order
            
            # Cost is number of steps minus 1
            cost = len(path) - 1
            return path, cost, expanded
        
        # Get all neighbors of current node
        neighbors = env.get_neighbors(current)
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    # If we get here, no path was found
    return None, float('inf'), expanded


def ucs(env, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List], float, int]:
    """
    Uniform Cost Search - Find path with lowest total cost.
    """
    
    # Priority queue: (cost, position)
    frontier = []
    heapq.heappush(frontier, (0, start))
    
    # Track visited nodes
    visited = set()
    
    # Track best cost to reach each node
    cost_so_far = {}
    cost_so_far[start] = 0
    
    # Store parent nodes for path reconstruction
    parent = {}
    parent[start] = None
    
    expanded = 0
    
    while frontier:
        # Get node with lowest cost
        current_cost, current = heapq.heappop(frontier)
        
        # Skip if already visited
        if current in visited:
            continue
            
        visited.add(current)
        expanded += 1
        
        # Check if we found the goal
        if current == goal:
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            return path, current_cost, expanded
        
        # Check all neighbors
        neighbors = env.get_neighbors(current)
        
        for neighbor in neighbors:
            if neighbor in visited:
                continue
                
            # Calculate new cost to reach neighbor
            move_cost = env.get_cost(current, neighbor)
            new_cost = current_cost + move_cost
            
            # If we found a better path to neighbor, or it's the first time
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(frontier, (new_cost, neighbor))
    
    # No path found
    return None, float('inf'), expanded


def astar(env, start: Tuple[int, int], goal: Tuple[int, int], 
          heuristic='manhattan') -> Tuple[Optional[List], float, int]:
    """
    A* Search - Find optimal path using cost + heuristic.
    """
    
    # Choose which heuristic to use
    if heuristic == 'manhattan':
        def h(pos):
            return env.manhattan_distance(pos, goal)
    elif heuristic == 'euclidean':
        def h(pos):
            return env.euclidean_distance(pos, goal)
    else:
        raise ValueError(f"Unknown heuristic: {heuristic}")
    
    # Priority queue for A*: (f_score, position)
    frontier = []
    heapq.heappush(frontier, (h(start), start))
    
    # Track visited nodes
    visited = set()
    
    # g_score = actual cost from start to node
    g_score = {}
    g_score[start] = 0
    
    # f_score = g_score + heuristic
    f_score = {}
    f_score[start] = h(start)
    
    # Parent pointers
    parent = {}
    parent[start] = None
    
    expanded = 0
    
    while frontier:
        current_f, current = heapq.heappop(frontier)
        
        if current in visited:
            continue
            
        visited.add(current)
        expanded += 1
        
        # Check if we found goal
        if current == goal:
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            return path, g_score[current], expanded
        
        # Check neighbors
        neighbors = env.get_neighbors(current)
        
        for neighbor in neighbors:
            if neighbor in visited:
                continue
                
            # Calculate tentative g_score
            move_cost = env.get_cost(current, neighbor)
            tentative_g = g_score[current] + move_cost
            
            # If this is a better path to neighbor
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h(neighbor)
                parent[neighbor] = current
                heapq.heappush(frontier, (f_score[neighbor], neighbor))
    
    # No path found
    return None, float('inf'), expanded


def reconstruct_path(parent: dict, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Reconstruct path from parent pointers.
    """
    path = []
    current = goal
    
    # Follow parent pointers from goal to start
    while current is not None:
        path.append(current)
        current = parent.get(current)
    
    # Reverse to get start-to-goal order
    path.reverse()
    
    # Check if we actually got from start to goal
    if path[0] == start:
        return path
    else:
        return []  # No valid path


# ============================================================================
# Testing Code (You can run this file directly to test your implementations)
# ============================================================================

if __name__ == "__main__":
    from environment import GridWorld
    
    print("=" * 60)
    print("  Testing Search Algorithms")
    print("=" * 60 + "\n")
    
    # Create a test environment
    env = GridWorld(width=10, height=10)
    
    # Add obstacles
    for i in range(3, 8):
        env.add_obstacle(i, 5)
    
    start = (0, 0)
    goal = (9, 9)
    
    print(f"Grid: {env.width}x{env.height}")
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")
    
    # Test each algorithm
    algorithms = [
        ('BFS', lambda: bfs(env, start, goal)),
        ('UCS', lambda: ucs(env, start, goal)),
        ('A* (Manhattan)', lambda: astar(env, start, goal, 'manhattan')),
        ('A* (Euclidean)', lambda: astar(env, start, goal, 'euclidean')),
    ]
    
    results = []
    
    for name, algo_func in algorithms:
        print(f"\nTesting {name}...")
        print("-" * 40)
        try:
            path, cost, expanded = algo_func()
            if path:
                print(f"✓ Success!")
                print(f"  Path length: {len(path)} steps")
                print(f"  Path cost: {cost:.2f}")
                print(f"  Nodes expanded: {expanded}")
                results.append((name, True, len(path), cost, expanded))
            else:
                print(f"✗ No path found")
                results.append((name, False, 0, 0, 0))
        except NotImplementedError:
            print(f"⚠️  Not implemented yet")
            results.append((name, False, 0, 0, 0))
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append((name, False, 0, 0, 0))
    
    # Summary table
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"{'Algorithm':<20} {'Status':<10} {'Length':<8} {'Cost':<8} {'Expanded':<10}")
    print("-" * 60)
    
    for name, success, length, cost, expanded in results:
        status = "✓" if success else "✗"
        length_str = str(length) if success else "-"
        cost_str = f"{cost:.2f}" if success else "-"
        expanded_str = str(expanded) if success else "-"
        print(f"{name:<20} {status:<10} {length_str:<8} {cost_str:<8} {expanded_str:<10}")
    
    print("-" * 60)
    print("\n💡 Tip: Implement the algorithms one at a time and test each one!")
    print("   Start with BFS (simplest), then UCS, then A*\n")