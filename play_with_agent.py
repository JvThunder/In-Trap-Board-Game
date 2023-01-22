from agents.heuristic_v1_agent import HeuristicAgent
from InTrap_env import InTrap

env = InTrap()

def UserAgent(env):

    mtype_list = {"spawn": 1, "move": 2}
    id_list = {}
    for piece in env.pieces:
        if piece and piece['color'] == 1:
            id_list[piece['display']] = piece['id']
    direction_list = {
        "north"     : "N",
        "south"     : "S",
        "east"      : "E",
        "west"      : "W",
        "northeast" : "NE",
        "northwest" : "NW",
        "southeast" : "SE",
        "southwest" : "SW",
    }

    def check_input(mtype, id, direction):
        if mtype in mtype_list and id in id_list and direction in direction_list:
            mtype = mtype_list[mtype]
            id = id_list[id]
            direction = direction_list[direction]
            return env.check_move(mtype, id, direction, error_message = True)
        return False
        
    mtype, id, direction = input("Enter your move: ").split(' ')
    while check_input(mtype, id, direction) == False:
        print("Invalid move, please make another move.")
        mtype, id, direction = input("Enter your move: ").split(' ')

    mtype = mtype_list[mtype]
    id = id_list[id]
    direction = direction_list[direction]
    return (mtype, id, direction)


agent_mtype = {1:"spawn", 2:"move"}
agent_id = {}
for piece in env.pieces:
    if piece and piece['color'] == 2:
        agent_id[piece['id']] = piece['display']
agent_direction = {
    "N" : "north",
    "S" : "south",
    "E" : "east",
    "W" : "west",
    "NE": "northeast",
    "NW": "northwest",
    "SE": "southeast",
    "SW": "southwest",
}

MAX_STEPS = 200
print("Start game:")
print(env)
for i in range(MAX_STEPS):
        if env.player_turn == 1:
            mtype, id, direction = UserAgent(env)
            valid = env.move(mtype, id, direction)
        else:
            mtype, id, direction = HeuristicAgent(env)
            valid = env.move(mtype, id, direction)
            print(f"Bot plays: {agent_mtype[mtype]} {agent_id[id]} {agent_direction[direction]}")
        print(env)
        if env.winner != 0:
            if env.winner == 1: print('Congrats, you win :D')
            else: print('Sorry, you lose :(')