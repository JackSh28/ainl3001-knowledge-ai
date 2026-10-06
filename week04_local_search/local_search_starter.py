"""
AINL3001 — Knowledge-Driven AI
Week 4 — Local Search and Optimisation
BSP 2026

This week introduces local search.

In previous weeks, search algorithms explored paths through
a state space in order to reach a goal.

Local search takes a different approach:

    1. Start with a state.
    2. Evaluate how good that state is.
    3. Generate neighbouring states.
    4. Move to a better neighbour.
    5. Repeat.

We will explore this using the N-Queens problem.

Tasks
-----

1. Understand the problem representation.
2. Implement conflict counting.
3. Explore neighbouring states.
4. Implement Hill Climbing.
5. Implement Simulated Annealing.
"""

import math
import random

from queens_problem import QueensProblem

N = 8


# --------------------------------------------------
# TASK 0 — UNDERSTANDING THE STATE
# --------------------------------------------------

example_board = [0, 1, 2, 3]

print("Manual Exploration Board:")
print(example_board)

print(
    "\nEach list position represents a column."
)

print(
    "Each value represents the row containing the queen."
)

print(
    "\nQuestion: How many conflicts exist on this board?"
)


# --------------------------------------------------
# TASK 1 — EVALUATE A STATE
# --------------------------------------------------

def count_conflicts(board):
    """
    Return the number of pairs of queens
    that attack each other.

    Lower values are better.

    A solution has:

        conflict count = 0
    """

    # Approach:
    # Compare each queen with every queen
    # that comes after it.
    #
    # Queens conflict when they are:
    #
    #   1. in the same row
    #   2. on the same diagonal
 
    conflicts = 0
    n = len(board)
 
    for i in range(n):
        for j in range(i + 1, n):
 
            # same row
            if board[i] == board[j]:
                conflicts += 1
 
            # same diagonal: the row difference equals
            # the column difference
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
 
    return conflicts


# --------------------------------------------------
# TASK 2 — EXPLORE THE PROBLEM
# --------------------------------------------------

def generate_neighbours(problem, board):
    """
    Generate all neighbouring boards.

    Use the Problem interface introduced this week:

        problem.actions(state)
        problem.result(state, action)
    """

    neighbours = []

    # Approach:
    #
    # 1. Ask the problem for the available actions.
    # 2. Apply each action.
    # 3. Add the resulting state to neighbours.
 
    for action in problem.actions(board):
        new_board = problem.result(board, action)
        neighbours.append(new_board)
 
    return neighbours


# --------------------------------------------------
# TASK 3 — HILL CLIMBING
# --------------------------------------------------

def hill_climbing(problem, start_board):
    """
    Use Hill Climbing to reduce the number
    of conflicts.

    Algorithm:

        current = start state

        repeat:

            generate neighbours

            find the neighbour with the
            lowest conflict count

            if the neighbour is not better:
                stop

            otherwise:
                move to the neighbour

        return current
    """

    current = start_board
    current_cost = count_conflicts(current)
 
    while True:
 
        # a solution has no conflicts, so we can stop
        if current_cost == 0:
            return current
 
        neighbours = generate_neighbours(problem, current)
 
        # find the neighbour with the lowest conflict count
        best_neighbour = neighbours[0]
        best_cost = count_conflicts(best_neighbour)
 
        for neighbour in neighbours:
            cost = count_conflicts(neighbour)
 
            if cost < best_cost:
                best_neighbour = neighbour
                best_cost = cost
 
        # if the best neighbour is not better, we are stuck
        if best_cost >= current_cost:
            return current
 
        # otherwise move to it
        current = best_neighbour
        current_cost = best_cost


# --------------------------------------------------
# TASK 4 — SIMULATED ANNEALING
# --------------------------------------------------

def simulated_annealing(problem, start_board):
    """
    Use Simulated Annealing to search for
    a solution.

    Unlike Hill Climbing, Simulated Annealing
    can sometimes accept a worse state.

    This can help escape local minima.
    """

    current = start_board
 
    temperature = 10.0
    cooling_rate = 0.95
 
    # how many random moves we try at each temperature
    steps_per_temperature = 100
 
    current_cost = count_conflicts(current)
 
    # keep track of the best board we have seen
    best = current
    best_cost = current_cost
 
    while temperature > 0.01 and best_cost > 0:
 
        for step in range(steps_per_temperature):
 
            # pick one random neighbour using the Problem interface
            action = random.choice(problem.actions(current))
            neighbour = problem.result(current, action)
            neighbour_cost = count_conflicts(neighbour)
 
            # positive difference means the neighbour is worse
            difference = neighbour_cost - current_cost
 
            # always accept a better (or equal) board
            # sometimes accept a worse board
            if difference <= 0:
                accept = True
            else:
                probability = math.exp(-difference / temperature)
                accept = random.random() < probability
 
            if accept:
                current = neighbour
                current_cost = neighbour_cost
 
                if current_cost < best_cost:
                    best = current
                    best_cost = current_cost
 
            if best_cost == 0:
                break
 
        # cool down
        temperature = temperature * cooling_rate
 
    return best


# --------------------------------------------------
# EXTENSIONS
# --------------------------------------------------
 
def random_board():
    """
    Return a random board with one queen in each column.
    """
 
    return [random.randint(0, N - 1) for _ in range(N)]
 
 
# Extension 1 - show the board
 
def show_board(board):
    """
    Print the board using Q for a queen
    and . for an empty square.
    """
 
    for row in range(len(board)):
 
        line = ""
 
        for column in range(len(board)):
            if board[column] == row:
                line = line + "Q "
            else:
                line = line + ". "
 
        print(line)
 
 
# Extension 2 - random restart hill climbing
 
def random_restart_hill_climbing(max_restarts):
    """
    Run Hill Climbing from new random boards until
    a solution is found or we run out of restarts.
 
    Returns the best board and the number of
    restarts that were used.
    """
 
    best = None
    best_cost = None
 
    for attempt in range(1, max_restarts + 1):
 
        start = random_board()
        problem = QueensProblem(start)
        final = hill_climbing(problem, start)
        cost = count_conflicts(final)
 
        if best is None or cost < best_cost:
            best = final
            best_cost = cost
 
        if cost == 0:
            return best, attempt
 
    return best, max_restarts


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":
 
    board = [
        random.randint(0, N - 1)
        for _ in range(N)
    ]
 
    problem = QueensProblem(board)
 
    print("\nRandom Board")
    print(board)
 
    print("\nConflicts")
    print(
        count_conflicts(board)
    )
 
    print("\nPossible Actions")
 
    actions = problem.actions(board)
 
    print(
        f"{len(actions)} actions available"
    )
 
    print("\nNeighbours")
 
    neighbours = generate_neighbours(
        problem,
        board
    )
 
    print(
        f"{len(neighbours)} neighbours generated"
    )
 
    # ----------------------------------------------
    # Tasks 3 and 4 - test
    # ----------------------------------------------
 
    print("\nTask 0 check: [0, 1, 2, 3] has",
          count_conflicts([0, 1, 2, 3]), "conflicts")
 
    print("\nHill Climbing - 5 runs")
 
    for attempt in range(1, 6):
        start = random_board()
        problem = QueensProblem(start)
        final = hill_climbing(problem, start)
        print(attempt, "final cost:", count_conflicts(final))
 
    print("\nSimulated Annealing - 5 runs")
 
    for attempt in range(1, 6):
        start = random_board()
        problem = QueensProblem(start)
        final = simulated_annealing(problem, start)
        print(attempt, "final cost:", count_conflicts(final))
 
    # compare the two over 100 runs
    runs = 100
    hc_solved = 0
    sa_solved = 0
 
    for _ in range(runs):
        start = random_board()
        problem = QueensProblem(start)
 
        if count_conflicts(hill_climbing(problem, start)) == 0:
            hc_solved += 1
 
        if count_conflicts(simulated_annealing(problem, start)) == 0:
            sa_solved += 1
 
    print("\nSolved out of", runs, "runs")
    print("Hill Climbing:", hc_solved)
    print("Simulated Annealing:", sa_solved)
    
    # Extension 1
    print("\nExtension 1 - final board from Simulated Annealing")
    start = random_board()
    problem = QueensProblem(start)
    final = simulated_annealing(problem, start)
    print("Start:", start)
    show_board(start)
    print("Final:", final)
    show_board(final)
 
    # Extension 2
    print("\nExtension 2 - Random Restart Hill Climbing")
    board, restarts = random_restart_hill_climbing(20)
    print("Conflicts:", count_conflicts(board),
          "after", restarts, "restart(s)")