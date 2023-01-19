def NegaMaxAgent(env):
    '''
    Simple Agent checking with depth 3. 
    The agent will try to save the Spawner.
    A good benchmark will be to defeat this agent.
    (This version is quite slow to run)
    '''

    import copy
    import random
    
    def find_valid_moves(curr_env):
        possible_moves = []
        
        # mtype = 1
        for piece in curr_env.pieces:
            if piece:
                if piece['position'] == (-1,-1):
                    for direction in curr_env.direction_list:
                        id = piece['id']
                        if curr_env.check_move(1, id, direction):
                            possible_moves.append((1, id, direction))
        
        # mtype = 2
        for piece in curr_env.pieces:
            if piece:
                id = piece['id']
                if piece['color'] == curr_env.player_turn:
                    for direction in curr_env.direction_list:
                        if curr_env.check_move(2, id, direction):
                            possible_moves.append((2, id, direction))
        
        return possible_moves
    
    def negamax_tree(curr_env, depth = 2, player_sign = 1):
        if depth == 0:
            return 0, (-1,-1,-1)
            
        if curr_env.winner != 0:
            return -player_sign, (-1,-1,-1)

        max_reward = 0
        best_move = []

        possible_moves = find_valid_moves(curr_env)
        for mtype, id, direction in possible_moves:
            nxt_env = copy.deepcopy(curr_env)
            valid = nxt_env.move(mtype, id, direction, check_validity = False)
            if not valid:
                continue
            reward, move = negamax_tree(nxt_env, depth-1, -player_sign)
            if reward > max_reward:
                max_reward = reward
                best_move = [(mtype, id, direction)]
            elif reward == max_reward:
                best_move.append((mtype, id, direction))

        return max_reward, random.choice(best_move)
    
    max_reward, best_move = negamax_tree(env)
    return best_move