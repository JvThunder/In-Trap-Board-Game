# In-Trap-Board-Game
A turn-based board game originally created by me (Joshua AC). 
All codes are also written by me.
Feel free to give feedback to the game and code.

## Board and Pieces
The game will be played in a 6x6 grid. 
Each player will have 1 spawner piece and (currently) 8 other pieces.
Each tile can only be placed by 1 piece.
The details of the name and movement of the pieces is in the pieces.json file.
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

## Move
Each player will take turns doing an action.
There are 2 actions available:
1. Placing a piece on an empty tile adjacent (the 8 neighbouring tiles) to the Spawner piece.
2. Move a piece on the board to an empty tile according to their moveset from the pieces.json file. The board wraps itself on both columns and rows.  

If the player jumps over an opponent's piece, the opponent's piece will be captured and removed from the board.
The opponent can respawn this piece after 5 turns.
However, if the player lands on a tile with an opponent's piece, the opponent's piece will NOT be captured and the move is invalid.

## Winning Condition
A player instantly wins if they capture the opponent's spawner. 
The game will automatically end as a draw in 200 moves if no spawners are captured yet.

## Updates
### Version 1.0
Create the base logic of the game. 
Added simple agents (Random, CheckTrap, NegaMax). 
Added Heuristic Template.
Functions are available for testing agents.

### Version 1.1
Added a simple Heuristic Agent.
Currently Heuristic vs Heuristic ends up in a neverending game. 
(Will be fixed by adjusting rules and pieces in the future)
Separated the game environment, evaluation functions and agents as modules.

### Version 1.2
Changed the queue into 5 instead of 3 to incentivize capturing more.
Add 1 piece to the pieces.json file making a total of 9 pieces including the spawner.

### Version 1.3
Cleaning code, readme, adding main.py and adding an option for user to play with agent.
Also planning on optimizing several lines.