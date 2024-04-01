NeutralAtomVisualizer

This program takes in a .txt file specifying the movement sequence at outputs an .mp4 video of the sequence.

Example:

```
qubits
1 2 3 4 5 6 7 8 9 10 11 12
initial positions
[0,0] [1,0] [2,0] [0,1] [1,1] [2,1] [0,2] [1,2] [2,2] [0,3] [1,3] [2,3]
move 0.4 0 0.25s
1 2 3 4 5 6
move 0 2 1s
1 2 3 4 5 6
wait 1s
move 0 -2 1s
1 2 3 4 5 6
move -0.4 0 0.25s
1 2 3 4 5 6
wait 1s
```

Resulting in

![](output.mp4)

The first 4 lines are for the qubit IDs and initial positions, then you can specify movements of groups of atoms.


