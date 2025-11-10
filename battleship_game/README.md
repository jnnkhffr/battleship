# battleship
Game to play battleship.

The playing field should be a 10 x 10 grid. This gives us 100 boxes where the “bombs” can land.
Seven ships are to be hidden. Four of these ships are submarines that are only one box in size. Then there is a frigate 
that is two boxes in size. A destroyer is three squares in size, and aircraft carriers are four squares in size. 

At the beginning, the player places the ships on the playing field. We have a start screen where you can click on the 
ships next to the playing field and then click on the grid boxes to place the ship on the playing field. 
The opponent, in our case the computer, then has one shot per round. They must fire by selecting a box. If no ship is 
hit, a small blue dot appears on the playing field. If part of a ship is hit, i.e., only one box and not the entire 
ship, an orange cross appears on that spot. If all boxes of the ship are hit, the ship is destroyed and sunk. 
All squares along the length of the ship are then marked with a thicker red cross. 

The aim of the game is to sink all the ships arranged by the computer before the computer sinks the ships we have arranged.


- we should use classes for example for every ship