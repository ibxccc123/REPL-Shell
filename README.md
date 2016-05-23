# REPL-Shell-Python
A REPL shell in Python 2 with extended functionality for string parsing and mathematical computations.  The shell is also capable of creating closures to encapsulate multiple command lines into one.

The interactive shell prompts the user for each instruction; upon receiving integers or boolean values, it pushes them onto a stack data structure. Upon receiving instructions such as operations, the shell will pop off the top-most members of the stack and print the result onto the screen. The shell also utilizes a dictionary data structure to map keys to values, for handling closure binding and applications.  The list of commands that the shell is capable is as follows:

A) Mathematical operators (+,-,*,%)

B) Logical operators (AND,OR,NOT)

C) If statements 

D) Equality operators (=,<,>)

E) Text parsing from an input file 

F) Closure binding (pops off top members of stack and binds the pushing of those to the stack to a string name)

G) Stack manipulation (Swapping top two members of stack, popping off topmost, etc.)


Written in February 2016.
