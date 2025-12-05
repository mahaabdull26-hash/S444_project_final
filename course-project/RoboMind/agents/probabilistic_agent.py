"""
Probabilistic Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Implement probabilistic reasoning with Bayes' rule
Phase 3 of the project (Week 5-6)
"""

from environment import GridWorld
from ai_core.bayes_reasoning import bayes_update, compute_evidence


class ProbabilisticAgent:
    """
    An agent that uses Bayesian reasoning to handle uncertainty.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the probabilistic agent."""
        self.env = environment
        self.current_pos = environment.start
        
        # Initialize belief map with uniform prior
        self.beliefs = {}
        for r in range(environment.height):
            for c in range(environment.width):
                # Start with a small prior probability of obstacle
                self.beliefs[(r, c)] = 0.2
    
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
    
    def get_sensor_reading(self, position):
        """Get a (possibly noisy) sensor reading."""
        # Simulate sensor with 90% accuracy
        import random
        
        actual_free = self.is_free(position)
        sensor_accuracy = 0.9
        
        # Generate reading based on accuracy
        if random.random() < sensor_accuracy:
            # Correct reading
            return not actual_free  # True = obstacle detected
        else:
            # Incorrect reading
            return actual_free  # False = free detected
    
    def update_beliefs(self, sensor_readings):
        """Update beliefs using Bayes' rule for multiple readings."""
        sensor_accuracy = 0.9
        
        for position, reading in sensor_readings.items():
            prior = self.beliefs[position]
            
            # Determine likelihoods based on sensor reading
            if reading:  # Sensor says "obstacle"
                likelihood_h = sensor_accuracy  # P(sensor=True | obstacle)
                likelihood_not_h = 1 - sensor_accuracy  # P(sensor=True | free)
            else:  # Sensor says "free"
                likelihood_h = 1 - sensor_accuracy  # P(sensor=False | obstacle)
                likelihood_not_h = sensor_accuracy  # P(sensor=False | free)
            
            # Compute evidence
            evidence = compute_evidence(prior, likelihood_h, likelihood_not_h)
            
            # Update belief
            posterior = bayes_update(prior, likelihood_h, evidence)
            self.beliefs[position] = posterior
    
    def act(self):
        """Decide action based on probabilistic beliefs."""
        row, col = self.current_pos
        
        # Get sensor readings for adjacent cells
        neighbors = self.env.get_neighbors(self.current_pos)
        sensor_readings = {}
        
        for neighbor in neighbors:
            # Get noisy sensor reading
            reading = self.get_sensor_reading(neighbor)
            sensor_readings[neighbor] = reading
        
        # Update beliefs based on sensor readings
        self.update_beliefs(sensor_readings)
        
        # Also update belief about current cell (we know it's free)
        self.beliefs[self.current_pos] = 0.0  # We're standing here, so definitely free
        
        # Choose move based on beliefs
        possible_moves = []
        move_probabilities = []
        
        for neighbor in neighbors:
            # Probability that neighbor is free = 1 - probability it has obstacle
            prob_free = 1 - self.beliefs[neighbor]
            
            # Also check if actually free in environment (using is_valid)
            if self.env.is_valid(neighbor):
                possible_moves.append(neighbor)
                move_probabilities.append(prob_free)
        
        # Choose move with highest probability of being free
        if possible_moves:
            best_move = None
            best_prob = -1
            
            for move, prob in zip(possible_moves, move_probabilities):
                if prob > best_prob:
                    best_prob = prob
                    best_move = move
            
            if best_move:
                print(f"Probabilistic Agent moving from {self.current_pos} to {best_move}")
                print(f"  Belief it's free: {best_prob:.1%}")
                self.current_pos = best_move
                self.env.agent_pos = best_move
                return True
        
        print("Probabilistic Agent: No safe moves found!")
        return False


# Simple test
if __name__ == "__main__":
    print("Testing Probabilistic Agent...")
    
    # Create environment
    env = GridWorld(width=5, height=5)
    env.start = (0, 0)
    env.goal = (4, 4)
    
    # Add some obstacles
    env.add_obstacle(0, 1)
    env.add_obstacle(1, 1)
    
    # Create agent
    agent = ProbabilisticAgent(env)
    
    # Take a few steps
    for i in range(5):
        print(f"\nStep {i+1}:")
        success = agent.act()
        if not success:
            break
    
    print("\n✅ Probabilistic Agent test complete!")
    
    # Show final beliefs
    print("\nFinal belief map (probability of obstacle):")
    for r in range(5):
        row_str = ""
        for c in range(5):
            belief = agent.beliefs.get((r, c), 0)
            row_str += f"{belief:.2f} "
        print(row_str)