## An exploration of peephole optimizations in Python

Code & examples for a short talk given at Hacker School on the CPython peephole optimizer and why it presents a problem for authors of test coverage tools.

For context, see https://mail.python.org/pipermail/python-ideas/2014-May/027893.html

To explore:

1. Read the simple `example.py`. Run the tests and measure test coverage with `coverage.py`. `TinyCoverage` is about the most minimal test coverage tool possible.  We think our tests are thorough, but it looks like the `else` line isn't executing! What?

2. Look at `iffer_dis.txt`. You don't have to understand everything about the bytecode, but notice that line #4, the `else`, doesn't appear in the bytecode. (The left-hand column shows the line number.) This makes sense: there's no operation to do on an `else`, since once the `if` statement has been evaluated the interpreter is heading to either one branch or the other. From the perspective of bytecode, there's no difference at all between writing this:

    ~~~~.py
    if a:
        ...
    else:
        if b:
           ...
        else:
            ...
    ~~~~
    and this:
    ~~~~.py
    if a:
        ...
    elif b:
       ...
    else:
        ...
    ~~~~
    (even though the second is better style).

3. We'll decide to cheat and exclude lines that end in `else:`.  Run `coverage2.py` - the only difference is line [26](https://github.com/akaptur/peephole-optimization/blob/master/coverage2.py#L26).

4. Read through `example3.py`, then run `coverage2.py` on it.  What happened? Look at `continuer_dis.txt` and notice that the `continue` line *does* appear in the disassembly. Why doesn't it appear to be executed?

5. The `continue` line isn't executed because of a compiler optimization - this bytecode that we're looking at has already been optimzed. In this particular optimization, the compiler notices that two instructions in a row are jumps, and it combines these two hops into one larger jump. So, in a very real sense, the `continue` line didn't actually execute - it was optimized out - even though the logic contained in the `continue` did actually happen. This is one of several optimizations known as peephole optimizations because they operate on a small chunk of the bytecode at one time. The other optimations, including some simpler ones like constant folding on binary operations, are implemented in [peephole.c](http://hg.python.org/cpython/file/118d6f49d6d6/Python/peephole.c).

    An example of constant folding:
    ~~~~.py
        >>> def foo():
        ...     return 1 + 2
        ...
        >>> import dis
        >>> dis.dis(foo)
          2           0 LOAD_CONST               3 (3)
                      3 RETURN_VALUE
    ~~~~

6. Go back to `continuer_dis.txt` and trace through the jumps carefully. Here are some things you'll need to know:
  * The second column is the index in the bytecode, the third is the byte name, and the fourth is the argument.  The fifth is sometimes a hint about the meaning of the argument.
  * `POP_JUMP_IF_FALSE`, `POP_JUMP_IF_TRUE`, and `JUMP_ABSOLUTE` have the jump target as their argument. So, e.g. `POP_JUMP_IF_TRUE 27` means "if the popped expression is true, jump to position 27."
  * `JUMP_FORWARD`'s argument specifies the distance to jump forward in the bytecode, and the fifth column shows where the jump will end.
  * When an interator is done, `FOR_ITER` jumps forward the number of bytes specified in its argument.

  Notice that no matter how hard you try, you couldn't end up on bytes 66 or 69, the two that belong to line 19. This line of code is unreachable after the optimizations are finished.
