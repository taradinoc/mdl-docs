.. _ch-machine-words-and-bits:

Chapter 18. Machine Words and Bits
==================================

The MDL facility for dealing with uninterpreted machine words and bits
involves two data TYPEs: WORD and BITS. A WORD is simply an
uninterpreted machine word, while a BITS is a “pointer” to a set of bits
within a WORD. Operating on WORDs is usually done only when compiled
programs are used (chapter 19).

18.1. WORDs
-----------

A ``WORD`` in MDL is a PDP-10 machine word of 36 bits. A ``WORD`` always
``PRINT``\ s in “# format”, and its contents are always printed in octal
(hence preceded and followed by ``*``). Examples:

::

    #WORD 0                  ;"all 0s"$
    #WORD *000000000000*

    #WORD *2000*             ;"one bit 1"$
    #WORD *000000002000*

    #WORD *525252525252*     ;"every other bit 1"$
    #WORD *525252525252*

``WORD`` is its own ``PRIMTYPE``; it is also the ``PRIMTYPE`` of
``FIX``, ``FLOAT``, ``CHARACTER``, and any other ``TYPE`` which can fit
its data into one machine word.

A ``WORD`` cannot be an argument to ``+``, ``-``, or indeed any
``SUBR``\ s except for ``CHTYPE``, ``GETBITS``, ``PUTBITS`` and several
bit-manipulating functions, all to be described below. Thus any
arithmetic bit manipulation must be done by ``CHTYPE``\ ing a ``WORD``
to ``FIX``, doing the arithmetic, and then ``CHTYPE``\ ing back to
``WORD``. However, bit manipulation can be done without ``CHTYPE``\ ing
the thing to be played with to a ``WORD``, so long as it is of
``PRIMTYPE`` ``WORD``; the result of the manipulation will be of the
same ``TYPE`` as the original object or can be ``CHTYPE``\ d to it.

18.2. BITS
----------

An object of ``TYPE`` ``BITS`` is of ``PRIMTYPE`` ``WORD``, and
``PRINT``\ s just like a ``WORD``. The internal form of a ``BITS`` is
precisely that of a PDP-10 “byte pointer”, which is, in fact, just what
a ``BITS`` is.

For purposes of explaining what a ``BITS`` is, assume that the bits in a
``WORD`` are numbered from **right** to **left**, with the rightmost bit
numbered 0 and the leftmost numbered 35, as in

::

    35 34 33 ... 2 1 0

(This is not the “standard” ordering: the “standard” one goes from left
to right.)

A ``BITS`` is most conveniently created via the ``SUBR`` ``BITS``:

::

    <BITS width:fix right-edge:fix>

returns a ``BITS`` which “points to” a set of bits *width* wide, with
rightmost bit *right-edge*. Both arguments must be of ``TYPE`` ``FIX``,
and the second is optional, 0 by default.

Examples: the indicated application of ``BITS`` returns an object of
``TYPE`` ``BITS`` which points to the indicated set of bits in a
``WORD``:

+-----------------+--------------------------------+
| Example         | Returns                        |
+=================+================================+
| ``<BITS 7>``    | 35 … 7 **6 … 0**               |
+-----------------+--------------------------------+
| ``<BITS 4 18>`` | 35 … 22 **21 20 19 18** 17 … 0 |
+-----------------+--------------------------------+
| ``<BITS 36>``   | ***35 … 0***                   |
+-----------------+--------------------------------+

18.3. GETBITS
-------------

::

    <GETBITS from:primtype-word bits>

where *from* is an object of ``PRIMTYPE`` ``WORD``, returns a **new**
object whose ``TYPE`` is ``WORD``. This object is constructed in the
following way: the set of bits in *from* pointed to by *bits* is copied
into the new object, right-adjusted, that is, lined up against the right
end (bit number 0) of the new object. All those bits of the new object
which are not copied are set to zero. In other words, ``GETBITS`` takes
bits from an arbitrary place in *from* and puts them at the right of a
new object. The *from* argument to ``GETBITS`` is not affected.

Examples:

::

    <GETBITS #WORD *777777777777* <BITS 3>>$
    #WORD *000000000007*
    <GETBITS *012345670123* <BITS 6 18>>$
    #WORD *000000000045*

18.4. PUTBITS
-------------

::

    <PUTBITS to:primtype-word bits from:primtype-word>

where *to* and *from* are of ``PRIMTYPE`` ``WORD``, returns a **copy**
of *to*, modified as follows: the set of bits in *to* which are pointed
to by *bits* are replaced by the appropriate number of rightmost bits
copied from *from* (optional, 0 by default). In other words: ``PUTBITS``
takes bits from the right of *from* and stuffs them into an arbitrary
position in a copy of *to*. **None** of the arguments to ``PUTBITS`` is
affected.

Examples:

::

    <PUTBITS #WORD *777777777777* <BITS 6 3>>$
    #WORD *777777777007*
    <PUTBITS #WORD *666777000111* <BITS 5 15> #WORD *123*>$
    #WORD *666776300111*
    <PUTBITS #WORD *765432107654* <BITS 18>>$
    #WORD *765432000000*

18.5. Bitwise Boolean Operations
--------------------------------

Each of the ``SUBR``\ s ``ANDB``, ``ORB``, ``XORB``, and ``EQVB`` takes
arguments of ``PRIMTYPE`` ``WORD`` and returns a ``WORD`` which is the
bitwise Boolean “and”, inclusive “or”, exclusive “or”, or “equivalence”
(inverse of exclusive “or”), respectively, of its arguments. Each takes
any number of arguments. If no argument is given, a ``WORD`` with all
bits off (``ORB`` and ``XORB``) or on (``ANDB`` and ``EQVB``) is
returned. If only one argument is given, it is returned unchanged but
``CHTYPE``\ d to a ``WORD``. If more than two arguments are given, the
operator is applied to the first two, then applied to that result and
the third, etc. Be sure not to confuse ``AND`` and ``OR`` with ``ANDB``
and ``ORB``.

18.6. Bitwise Shifting Operations
---------------------------------

::

    <LSH from:primtype-word amount:fix>

returns a **new** ``WORD`` containing the bits in *from*, shifted the
number of bits specified by *amount* (mod 256, says the hardware). Zero
bits are brought in at the end being vacated; bits shifted out at the
other end are lost. If *amount* is positive, shifting is to the left; if
*amount* is negative, shifting is to the right. Examples:

::

    <LSH 8 6>$
    #WORD *000000001000*
    <LSH 8 -6>$
    #WORD *000000000000*

    <ROT from:primtype-word amount:fix>

returns a **new** ``WORD`` containing the bits from *from*, rotated the
number of bits specified by *amount* (mod 256, says the hardware).
Rotation is a cyclic bitwise shift where bits shifted out at one end are
put back in at the other. If *amount* is positive, rotation is to the
left; if *amount* is negative, rotation is to the right. Examples:

::

    <ROT 8 6>$
    #WORD *000000001000*
    <ROT 8 -6>$
    #WORD *100000000000*
