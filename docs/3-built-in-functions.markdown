# Chapter 3. Built-in Functions

## 3.1 Representation [1]

Up to this point, all the objects we have been concerned with have had 
no internal structure discernible in MDL. While the characteristics of 
objects with internal structure differ greatly, the way `READ` and 
`PRINT` handle them is uniform, to wit:

* `READ`, when applied to the representation of a structured object, 
builds and returns an object of the indicated `TYPE` with elements 
formed by applying `READ` to each of their representations in turn.

* `PRINT`, when applied to a structured object, produces a 
representation of the object, with its elements represented as `PRINT` 
applied to each of them in turn.

A MDL object which is used to represent the application of a function 
to its arguments is an argument of `TYPE` `FORM`. Its printed 
representation is

```no-highlight
< func arg-1 arg-2 ... arg-N >
```

where *func* is an object which designates the function to be applied, 
and *arg-1* through *arg-N* are object which designate the arguments 
or "actual parameters" or "inputs". A `FORM` is just a structured 
object which is stored and can be manipulated like a `LIST` (its 
"primitive type" is `LIST`—chapter 6). The application of the function 
to the arguments is done by `EVAL`. The usual meaning of "function" 
(uncapitalized) in this document will be anything applicable to 
arguments.

## 3.2 Evaluation [1]

`EVAL` applied to a `FORM` acts as if following these directions:

First, example the *func* (first element) of the `FORM`. If it is an 
`ATOM`, look at its "value" (global or local, in that order—see next 
chapter). If it is not an `ATOM`, `EVAL` it and look at the result of 
the evaluation. If what you are looking at is not something which can 
be applied to arguments, complain (via the `ERROR` function). 
Otherwise, inspect what you are looking at and follow its directions 
in evaluating or not evaluating the arguments (chapters 9 and 19) and 
then "apply the function"—that is, `EVAL` the body of the object 
gotten from *func*.

## 3.3 Built-in Functions (TYPE SUBR, TYPE FSUBR) [1]

The built-in functions of MDL come in two varieties: those which have 
all their arguments `EVAL`ed before operating on them (`TYPE` `SUBR`, 
for "subroutine", pronounced "subber") and those which have none of 
their arguments `EVAL`ed (`TYPE` `FSUBR`, historically from Lisp 
(Moon, 1974), pronounced "effsubber"). Collectively they will be 
called `F/SUBR`s, although that term is not meaningful to the 
interpreter. See appendix 2 for a listing of all `F/SUBR`s and short 
descriptions. The term "Subroutine" will be used herein to mean both 
`F/SUBR`s and compiled user programs (`RSUBR`s and 
`RSUBR-ENTRY`s—chapter 19).

Unless otherwise stated, **every** MDL built-in Subroutine is of 
`TYPE` **`SUBR`**. Also, when it is stated that an argument of a 
`SUBR` must be of a particular `TYPE`.

Another convenient abbreviation which will be used is "the `SUBR` 
*pname*" in place of "the `SUBR` which is initially the 'value' of the 
`ATOM` of `PNAME` *pname*". "The `FSUBR` *pname*" will be used with a 
similar meaning.

## 3.4 Examples (+ and FIX; Arithmetic) [1]

```no-highlight
<+ 2 4 6>$
12
```

The `SUBR` `+` adds numbers. Most of the usual arithmetic functions 
are MDL `SUBR`s: `+`, `-`, `*`, `/`, `MIN`, `MAX`, `MOD`, `SIN`, 
`COS`, `ATAN`, `SQRT`, `LOG`, `EXP`, `ABS`. (See appendix 2 for short 
descriptions of these.) All except `MOD`, which wants `FIX`es, are 
indifferent as to whether their arguments are `FLOAT` or `FIX` or a 
mixture. In the last case they exhibit "contagious `FLOAT`ing": of 
argument of `TYPE` `FLOAT` forces the result to be of `TYPE` `FLOAT`.

```no-highlight
<FIX 1.0>$
1
```

The `SUBR` `FIX` explicitly returns a `FIX`ed-point number 
corresponding to a `FLOAT`ing-point number. `FLOAT` does the opposite.

```no-highlight
<+ 5 <* 2 3>>$
11

<SQRT <+ <* 3 3> <* 4 4>>>$
5.0

<- 5 3 2>$
0

<- 5>$
-5

<MIN 1 2.0>$
1.0

</ 11 7 2.0>$
0.5
```

Note this last result: the division of two `FIX`es gives a `FIX` with 
truncation, not rounding, of the remainder: the intermediate result 
remains a `FIX` until a `FLOAT` argument is encountered.

## 3.5 Arithmetic Details

`+`, `-`, `*`, `/`, `MIN`, and `MAX` all take any number of arguments, 
doing the operation with the first argument and the second, then with 
that result and the third argument, etc. If called with no arguments, 
each returns the identity for its operation (`0`, `0`, `1`, `1`, the 
greatest `FLOAT`, and the least `FLOAT`, respectively): if called with 
one argument, each acts as if the identity and the argument has been 
supplied. They all will cause an overflow or underflow error if any 
result, intermediate or final, is too large or too small for the 
machine's capacity. (That error can be disabled if necessary—section 
16.9).

One arithmetic function that always requires some discussion is the pseudo-random-number generator. MDL's is named `RANDOM`, and it always returns a `FIX`, uniformly distributed over the whole range of `FIX`es. If `RANDOM` is never called with arguments, it always returns the exact same sequence of numbers, for convenience in debugging. "Debugged" programs should give `RANDOM` two arguments on the first call, which become seeds for a new sequence. Popular choices of new seeds are the numbers given by `TIME` (which see), possibly with bits modified (chapter 18). Example ("pick a number from one to ten"):

```no-highlight
<+ 1 <MOD <RANDOM> 10>>$
4
```
