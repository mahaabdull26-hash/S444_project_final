"""
Hybrid Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Integrate search + logic + probability
Phase 4 of the project (Week 7-8) - Final Integration
"""

from environment import GridWorld
from agents.search_agent import SearchAgent
from agents.logic_agent import LogicAgent
from agents.probabilistic_agent import ProbabilisticAgent
from ai_core.knowledge_base import KnowledgeBase
from ai_core.bayes_reasoning import bayes_update


class HybridAgent:
    """
    A rational agent that integrates search, logic, and probabilistic reasoning.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the hybrid agent."""
        self.env = environment
        self.current_pos = environment.start
        
        # Initialize all components
        self.search_agent = SearchAgent(environment)
        self.logic_agent = LogicAgent(environment)
        self.prob_agent = ProbabilisticAgent(environment)
        
        # Knowledge base for hybrid reasoning
        self.kb = KnowledgeBase()
        
        # Beliefs for uncertain areas
        self.beliefs = {}
        
        # Strategy tracker
        self.strategy = "search"  # Default strategy
        
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


      # ------------------------------------------------------------------
    # Perception + simple logical facts
  # ------------------------------------------------------------------
    
    def perceive(self):
        """
        Get sensor readings from environment.
        """
        # Get current position info
        row, col = self.current_pos
        
        # Update knowledge base with basic facts
        self.kb.tell(f"At({row},{col})")
        self.kb.tell(f"Explored({row},{col})")
        
        # Since we're here, it must be free
        self.kb.tell(f"Free({row},{col})")
        
        # Check line of sight to goal
        if self.has_line_of_sight():
            self.kb.tell("GoalVisible")
        else:
            self.kb.tell("GoalHidden")
        
        # Check if path seems clear (simple heuristic)
        if self.path_clearness() > 0.7:
            self.kb.tell("PathClear")
        else:
            self.kb.tell("PathUncertain")
    
    def has_line_of_sight(self):
        """Check if we can see the goal directly."""
        # Simple line-of-sight check (ignoring obstacles for simplicity)
        row, col = self.current_pos
        goal_row, goal_col = self.env.goal
        
        # If we're close to goal in Manhattan distance
        distance = abs(row - goal_row) + abs(col - goal_col)
        return distance < 5
    
    def path_clearness(self):
        """Estimate how clear the path to goal is."""
        # Simple estimate based on known obstacles
        row, col = self.current_pos
        goal_row, goal_col = self.env.goal
        
        # Count how many cells we've explored
        explored_count = 0
        free_count = 0
        
        # Simple area check
        for r in range(min(row, goal_row), max(row, goal_row) + 1):
            for c in range(min(col, goal_col), max(col, goal_col) + 1):
                if 0 <= r < self.env.height and 0 <= c < self.env.width:
                    explored_count += 1
                    if self.is_free((r, c)):
                        free_count += 1
        
        if explored_count == 0:
            # If we know nothing, return a neutral value
            return 0.5  # Unknown
        
        return free_count / explored_count

      # ------------------------------------------------------------------
    # Search-based planning
       # ------------------------------------------------------------------
    
    def plan(self):
        """
        Use search algorithms to plan path to goal.
        """
       # Try A* with Manhattan heuristic
        path, cost, expanded = self.search_agent.search('astar', 'manhattan')
        
        if path:
            print(f"Search found path with {len(path)} steps, cost {cost}")
            return path
        else:
            print("Search failed to find path")
            return None

     # ------------------------------------------------------------------
    # Logical reasoning about which strategy to use
      # ------------------------------------------------------------------
    
    def reason(self):
        """
        Use logic to infer safe moves and update knowledge base.
        """
        # Add hybrid-specific rules
        self.kb.add_rule(["GoalVisible", "PathClear"], "UseSearch")
        self.kb.add_rule(["GoalHidden"], "UseLogic")
        self.kb.add_rule(["PathUncertain"], "UseProbability")
        
        # Run inference
        self.kb.infer()
        
        # Determine strategy
        if self.kb.ask("UseSearch"):
            self.strategy = "search"
        elif self.kb.ask("UseLogic"):
            self.strategy = "logic"
        elif self.kb.ask("UseProbability"):
            self.strategy = "probability"
        
        print(f"Strategy selected: {self.strategy}")
    
    def update_beliefs(self):
        """
        Use Bayesian inference to handle uncertain sensor readings.
        """
        # Simple belief update for adjacent cells
        neighbors = self.env.get_neighbors(self.current_pos)
        
        for neighbor in neighbors:
            if neighbor not in self.beliefs:
                # Initialize with prior
            self.beliefs[neighbor] = 0.3
            
            # Simulate sensor reading (90% accurate)
         actual_free = self.is_free(neighbor)
            sensor_accuracy = 0.9
            
            # Generate reading
            import random
            if random.random() < sensor_accuracy:
                reading = not actual_free  # Correct reading
            else:
                reading = actual_free  # Incorrect reading
            
         # Update belief using Bayes
            prior = self.beliefs[neighbor]
            
     if reading:  # Sensor says "obstacle"
                likelihood = sensor_accuracy
            else:  # Sensor says "free"
                likelihood = 1 - sensor_accuracy
            
            # Simple update (normalized)
            evidence = (likelihood * prior) + ((1 - likelihood) * (1 - prior))
         if evidence > 0:
                posterior = (likelihood * prior) / evidence
                self.beliefs[neighbor] = posterior
    
    def act(self):
        """
        Integrate all reasoning techniques to decide next action.
        """
     # Perceive environment
        self.perceive()
        
         # Reason about strategy
        self.reason()
        
     # Update probabilistic beliefs
        self.update_beliefs()
        
 # act based on chosen strategy
        if self.strategy == "search":
            # Try to use search
            path = self.plan()
            if path and len(path) > 1:
                # Move along planned path
                next_pos = path[1]  # Current pos is path[0]
                print(f"Hybrid Agent (search) moving to {next_pos}")
                self.current_pos = next_pos
                self.env.agent_pos = next_pos
                return True
        
        elif self.strategy == "logic":
            # Use logic reasoning
            # Simplified logic-based move selection
            neighbors = self.env.get_neighbors(self.current_pos)
            for neighbor in neighbors:
                if self.is_free(neighbor):
                    # Move to first free neighbor
                    print(f"Hybrid Agent (logic) moving to {neighbor}")
                    self.current_pos = neighbor
                    self.env.agent_pos = neighbor
                    return True
        
        elif self.strategy == "probability":
            # Use probabilistic reasoning
            # Choose move with lowest belief of obstacle
            neighbors = self.env.get_neighbors(self.current_pos)
            best_move = None
            best_belief = 2.0  # Start higher than possible
            
            for neighbor in neighbors:
                if self.is_free(neighbor):
                    # Get belief this cell has obstacle
                    belief = self.beliefs.get(neighbor, 0.5)
                    if belief < best_belief:
                        best_belief = belief
                        best_move = neighbor
            
            if best_move:
                print(f"Hybrid Agent (probability) moving to {best_move}")
                print(f"  Belief of obstacle: {best_belief:.1%}")
                self.current_pos = best_move
                self.env.agent_pos = best_move
                return True

          # 5) fallback strategy: if everything else failed  just move to any free neighbor
        neighbors = self.env.get_neighbors(self.current_pos)
        for neighbor in neighbors:
            if self.is_free(neighbor):
                print(f"Hybrid Agent (fallback) moving to {neighbor}")
                self.current_pos = neighbor
                self.env.agent_pos = neighbor
                return True

        # If we reach this point, there are no valid moves at all
        print("Hybrid Agent: No valid moves!")
        return False


# Example usage
if __name__ == "__main__":
    print("Hybrid Agent - combines Search + Logic + Probability")
    print("This is the final phase - integrate everything!")
    
    # Create test environment
    env = GridWorld(width=8, height=8)
    env.start = (0, 0)
    env.goal = (7, 7)
    
    # Add some obstacles
    obstacles = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    for obs in obstacles:
        env.add_obstacle(*obs)
    
    # Create hybrid agent
    agent = HybridAgent(env)
    
    # Run for a few steps
    for step in range(10):
        print(f"\n=== Step {step + 1} ===")
        success = agent.act()
        
        if not success:
            print("Agent stuck!")
            break
        
        if agent.current_pos == env.goal:
            print("🎉 Goal reached!")
            break
    
    print("\n✅ Hybrid Agent test complete!")
