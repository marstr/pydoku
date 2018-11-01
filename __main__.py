import sys

from board import Board

subject = Board(2, 2)

print(subject.solve())

subject = Board()
print(subject.solve())