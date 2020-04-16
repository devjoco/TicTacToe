# TicTacToe
Implementation of Tic-Tac-Toe.

## Description
Can be played against a computer, or against another person.

### Synopsis

```
       python3 tictactoe.py [-m] [-p|-c] [-s <size>]
```

### Options
       -c, --comp, --computer
           Specify that the computer will make the first move. Cannot be combined with -p or -m.
           Combining with -m will make 'O' the first move.

       -m, --multi, --multiplayer
           Specify that there will be two human players. Cannot be combined with -c or -p.

       -p, --player
           Specify that the player will make the first move. Cannot be combined with -m.
           Combining with -m has no effect, 'X' will still be first move.

       -s <size>
           Determines how large the Tic-Tac-Toe board will be. Defaults to 3

## Future Enhanccements

 - Optimizations in win calculation
 - Smarter moves by computer
