def HeuristicAgent(env):
    '''
    The best agent so far. It evaluates certain heuristics valuing the pieces on the board 
    and also whether the king is under attacked or not.
    '''
    
    import copy
    
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
    
    # Edit Heuristic Valuation here
    def calc_value_board(curr_env, player_turn):
        value = 0
        if curr_env.winner != 0:
            value += 100
        
        for piece in curr_env.pieces:
            if piece == None:
                continue
            if piece['color'] == player_turn:
                value += 10
                for direction in curr_env.direction_list:
                    capture_list = curr_env.check_capture(2, piece['id'], direction)
                    if (3 - player_turn) in capture_list:
                        value += 50
            else:
                value -= 15
                for direction in curr_env.direction_list:
                    capture_list = curr_env.check_capture(2, piece['id'], direction)
                    if player_turn in capture_list:
                        value -= 50
        return value
        
    possible_moves = find_valid_moves(env)
    best_move = (-1,-1,-1)
    best_value = -100
    for mtype, id, direction in possible_moves:
        curr_env = copy.deepcopy(env)
        curr_env.move(mtype, id, direction)
        value = calc_value_board(curr_env, env.player_turn)
        if value > best_value:
            best_value = value
            best_move = (mtype, id, direction)

    return best_move