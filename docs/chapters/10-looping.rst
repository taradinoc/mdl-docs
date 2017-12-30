Looping
===================

PROG and REPEAT [1]
-------------------------

:func:`PROG` and :func:`REPEAT` are almost identical |FSUBR|\ s which make it
possible to vary the order of :func:`EVAL`\ uation arbitrarily – that is, to
have “jumps”. The syntax of :func:`PROG` (“program”) is

.. parsed-literal::

    :samp:`<PROG {act:atom} {aux:list} {body}>`

where

-  *act* is an optional |ATOM|, which is bound to the |ACTIVATION|
   of the :func:`PROG`.
-  *aux* is a |LIST| which looks exactly like that part of a
   |FUNCTION|\ ’s argument |LIST| which follows an ``"AUX"``, and
   serves exactly the same purpose. It is not optional. If you need no
   temporary variables of ``"ACT"``, make it ``()``.
-  *body* is a non-zero number of arbitrary MDL expressions.

The syntax of :func:`REPEAT` is identical, except that, of course,
``REPEAT`` is the first element of the |FORM|, not ``PROG``.

Basic EVALuation [1]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upon entering a :func:`PROG`, an |ACTIVATION| is **always** generated. If
there is an |ATOM| in the right place, the |ACTIVATION| is also
bound to that |ATOM|. The variables in the *aux* (if any) are then
bound as indicated in the *aux*. All of the expressions in *body* are
then :func:`EVAL`\ uated in their order of occurrence. If nothing untoward
happens, you leave the :func:`PROG` upon evaluating the last expression in
*body*, returning the value of that last expression.

:func:`PROG` thus provides a way to package together a group of things you
wish to do, in a somewhat more limited way than can be done with a
|FUNCTION|. But :func:`PROG`\ s are generally used for their other
properties.

:func:`REPEAT` acts in all ways **exactly** like a :func:`PROG` whose last
expression is `<AGAIN>`. The only way to leave a :func:`REPEAT` is to
explicitly use :func:`RETURN` (or :func:`GO` with a ``TAG`` – section 10.4).

AGAIN and RETURN in PROG and REPEAT [1]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Within a :func:`PROG` or :func:`REPEAT`, you always have a defined
|ACTIVATION|, whether you bind it to an |ATOM| or not. |LProgInterruptsExpert|

.. |LProgInterruptsExpert| replace-class:: expert

    In fact the interpreter binds it to the |ATOM| ``LPROG\ !-INTERRUPTS``
    (“last PROG”). The :tref:`FSUBR BIND` is identical to :func:`PROG` except
    that :func:`BIND` does not bind that |ATOM|, so that :func:`AGAIN` and
    :func:`RETURN` with no |ACTIVATION| argument will not refer to it. This
    feature could be useful within |MACRO|\ s.

If :func:`AGAIN` is used with no arguments, it uses the |ACTIVATION| of
the closest surrounding :func:`PROG` or :func:`REPEAT` **within the current
function** (an error occurs if there is none) and re-starts the :func:`PROG`
or :func:`REPEAT` without rebinding the *aux* variables, just the way it
works in a |FUNCTION|. With an argument, it can of course re-start any
Function (:func:`PROG` or :func:`REPEAT` or :func:`FUNCTION`) within which it is
embedded at run time.

As with :func:`AGAIN`, if :func:`RETURN` is given no |ACTIVATION| argument, it
uses the |ACTIVATION| of the closest surrounding :func:`PROG` or
:func:`REPEAT` within the current function and causes that :func:`PROG` or
:func:`REPEAT` to terminate and return :func:`RETURN`\ ’s first argument. If
:func:`RETURN` is given **no** arguments, it causes the closest surrounding
:func:`PROG` or :func:`REPEAT` to return the :tref:`ATOM T`. Also like
:func:`AGAIN`, it can, with an |ACTIVATION| argument, terminate any
Function within which it is embedded at run time.

Examples [1]
~~~~~~~~~~~~~~~~~~~~

Examples of the use of :func:`PROG` are difficult to find, since it is
almost never necessary, and it slows down the interpreter (chapter 24).
:func:`PROG` can be useful as a point of return from the middle of a
computation, or inside a :func:`COND` (which see), but we won’t exemplify
those uses. Instead, what follows is an example of a typically poor use
of :func:`PROG` which has been observed among Lisp (Moon, 1974) programmers
using MDL. Then, the same thing is done using :func:`REPEAT`. In both cases,
the example |FUNCTION| just adds up all its arguments and returns the
sum. (The :tref:`SUBR GO` is discussed in section 10.4.)

::

    ;"Lisp style"
        <DEFINE MY+ ("TUPLE" TUP)
                <PROG (SUM)
                        <SET SUM 0>
                  LP    <COND (<EMPTY? .TUP> <RETURN .SUM>)>
                        <SET SUM <+ .SUM <1 .TUP>>>
                        <SET TUP <REST .TUP>>
                        <GO LP>>>

    ;"MDL style"
        <DEFINE MY+ ("TUPLE" TUP)
                <REPEAT ((SUM 0))
                        <COND (<EMPTY? .TUP> <RETURN .SUM>)>
                        <SET SUM <+ .SUM <1 .TUP>>
                        <SET TUP <REST .TUP>>>>

Of course, neither of the above is optimal MDL code for this problem,
since ``MY+`` can be written using |SEGMENT| evaluation as

::

    <DEFINE MY+ ("TUPLE" TUP) <+ !.TUP>>

There are, of course, lots of problems which can’t be handled so simply,
and lots of uses for :func:`REPEAT`.

MAPF and MAPR: Basics [1]
-------------------------------

:func:`MAPF` (“map first”) and :func:`MAPR` (“map rest”) are two |SUBR|\ s
which take care of a majority of cases which require loops over data.
The basic idea is the following:

Suppose you have a |LIST| (or other structure) of data, and you want
to apply a particular function to each element. That is exactly what
:func:`MAPF` does: you give it the function and the structure, and it
applies the function to each element of the structure, starting with the
first.

On the other hand, suppose you want to **change** each element of a
structure according to a particular algorithm. This can be done only
with great pain using :func:`MAPF`, since you don’t have easy access to the
**structure** inside the function: you have only the structure’s
elements. :func:`MAPR` solves the problem by applying a function to
:func:`REST`\ s of a structure: first to :samp:`<REST {structure} 0>`, then to
:samp:`<REST {structure} 1>`, etc. Thus, the function can change the structure
by changing its argument, for example, by a
:samp:`<PUT {argument} 1 {something}>`. It can even :func:`PUT` a new element
farther down the structure, which will be seen by the function on
subsequent applications.

Now suppose, in addition to applying a function to a structure, you want
to record the results – the values returned by the function – in another
structure. Both :func:`MAPF` and :func:`MAPR` can do this: they both take an
additional function as an argument, and, when the looping is over, apply
the additional function to **all** the results, and then return the
results of that application. Thus, if the additional function is
`,LIST`, you get a |LIST| of the previous results; if it is
`.VECTOR`, you get a |VECTOR| of results; etc.

Finally, it might be the case that you really want to loop a function
over more than one structure simultaneously. For instance, consider
creating a |LIST| whose elements are the element-by-element sum of the
contents of two other |LIST|\ s. Both :func:`MAPF` and :func:`MAPR` allow
this; you can, in fact, give each of them any number of structures full
of arguments for your looping function.

This was all mentioned because :func:`MAPF` and :func:`MAPR` appear to be
complex when seen baldly, due to the fact that the argument descriptions
must take into account the general case. Simpler, degenerate cases are
usually the ones used.

MAPF [1]
~~~~~~~~~~~~~~~~

::

    <MAPF finalf loopf s1 s2 ... sN>

where (after argument evaluation)

-  *finalf* is something applicable that evaluates all its arguments, or
   a |FALSE|;
-  *loopf* is something applicable to *N* arguments that evaluates all
   its arguments; and
-  *s1* through *sN* are structured objects (any |TYPE|)

does the following:

1. First, it applies *loopf* to *N* arguments: the first element of each
   of the structures. Then it :func:`REST`\ s each of the structures, and
   does the application again, looping until **any** of the structures
   runs out of elements. Each of the values returned by *loopf* is
   recorded in a |TUPLE|.
2. Then, it applies *finalf* to all the recorded values simultaneously,
   and returns the result of that application. If *finalf* is a
   |FALSE|, the recorded values are “thrown away” (actually never
   recorded in the first place) and the :func:`MAPF` returns only the last
   value returned by *loopf*. If any of the *si* structures is empty, to
   that *loopf* is never invoked, *finalf* is applied to **no**
   arguments; if *finalf* is a |FALSE|, :func:`MAPF` returns
   ``#FALSE ()``.

10.2.2 MAPR [1]
~~~~~~~~~~~~~~~

::

    <MAPR finalf loopf s1 s2 ... sN>

acts just like :func:`MAPF`, but, instead of applying *loopf* to :func:`NTH`\ s
of the structures – that is, ``<NTH si 1>``, ``<NTH si 2>``, etc. – it
applies it to :func:`REST`\ s of the structures – that is, ``<REST si 0>``,
``<REST si 1>``, etc.

.. examples-1-1:

Examples [1]
~~~~~~~~~~~~~~~~~~~~

Make the element-wise sum of two |LIST|\ s::

    <MAPF .LIST .+ '(1 2 3 4) '(10 11 12 13)>$
    (11 13 15 17)

Change a |UVECTOR| to contain double its values::

    <SET UV '![5 6 7 8 9]>$
    ![5 6 7 8 9!]
    <MAPR <>
           #FUNCTION ((L) <PUT .L 1 <* <1 .L> 2>>)
           .UV>$
    ![18!]
    .UV$
    ![10 12 14 16 18!]

Create a |STRING| from |CHARACTER|\ s::

    <MAPF ,STRING 1 '["MODELING" "DEVELOPMENT" "LIBRARY"]>$
    "MDL"

Sum the squares of the elements of a |UVECTOR|::

    <MAPF ,+ #FUNCTION ((N) <* .N .N>) '![3 4]>$
    25

A parallel assignment |FUNCTION| (Note that the arguments to :func:`MAPF`
are of different lengths.)::

    <DEFINE PSET ("TUPLE" TUP)
            <MAPF <>
                  ,SET
                  .TUP
                  <REST .TUP </ <LENGTH .TUP> 2>>>>$
    PSET
    <PSET A B C 1 2 3>$
    3
    .A$
    1
    .B$
    2
    .C$
    3

Note: it is easy to forget that *finalf* **must** evaluate its
arguments, which precludes the use of an |FSUBR|. It is primarily for
this reason that the |SUBR|\ s :func:`AND?` and :func:`OR?` were invented. As
an example, the predicate :func:`=?` could have been defined this way::

    <DEFINE =? (A B)
            <COND (<MONAD? .A> <==? .A .B>)
                  (<AND <NOT <MONAD? .B>>
                        <==? <TYPE .A> <TYPE .B>>
                        <==? <LENGTH .A> <LENGTH .B>>>
                   <MAPF ,AND? ,=? .A .B>)>>

.. rst-class:: expert

    By the way, the following shows how to construct a value that has the
    same |TYPE| as an argument.

    ::

        <DEFINE MAP-NOT (S)
        <COND (<MEMQ <PRIMTYPE .S> '![LIST VECTOR UVECTOR STRING]>
                <CHTYPE <MAPF ,<PRIMTYPE .S> ,NOT .S>
                        <TYPE .S>>)>>

    It works because the |ATOM|\ s that name the common ``STRUCTURED``
    |PRIMTYPE|\ s (|LIST|, |VECTOR|, |UVECTOR| and |STRING|) have
    as |GVAL|\ s the corresponding |SUBR|\ s to build objects of those
    |TYPE|\ s.

More on MAPF and MAPR
---------------------------

MAPRET
~~~~~~~~~~~~~~

:func:`MAPRET` is a |SUBR| that enables the *loopf* being used in a
:func:`MAPR` or :func:`MAPF` (and lexically within it, that is, not separated
from it by a function call) to return from zero to any number of values
as opposed to just one. For example, suppose a :func:`MAPF` of the following
form is used::

    <MAPF ,LIST <FUNCTION (E) ...> ...>

Now suppose that the programmer wants to add no elements to the final
|LIST| on some calls to the |FUNCTION| and add many on other calls
to the |FUNCTION|. To accomplish this, the |FUNCTION| simply calls
:func:`MAPRET` with the elements it wants added to the |LIST|. More
generally, :func:`MAPRET` causes its arguments to be added to the final
|TUPLE| of arguments to which the *finalf* will be applied.

Warning: :func:`MAPRET` is guaranteed to work only if it is called from an
explicit |FUNCTION| which is the second argument to a :func:`MAPF` or
:func:`MAPR`. In other words, the second argument to :func:`MAPF` or :func:`MAPR`
must be ``#FUNCTION (...)`` or ``<FUNCTION ...>`` if :func:`MAPRET` is to be
used.

Example: the following returns a |LIST| of all the |ATOM|\ s in an
|OBLIST| (chapter 15)::

    <DEFINE ATOMS (OB)
            <MAPF .LIST
                  <FUNCTION (BKT) <MAPRET !.BKT>>
                  .OB>>

MAPSTOP
~~~~~~~~~~~~~~~

:func:`MAPSTOP` is the same as :func:`MAPRET`, except that, after adding its
arguments, if any, to the final |TUPLE|, it forces the application of
*finalf* to occur, whether or not the structured objects have run out of
objects. Example: the following copies the first ten (or all) elements
of its argument into a |LIST|::

    <DEFINE FIRST-TEN (STRUC "AUX" (I 10))
     <MAPF ,LIST
          <FUNCTION (E)
              <COND (<0? <SET I <- .I 1>>> <MAPSTOP .E>)>
              .E>
          .STRUC>>

MAPLEAVE
~~~~~~~~~~~~~~~~

:func:`MAPLEAVE` is analogous to :func:`RETURN`, except that it works in
(lexically within) :func:`MAPF` or :func:`MAPR` instead of :func:`PROG` or
:func:`REPEAT`. It flushes the accumulated |TUPLE| of results and returns
its argument (optional, |T| by default) as the value of the :func:`MAPF`
or :func:`MAPR`. (It finds the MAPF/R that should returns in the current
binding of the |ATOM| ``LMAP\ !-INTERRUPTS`` (“last map”).) Example:
the following finds and returns the first non-zero element of its
argument, or ``#FALSE ()`` if there is none::

    <DEFINE FIRST-N0 (STRUC)
            <MAPF <>
                  <FUNCTION (X)
                    <COND (<N==? .X 0> <MAPLEAVE .X>)>>
                  .STRUC>>

Only two arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~

If :func:`MAPF` or :func:`MAPR` is given only two arguments, the iteration
function *loopf* is applied to no arguments each time, and the looping
continues indefinitely until a :func:`MAPLEAVE` or :func:`MAPSTOP` is invoked.
Example: the following returns a |LIST| of the integers from one less
than its argument to zero.

::

    <DEFINE LNUM (N)
            <MAPF ,LIST
                  <FUNCTION ()
                    <COND (<=? <SET N <- .N 1>>> <MAPSTOP 0>)
                          (ELSE .N)>>>>

One principle use of this form of MAPF/R involves processing input
characters, in cases where you don’t know how many characters are going
to arrive. The example below demonstrates this, using |SUBR|\ s which
are more fully explained in chapter 11. Another example can be found in
chapter 13.

Example: the following |FUNCTION| reads characters from the current
input channel until an ``$`` (ESC) is read, and then returns what was
read as one |STRING|. (The :tref:`SUBR READCHR` reads one character
from the input channel and returns it. :func:`NEXTCHR` returns the next
:func:`CHARACTER` which :func:`READCHR` will return – chapter 11.)

::

    <DEFINE RDSTR ()
      <MAPF .STRING
            <FUNCTION () <COND (<NOT <==? <NEXTCHR> <ASCII 27>>>
                                <READCHR>)
                               (T
                                <MAPSTOP>)>>>>$
    RDSTR

    <PROG () <READCHR> ;"Flush the ESC ending this input."
                 <RDSTR>>$
    ABC123<+ 3 4>$"ABC123<+ 3 4>"

STACKFORM
~~~~~~~~~~~~~~~~~

The :tref:`FSUBR STACKFORM` is archaic, due to improvements in the
implementation of MAPF/R, and it should not be used in new programs.

::

    <STACKFORM function arg pred>

is exactly equivalent to

::

    <MAPF function
          <FUNCTION () <COND (pred arg) (T <MAPSTOP>)>>>

In fact MAPF/R is more powerful, because :func:`MAPRET`, :func:`MAPSTOP`, and
:func:`MAPLEAVE` provide flexibility not available with :func:`STACKFORM`.

GO and TAG
----------------

:func:`GO` is provided in MDL for people who can’t recover from a youthful
experience with Basic, Fortran, PL/I, etc. The |SUBR|\ s previously
described in this chapter are much more tasteful for making good, clean,
“structured” programs. :func:`GO` just bollixes things.

:func:`GO` is a |SUBR| which allows you to break the normal order of
evaluation and re-start just before any top-level expression in a
:func:`PROG` or :func:`REPEAT`. It can take two |TYPE|\ s of arguments:
|ATOM| or :t:`TAG`.

Given an |ATOM|, :func:`GO` searches the *body* of the immediately
surrounding :func:`PROG` or :func:`REPEAT` within the current Function, starting
after *aux*, for an occurrence of that |ATOM| at the top level of
*body*. (This search is effectively a :func:`MEMQ`.) If it doesn’t find the
|ATOM|, an error occurs. If it does, evaluation is resumed at the
expression following the |ATOM|.

The :tref:`SUBR TAG` generates and returns objects of :tref:`TYPE TAG`.
This |SUBR| takes one argument: an |ATOM| which would be a legal
argument for a :func:`GO`. An object of :tref:`TYPE TAG` contains sufficient
information to allow you to :func:`GO` to any top-level position in a
:func:`PROG` or :func:`REPEAT` from within any function called inside the
:func:`PROG` or :func:`REPEAT`. :func:`GO` with a :t:`TAG` is vaguely like :func:`AGAIN`
with an |ACTIVATION|; it allows you to “go back” to the middle of any
:func:`PROG` or :func:`REPEAT` which called you. Also like |ACTIVATION|\ s,
:t:`TAG`\ s into a :func:`PROG` or :func:`REPEAT` can no longer be used after the
:func:`PROG` or :func:`REPEAT` has returned. :func:`LEGAL?` can be used to see if a
:t:`TAG` is still valid.

Looping versus Recursion
------------------------------

Since any program in MDL can be called recursively, champions of “pure
Lisp” (Moon, 1974) or somesuch may be tempted to implement any
repetitive algorithm using recursion. The advantage of the looping
techniques described in this chapter over recursion is that the overhead
of calls is eliminated. However, a long program (say, bigger than half a
printed page) may be more difficult to write iteratively than
recursively and hence more difficult to maintain. A program whose
repetition is controlled by a structured object (for example, “walking a
tree” to visit each monad in the object) often should use looping for
covering one “level” of the structure and recursion to change “levels”.
