from collections import deque
import random

class StateFarmer:
    def __init__(self, farmer, wolf, sheep, cabbage, dog, hurt=False):
        "Receives the initial states for each element"
        self.farmer = farmer
        self.wolf = wolf
        self.sheep = sheep
        self.cabbage = cabbage
        self.dog = dog
        self.hurt = hurt

    def __eq__(self, other_states):
        """Checks if two StateFarmer objects are equal by comparing their attributes."""
        return (self.farmer == other_states.farmer and
            self.wolf == other_states.wolf and
            self.sheep == other_states.sheep and 
            self.cabbage == other_states.cabbage and 
            self.dog == other_states.dog and
            self.hurt == other_states.hurt)
    
    def __hash__(self):
        """Generates a hash based on the state attributes for efficient use in hash-based collections like sets and dictionaries."""
        return hash((self.farmer, self.wolf, self.sheep, self.cabbage, self.dog, self.hurt))
    
    def __str__(self):
        """Returns string for visualization of the present states"""
        return f"[{self.farmer, self.wolf, self.sheep, self.cabbage, self.dog, self.hurt}]"
    
    def is_valid(self):
        """Verifies if the present state is valid"""
        # Sheep eats Cabbage if without farmer
        if (self.sheep == self.cabbage and self.sheep != self.farmer):
            return False
        # Wolf eats Sheep if without farmer
        if self.sheep == self.wolf and self.wolf != self.farmer:
            return False
        # Dog bites Wolf if they are alone
        # Dog plays with Cabbage and doesn't bite Wolf
        # If the wolf gets hurt in the process and it's not in the objective not valid state
        if (self.dog == self.wolf and self.dog != self.farmer and
            self.cabbage != self.dog and 
            self.wolf == "e"):
            return False
        
        return True
    
    def is_objective(self):
        """Verifies if the present state is the objective state"""
        return (self.farmer == 'd' and
                self.wolf == 'd' and
                self.sheep == 'd' and
                self.cabbage == 'd' and
                self.dog == 'd')
    
# Function to generate all possible successors of the current state
# Verifies if the change is possible and if the state is valid
# Returns a list of successors 
def generate_successors(state, allow_random=False):
    successors = []

    # Case where the Sheep jumps randomly into the boat because it's impatient
    if allow_random and state.sheep == state.farmer and random.choice([True, False]):
        if state.farmer == 'e':
            new_state = StateFarmer('d', state.wolf, 'd', state.cabbage, state.dog)
            if new_state.is_valid():
                successors.append(("takesSheepImpatience", new_state))
        else:
            new_state = StateFarmer('e', state.wolf, 'e', state.cabbage, state.dog)
            if new_state.is_valid():
                successors.append(("bringsSheepImpatience", new_state))

    # Operator 1: Farmer goes alone
    if state.farmer == 'e':
        new_state = StateFarmer('d', state.wolf, state.sheep, state.cabbage, state.dog)
        if new_state.is_valid():
            successors.append(("farmerGoes", new_state))
    else:
        new_state = StateFarmer('e', state.wolf, state.sheep, state.cabbage, state.dog)
        if new_state.is_valid():
            successors.append(("farmerCames", new_state))
    
    # Operator 2: Farmer takes Wolf
    # Verifies if they are on the same side
    if state.farmer == state.wolf:
        if state.farmer == 'e':
            new_state = StateFarmer('d', 'd', state.sheep, state.cabbage, state.dog)
            if new_state.is_valid(): 
                successors.append(("takesWolf",new_state))
        else:
            new_state = StateFarmer('e', 'e', state.sheep, state.cabbage, state.dog)
            if new_state.is_valid():
                successors.append(("bringsWolf", new_state))

    # Operator 3: Farmer takes Sheep
    # Verifies if they are on the same side
    if state.farmer == state.sheep:
        if state.farmer == 'e':
            new_state = StateFarmer('d', state.wolf, 'd', state.cabbage, state.dog)
            if new_state.is_valid():
                successors.append(("takesSheep", new_state))
        else:
            new_state = StateFarmer('e', state.wolf, 'e', state.cabbage, state.dog)
            if new_state.is_valid():
                successors.append(("bringsSheep", new_state))

    # Operator 4: Farmer takes Cabbage
    # Verifies if they are on the same side
    if state.farmer == state.cabbage:
        if state.farmer == 'e':
            new_state = StateFarmer('d', state.wolf, state.sheep, 'd', state.dog)
            if new_state.is_valid():
                successors.append(("takesCabbage", new_state))
        else:
            new_state = StateFarmer('e', state.wolf, state.sheep, 'e', state.dog)
            if new_state.is_valid():
                successors.append(("bringsCabbage", new_state))

    # Operator 5: Farmer takes Dog
    # Verifies if they are on the same side
    if state.farmer == state.dog:
        if state.farmer == 'e':
            new_state = StateFarmer('d', state.wolf, state.sheep, state.cabbage, 'd')
            if new_state.is_valid():
                successors.append(("takesDog", new_state))
        else:
            new_state = StateFarmer('e', state.wolf, state.sheep, state.cabbage, 'e')
            if new_state.is_valid():
                successors.append(("bringsDog", new_state))

    return successors

def breadth_first_search(initial_state=None, allow_random=False):
    """Performs a breadth-first search to find the solution"""
    if initial_state is None:
        initial_state = StateFarmer('e', 'e', 'e', 'e', 'e')
    # Creation of a list to store the visited states and never repeat them
    visited = set()
    # Creation of a queue to store the states to be visited
    # The queue stores tuples of (state, path)
    # The path is a list of tuples (action, state)
    queue = deque([(initial_state, [])])
    cont = 0
    while queue:
        state, path = queue.popleft()
        # Check if the state is the objective state
        if state.is_objective():
            print("Number of generated successors:", cont)
            return path
        # Do not allow repeat states
        visited.add(state)

        # Generate successors and verifies if not visited
        # The successors are generated based on the current state
        for action, successor in generate_successors(state, allow_random=allow_random):
            cont += 1
            # Hash and equality are used to check if the state is already visited quickly
            if successor not in visited:
                # Append the successor state and the path to get there
                queue.append((successor, path + [(action, successor)]))                

    return None

def print_solution(solution):
    """Prints the solution found in a readable format"""
    if solution is None:
        print("No solution found for the problem!")
    else:
        print("Number of steps in the solution path:", len(solution))
        print("Initial state: [e, e, e, e, e]")
        for i, (action, state) in enumerate(solution, 1):
            print(f"Step {i}: {action} -> {state}")

if __name__ == "__main__":
    initial_state = StateFarmer('e', 'e', 'e', 'e', 'e')
    # Set allow_random to True to enable the random sheep behavior
    solution = breadth_first_search(initial_state, allow_random=True)
    print_solution(solution)