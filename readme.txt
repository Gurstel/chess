README

PROJECT:

This code is for chess. It comprises of 5 python files and images of pieces.

My project should work as fully functioning chess with a start screen, player vs player mode,
and player vs ai mode. It incorporates all of the rules of chess including castling, en passant, and
pawn promotion.

The AI will evaluate the positioning and pieces on the board to make it's move





HOW TO RUN:

To use cmu_112_graphics.py, you need to have some modules installed. If they are 
not installed, you will see a message like this (or a similar one for "requests" instead of "PIL"):
**********************************************************
** Cannot import PIL -- it seems you need to install pillow
** This may result in limited functionality or even a runtime error.
**********************************************************
You can try to use 'pip' to install the missing modules, but it can be complicated 
making sure you are installing these modules for the same version of Python that you are running. Here are some more-reliable steps that should work for you:

For Windows:
Run this Python code block in a Python file (it will print the commands you need to paste into your command prompt):

import sys
print(f'"{sys.executable}" -m pip install pillow')
print(f'"{sys.executable}" -m pip install requests')

Open Command Prompt as an administrator user (right click - run as administrator)
Copy-paste each of the two commands printed in step 1 into the command prompt you opened in step 2.
Close the command prompt and close Python.
Re-open Python, and you're set (hopefully)!

For Mac or Linux:
Run this Python code block in a Python file (it will print the commands you need to paste into your command prompt):

import sys
print(f'sudo "{sys.executable}" -m pip install pillow')
print(f'sudo "{sys.executable}" -m pip install requests')

Open Terminal
Copy-paste each of the two commands printed in step 1 into the command prompt you opened in step 2.
If you see a lock and a password is requested, type in the same password that you use to log into your computer.
Close the terminal and close Python.
Re-open Python, and you're set (hopefully)!

Now all you need to have this folder, go to playChess.py and run that file. 
The other python files are the actual implementation of each sides legalities and
algorithmic complexities, so check those out to see how I actually made chess. playChess.py is
the culmanation of those files so you can easily access between the modes and it is what I created 
the start screen in.





NOTE:
This is hardcore chess, no take backs and the computer won't play for you.

Try to win!!

