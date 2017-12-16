Built-in Functions
==================

Representation [1]
------------------

Up to this point, all the objects we have been concerned with have had
no internal structure discernible in MDL. While the characteristics of
objects with internal structure differ greatly, the way :func:`READ` and
:func:`PRINT` handle them is uniform, to wit:

  - :func:`READ`, when applied to the representation of a structured object,
    builds and returns an object of the indicated |TYPE| with elements
    formed by applying :func:`READ` to each of their representations in turn.

  - :func:`PRINT`, when applied to a structured object, produces a
    representation of the object, with its elements represented as
    :func:`PRINT` applied to each of them in turn.

A MDL object which is used to represent the application of a function to
its arguments is an argument of :tref:`TYPE FORM`. Its printed
representation is

.. parsed-literal::

    :samp:`< {func} {arg-1} {arg-2} ... {arg-N} >`

where *func* is an object which designates the function to be applied,
and *arg-1* through *arg-N* are object which designate the arguments or
“actual parameters” or “inputs”. A |FORM| is just a structured object
which is stored and can be manipulated like a |LIST| (its “primitive
type” is |LIST| – :numref:`ch-data-types`). The application of the function
to the arguments is done by :func:`EVAL`. The usual meaning of “function”
(uncapitalized) in this document will be anything applicable to
arguments.

Evaluation [1]
--------------

.. index:: FORM; evaluating, function; applying

:func:`EVAL` applied to a |FORM| acts as if following these directions:

First, examine the *func* (first element) of the |FORM|. If it is an
|ATOM|, look at its “value” (global or local, in that order – see next
chapter). If it is not an |ATOM|, :func:`EVAL` it and look at the result
of the evaluation. If what you are looking at is not something which can
be applied to arguments, complain (via the :func:`ERROR` function).
Otherwise, inspect what you are looking at and follow its directions in
evaluating or not evaluating the arguments (chapters :numref:`%s <ch-functions>`
and :numref:`%s <ch-compiled-programs>`) and then “apply the function” – that
is, :func:`EVAL` the body of the object gotten from *func*.

Built-in Functions (TYPE SUBR, TYPE FSUBR) [1]
----------------------------------------------

.. index:: subroutines, SUBR, FSUBR

The built-in functions of MDL come in two varieties: those which have all their
arguments :func:`EVAL`\ ed before operating on them (\ :tref:`TYPE SUBR`), for
“subroutine”, pronounced “subber”) and those which have none of their arguments
:func:`EVAL`\ ed (:tref:`TYPE FSUBR`, historically from Lisp (Moon, 1974),
pronounced “effsubber”). Collectively they will be called |F/SUBR|\ s,
although that term is not meaningful to the interpreter. See appendix 2 for a
listing of all |F/SUBR|\ s and short descriptions. The term “Subroutine” will
be used herein to mean both |F/SUBR|\ s and compiled user programs
(:t:`RSUBR`\ s and :t:`RSUBR-ENTRY`\ s –
:numref:`chapter %s <ch-compiled-programs>`).

Unless otherwise stated, **every** MDL built-in Subroutine is of
|TYPE| :ut:`SUBR`. Also, when it is stated that an argument of a
|SUBR| must be of a particular |TYPE|, note that this means that
:func:`EVAL` of what is there must be of the particular |TYPE|.

Another convenient abbreviation which will be used is “the |SUBR|
*pname*” in place of “the |SUBR| which is initially the ‘value’ of the
|ATOM| of ``PNAME`` *pname*”. “The |FSUBR| *pname*” will be used
with a similar meaning.

Examples (+ and FIX; Arithmetic) [1]
------------------------------------

::

    <+ 2 4 6>$
    12

The :tref:`SUBR +` adds numbers. Most of the usual arithmetic functions are
MDL |SUBR|\ s: :func:`+`, :func:`-`, :func:`*`, :func:`/`, :func:`MIN`,
:func:`MAX`, :func:`MOD`, :func:`SIN`, :func:`COS`, :func:`ATAN`, :func:`SQRT`,
:func:`LOG`, :func:`EXP`, :func:`ABS`. (See appendix 2 for short descriptions of
these.) All except :func:`MOD`, which wants |FIX|\ es, are indifferent as to
whether their arguments are |FLOAT| or |FIX| or a mixture. In the last case
they exhibit “contagious |FLOAT|\ ing”: one argument of :tref:`TYPE FLOAT`
forces the result to be of :tref:`TYPE FLOAT`.

.. todo:: update appendix reference

::

    <FIX 1.0>$
    1

The :tref:`SUBR FIX` explicitly returns a |FIX|\ ed-point number
corresponding to a |FLOAT|\ ing-point number. :func:`FLOAT` does the
opposite.

::

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

Note this last result: the division of two |FIX|\ es gives a |FIX|
with truncation, not rounding, of the remainder: the intermediate result
remains a |FIX| until a |FLOAT| argument is encountered.

Arithmetic Details
------------------

:func:`+`, :func:`-`, :func:`*`, :func:`/`, :func:`MIN`, and :func:`MAX` all
take any number of arguments, doing the operation with the first argument and
the second, then with that result and the third argument, etc. If called with no
arguments, each returns the identity for its operation (\ ``0``, ``0``, ``1``,
\ ``1``, the greatest |FLOAT|, and the least |FLOAT|, respectively); if
called with one argument, each acts as if the identity and the argument has been
supplied. They all will cause an overflow or underflow error if any result,
intermediate or final, is too large or too small for the machine’s capacity.
(That error can be disabled if necessary – :numref:`OVERFLOW`).

One arithmetic function that always requires some discussion is the
pseudo-random-number generator. MDL’s is named :func:`RANDOM`, and it always
returns a |FIX|, uniformly distributed over the whole range of
|FIX|\ es. If :func:`RANDOM` is never called with arguments, it always
returns the exact same sequence of numbers, for convenience in
debugging. “Debugged” programs should give :func:`RANDOM` two arguments on
the first call, which become seeds for a new sequence. Popular choices
of new seeds are the numbers given by :func:`TIME` (which see), possibly
with bits modified (:numref:`ch-machine-words-and-bits`). Example (“pick a
number from one to ten”)::

    <+ 1 <MOD <RANDOM> 10>>$
    4
