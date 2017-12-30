Errors, Frames, etc.
================================

LISTEN
------------

This ``SUBR`` takes any number of arguments. It first checks the
``LVAL``\ s of ``INCHAN``, ``OUTCHAN``, and ``OBLIST`` for reasonability
and terminal usability. In each case, if the value is unreasonable, the
``ATOM`` is rebound to the corresponding ``GVAL``, if reasonable, or to
an invented reasonable value. ``LISTEN`` then does
``<TTYECHO .INCHAN T>`` and ``<ECHOPAIR .INCHAN .OUTCHAN>``. Next, it
``PRINT``\ s its arguments, then ``PRINT``\ s

::

    LISTENING-AT-LEVEL i PROCESS p

where *i* is an integer (``FIX``) which is incremented each time
``LISTEN`` is called recursively, and *p* is an integer identifying the
``PROCESS`` (chapter 20) in which the ``LISTEN`` was ``EVAL``\ ed.
``LISTEN`` then does ``<APPLY <VALUE REP>>``, if there is one, and if it
is ``APPLICABLE``. If not, it applies the ``SUBR`` ``REP`` (without
making a new ``FRAME`` – see below). This ``SUBR`` drops into an
infinite ``READ``-``EVAL``-``PRINT`` loop, which can be left via
``ERRET`` (section 16.4).

The standard ``LISTEN`` loop has two features for getting a handle on
objects that you have typed in and MDL has typed out. If the ``ATOM``
``L-INS`` has a local value that is a ``LIST``, ``LISTEN`` will keep
recent inputs (what ``READ`` returns) in it, most recent first.
Similarly, if the ``ATOM`` ``L-OUTS`` has a local value that is a
``LIST``, ``LISTEN`` will keep recent outputs (what ``EVAL`` returns) in
it, most recent first. The keeping is done before the ``PRINT``\ ing, so
that ^S does not defeat its purpose. The user can decide how much to
keep around by setting the length of each ``LIST``. Even if ``L-OUTS``
is not used, the atom ``LAST-OUT`` is always ``SET`` to the last object
returned by ``EVAL`` in the standard ``LISTEN`` loop. Example::

    <SET L-INS (NEWEST NEWER NEW)>$
    (NEWEST NEWER NEW)
    .L-INS$
    (.L-INS NEWEST NEWER)
    <SET FOO 69>$
    69
    <SET FIXIT <2 .LINS>>   ;"grab the last input"$
    <SET FOO 69>
    .L-INS$
    (.L-INS <SET FIXIT <2 .L-INS>> <SET FOO 69>)
    <PUT .FIXIT 3 105>$
    <SET FOO 105>
    <EVAL .FIXIT>$
    105
    .L-INS$
    (.L-INS <EVAL .FIXIT> <PUT .FIXIT 3 105>)
    .FOO$
    105

ERROR
-----------

This ``SUBR`` is the same as ``LISTEN``, except that (1) it generates an
interrupt (chapter 21), if enabled. and (2) it ``PRINT``\ s ``*ERROR*``
before ``PRINT``\ ing its arguments.

When any ``SUBR`` or ``FSUBR`` detects an anomalous condition (for
example, its arguments are of the wrong ``TYPE``), it calls ``ERROR``
with at least two arguments, including:

1. an ``ATOM`` whose ``PNAME`` describes the problem, normally from the
   ``OBLIST`` ``ERRORS!-`` (appendix 4),
2. the ``ATOM`` that names the ``SUBR`` or ``FSUBR``, and
3. any other information of interest, and **then returns whatever the
   call to ``ERROR`` returns**. Exception: a few (for example
   ``DEFINE``) will take further action that depends on the value
   returned. This nonstandard action is specified in the error message
   (first ``ERROR`` argument).

FRAME (the TYPE)

A ``FRAME`` is the object placed on a ``PROCESS``\ ’s control stack
(chapter 20) whenever a ``SUBR``, ``FSUBR``, ``RSUBR``, or
``RSUBR-ENTRY`` (chapter 19) is applied. (These objects are herein
collectively called “Subroutines”.) It contains information describing
what was applied, plus a ``TUPLE`` whose elements are the arguments to
the Subroutine applied. If any of the Subroutine’s arguments are to be
evaluated, they will have been by the time the ``FRAME`` is generated.

A ``FRAME`` is an anomalous ``TYPE`` in the following ways:

1. It cannot be typed in. It can be generated only by applying a
   Subroutine.
2. It does not type out in any standard format, but rather as ``#FRAME``
   followed by the ``PNAME``\ of the Subroutine applied.

ARGS

::

    <ARGS frame>

(“arguments”) returns the argument ``TUPLE`` of *frame*.

FUNCT

::

    <FUNCT frame>

(“function”} returns the ``ATOM`` whose ``G/LVAL`` is being applied in
*frame*.

FRAME (the SUBR)

::

    <FRAME frame>

returns the ``FRAME`` stacked **before** *frame* or, if there is none,
it will generate an error. The oldest (lowest) ``FRAME`` that can be
returned without error has a ``FUNCT`` of ``TOPLEVEL``. If called with
no arguments, ``FRAME`` returns the topmost ``FRAME`` used in an
application of ``ERROR`` or ``LISTEN``, which was bound by the
interpreter to the ``ATOM`` ``LERR\ I-INTERRUPTS`` (“last error”).

Examples

Say you have gotten an error. You can now type at ``ERROR``\ ’s
``LISTEN`` loop and get things ``EVAL``\ ed. For example,

::

    <FUNCT <FRAME>>$
    ERROR
    <FUNCT <FRAME <FRAME>>>$
    the-name-of-the-Subroutine-which-called-ERROR:atom
    <ARGS <FRAME <FRAME>>>$
    the-arguments-to-the-Subroutine-which-called-ERROR:tuple

ERRET

::

    <ERRET any frame>

This ``SUBR`` (“error return”) (1) causes the control stack to be
stripped down to the level of *frame*, and (2) **then** returns *any*.
The net result is that the application which generated *frame* is forced
to return *any*. Additional side effects that would have happened in the
absence of an error may not have happened.

The second argument to ``ERRET`` is optional, by default the ``FRAME``
of the last invocation of ``ERROR`` or ``LISTEN``.

If ``ERRET`` is called with **no** arguments, it drops you **all** the
way down to the **bottom** of the control stack – **before** the level-1
``LISTEN`` loop – and then calls ``LISTEN``. As always, ``LISTEN`` first
ensures that MDL is receptive.

Examples::

    <* 3 <+ a 1>>$
    *ERROR*
    ARG-WRONG-TYPE
    +
    LISTENING-AT-LEVEL 2 PROCESS 1
    <ARGS <FRAME <FRAME>>>$
    [a 1]
    <ERRET 5>$  ;"This causes the + to return 5."
    15      ;"finally returned by the *"

Note that when you are in a call to ``ERROR``, the most recent set of
bindings is still in effect. This means that you can examine values of
dummy variables while still in the error state. For example,

::

    <DEFINE F (A "AUX" (B "a string"))
        #DECL ((VALUE) LIST (A) STRUCTURED (B) STRING)
        (.B <REST .A 2>)    ;"Return this LIST.">$
    F
    <F '(1)>$

    *ERROR*
    OUT-OF-BOUNDS
    REST
    LISTENING-AT-LEVEL 2 PROCESS 1
    .A$
    (1)
    .B$
    "a string"
    <ERRET '(5)>    ; "Make the REST return (5)."$
    ("a string" (5))

RETRY

::

    <RETRY frame>

causes the control stack to be stripped down just beyond *frame*, and
then causes the Subroutine call that generated *frame* to be done again.
*frame* is optional, by default the ``FRAME`` of the last invocation of
``ERROR`` or ``LISTEN``. ``RETRY`` differs from ``AGAIN`` in that (1) it
is not intended to be used in programs; (2) it can retry any old *frame*
(any Subroutine call), whereas ``AGAIN`` requires an ``ACTIVATION``
(``PROG`` or ``REPEAT`` or ``"ACT"``); and (3) if it retries the
``EVAL`` of a ``FORM`` that makes an ``ACTIVATION``, it will cause
rebinding in the argument ``LIST``, thus duplicating side effects.

UNWIND

``UNWIND`` is an ``FSUBR`` that takes two arguments, usually
``FORM``\ s. It ``EVAL``\ s the first one, and, if the ``EVAL`` returns
normally, the value of the ``EVAL`` call is the value of ``UNWIND``. If,
however, during the ``EVAL`` a non-local return attempts to return below
the ``UNWIND`` ``FRAME`` in the control stack, the second argument is
``EVAL``\ ed, its value is ignored, and the non-local return is
completed. The second argument is evaluated in the environment that was
present when the call to ``UNWIND`` was made. This facility is useful
for cleaning up data bases that are in inconsistent states and for
closing temporary ``CHANNEL``\ s that may be left around. ``FLOAD`` sets
up an ``UNWIND`` to close its ``CHANNEL`` if the user attempts to
``ERRET`` without finishing the ``FLOAD``. Example::

    <DEFINE CLEAN ACT ("AUX" (C <OPEN "READ" "A FILE">))
        #DECL ((C) <OR CHANNEL FALSE> ...)
        <COND (.C
            <UNWIND <PROG () ... <CLOSE .C>>
                <CLOSE .C>>)>>

Control-G (^G)

Typing control-G (^G, ``<ASCII 7>``) at MDL causes it to act just as if
an error had occurred in whatever was currently being done. You can then
examine the values of variables as above, continue by applying ``ERRET``
to one argument (which is ignored), ``RETRY`` a ``FRAME`` lower on the
control stack, or flush everything by applying ``ERRET`` to no
arguments.

Control-S (^S)

Typing control-S (^S, ``<ASCII 19>``) at MDL causes it to stop what is
happening and return to the ``FRAME`` ``.LERR\ !-INTERRUPTS``, returning
the ``ATOM`` ``T``. (In the Tenex and Tops-20 versions, ^O also has the
same effect.)

OVERFLOW

::

    <OVERFLOW false-or-any>

There is one error that can be disabled: numeric overflow and underflow
caused by the arithmetic ``SUBR``\ s (``+``, ``-``, ``*``, ``/``). The
``SUBR`` ``OVERFLOW`` takes one argument: if it is of ``TYPE``
``FALSE``, under/overflow errors are disabled; otherwise they are
enabled. The initial state is enabled. ``OVERFLOW`` returns ``T`` or
``#FALSE ()``, reflecting the previous state. Calling it with no
argument returns the current state.
