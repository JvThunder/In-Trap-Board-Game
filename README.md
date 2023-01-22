# In-Trap-Board-Game
A turn-based board game originally created by me (Joshua AC). 
All codes are also written by me.
Feel free to give feedback to the game and code.

## Board and Pieces
The game will be played in a 6x6 grid. 
Each player will have 1 spawner piece and (currently) 8 other pieces.
Each tile can only be placed by 1 piece.
The details of the name, spawn cost, and movement of the pieces is in the pieces.json file.
Each piece has a different moveset and might jump to 8 directions.
The current list of pieces are:
- Spawner
- Flier
- Jumper
- Dasher
- Charger
- Crazy-Crab
- Swinger
- Left-Swinger
- Right-Swinger  

For each piece, the json dictionary contains information in the following format:
<pre>
{
        "name"        : The name of the piece,
        "display"     : The initial you need to write when using play_with_agent.py,
        "cost"        : The amount of mana you will need to spawn this piece,
        "movement"    : [[northwest,north,northeast],
                         [west,0,east],
                         [southwest,south,southeast]]
                         (For each value, it will move the piece in that direction according to the value)
}
</pre>

## Setup
The initial setup will look like this:
<pre>
   ^  ^  ^  ^  ^  ^
<  x  x  x  x SP2 x  >
<  x  x  x  x  x  x  >
<  x  x  x  x  x  x  >
<  x  x  x  x  x  x  >
<  x SP1 x  x  x  x  >
   v  v  v  v  v  v
</pre>
Player 1 will start with 4 mana.
Player 2 will start with 5 mana.

## Move
Each player will take turns doing an action.
There are 2 actions available:
1. Placing a piece on an empty tile adjacent (the 8 neighbouring tiles) to the Spawner piece. This will reduce the mana by the cost of the piece.  
2. Move a piece on the board to an empty tile according to their moveset from the pieces.json file. The board wraps itself on both columns and rows.  

If the player jumps over an opponent's piece, the opponent's piece will be captured and removed from the board. 
For every piece captured, the player gets 1 mana.
The opponent can respawn this piece with a some cost of mana described in pieces.json.
However, if the player lands on a tile with an opponent's piece, the opponent's piece will NOT be captured and the move is invalid.  
After the turn ends, the player will get 1 additional mana replenished.

## Winning Condition
A player instantly wins if they capture the opponent's spawner. 
The game will automatically end as a draw in 200 moves if no spawners are captured yet.

## How to play with Agent
You can now play with my heuristic agent by running play_with_agent.py.
The move format should be int the form of: <move_type> <piece_display_name> <move_direction>.  
<move_type> can be either "spawn" or "move".  
<piece_display_name> follows the display names on piece.json.  
<move_direction> can be "north", "south", "east", "west", "northwest", "northeast", "southwest", "southeast"  
Example move: "spawn FL north"  
Example of me playing with the bot can be seen on the file sample_game_with_user.txt.  

## Updates
### Version 0.1.0
Create the base logic of the game. 
Added simple agents (Random, NegaMax). 
Added Heuristic Template.
Functions are available for testing agents.

### Version 0.1.1
Added a simple Heuristic Agent.
Separated the game environment, evaluation functions and agents as file modules.

### Version 0.1.2
Modified the queue system incentivize capturing more.
Add 1 piece to the pieces.json file making a total of 9 pieces including the spawner.

### Version 0.1.3
Replace the queueing system to using mana costs for rebalancing.
Cleaning code, readme, adding main.py and adding an option for user to play with agent. 
