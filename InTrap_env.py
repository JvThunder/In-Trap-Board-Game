import numpy as np
import json

class InTrap():    
    DIRECTION = {
        "NW"  : (-1, -1), # North West (Top Left)
        "N"   : (-1,  0), # North      (Top)
        "NE"  : (-1,  1), # North East (Top Right)
        "W"   : ( 0, -1), # West       (Left)
        "E"   : ( 0,  1), # East       (Right)
        "SW"  : ( 1, -1), # South West (Bottom Left)
        "S"   : ( 1,  0), # South      (Bottom)
        "SE"  : ( 1,  1), # South East (Bottom Right)
    }

    QUEUE_TURN = 5

    def add_pieces(self):
        '''
        We will extract the pieces information from the json file.
        If you want to customize the pieces, directly change it on the json file.
        1st player spawner id: 1.
        2nd player spawner id: 2.
        '''

        f = open('pieces.json')
        data = json.load(f)
        id_cnt = 1
        self.pieces.append(None)
        for piece in data:
            for color in range(1,3,1):
                mod_piece = piece.copy()
                mod_piece['position'] = (-1,-1)
                mod_piece['color'] = color
                mod_piece['id'] = id_cnt
                mod_piece['queue'] = 0
                id_cnt += 1
                self.pieces.append(mod_piece)
        self.n_pieces = len(self.pieces) - 1
        return
    
    def setup(self):
        '''
        The initial setup of the board is as follows.
           ^  ^  ^  ^  ^  ^
        <  x  x  x  x  SP x  >
        <  x  x  x  x  x  x  >
        <  x  x  x  x  x  x  >
        <  x  x  x  x  x  x  >
        <  x  SP x  x  x  x  >
           v  v  v  v  v  v
        '''

        self.pieces = []
        self.add_pieces()
        self.board = np.zeros((self.n_row, self.n_col), dtype=np.int32)
        
        self.board[self.n_row-1][1] = 1
        self.pieces[1]['position'] = (self.n_row-1,1)

        self.board[0][self.n_col-2] = 2
        self.pieces[2]['position'] = (0,self.n_col-2)
        
        self.player_turn = 1 
        self.winner = 0
        return
        
    def __init__(self, n_row = 6, n_col = 6):
        '''
        The important variables to initialize.
        '''

        self.direction_list = list(self.DIRECTION.keys())
        self.n_row = n_row
        self.n_col = n_col
        self.player_turn = 0 # 1 or 2
        self.winner = 0 # 1 or 2
        self.board = np.zeros((n_row, n_col), dtype=np.int32)
        self.setup()
        return
    
    def __repr__(self):
        '''
        The simple text representation of the board.
        '''

        txt = ""
        for row in range(self.n_row):
            for col in range(self.n_col):
                txt += " "
                if self.board[row][col] == 0:
                    txt += " X "
                    continue
                id = self.board[row][col]
                piece = self.pieces[id]
                txt += piece['display'] + str(piece['color'])
            txt += "\n"
        return txt
    
    def wrap(self, row, col):
        '''
        Wrap the board around the edge.
        '''
        return (row % self.n_row + self.n_row) % self.n_row, (col % self.n_col + self.n_col) % self.n_col

    def update_queue(self):
        '''
        Update the queue list of the pieces
        '''
        for piece in self.pieces:
            if piece == None:
                continue
            if piece['color'] == self.player_turn:
                piece['queue'] = max(0, piece['queue']-1)
        return

    def check_move(self, mtype, id, direction):
        '''
        Check if the move is valid.
        '''

        piece = self.pieces[id]
        drow, dcol = self.DIRECTION[direction]
        djump = piece["movement"][drow+1][dcol+1]
        player_color = self.player_turn
        spawner = self.pieces[player_color]
        
        # Check if the piece id is the current player
        if piece['color'] != player_color:
            return False

        # Piece is still outside of the board
        if mtype == 1:
            # Check if piece is outside of the board
            if piece['position'] != (-1,-1):
                return False

            # Check if pos tile is already filled
            new_pos = self.wrap(spawner['position'][0]+drow, spawner['position'][1]+dcol)
            if self.board[new_pos] != 0:
                return False

             # Check if the piece queue is done:
            if piece['queue'] != 0:
                return False
                
            return True

        # Piece already inside the board
        elif mtype == 2:
            # Check if piece is inside of the board
            if piece['position'] == (-1,-1):
                return False

            # Check if pos tile is already filled
            new_pos = self.wrap(piece['position'][0]+drow*djump, piece['position'][1]+dcol*djump)
            if self.board[new_pos] != 0:
                return False
            
            return True
    
    def check_capture(self, mtype, id, direction):
        '''
        Check which enemy piece is being captured.
        '''
        piece = self.pieces[id]
        drow, dcol = self.DIRECTION[direction]
        djump = piece["movement"][drow+1][dcol+1]
        player_color = self.player_turn
        capture_list = []
        for i in range(1, djump):
            cur_row, cur_col = self.wrap(piece['position'][0] + drow * i, piece['position'][1] + dcol * i)
            cap_id = self.board[cur_row][cur_col]
            if cap_id == 0:
                continue
            if self.pieces[cap_id]['color'] != player_color:
                capture_list.append(cap_id)
        return capture_list
    
    def remove_piece(self, id):
        '''
        Remove pieces from the board and update their position and queue.
        '''
        c_pos = self.pieces[id]['position']
        self.board[c_pos[0]][c_pos[1]] = 0
        self.pieces[id]['position'] = (-1,-1)
        self.pieces[id]['queue'] = self.QUEUE_TURN
        
    def place_piece(self, id, pos):
        '''
        Place a new piece on the board.
        '''
        self.board[pos[0]][pos[1]] = id
        self.pieces[id]['position'] = pos
        return

    def move(self, mtype, id, direction, check_validity = True):
        '''
        There is two possible moves (mtype):
        1. Place a piece on a tile adjacent to the Spawner piece.
        2. Move a piece on the board.
        For both type of move, the id variable shows the piece to move, 
        the direction variable shows which direction to move the piece.
        '''
        
        # Check if the range is correct
        if not ((1 <= mtype <= 2) and (1 <= id < len(self.pieces))):
            return False

        # if not one of the corrent string action then invalid move
        if direction not in self.direction_list:
            return False

        piece = self.pieces[id]
        drow, dcol = self.DIRECTION[direction]
        djump = piece["movement"][drow+1][dcol+1]
        player_color = self.player_turn
        spawner = self.pieces[player_color]

        # Check validity
        if check_validity: 
            if self.check_move(mtype, id, direction) == False:
                return False

        # Piece is still outside of the board
        if mtype == 1:
            new_pos = self.wrap(spawner['position'][0]+drow, spawner['position'][1]+dcol)
            # Place on the new tile
            self.place_piece(id, new_pos)

        # Piece already inside the board
        elif mtype == 2:
            prv_pos = piece['position']

            # Find all pieces that are captured by this piece
            capture_list = self.check_capture(mtype, id, direction)
            for cap_id in capture_list:
                self.remove_piece(cap_id)
            if 1 in capture_list:
                self.winner = 2
            if 2 in capture_list:
                self.winner = 1            
            
            # Remove piece from the previous tile
            self.remove_piece(id)
            
            # Place on the new tile
            new_pos = self.wrap(prv_pos[0]+drow*djump, prv_pos[1]+dcol*djump)
            self.place_piece(id, new_pos)

        # FLip the player_turn
        self.player_turn = 3 - self.player_turn

        # Update the queue
        self.update_queue()
    
        return True

GLOBAL_MAX_STEPS = 200

def simulate_game(env, agent1, agent2, MAX_STEPS = GLOBAL_MAX_STEPS, verbose = False):
    '''
    Simulates a game between agent1 and agent2.
    Verbose mode prints the game.
    '''
    env.setup()
    if verbose: print(env)
    for i in range(MAX_STEPS):
        if env.player_turn == 1:
            mtype, id, direction = agent1(env)
            env.move(mtype, id, direction)
        else:
            mtype, id, direction = agent2(env)
            env.move(mtype, id, direction)
        if verbose: print(env)
        if env.winner != 0:
            if verbose: print(f'Winner is player {env.winner}.')
            return env.winner
    return 0

def evaluate(env, agent1, agent2, verbose = False, N_GAMES = 100, MAX_STEPS = GLOBAL_MAX_STEPS):
    '''
    Simulates N_GAMES amount of games between agent1 and agent2.
    Verbose mode prints the game.
    '''
    stats = [0, 0]
    for i in range(N_GAMES):
        if verbose and i%10==9:
            print(stats)
        winner = simulate_game(env, agent1, agent2, verbose = verbose, MAX_STEPS = MAX_STEPS)
        if winner != 0:
            stats[winner-1] += 1
    print(f'Agent 1 wins {stats[0]*100//N_GAMES}% of the time.')
    print(f'Agent 2 wins {stats[1]*100//N_GAMES}% of the time.')
    print(f'Draw {100-stats[0]*100//N_GAMES-stats[1]*100//N_GAMES}% of the time.')
    return stats