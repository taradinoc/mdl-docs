Chapter 24. Efficiency and Tastefulness
=======================================

24.1. Efficiency
----------------

Actually, you make MDL programs efficient by thinking hard about what
they really make the interpreter **do**, and making them do less. Some
guidelines, in order of decreasing expense:

1. Free storage is expensive.
2. Calling functions is expensive.
3. ``PROG`` and ``REPEAT`` are expensive, except when compiled.

Explanation:

1. Unnecessary use of free storage (creating needless ``LIST``\ s,
   ``VECTOR``\ s, ``UVECTOR``\ s, etc.) will cause the garbage collector
   to run more often. This is **expensive!** A fairly large MDL (for
   example, 60,000 36-bit words) can take ten seconds of PDP-10 CPU time
   for a garbage collection. Be especially wary of constructions like
   ``(0)``. Every time that is evaluated, it creates a new one-element
   ``LIST``; it is too easy to write such things when they aren’t really
   necessary. Unless you are doing ``PUT``\ s or ``PUTREST``\ s on it,
   use ``'(0)`` instead.
2. Sad, but true. Also generally ignored. If you call a function only
   once, or if it is short (less than one line), you are much better off
   in speed if you substitute its body in by hand. On the other hand,
   you may be much worse off in modularity. There are techniques for
   combining several ``FUNCTION``\ s into one ``RSUBR`` (with
   ``RSUBR-ENTRY``\ s), either during or after compilation, and for
   changing ``FUNCTION``\ s into ``MACRO``\ s.
3. ``PROG`` is almost never necessary, given (a) ``"AUX"`` in
   ``FUNCTION``\ s; (b) the fact that ``FUNCTION``\ s can contain any
   number of ``FORM``\ s; (c) the fact that ``COND`` clauses can contain
   any number of ``FORM``\ s; and (d) the fact that new variables can be
   generated and initialized by ``REPEAT``. However, ``PROG`` may be
   useful when an error occurs, to establish bindings needed for
   cleaning things up or interacting with a human.

The use of ``PROG`` may be sensible when the normal flow of control can
be cut short by unusual conditions, so that the program wants to
``RETURN`` before reaching the end of ``PROG``. Of course, nested
``COND``\ s can accomplish the same end, but deep nesting may tend to
make the program unreadable. For example:

::

    <PROG (TEMP)
          <OR <SET TEMP <OK-FOR-STEP-1?>>
              <RETURN .TEMP>>
          <STEP-1>
          <OR <SET TEMP <OK-FOR-STEP-2?>>
              <RETURN .TEMP>>
          <STEP-2>>

could instead be written

::

    <COND (<OK-FOR-STEP-1?>
           <STEP-1>
           <COND (<OK-FOR-STEP-2?>
                  <STEP-2>)>)>

By the way, ``REPEAT`` is faster than ``GO`` in a ``PROG``. The
``<GO x>`` ``FORM`` has to be separately interpreted, right? In fact, if
you organize things properly you **very** seldom need a ``GO``; using
``GO`` is generally considered “bad style”, but in some cases it’s
needed. Very few.

In many cases, a ``REPEAT`` can be replaced with a ``MAPF`` or ``MAPR``,
or an ``ILIST``, ``IVECTOR``, etc. of the form

::

    <ILIST .N '<SET X <+ .X 1>>

which generates an ``N``-element ``LIST`` of successive numbers starting
at ``X+1``.

Whether a program is interpreted or compiled, the first two
considerations mentioned above hold: garbage collection and function
calling remain expensive. Garbage collection is, clearly, exactly the
same. Function calling is relatively more expensive. However, the
compiler careth not whether you use ``REPEAT``, ``GO``, ``PROG``,
``ILIST``, ``MAPF``, or whatnot: it all gets compiled into practically
the same thing. However, the ``REPEAT`` or ``PROG`` will be slower if it
has an ``ACTIVATION`` that is ``SPECIAL`` or used other than by
``RETURN`` or ``AGAIN``.

24.1.1. Example
~~~~~~~~~~~~~~~

There follows an example of a ``FUNCTION`` that does many things wrong.
It is accompanied by commentary, and two better versions of the same
thing. (This function actually occurred in practice. Needless to say,
names are withheld to protect the guilty.)

Blunt comment: this is terrible. Its purpose is to output the characters
needed by a graphics terminal to draw lines connecting a set of points.
The points are specified by two input lists: ``X`` values and ``Y``
values. The output channel is the third argument. The actual characters
for each line are returned in a ``LIST`` by the function ``TRANS``.

::

    <DEFINE PLOTVDSK (X Y CHN "AUX" L LIST)
       <COND (<NOT <==? <SET L <LENGTH .X>><LENGTH .Y> >>
              <ERROR "LENGTHS NOT EQUAL">)>
       <SET LIST (29)>
       <REPEAT ((N 1))
           <SET LIST (!.LIST !<TRANS <.N .X> <.N .Y>>)>
           <COND (<G? <SET N <+ .N 1>> .L><RETURN .N>)> >
       <REPEAT ((N 1) (L1 <LENGTH .LIST>))
           <PRINC <ASCII <.N .LIST>> .CHN>
           <COND (<G? <SET N <+ .N 1>> .L1>
                  <RETURN "DONE">)> >>

Comments:

1. ``LIST`` is only temporarily necessary. It is just created and then
   thrown away.
2. Worse, the construct ``(!.LIST !<TRANS ...>)`` **copies** the
   previous elements of ``LIST`` every time it is executed!
3. Indexing down the elements of ``LIST`` as in ``<.N .LIST>`` takes a
   long time, if the ``LIST`` is long. ``<3 ...>`` or ``<4 ...>`` is not
   worth worrying about, but ``<10 ...>`` is, and ``<100 ...>`` takes
   quite a while. Even if the indexing were not phased out, the compiler
   would be happier with ``<NTH .LIST .N>``.
4. The variable ``CHN`` is unnecessary if ``OUTCHAN`` is bound to the
   argument ``CHANNEL``.
5. It is tasteful to call ``ERROR`` in the same way that F/SUBRs do.
   This includes using an ``ATOM`` from the ``ERRORS`` ``OBLIST`` (if
   one is appropriate) to tell what is wrong, and it includes
   identifying yourself.

So, do it this way:

::

    <DEFINE PLOTVDSK (X Y OUTCHAN)
    #DECL ((OUTCHAN <SPECIAL CHANNEL>)
    <COND (<NOT <==? <LENGTH .X> <LENGTH .Y>>>
            <ERROR VECTOR-LENGTHS-DIFFER!-ERRORS PLOTVDSK>)>
    <PRINC <ASCII 29>>
    <REPEAT ()
            <COND (<EMPTY? .X> <RETURN "DONE">)>
            <REPEAT ((OL <TRANS <1 .X> <1 .Y>>))
                    <PRINC <ASCII <1 .OL>>>
                    <COND (<EMPTY? <SET OL <REST .OL>>>
                           <RETURN>)>>
            <SET X <REST .X>>
            <SET Y <REST .Y>>>>

Of course, if you know how long is the ``LIST`` that ``TRANS`` returns,
you can avoid using the inner ``REPEAT`` loop and have explicit
``PRINC``\ s for each element. This can be done even better by using
``MAPF``, as in the next version, which does exactly the same thing as
the previous one, but uses ``MAPF`` to do the ``REST``\ ing and the end
conditional:

::

    <DEFINE PLOTVDSK (X Y OUTCHAN)
    #DECL ((OUTCHAN <SPECIAL CHANNEL>)
    <COND (<NOT <==? <LENGTH .X> <LENGTH .Y>>>
            <ERROR VECTOR-LENGTHS-DIFFER!-ERRORS PLOTVDSK>)>
    <PRINC <ASCII 29>> <MAPF <>
          #FUNCTION ((XE YE)
                    <MAPF <> #FUNCTION ((T) <PRINC <ASCII .T>>) <TRANS
    .XE .YE>>)
          .X
          .Y>
    "DONE">

24.2. Creating a LIST in Forward Order
--------------------------------------

If you must create the elements of a ``LIST`` in sequence from first to
last, you can avoid copying earlier ones when adding a later one to the
end. One way is to use ``MAPF`` or ``MAPR`` with a first argument of
``,LIST``: the elements are put on the control stack rather than in free
storage, until the final call to ``LIST``. If you know how many elements
there will be, you can put them on the control stack yourself, in a
``TUPLE`` built for that purpose. Another way is used when ``REPEAT`` is
necessary:

::

    <REPEAT ((FIRST (T)) (LAST .FIRST) ...)
            #DECL ((VALUE FIRST LAST) LIST ...)
            ...
            <SET LAST <REST <PUTREST .LAST (.NEW)>>>
            ...
            <RETURN <REST .FIRST>>>
            ...>

Here, ``.LAST`` always points to the current last element of the
``LIST``. Because of the order of evaluation, the ``<SET LAST ...>``
could also be written ``<PUTREST .LAST (SET LAST (.NEW)>>``.

24.3. Read-only Free Variables
------------------------------

If a Function uses the value of a free variable
(``<GVAL unmanifest:atom>`` or ``<LVAL special:atom>``) without changing
it, the compiled version may be more efficient if the value is assigned
to a dummy ``UNSPECIAL`` ``ATOM`` in the Function’s ``"AUX"`` list. This
is true because an ``UNSPECIAL`` ``ATOM`` gets compiled into a slot on
the control stack, which is accessible very quickly. The tradeoff is
probably worthwhile if a *special* is referenced more than once, or if
an *unmanifest* is referenced more than twice. Example:

::

    <DEFINE MAP-LOOKUP (THINGS "AUX" (DB ,DATA-BASE))
            #DECL ((VALUE) VECTOR (THINGS DB) <UNSPECIAL <PRIMTYPE LIST>>)
            <MAPF ,VECTOR <FUNCTION (T) <MEMQ .T .DB>> .THINGS>>

24.4. Global and Local Values
-----------------------------

In the interpreter the sequence ``,X .X ,X .X`` is slower than
``,X ,X .X .X`` because of interference between the ``GVAL`` and
``LVAL`` mechanisms (appendix 1). Thus it is not good to use both the
``GVAL`` and ``LVAL`` of the same ``ATOM`` frequently, unless references
to the ``LVAL`` will be compiled away (made into control stack
references).

24.5. Making Offsets for Arrays
-------------------------------

It is often the case that you want to attach some meaning to each
element of an array and access it independently of other elements.
Firstly, it is a good idea to use names (``ATOM``\ s) rather than
integers (``FIX``\ es or even ``OFFSET``\ s) for offsets into the array,
to make future changes easier. Secondly, it is a good idea to use the
``GVAL``\ s of the name ``ATOM``\ s to remember the actual ``FIX``\ es,
so that the ``ATOM``\ s can be ``MANIFEST`` for the compiler’s benefit.
Thirdly, to establish the ``GVAL``\ s, both the interpreter and the
compiler will be happier with ``<SETG name offset>`` rather than
``<DEFINE name ("TUPLE" T) <offset !.T>>``.

24.6. Tables
------------

There are several ways in MDL to store a table, that is, a collection of
(names and) values that will be searched. Unsurprisingly, choosing the
best way is often dictated by the size of the table and/or the nature of
the (names and) values.

For a small table, the names and values can be put in (separate)
structures – the choice of ``LIST`` or array being determined by
volatility and limitability – which are searched using ``MEMQ`` or
``MEMBER``. This method is very space-efficient. If the table gets
larger, and if the elements are completely orderable, a (uniform) vector
can be used, kept sorted, and searched with a binary search.

For a large table, where reasonably efficient searches are required, a
hashing scheme is probably best. Two methods are available in MDL:
associations and ``OBLIST``\ s.

In the first method, ``PUTPROP`` and ``GETPROP`` are used, which are
very fast. The number of hashing buckets is fixed. Duplicates are
eliminated by ``==?`` testing. If it is necessary to use ``=?`` testing,
or to find all the entries in the table, you can duplicate the table in
a ``LIST`` or array, to be used only for those purposes.

In the second method, ``INSERT`` and ``LOOKUP`` on a specially-built
``OBLIST`` are used. (If the names are not ``STRING``\ s, they can be
converted to ``STRING``\ s using ``UNPARSE``, which takes a little
time.) The number of hashing buckets can be chosen for best efficiency.
Duplicates are eliminated by ``=?`` testing. MAPF/R can be used to find
all the entries in the table.

24.7. Nesting
-------------

The beauty of deeply-nested control structures in a single ``FUNCTION``
is definitely in the eye of the beholder. (``PPRINT``, a preloaded
``RSUBR``, finds them trying. However, the compiler often produces
better code from them.) **If** you don’t like excessive nesting, then
you will agree that

::

    <SET X ...>
    <COND (<0? .X> ...) ...>

looks better than

::

    <COND (<0? <SET X ...>> ...) ...>

and that

::

    <REPEAT ...
            <COND ...
                  (... <RETURN ...>)>
            ...
            ...>

looks better than

::

    <REPEAT ...
            <COND ...
                  (... <RETURN ...>)
                  (ELSE ...)>
            ...>

You can see the nature of the choices. Nesting is still and all better
than ``GO``.
