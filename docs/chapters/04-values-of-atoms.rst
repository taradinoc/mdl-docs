Values of Atoms
===============

General [1]
-----------

There are two kinds of “value” which can be attached to an |ATOM|. An
|ATOM| can have either, both, or neither. They interact in no way
(except that alternately referring to one and then the other is
inefficient). These two values are referred to as the **local value**
and the **global value** of an |ATOM|. The terms “local” and “global”
are relative to :t:`PROCESS`\ es (:numref:`ch-coroutines`), not functions
or programs. The |SUBR|\ s which reference the local and global values of an
|ATOM|, and some of the characteristics of local versus global values,
follow.

Global Values
-------------

SETG [1]
~~~~~~~~

A global value can be assigned to an |ATOM| by the :tref:`SUBR SETG`
(“set global”), as in

.. function:: <SETG atom any>

where *atom* must :func:`EVAL` to an |ATOM|, and *any* can :func:`EVAL` to
anything. :func:`EVAL` of the second argument becomes the global value of
:func:`EVAL` of the first argument. The value returned by the :func:`SETG` is
its second argument, namely the new global value of *atom*.

Examples::

    <SETG FOO <SETG BAR 500>>$
    500

The above made the global values of both the :tref:`ATOM FOO` and the
:tref:`ATOM BAR` equal to the |FIX|\ ed-point number 500.

::

    <SETG BAR FOO>$
    FOO

That made the global value of the :tref:`ATOM BAR` equal to the
:tref:`ATOM FOO`.

GVAL [1]
~~~~~~~~

The :tref:`SUBR GVAL` (“global value”) is used to reference the global
value of an |ATOM|.

.. function:: <GVAL atom>

returns as a value the global value of *atom*. If *atom* does not
evaluate to an |ATOM|, or if the |ATOM| to which it evaluates has no
global value, an error occurs.

:func:`GVAL` applied to an |ATOM| anywhere, in any :t:`PROCESS`, in any
function, will return the same value. Any :func:`SETG` anywhere changes the
global value for everybody. Global values are context-independent.

:func:`READ` understands the character ``,`` (comma) as an abbreviation for
an application of :func:`GVAL` to whatever follows it. :func:`PRINT` always
translates an application of :func:`GVAL` into the comma format. The
following are absolutely equivalent::

    ,atom        <GVAL atom>

Assuming the examples in :numref:`SETG` were carried out in the
order given, the following will evaluate as indicated::

    ,FOO$
    500
    <GVAL FOO>$
    500
    ,BAR$
    FOO
    ,,BAR$
    500

Note on SUBRs and FSUBRs
~~~~~~~~~~~~~~~~~~~~~~~~

The initial :func:`GVAL`\ s of the |ATOM|\ s used to refer to MDL
“built-in” Subroutines are the |SUBR|\ s and |FSUBR|\ s which
actually get applied when those |ATOM|\ s are referenced. If you don’t
like the way those supplied routines work, you are perfectly free to
:func:`SETG` the |ATOM|\ s to your own versions.

GUNASSIGN
~~~~~~~~~

.. function:: <GUNASSIGN atom>

(“global unassign”) causes *atom* to have no assigned global value,
whether or not it had one previously. The storage used for the global
value can become free for other uses.

Local Values
------------

SET [1]
~~~~~~~

The :tref:`SUBR SET` is used to assign a local value to an |ATOM|.
Applications of :func:`SET` are of the form

.. function:: <SET atom any>

:func:`SET` returns :func:`EVAL` of *any* just like :func:`SETG`.

Examples::

    <SET BAR <SET FOO 100>>$
    100

Both ``BAR`` and ``FOO`` have been given local values equal to the
|FIX|\ ed-point number 100.

::

    <SET FOO BAR>$
    BAR

\ ``FOO`` has been given the local value ``BAR``.

Note that neither of the above did anything to any global values ``FOO``
and ``BAR`` might have had.

LVAL [1]
~~~~~~~~

The |SUBR| used to extract the local value of an |ATOM| is named :func:`LVAL`.
As with :func:`GVAL`, :func:`READ` understands an abbreviation for an
application of :func:`LVAL`: the character ``.`` (period), and :func:`PRINT`
produces it. The following two representations are equivalent, and when
:func:`EVAL` operates on the corresponding MDL object, it returns the current
local value of *atom*::

    <LVAL atom>        .atom

The local value of an |ATOM| is unique within a :t:`PROCESS`.
:func:`SET`\ ting an |ATOM| in one :t:`PROCESS` has no effect on its
:func:`LVAL` in another :t:`PROCESS`, because each :t:`PROCESS` has its own
“control stack” (chapters :numref:`%s <ch-coroutines>` and
:numref:`%s <ch-storage-management>`).

Assume **all** of the previous examples in this chapter have been done.
Then the following evaluate as indicated::

    .BAR$
    100
    <LVAL BAR>$
    100
    .FOO$
    BAR
    ,.FOO$
    FOO

UNASSIGN
~~~~~~~~

.. function:: <UNASSIGN atom>

causes *atom* to have no assigned local value, whether or not it had one
previously.

VALUE
-----

.. function:: <VALUE atom>
  :nodoc:

:func:`VALUE` is a |SUBR| which takes an |ATOM| as an argument, and
then:

  1. if the |ATOM| has an :func:`LVAL`, returns the :func:`LVAL`;
  2. if the |ATOM| has no :func:`LVAL` but has a :func:`GVAL`, returns the
     :func:`GVAL`;
  3. if the |ATOM| has neither a :func:`GVAL` nor an :func:`LVAL`, calls the
     :func:`ERROR` function.

This order of seeking a value is the **opposite** of that used when an
|ATOM| is the first element of a |FORM|. The latter will be called
the |G/LVAL|, even though that name is not used in MDL.

Example::

    <UNASSIGN A>$
    A
    <SETG A 1>$
    1
    <VALUE A>$
    1
    <SET A 2>$
    2
    <VALUE A>$
    2
    ,A$
    1
