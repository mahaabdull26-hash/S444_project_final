"""
Bayesian Reasoning Module
SE444 - Artificial Intelligence Course Project

TODO: Implement Bayesian belief updates for handling uncertainty
Phase 3 (Week 5-6)
"""

from typing import Dict, Tuple


def bayes_update(prior: float, likelihood: float, evidence: float) -> float:
    """
    Update belief using Bayes' Rule.
    """
    # Bayes' Rule: P(H|E) = P(E|H) * P(H) / P(E)
    
    # Check for division by zero
    if evidence == 0:
        return 0.0
    
    posterior = (likelihood * prior) / evidence
    return posterior


def compute_evidence(prior: float, likelihood_h: float, likelihood_not_h: float) -> float:
    """
    Compute total probability of evidence P(E) using law of total probability.
    """
    # Law of total probability: P(E) = P(E|H)*P(H) + P(E|¬H)*P(¬H)
    p_not_h = 1 - prior  # Probability hypothesis is false
    
    evidence = (likelihood_h * prior) + (likelihood_not_h * p_not_h)
    return evidence


def update_belief_map(belief_map: Dict[Tuple[int, int], float],
                      sensor_reading: bool,
                      sensor_accuracy: float = 0.9) -> Dict[Tuple[int, int], float]:
    """
    Update entire grid belief map based on sensor reading.
    """
    updated_map = {}
    
    for cell, prior in belief_map.items():
        # Determine likelihood based on sensor reading
        if sensor_reading:
            # Sensor says "obstacle"
            likelihood_h = sensor_accuracy  # P(sensor=True | obstacle)
            likelihood_not_h = 1 - sensor_accuracy  # P(sensor=True | free)
        else:
            # Sensor says "free"
            likelihood_h = 1 - sensor_accuracy  # P(sensor=False | obstacle)
            likelihood_not_h = sensor_accuracy  # P(sensor=False | free)
        
        # Compute total evidence probability
        evidence = compute_evidence(prior, likelihood_h, likelihood_not_h)
        
        # Apply Bayes' rule
        posterior = bayes_update(prior, likelihood_h, evidence)
        
        updated_map[cell] = posterior
    
    return updated_map


def sensor_model(actual_state: bool, sensor_accuracy: float = 0.9) -> Tuple[float, float]:
    """
    Define the sensor model probabilities.
    """
    if actual_state:  # obstacle exists
        return sensor_accuracy, 1 - sensor_accuracy
    else:  # no obstacle
        return 1 - sensor_accuracy, sensor_accuracy


# ============================================================================
# Testing Code
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing Bayesian Reasoning")
    print("=" * 60 + "\n")
    
    print("Example: Medical diagnosis")
    print("-" * 40)
    print("Disease prevalence: 1% (P(Disease) = 0.01)")
    print("Test accuracy: 95% (P(+|Disease) = 0.95)")
    print("False positive: 10% (P(+|Healthy) = 0.10)")
    print("\nPatient tests positive. What's the probability they have the disease?")
    
    try:
        # Prior
        P_disease = 0.01
        P_healthy = 1 - P_disease
        
        # Likelihood
        P_pos_given_disease = 0.95
        P_pos_given_healthy = 0.10
        
        # Evidence
        P_pos = compute_evidence(P_disease, P_pos_given_disease, P_pos_given_healthy)
        
        # Posterior
        P_disease_given_pos = bayes_update(P_disease, P_pos_given_disease, P_pos)
        
        print(f"\nResult: P(Disease|+) = {P_disease_given_pos:.1%}")
        print("(Surprisingly low despite positive test!)")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("  Example: Robot Sensor")
    print("=" * 60)
    print("\nRobot sensor is 90% accurate")
    print("Prior belief cell has obstacle: 30%")
    print("Sensor detects obstacle")
    print("\nWhat's updated belief?")
    
    try:
        P_obstacle = 0.30
        P_detect_if_obstacle = 0.90
        P_detect_if_free = 0.10
        
        P_detect = compute_evidence(P_obstacle, P_detect_if_obstacle, P_detect_if_free)
        P_obstacle_given_detect = bayes_update(P_obstacle, P_detect_if_obstacle, P_detect)
        
        print(f"\nResult: P(Obstacle|Detected) = {P_obstacle_given_detect:.1%}")
        print(f"Belief increased from {P_obstacle:.1%} to {P_obstacle_given_detect:.1%}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("  Testing Belief Map Update")
    print("=" * 60)
    
    try:
        # Create a simple belief map
        beliefs = {
            (0, 0): 0.5,  # 50% chance obstacle
            (0, 1): 0.3,  # 30% chance obstacle
            (1, 0): 0.7,  # 70% chance obstacle
        }
        
        print("\nInitial beliefs:")
        for cell, belief in beliefs.items():
            print(f"  Cell {cell}: {belief:.1%}")
        
        # Update based on sensor reading
        sensor_says_obstacle = True
        updated = update_belief_map(beliefs, sensor_says_obstacle, 0.9)
        
        print("\nUpdated beliefs (sensor says 'obstacle'):")
        for cell, belief in updated.items():
            print(f"  Cell {cell}: {belief:.1%}")
        
        print("\n✅ All Bayesian reasoning tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n💡 Tip: Start with the basic bayes_update() function,")
    print("   then build up to belief maps!")