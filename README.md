lpsolver
========

A Simple Letterpress Solver in Python


Usage
=====

	lpsolver.py lowercase-board coloring-of-tiles

Example:

	lpsolver.py abcdeabcdeabcdeabcdeabcde 01234012340123401234

Boards are lowercase letters from left to right, top to bottom.

Colorings are numeric values as follows:

	0 - empty tile
	1 - unprotected blue
	2 - protected blue
	3 - unprotected red
	4 - protected red

The top moves are printed with their relative scores, the subsequent opponent move is calculated and shown with the new coloring.

