# TicTacToe
Implementation of Tic-Tac-Toe.

## Description
Can be played against a computer, or against another person.

### Synopsis

```
       python3 tictactoe.py [-m] [-p|-c] [-s <size>]
```

### Options
       -c, --computer
           Specify that the computer will make the first move.

       -m, --multiplayer
           Specify that there will be two human players.
           Combined with -c, 'O' will be first move.
           Combined with -m, 'X' will still be first move.

       -p, --player
           Specify that the player will make the first move.

       -s <size>
           Determines how large the Tic-Tac-Toe board will be. Defaults to 3

## Future Enhanccements

 - Optimizations in win calculation
 - Smarter moves by computer
