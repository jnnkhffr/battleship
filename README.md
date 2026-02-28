# Battleship
Game to play battleship.

There are essentially two playing fields next to each other. Both are 10 x 10 grids. The right playing field is the 
computer sea area where the computer places its ships automatically. The left playing field is the 
player's sea area, where the player can place their seven ships.  
Four of these ships are submarines that are only one box in size. Then there is a frigate 
that is two boxes in size. A destroyer is three squares in size, and aircraft carriers are four squares in size. 


 __How to play the game__: 

At the beginning, you have to select a difficulty level. Here you can choose between Easy, Medium, and Hard by clicking 
on the level you want to play. 

Then the player has to place the ships on the playing field. The ships cannot be selected individually. 
The game starts with the largest ship. If you move the mouse over the left playing field, which is our sea area, 
you can see how to position the ship. The ship is displayed with 50% of its color intensity so that you can see where 
the ship would be located. Press the space bar to rotate the ship 90°. Press it again to rotate it back. Click the mouse
to confirm the ship's position at the location where the mouse is currently located. The ship is now placed and the next
smaller ship can now be placed. 

However, there are a few rules governing how the next ships may be placed. They are not allowed to overlap or be placed 
directly 
next to each other. This is indicated by the ship turning red at points where it cannot be placed, and it cannot be 
confirmed in place with a click. Only when the ship turns white again can it be placed at that location. This continues
until all ships are placed. Then a message appears: "THE BATTLE STARTS", 
and the player knows that all ships are placed, and he can now fire the first shot. The computer always follows suit and 
fires after we have fired. 
The opponent, in our case the computer, then has one shot per round. You must fire by selecting a box and click on it. 

If no ship is hit, the gridbox is marked blue on the playing field. If part of a ship is hit, i.e., only one box and 
not the entire ship, the gridbox is marked green. If all boxes of the ship are hit, the ship is destroyed and sunk. 
All squares along the length of the ship, are then marked red. 

The aim of the game is to sink all the ships arranged by the computer before the computer sinks the ships you have 
arranged. Depending on the level you are playing, the computer follows different strategies to sink your fleet. At the 
end, you can win or lose the battle. Afterwards, you have the option to repeat the game at the same difficulty level or 
return to the main menu and select a different difficulty level. 


## Installation

### Requirements
- Python 3.12 or higher
- `pip` (Python package manager)
-  Assets Dependencies

### StepsClone this repository:
   ```bash
   git clone https://github.com/jnnkhffr/battleship
   ```

### Install dependencies:
pip install -r requirements.txt


## Execution
From the project root, run:
- python -m battleship_game.main


# Gameplan

- define ships  *-> DONE*
- open second game field *-> DONE*
- place ships on board *-> DONE*
  - check function that ships don't overlap and have at least on grid cell space *-> DONE*
  - first step is to place them on board via hard-code *-> DONE*
- hit logic *-> DONE*
- opponent (computer) *-> DONE*
  - set of that computer creates a board and places his ships as well *-> DONE*
  - computer should also run the hit logic *-> DONE*
- Start and End Screens *-> DONE*
- small text between ship placement and the start of firing (only visible for 3 Seconds) *-> DONE*
- timedelay for the computershot? *-> DONE*
- adding useful things from the "difficulites_factory_pattern" Branch *-> DONE*


- run mypy; ruff and black for Code-Style *-> DONE*
- files that we don´t use should be deleted for a better overview *-> DONE*
- (meaningful) Docstrings at every class,function? *-> OPEN*
- unnecessary comments within the code deleted? *-> OPEN*
- Can we use more design patterns anywhere else? *-> DONE?*
- Game instructions in the README. *-> FIRST DRAFT*
- requirements fully documented? *-> OPEN*