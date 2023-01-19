if __name__ == "__main__":
    # Simulate a game
    from InTrap_env import InTrap, simulate_game, evaluate
    from agents.heuristic_v1_agent import HeuristicAgent
    env = InTrap()

    # To simulate 1 game using the code below 
    simulate_game(env, HeuristicAgent, HeuristicAgent, verbose = True)

    # To check winning rate on 100 games using the code below
    # evaluate(env, HeuristicAgent, HeuristicAgent, N_GAMES = 10, verbose = False)