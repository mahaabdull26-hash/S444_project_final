"""
Logic Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Implement logic-based reasoning agent
Phase 2 of the project (Week 3-4)
"""

from environment import GridWorld
from ai_core.knowledge_base import KnowledgeBase


class LogicAgent:
    """
    An agent that uses propositional logic to reason about the world.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the logic agent."""
        self.env = environment
        self.kb = KnowledgeBase()
        self.current_pos = environment.start
        
    def is_free(self, pos):
        """Check if a position is free (not obstacle)."""
        return self.env.is_valid(pos)
    
    def is_obstacle(self, pos):
        """Check if a position has an obstacle."""
        row, col = pos
        # Check bounds first
        if row < 0 or row >= self.env.height or col < 0 or col >= self.env.width:
            return True
        # Check if it's an obstacle
        return self.env.grid[row][col] == 1
    
    def perceive(self):
        """Perceive the environment and update knowledge base."""
        # Get current position
        row, col = self.current_pos
        
        # Check adjacent cells
        neighbors = self.env.get_neighbors(self.current_pos)
        
        # Add facts about current position
        self.kb.tell(f"At({row},{col})")
        self.kb.tell(f"Explored({row},{col})")
        
        # Since we can get to current position, it must be free
        self.kb.tell(f"Free({row},{col})")
        self.kb.tell(f"Safe({row},{col})")
        
        # Add facts about adjacent cells we can see
        for nr, nc in neighbors:
            # If a cell is in neighbors, it must be free (get_neighbors filters obstacles)
            self.kb.tell(f"Free({nr},{nc})")
            self.kb.tell(f"VisibleFree({nr},{nc})")
            
            # Adjacency facts
            self.kb.tell(f"Adjacent({row},{col},{nr},{nc})")
        
        # Check for obstacles in adjacent positions that aren't in neighbors
        # (positions that would be adjacent but are obstacles)
        all_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in all_directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.env.height and 0 <= nc < self.env.width:
                # If this position exists but is not in neighbors, it's probably an obstacle
                if (nr, nc) not in neighbors and self.is_obstacle((nr, nc)):
                    self.kb.tell(f"VisibleObstacle({nr},{nc})")
    
    def reason(self):
        """Use logic inference to make decisions."""
        # Add some basic rules
        self.kb.add_rule(["At(X,Y)", "Adjacent(X,Y,NX,NY)", "VisibleFree(NX,NY)", "Free(NX,NY)"], "CanMove(X,Y,NX,NY)")
        self.kb.add_rule(["At(X,Y)", "Adjacent(X,Y,NX,NY)", "VisibleObstacle(NX,NY)"], "Blocked(X,Y,NX,NY)")
        self.kb.add_rule(["Explored(X,Y)", "Free(X,Y)"], "Safe(X,Y)")
        
        # Run inference
        self.kb.infer()
    
    def act(self):
        """Decide and execute next action."""
        self.perceive()
        self.reason()
        
        # Get current position
        row, col = self.current_pos
        
        # Check which moves are possible
        neighbors = self.env.get_neighbors(self.current_pos)
        possible_moves = []
        
        for nr, nc in neighbors:
            # Check if we can move here using logic
            query = f"CanMove({row},{col},{nr},{nc})"
            if self.kb.ask(query):
                possible_moves.append((nr, nc))
        
        # If no moves from logic, use basic checking (just use all neighbors)
        if not possible_moves:
            possible_moves = neighbors
        
        # Choose a move (simple: first possible move toward goal)
        if possible_moves:
            # Try to move toward goal
            goal_row, goal_col = self.env.goal
            
            # Simple heuristic: choose move that gets us closer to goal
            best_move = None
            best_distance = float('inf')
            
            for move in possible_moves:
                mr, mc = move
                distance = abs(mr - goal_row) + abs(mc - goal_col)
                if distance < best_distance:
                    best_distance = distance
                    best_move = move
            
            if best_move:
                print(f"Logic Agent moving from {self.current_pos} to {best_move}")
                self.current_pos = best_move
                self.env.agent_pos = best_move
                return True
        
        print("Logic Agent: No valid moves found!")
        return False


# Simple test
if __name__ == "__main__":
    print("Testing Logic Agent...")
    
    # Create environment
    env = GridWorld(width=5, height=5)
    env.start = (0, 0)
    env.goal = (4, 4)
    
    # Add an obstacle
    env.add_obstacle(0, 1)
    
    # Create agent
    agent = LogicAgent(env)
    
    # Take a few steps
    for i in range(5):
        print(f"\nStep {i+1}:")
        success = agent.act()
        if not success:
            break
    
    print("\n✅ Logic Agent test complete!")