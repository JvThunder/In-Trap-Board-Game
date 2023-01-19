def RandomAgent(env):
    '''
    Choosing a random valid move every turn.
    '''
    
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

    possible_moves = find_valid_moves(env)
    mtype, id, direction = random.choice(possible_moves)
    return mtype, id, direction