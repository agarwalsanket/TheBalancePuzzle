# TheBalancePuzzle
Implementation of the balance puzzle using Python.
The code takes a user input as file name which has the description of the beams we need to calculate if they are balanced, and if 
not balanced calculate the value of the weight to be kept in an empty pan , to make the beams balanced.
File content can be like this:
B1 -4 5 -2 1 1 22
B2 -4 11 -1 19 3 21
B3 -1 B2 2 6 3 -1
B -3 14 -1 B1 1 B3


Here B is the reresentation of a beam followed by a number.
Each beam can have another beam attached to it, The first number in the beam representation ,is the distance from the hanging point, and the
second number is the weight. Negative means left and positive means right to the hanging point. -1 represents empty pan.

I have also used turtle for drawing the beam.
