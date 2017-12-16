.. _ch-functions:

Chapter 9. Functions
====================

This chapter could be named “fun and games with argument ``LIST``\ s”.
Its purpose is to explain the more complicated things which can be done
with ``FUNCTION``\ s, and this involves, basically, explaining all the
various tokens which can appear in the argument ``LIST`` of a
``FUNCTION``. Topics are covered in what is approximately an order of
increasing complexity. This order has little to do with the order in
which tokens can actually appear in an argument ``LIST``, so what an
argument ``LIST`` “looks like” overall gets rather lost in the shuffle.
To alleviate this problem, section 9.9 is a summary of everything that
can go into an argument ``LIST``, in the correct order. If you find
yourself getting lost, please refer to that summary.

9.1. “OPTIONAL” [1]
-------------------

MDL provides very convenient means for allowing optional arguments. The
``STRING`` ``"OPTIONAL"`` (or ``"OPT"`` – they’re totally equivalent) in
the argument ``LIST`` allows the specification of optional arguments
with values to be assigned by default. The syntax of the ``"OPTIONAL"``
part of the argument ``LIST`` is as follows::

    "OPTIONAL" al-1 al-2 ... al-N

First, there is the ``STRING`` ``"OPTIONAL"``. Then there is any number
of either ``ATOM``\ s or two-element ``LIST``\ s, intermixed, one per
optional argument. The first element of each two-element ``LIST`` must
be an ``ATOM``; this is the dummy variable. The second element is an
arbitrary MDL expression. If there are required arguments, they must
come before the ``"OPTIONAL"``.

When ``EVAL`` is binding the variables of a ``FUNCTION`` and sees
``"OPTIONAL"``, the following happens:

-  If an explicit argument was given in the position of an optional one,
   the explicit argument is bound to the corresponding dummy ``ATOM``.
-  If there is no explicit argument and the ``ATOM`` stands alone, that
   is, it is not the first element of a two-element ``LIST``, that
   ``ATOM`` becomes “bound”, but no local value is assigned to it [see
   below]. A local value can be assigned to it by using ``SET``.
-  If there is no explicit argument and the ``ATOM`` is the first
   element of a two-element ``LIST``, the MDL expression in the ``LIST``
   with the ``ATOM`` is evaluated and bound to the ``ATOM``.

[Until an ``ATOM`` is assigned, any attempt to reference its ``LVAL``
will produce an error. The predicate ``SUBR``\ s ``BOUND?`` and
``ASSIGNED?`` can be used to check for such situations. ``BOUND?``
returns ``T`` if its argument is currently bound via an argument
``LIST`` or has ever been ``SET`` while not bound via an argument
``LIST``. The latter kind of binding is called “top-level binding”,
because it is done outside all active argument-\ ``LIST`` binding.
``ASSIGNED?`` will return ``#FALSE ()`` if its argument is **either**
unassigned **or** unbound. By the way, there are two predicates for
global values similar to ``BOUND?`` and ``ASSIGNED?``, namely
``GBOUND?`` and ``GASSIGNED?``. Each returns ``T`` only if its argument,
which (as in ``BOUND?`` and ``ASSIGNED?``) must be an ``ATOM``, has a
global value “slot” (chapter 22) or a global value, respectively.]

Example::

    <DEFINE INC1 (A "OPTIONAL" (N 1)) <SET .A <+ ..A .N>>>$
    INC1
    <SET B 0>$
    0
    <INC1 B>$
    1
    <INC1 B 5>$
    0

Here we defined another (not quite working) increment ``FUNCTION``. It
now takes an optional argument specifying how much to increment the
``ATOM`` it is given. If not given, the increment is ``1``. Now, ``1``
is a pretty simple MDL expression: there is no reason why the optional
argument cannot be complicated – for example, a call to a ``FUNCTION``
which reads a file on an I/O device.

9.2. TUPLEs
-----------

9.2.1. “TUPLE” and TUPLE (the TYPE) [1]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are also times when you want to be able to have an arbitrary
number of arguments. You can always do this by defining the ``FUNCTION``
as having a structure as its argument, with the arbitrary number of
arguments as elements of the structure. This can, however, lead to
inelegant-looking ``FORM``\ s and extra garbage to be collected. The
``STRING`` ``"TUPLE"`` appearing in the argument ``LIST`` allows you to
avoid that. It must follow explicit and optional dummy arguments (if
there are any of either) and must be followed by an ``ATOM``.

The effect of ``"TUPLE"`` appearing in an argument ``LIST`` is the
following: any arguments left in the ``FORM``, after satisfying explicit
and optional arguments, are ``EVAL``\ ed and made sequential elements of
an object of ``TYPE`` and ``PRIMTYPE`` ``TUPLE``. The ``TUPLE`` is the
bound to the ``ATOM`` following ``"TUPLE"`` in the argument ``LIST``. If
there were no arguments left by the time the ``"TUPLE"`` was reached, an
empty ``TUPLE`` is bound to the ``ATOM``.

An object of ``TYPE`` ``TUPLE`` is exactly the same as a ``VECTOR``
except that a ``TUPLE`` is not held in garbage-collected storage. It is
instead held with ``ATOM`` bindings in a control stack. This does not
affect manipulation of the ``TUPLE`` within the function generating it
or any function called within that one: it can be treated just like a
``VECTOR``. Note, however, that a ``TUPLE`` ceases to exist when the
function which generated it returns. Returning a ``TUPLE`` as a value is
a good way to generate an error. (A copy of a ``TUPLE`` can easily be
generated by segment-evaluating the ``TUPLE`` into something; that copy
can be returned.) The predicate ``LEGAL?`` returns ``#FALSE ()`` if it
is given a ``TUPLE`` generated by an ``APPLICABLE`` object which has
already returned, and ``T`` if it is given a ``TUPLE`` which is still
“good”.

Example::

    <DEFINE NTHARG (N "TUPLE" T)
                    ;"Get all but first argument into T."
        <COND (<==? 1 .N> 1)
                    ;"If N is 1, return 1st arg, i.e., .N,
                      i.e., 1.  Note that <1? .N> would be
                      true even if .N were 1.0."
              (<L? <LENGTH .T> <SET N <- .N 1>>>
               #FALSE ("DUMMY"))
                    ;"Check to see if there is an Nth arg,
                      and make N a good index into T while
                      you're at it.
                      If there isn't an Nth arg, complain."
              (ELSE <NTH .T .N>)>>

``NTHARG``, above, takes any number of arguments. Its first argument
must be of ``TYPE`` ``FIX``. It returns ``EVAL`` of its Nth argument, if
it has an Nth argument. If it doesn’t, it returns ``#FALSE ("DUMMY")``.
(The ``ELSE`` is not absolutely necessary in the last clause. If the Nth
argument is a ``FALSE``, the ``COND`` will return that ``FALSE``.)
Exercise for the reader: ``NTHARG`` will generate an error if its first
argument is not ``FIX``. Where and why? (How about
``<NTHARG 1.5 2 3>``?) Fix it.

9.2.2. TUPLE (the SUBR) and ITUPLE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These ``SUBR``\ s are the same as ``VECTOR`` and ``IVECTOR``, except
that they build ``TUPLE``\ s (that is, vectors on the control stack).
They can be used only at top level in an ``"OPTIONAL"`` list or
``"AUX"`` list (see below). The clear advantage of ``TUPLE`` and
``ITUPLE`` (“implicit tuple”) is in storage-management efficiency. They
produce no garbage, since they are flushed automatically upon function
return.

Examples::

    <DEFINE F (A B "AUX" (C <ITUPLE 10 3>)) ...>

creates a 10-element ``TUPLE`` and ``SET``\ s ``C`` to it.

::

    <DEFINE H ("OPTIONAL" (A <ITUPLE 10 '<I>>)
                    "AUX" (B <TUPLE !.A 1 2 3>))
                    ...>

These are valid uses of ``TUPLE`` and ``ITUPLE``. However, the following
is **not** a valid use of ``TUPLE``, because it is not called at top
level of the ``"AUX"``::

    <DEFINE NO (A B "AUX" (C <REST <TUPLE !.A>>)) ...>

However, the desired effect could be achieved by

::

    <DEFINE OK (A B "AUX" (D <TUPLE !.A>) (C <REST .D>)) ...>

9.3 “AUX” [1]
-------------

``"AUX"`` (or ``"EXTRA"`` – they’re totally equivalent) are
``STRING``\ s which, placed in an argument ``LIST``, serve to
dynamically allocate temporary variables for the use of a Function.

``"AUX"`` must appear in the argument ``LIST`` after any information
about explicit arguments. It is followed by ``ATOM``\ s or two-element
``LIST``\ s as if it were ``"OPTIONAL"``. ``ATOM``\ s in the two-element
``LIST``\ s are bound to ``EVAL`` of the second element in the ``LIST``.
Atoms not in such ``LIST``\ s are initially **unassigned**: they are
explicitly given “no” ``LVAL``.

All binding specified in an argument ``LIST`` is done sequentially from
first to last, so initialization expressions for ``"AUX"`` (or
``"OPTIONAL"``) can refer to objects which have just been bound. For
example, this works::

    <DEFINE AUXEX ("TUPLE" T
                     "AUX" (A <LENGTH .T>) (B <* 2 .A>))
            ![.A .B]>$
    AUXEX
    <AUXEX 1 2 "FOO">$
    ![3 6!]

9.4. QUOTEd arguments
---------------------

If an ``ATOM`` in an argument ``LIST`` which is to be bound to a
required or optional argument is surrounded by a call to ``QUOTE``, that
``ATOM`` is bound to the **unevaluated** argument. Example::

    <DEFINE Q2 (A 'B) (.A .B)>$
    Q2
    <Q2 <+ 1 2> <+ 1 2>>$
    (3 <+ 1 2>)

It is not often appropriate for a function to take its arguments
unevaluated, because such a practice makes it less modular and harder to
maintain: it and the programs that call it tend to need to know more
about each other, and a change in its argument structure would tend to
require more changes in the programs that call it. And, since few
functions, in practice, do take unevaluated arguments, users tend to
assume that no functions do (except ``FSUBR``\ s of course), and
confusion inevitably results.

9.5. “ARGS”
-----------

The indicator ``"ARGS"`` can appear in an argument ``LIST`` with
precisely the same syntax as ``"TUPLE"``. However, ``"ARGS"`` causes the
``ATOM`` following it to be bound to a ``LIST`` of the remaining
**unevaluated** arguments.

``"ARGS"`` does not cause any copying to take place. It simply gives you

::

    <REST application:form fix>

with an appropriate *fix*. The ``TYPE`` change to ``LIST`` is a result
of the ``REST``. Since the ``LIST`` shares all its elements with the
original ``FORM``, ``PUT``\ s into the ``LIST`` will change the calling
program, however dangerous that may be.

Examples::

    <DEFINE QIT (N "ARGS" L) <.N .L>>$
    QIT
    <QIT 2 <+ 3 4 <LENGTH ,QALL> FOO>$
    <LENGTH ,QALL>

    <DEFINE FUNCT1 ("ARGS" ARGL-AND-BODY)
            <CHTYPE .ARGL-AND-BODY FUNCTION>>$
    FUNCT1
    <FUNCT1 (A B) <+ .A .B>>$
    #FUNCTION ((A B) <+ .A .B>)

The last example is a perfectly valid equivalent of the ``FSUBR``
``FUNCTION``.

9.6. “CALL”
-----------

The indicator ``"CALL"`` is an ultimate ``"ARGS"``. If it appears in an
argument ``LIST``, it must be followed by an ``ATOM`` and must be the
only thing used to gather arguments. ``"CALL"`` causes the ``ATOM``
which follows it to become bound to the actual ``FORM`` that is being
evaluated – that is, you get the “function call” itself. Since
``"CALL"`` binds to the ``FORM`` itself, and not a copy, ``PUT``\ s into
that ``FORM`` will change the calling code.

``"CALL"`` exists as a Catch-22 for argument manipulation. If you can’t
do it with ``"CALL"``, it can’t be done.

9.7. EVAL and “BIND”
--------------------

Obtaining unevaluated arguments, for example, for ``QUOTE`` and
``"ARGS"``, very often implies that you wish to evaluate them at some
point. You can do this by explicitly calling ``EVAL``, which is a
``SUBR``. Example::

    <SET F '<+ 1 2>>$
    <+ 1 2>
    <EVAL .F>$
    3

``EVAL`` can take a second argument, of ``TYPE`` ``ENVIRONMENT`` (or
others, see section 20.8). An ``ENVIRONMENT`` consists basically of a
state of ``ATOM`` bindings; it is the “world” mentioned in chapter 5.
Now, since binding changes the ``ENVIRONMENT``, if you wish to use
``EVAL`` within a ``FUNCTION``, you probably want to get hold of the
environment which existed **before** that ``FUNCTION``\ ’s binding took
place. The indicator ``"BIND"``, which must, if it is used, be the first
thing in an argument ``LIST``, provides this information. It binds the
``ATOM`` immediately following it to the ``ENVIRONMENT`` existing “at
call time” – that is, just before any binding is done for its
``FUNCTION``. Example::

    <SET A 0>$
    0
    <DEFINE WRONG ('B "AUX" (A 1)) <EVAL .B>>$
    WRONG
    <WRONG .A>
    1
    <DEFINE RIGHT ("BIND" E 'B "AUX" (A 1)) <EVAL .B .E>>$
    RIGHT
    <RIGHT .A>$
    0

9.7.1. Local Values versus ENVIRONMENTs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``SET``, ``LVAL``, ``VALUE``, ``BOUND?``, ``ASSIGNED?``, and
``UNASSIGN`` all take a final optional argument which has not previously
been mentioned: an ``ENVIRONMENT`` (or other ``TYPE``\ s, see section
20.8). If this argument is given, the ``SET`` or ``LVAL`` is done in the
``ENVIRONMENT`` specified. ``LVAL`` cannot be abbreviated by ``.``
(period) if it is given an explicit second argument.

This feature is just what is needed to cure the ``INC`` bug mentioned in
chapter 5. A “correct” ``INC`` can be defined as follows::

    <DEFINE INC ("BIND" OUTER ATM)
            <SET .ATM <+ 1 <LVAL .ATM .OUTER>> .OUTER>>

9.8. ACTIVATION, “NAME”, “ACT”, “AGAIN”, and RETURN [1]
-------------------------------------------------------

``EVAL``\ uation of a ``FUNCTION``, after the argument ``LIST`` has been
taken care of, normally consists of ``EVAL``\ uating each of the objects
in the body in the order given, and returning the value of the last
thing ``EVAL``\ ed. If you want to vary this sequence, you need to know,
at least, where the ``FUNCTION`` begins. Actually, ``EVAL`` normally
hasn’t the foggiest idea of where its current ``FUNCTION`` began.
“Where’d I start” information is bundled up with a ``TYPE`` called
``ACTIVATION``. In “normal” ``FUNCTION`` ``EVAL``\ uation,
``ACTIVATION``\ s are not generated: one can be generated, and bound to
an ``ATOM``, in either of the two following ways:

1. Put an ``ATOM`` immediately before the argument ``LIST``. The
   ``ACTIVATION`` of the Function will be bound to that ``ATOM``.
2. As the last thing in the argument ``LIST``, insert either of the
   ``STRING``\ s ``"NAME"`` or ``"ACT"`` and follow it with an ``ATOM``.
   The ``ATOM`` will be bound to the ``ACTIVATION`` of the Function.

In this document “Function” (capitalized) will designate anything that
can generate an ``ACTIVATION``; besides ``TYPE`` ``FUNCTION``, this
class includes the ``FSUBR``\ s ``PROG``, ``BIND``, and ``REPEAT``, yet
to be discussed.

Each ``ACTIVATION`` refers explicitly to a particular evaluation of a
Function. For example, if a recursive ``FUNCTION`` generates an
``ACTIVATION``, a new ``ACTIVATION`` referring explicitly to each
recursion step is generated on every recursion.

Like ``TUPLE``\ s, ``ACTIVATION``\ s are held in a control stack. Unlike
``TUPLE``\ s, there is **no way** to get a copy of an ``ACTIVATION``
which can usefully be returned as a value. (This is a consequence of the
fact that ``ACTIVATION``\ s refer to evaluations; when the evaluation is
finished, the ``ACTIVATION`` no longer exists.) ``ACTIVATION``\ s can be
tested, like ``TUPLE``\ s, by ``LEGAL?`` for legality. They are used by
the ``SUBR``\ s ``AGAIN`` and ``RETURN``.

``AGAIN`` can take one argument: an ``ACTIVATION``. It means “start
doing this again”, where “this” is specified by the ``ACTIVATION``.
Specifically, ``AGAIN`` causes ``EVAL`` to return to where it started
working on the **body** of the Function in the evaluation specified by
the ``ACTIVATION``. The evaluation is not redone completely: in
particular, no re-binding (of arguments, ``"AUX"`` variables, etc.) is
done.

``RETURN`` can take two arguments: an arbitrary expression and an
``ACTIVATION``, in that order. It causes the Function evaluation whose
``ACTIVATION`` it is given to terminate and return ``EVAL`` of
``RETURN``\ ’s first argument. That is, ``RETURN`` means “quit doing
this and return that”, where “this” is the ``ACTIVATION`` – its second
argument – and “that” is the expression – its first argument. Example::

    <DEFINE MY+ ("TUPLE" T "AUX" (M 0) "NAME" NM)
            <COND (<EMPTY? .T> <RETURN .M .NM>)>
            <SET M <+ .M <1 .T>>>
            <SET T <REST .T>>
            <AGAIN .NM>>$
    MY+
    <MY+ 1 3 <LENGTH "FOO">>$
    7
    <MY+>$
    0

Note: suppose an ``ACTIVATION`` of one Function (call it ``F1``) is
passed to another Function (call it ``F2``) – for example, via an
application of ``F2`` within ``F1`` with ``F1``\ ’s ``ACTIVATION`` as an
argument. If ``F2`` ``RETURN``\ s to ``F1``\ ’s ``ACTIVATION``, ``F2``
**and** ``F1`` terminate immediately, and **``F1``** returns the
``RETURN``\ ’s first argument. This technique is suitable for error
exits. ``AGAIN`` can clearly pull a similar trick. In the following
example, ``F1`` computes the sum of ``F2`` applied to each of its
arguments; ``F2`` computes the product of the elements of its structured
argument, but it aborts if it finds an element that is not a number.

::

    <DEFINE F1 ACT ("TUPLE" T "AUX" (T1 .T))
            <COND (<NOT <EMPTY? .T1>>
                   <PUT .T1 1 <F2 <1 .T1> .ACT>>
                   <SET T1 <REST .T1>>
                   <AGAIN .ACT>)
                  (ELSE <+ !.T>)>>$
    F1
    <DEFINE F2 (S A "AUX" (S1 .S))
            <REPEAT MY-ACT ((PRD 1))
               <COND (<NOT <EMPTY? .S1>>
                      <COND (<NOT <TYPE? 1 .S1> FIX FLOAT>>
                             <RETURN #FALSE ("NON-NUMBER") .A>)
                            (ELSE <SET PRD <* .PRD <1 .S1>>>)>
                      <SET S1 <REST .S1>>)
                     (ELSE <RETURN .PRD>)>>>$
    F2

    <F1 '(1 2) '(3 4)>$
    14
    <F1 '(T 2) '(3 4)>$
    #FALSE ("NON-NUMBER")

9.9. Argument List Summary
--------------------------

The following is a listing of all the various tokens which can appear in
the argument ``LIST`` of a ``FUNCTION``, in the order in which they can
occur. Short descriptions of their effects are included. **All** of them
are **optional** – that is, any of them (in any position) can be left
out or included – but the order in which they appear **must** be that of
this list. “``QUOTE``\ d ``ATOM``”, “matching object”, and “2-list” are
defined below.

(1) ``"BIND"``

must be followed by an ``ATOM``. It binds that ``ATOM`` to the
``ENVIRONMENT`` which existed when the ``FUNCTION`` was applied.

(2) ``ATOM``\ s and ``QUOTE``\ d ``ATOM``\ s (any number)

are required arguments. ``QUOTE``\ d ``ATOM``\ s are bound to the
matching object. ``ATOM``\ s are bound to ``EVAL`` of the matching
object in the ``ENVIRONMENT`` existing when the ``FUNCTION`` was
applied.

(3) ``"OPTIONAL"`` or ``"OPT"`` (they’re equivalent)

is followed by any number of ``ATOM``\ s, ``QUOTE``\ d ``ATOM``\ s, or
2-lists. These are optional arguments. If a matching object exists, an
``ATOM`` – either standing alone or the first element of a 2-list – is
bound to ``EVAL`` of the object, performed in the ``ENVIRONMENT``
existing when the ``FUNCTION`` was applied. A ``QUOTE``\ d ``ATOM`` –
alone or in a 2-list – is bound to the matching object itself. If no
such object exists, ``ATOM``\ s and ``QUOTE``\ d ``ATOM``\ s are left
unbound, and the first element of each 2-list is bound to ``EVAL`` of
the corresponding second element. (This ``EVAL`` is done in the new
``ENVIRONMENT`` of the Function as it is being constructed.)

(4) ``"ARGS"`` (and **not** ``"TUPLE"``)

must be followed by an ``ATOM``. The ``ATOM`` is bound to a ``LIST`` of
**all** the remaining arguments, **unevaluated**. (If there are no more
arguments, the ``LIST`` is empty.) This ``LIST`` is actually a ``REST``
of the ``FORM`` applying the ``FUNCTION``. If ``"ARGS"`` appears in the
argument ``LIST``, ``"TUPLE"`` should not appear.

(4) ``"TUPLE"`` (and **not** ``"ARGS"``)

must be followed by an ``ATOM``. The ``ATOM`` is bound to a ``TUPLE``
(“``VECTOR`` on the control stack”) of all the remaining arguments,
**evaluated** in the environment existing when the ``FUNCTION`` was
applied. (If no arguments remain, the ``TUPLE`` is empty.) If
``"TUPLE"`` appears in the argument ``LIST``, ``"ARGS"`` should not
appear.

(5) ``"AUX"`` or ``"EXTRA"`` (they’re equivalent)

is followed by any number of ``ATOM``\ s or 2-lists. These are auxiliary
variables, bound away from the previous environment for the use of this
Function. ``ATOM``\ s are bound in the ``ENVIRONMENT`` of the Function,
but they are unassigned; the first element of each 2-list is both bound
and assigned to ``EVAL`` of the corresponding second element. (This
``EVAL`` is done in the new ``ENVIRONMENT`` of the Function as it is
being constructed.)

(6) ``"NAME"`` or ``"ACT"`` (they’re equivalent)

must be followed by an ``ATOM``. The ``ATOM`` is bound to the
``ACTIVATION`` of the current evaluation of the Function.

**ALSO** – in place of sections (2) (3) **and** (4), you can have

(2-3-4) ``"CALL"``

which must be followed by an ``ATOM``. The ``ATOM`` is bound to the
``FORM`` which caused application of this ``FUNCTION``.

The special terms used above mean this:

“``QUOTE``\ d ``ATOM``” – a two-element ``FORM`` whose first element is
the ``ATOM`` ``QUOTE``, and whose second element is any ``ATOM``. (Can
be typed – and will be ``PRINT``\ ed – as ``'atom``.)

“Matching object” – that element of a ``FORM`` whose position in the
``FORM`` matches the position of a required or optional argument in an
argument ``LIST``.

“2-list” – a two-element ``LIST`` whose first element is an ``ATOM`` (or
``QUOTE``\ d ``ATOM``: see below) and whose second element can be
anything but a ``SEGMENT``. ``EVAL`` of the second element is assigned
to a new binding of the first element (the ``ATOM``) as the “value by
default” in ``"OPTIONAL"`` or the “initial value” in ``"AUX"``. In the
case of ``"OPTIONAL"``, the first element of a 2-list can be a
``QUOTE``\ d ``ATOM``; in this case, an argument which is supplied is
not ``EVAL``\ ed, but if it is not supplied the second element of the
``LIST`` **is** ``EVAL``\ ed and assigned to the ``ATOM``.

9.10. APPLY [1]
---------------

Occasionally there is a valid reason for the first element of a ``FORM``
not to be an ``ATOM``. For example, the object to be applied to
arguments may be chosen at run time, or it may depend on the arguments
in some way. While ``EVAL`` is perfectly happy in this case to
``EVAL``\ uate the first element and go on from there, the compiler
(Lebling, 1979) can generate more efficient code if it knows whether the
result of the evaluation will (1) always be of ``TYPE`` ``FIX``, (2)
always be an applicable non-\ ``FIX`` object that evaluates all its
arguments, or (3) neither. The easiest way to tell the compiler if (1)
or (2) is true is to use the ``ATOM`` ``NTH`` (section 7.1.2) or ``PUT``
(section 7.1.4) in case (1) or ``APPLY`` in case (2) as the first
element of the ``FORM``. (Note: case (1) can compile into in-line code,
but case (2) compiles into a fully mediated call into the interpreter.)

::

    <APPLY object arg-1 ... arg-N>

evaluates *object* and all the *arg-i*\ ’s and then applies the former
to all the latter. An error occurs if *object* evaluates to something
not applicable, or to an ``FSUBR``, or to a ``FUNCTION`` (or user
Subroutine – chapter 19) with ``"ARGS"`` or ``"CALL"`` or ``QUOTE``\ d
arguments.

Example::

    <APPLY <NTH .ANALYZERS
                <LENGTH <MEMQ <TYPE .ARG> .ARGTYPES>>>
           .ARG>

calls a function to analyze ``.ARG``. Which function is called depends
on the ``TYPE`` of the argument; this represents the idea of a dispatch
table.

9.11. CLOSURE
-------------

::

    <CLOSURE function a1 ... aN>

where *function* is a ``FUNCTION``, and *a1* through *aN* are any number
of ``ATOM``\ s, returns an object of ``TYPE`` ``CLOSURE``. This can be
applied like any other function, but, whenever it is applied, the
``ATOM``\ s given in the call to ``CLOSURE`` are **first** bound to the
``VALUE``\ s they had when the ``CLOSURE`` was generated, then the
*function* is applied as normal. This is a “poor man’s ``funarg``”.

A ``CLOSURE`` is useful when a ``FUNCTION`` must have state information
remembered between calls to it, especially in these two cases: when the
``LVAL``\ s of external state ``ATOM``\ s might be compromised by other
programs, or when more than one distinct sequence of calls are active
concurrently. Example of the latter: each object of a structured
``NEWTYPE`` might have an associated ``CLOSURE`` that coughs up one
element at a time, with a value in the ``CLOSURE`` that is a structure
containing all the relevant information.
