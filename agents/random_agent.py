def RandomAgent(env):
    '''
    Choosing a random move every turn.
    '''

    import random
    mtype = random.randint(1,2)
    direction = random.choice(env.direction_list)
    id = None
    if mtype == 1:
        unique_id = []
        for piece in env.pieces:
            if piece == None:
                continue
            if piece['position'] == (-1,-1):
                unique_id.append(piece['id'])
        if len(unique_id) == 0:
            return RandomAgent(env)
        id = random.choice(unique_id)
    else:
        unique_id = []
        for rows in env.board:
            for id in rows:
                if id == 0:
                    continue
                if id not in unique_id:
                    if env.pieces[int(id)]['color'] == env.player_turn:
                        unique_id.append(id)
        if len(unique_id) == 0:
            return RandomAgent(env)
        id = random.choice(unique_id)
    return mtype, id, direction