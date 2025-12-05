"""
Knowledge Base - Logic Reasoning Module
SE444 - Artificial Intelligence Course Project

TODO: Implement propositional logic knowledge base with inference
Phase 2 (Week 3-4)
"""

from typing import Set, List


class KnowledgeBase:
    """
    A simple knowledge base for propositional logic.
    """
    
    def __init__(self):
        """Initialize empty knowledge base."""
        self.facts = set()   # Known facts
        self.rules = []      # Rules: (premises, conclusion)
    
    def tell(self, fact: str):
        """
        Add a fact to the knowledge base.
        """
        self.facts.add(fact)
        print(f"Added fact: {fact}")
    
    def add_rule(self, premises: List[str], conclusion: str):
        """
        Add an inference rule.
        """
        self.rules.append((premises, conclusion))
        print(f"Added rule: {' AND '.join(premises)} → {conclusion}")
    
    def ask(self, query: str) -> bool:
        """
        Check if a query can be inferred from the knowledge base.
        """
        return query in self.facts
    
    def infer(self):
        """
        Apply forward chaining to derive new facts from rules.
        """
        new_facts_added = True
        
        # Keep going until no new facts are added
        while new_facts_added:
            new_facts_added = False
            
            # Check each rule
            for premises, conclusion in self.rules:
                # Check if all premises are in facts
                all_premises_true = True
                for premise in premises:
                    if premise not in self.facts:
                        all_premises_true = False
                        break
                
                # If all premises are true, add conclusion
                if all_premises_true and conclusion not in self.facts:
                    self.tell(conclusion)
                    new_facts_added = True
    
    def __str__(self) -> str:
        """String representation of KB."""
        facts_list = list(self.facts)
        facts_list.sort()
        
        result = "Knowledge Base:\n"
        result += "Facts:\n"
        for fact in facts_list:
            result += f"  - {fact}\n"
        
        result += "\nRules:\n"
        for premises, conclusion in self.rules:
            result += f"  - {' AND '.join(premises)} → {conclusion}\n"
        
        return result


# ============================================================================
# Testing Code
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing Knowledge Base")
    print("=" * 60 + "\n")
    
    # Create KB
    kb = KnowledgeBase()
    
    # Add some facts
    print("Adding facts...")
    kb.tell("Safe(2,3)")
    kb.tell("Free(2,3)")
    kb.tell("Adjacent(2,3,2,4)")
    kb.tell("Free(2,4)")
    
    # Add some rules
    print("\nAdding rules...")
    kb.add_rule(["Safe(2,3)", "Free(2,3)"], "CanMove(2,3)")
    kb.add_rule(["Safe(2,3)", "Adjacent(2,3,2,4)", "Free(2,4)"], "SafePath(2,3,2,4)")
    kb.add_rule(["SafePath(2,3,2,4)", "Safe(2,4)"], "CanMove(2,4)")
    
    # Query
    print("\nQuerying before inference...")
    print(f"Is Safe(2,3) known? {kb.ask('Safe(2,3)')}")
    print(f"Is CanMove(2,3) known? {kb.ask('CanMove(2,3)')}")
    print(f"Is SafePath(2,3,2,4) known? {kb.ask('SafePath(2,3,2,4)')}")
    
    # Try inference
    print("\nRunning inference...")
    kb.infer()
    
    print("\nQuerying after inference...")
    print(f"Is CanMove(2,3) known? {kb.ask('CanMove(2,3)')}")
    print(f"Is SafePath(2,3,2,4) known? {kb.ask('SafePath(2,3,2,4)')}")
    
    print(f"\n{kb}")
    print("\n✅ Forward chaining implemented successfully!")