Appendix 1. A Look Inside
=========================

This appendix tells about the mapping between MDL objects and PDP-10
storage – in other words, the way things look “on the inside”. None of
this information is essential to knowing how to program in MDL, but it
does give some reasons for capabilities and restrictions that otherwise
you have to memorize. The notation and terminology get a little awkward
in this discussion, because we are in a twilight zone between the worlds
of MDL objects and of bit patterns. In general the words and phrases
appearing in diagrams refer to bit patterns not MDL objects. A
lower-case word (like “tuple”) refers to the storage occupied by an
object of the corresponding ``PRIMTYPE`` (like ``TUPLE``).

First some terminology needs discussion. The sine qua non of any MDL
object is a **pair** of 36-bit computer words. In general, lists consist
of pairs chained together by pointers (addresses), and vectors consist
of contiguous blocks of pairs. ``==?`` essentially tests two pairs to
see whether they contain the same bit patterns.

The first (lower-addressed) word of a pair is called the **``TYPE``
word**, because it contains a numeric **``TYPE`` code** that represents
the object’s ``TYPE``. The second (higher-addressed) word of a pair is
called the **value word**, because it contains (part of or the beginning
of) the “data part” of the object. The ``TYPE`` word (and sometimes the
value word) is considered to be made of a left half and a right half. We
will picture a pair like this:

::

    ---------------------------------
    |      TYPE     |               |
    | - - - - - - - - - - - - - - - |
    |             value             |
    ---------------------------------

where a vertical bar in the middle of a word means the word’s halves are
used independently. You can see that the ``TYPE`` code is confined to
the left half of the ``TYPE`` word. (Half-)words are sometimes
subdivided into **fields** appropriate for the context; fields are also
pictured as separated by vertical bars. The right half of the ``TYPE``
word is used for different purposes depending on the ``TYPE`` of the
object and actual location of the value.

Actually the 18-bit ``TYPE`` field is further decoded. The high-order
(leftmost) bit is the mark bit, used exclusively by the garbage
collector when it runs. The next two bits are monitor bits, used to
cause ``"READ"`` and ``"WRITE"`` interrupts on read and write references
to the pair. The next bit is used to differentiate between list elements
and vector dope words. The next bit is unused but could be used in the
future for an “execute” monitor. The remaining 13 bits specify the
actual ``TYPE`` code. What ``CHTYPE`` does is to copy the pair and put a
new ``TYPE`` code into the new pair.

Each data ``TYPE`` (predefined and ``NEWTYPE``\ s) must belong to one of
about 25 “storage allocation classes” (roughly corresponding to MDL
``PRIMTYPE``\ s). These classes are characterized primarily by the
manner in which the garbage collector treats them. Some of these classes
will now be described.

“One Word”

This class includes all data that are not pointers to some kind of
structure. All external (program-available) ``TYPE``\ s in this class
are of ``PRIMTYPE`` ``WORD``. Example:

::

    ---------------------------------
    |       FIX     |       0       |
    | - - - - - - - - - - - - - - - |
    |              105              |
    ---------------------------------

“Two Word”

The members of this class are all 18-bit pointers to list elements. All
external ``TYPE``\ s in this class are of ``PRIMTYPE`` ``LIST``.
Example:

::

    ---------------------------------
    |      LIST     |       0       |
    | - - - - - - - - - - - - - - - |
    |       0       |    pointer    |
    ---------------------------------

where ``pointer`` is a pointer to the first list element. If there are
no elements, ``pointer`` is zero; thus empty objects of ``PRIMTYPE``
``LIST`` are ``==?`` if their ``TYPE``\ s are the same.

“Two N Word”

Members of this class are all “counting pointers” to blocks of two-word
pairs. The right half of a counting pointer is an address, and the left
half is the negative of the number of 36-bit words in the block. (This
format is tailored to the PDP-10 ``AOBJN`` instruction.) The number of
pairs in the block (``LENGTH``) is half that number, since each pair is
two words. All external ``TYPE``\ s in this class are of ``PRIMTYPE``
``VECTOR``. Example:

::

    ---------------------------------
    |     VECTOR    |       0       |
    | - - - - - - - - - - - - - - - |
    |   -2*length   |    pointer    |
    ---------------------------------

where ``length`` is the ``LENGTH`` of the ``VECTOR`` and ``pointer`` is
the location of the start (the element selected by an ``NTH`` argument
of 1) of the ``VECTOR``.

“N word”

This class is the same as the previous one, except that the block
contains objects all of the same ``TYPE`` without individual ``TYPE``
words. The ``TYPE`` code for all the elements is in vector dope words,
which are at addresses just larger than the block itself. Thus, any
object that carries information in its ``TYPE`` word cannot go into the
block: ``PRIMTYPE``\ s ``STRING``, ``BYTES``, ``TUPLE`` (and the
corresponding locatives ``LOCS``, ``LOCB``, ``LOCA``), ``FRAME``, and
``LOCD``. All external ``TYPE``\ s in this class are of ``PRIMTYPE``
``UVECTOR``. Example:

::

    ---------------------------------
    |    UVECTOR    |       0       |
    | - - - - - - - - - - - - - - - |
    |    -length    |    pointer    |
    ---------------------------------

where ``length`` is the ``LENGTH`` of the ``UVECTOR`` and ``pointer``
points to the beginning of the ``UVECTOR``.

“Byte String” and “Character String”

These two classes are almost identical. Byte strings are byte pointers
to strings of arbitrary-size bytes. ``PRIMTYPE`` ``BYTES`` is the only
member of this class. Character strings are byte pointers to strings of
ASCII characters. ``PRIMTYPE`` ``STRING`` is the only member of this
class. Both of these classes consist of a length and a PDP-10 byte
pointer. In the case of character strings, the byte-size field in the
byte pointer is always seven bits per byte (hence five bytes per word).
Example:

::

    ---------------------------------
    |     STRING    |    length     |
    | - - - - - - - - - - - - - - - |
    |         byte-pointer          |
    ---------------------------------

where ``length`` is the ``LENGTH`` of the ``STRING`` (in bytes) and
``byte-pointer`` points to a byte just before the beginning of the
string (an ``ILDB`` instruction is needed to get the first byte). A
newly-created ``STRING`` always has ``*010700*`` in the left half of
``byte-pointer``. Unless the string was created by ``SPNAME``,
``byte-pointer`` points to a uvector, where the elements (characters) of
the ``STRING`` are stored, packed together five to a word.

“Frame”

This class gives the user program a handle on its control and
variable-reference structures. All external ``TYPE``\ s in this class
are of ``PRIMTYPE`` ``FRAME``. Three numbers are needed to designate a
frame: a unique 18-bit identifying number, a pointer to the frame’s
storage on a control stack, and a pointer to the ``PROCESS`` associated
with the frame. Example:

::

    ---------------------------------
    |     FRAME     |PROCESS-pointer|
    | - - - - - - - - - - - - - - - |
    |   unique-id   | frame-pointer |
    ---------------------------------

where ``PROCESS-pointer`` points to the dope words of a ``PROCESS``
vector, and ``unique-id`` is used for validating (testing ``LEGAL?``)
the ``frame-pointer``, which points to a frame for some Subroutine call
on the control stack.

“Tuple”

A tuple pointer is a counting pointer to a vector on the control stack.
It may be a pointer to the arguments to a Subroutine or a pointer
generated by the ``"TUPLE"`` declaration in a ``FUNCTION``. Like objects
in the previous class, these objects contain a unique identifying number
used for validation. ``PRIMTYPE`` ``TUPLE`` is the only member of this
class. Example:

::

    ---------------------------------
    |     TUPLE     |   unique-id   |
    | - - - - - - - - - - - - - - - |
    |   -2*length   |    pointer    |
    ---------------------------------

Other Storage Classes

The rest of the storage classes include strictly internal ``TYPE``\ s
and pointers to special kinds of lists and vectors like locatives,
``ATOM``\ s and ``ASOC``\ s. A pair for any ``LOCATIVE`` except a
``LOCD`` looks like a pair for the corresponding structure, except of
course that the ``TYPE`` is different. A ``LOCD`` pair looks like a
tuple pair and needs a word and a half for its value; the ``unique-id``
refers to a binding on the control stack or to the “global stack” if
zero. Thus ``LOCD``\ s are in a sense “stack objects” and are more
restricted than other locatives.

An ``OFFSET`` is stored with the ``INDEX`` in the right half of the
value word and the Pattern in the left half. Since the Pattern can be
either an ``ATOM`` or a ``FORM``, the left half actually points to a
pair, which points to the actual Pattern. The Patttern ``ANY`` is
recognized as a special case: the left-half pointer is zero, and no pair
is used. Thus, if you’re making the production version of your program
and want to save some storage, can do something like
``<SETG FOO <PUT-DECL ,FOO ANY>>`` for all ``OFFSET``\ s.

Basic Data Structures
---------------------

Lists

List elements are pairs linked together by the right halves of their
first words. The list is terminated by a zero in the right half of the
last pair. For example the ``LIST`` ``(1 2 3)`` would look like this:

::

    -------------
    | LIST | 0  |
    | - - - - - |   -----------     -----------     -----------
    |  0   | ------>| FIX | ------->| FIX | ------->| FIX | 0 |
    -------------   | - - - - |     | - - - - |     | - - - - |
                    |    1    |     |    2    |     |    3    |
                    -----------     -----------     -----------

The use of pointers to tie together elements explains why new elements
can be added easily to a list, how sharing and circularity work, etc.
The links go in only one direction through the list, which is why a list
cannot be ``BACK``\ ed or ``TOP``\ ped: there’s no way to find the
``REST``\ ed elements.

Since some MDL values require a word and a half for the value in the
pair, they do not fit directly into list elements. This problem is
solved by having “deferred pointers”. Instead of putting the datum
directly into the list element, a pointer to another pair is used as the
value with the special internal ``TYPE`` ``DEFER``, and the real datum
is put in the deferred pair. For example the ``LIST`` ``(1 "hello" 3)``
would look like this:

::

    -------------
    | LIST | 0  |
    | - - - - - |   -----------     -----------     -----------
    |  0   | ------>| FIX | ------->|DEFER| ------->| FIX | 0 |
    -------------   | - - - - |     | - - - - |     | - - - - |
                    |    1    |     |       -----   |    3    |
                    -----------     ----------- |   -----------
                                                |
                                    ----------- |
                                    |STRING| 5|<-
                                    | - - - - |
                                    |byte-pntr|
                                    -----------

Vectors

A vector is a block of contiguous words. More than one pair can point to
the block, possibly at different places in the block; this is how
sharing occurs among vectors. Pointers that are different arise from
``REST`` or ``GROW``/``BACK`` operations. The block is followed by two
“dope words”, at addresses just larger than the largest address in the
block. Dope words have the following format:

::

    /                               /
    |                               |
    |                               |
    ---------------------------------
    |      type     |      grow     |
    | - - - - - - - - - - - - - - - |
    |     length    |       gc      |
    ---------------------------------

The various fields have the following meanings:

``type`` – The fourth bit from the left (the “vector bit”, ``40000``
octal) is always one, to distinguish these vector dope words from a
``TYPE``/value pair.

If the high-order bit is zero, then the vector is a ``UVECTOR``, and the
remaining bits specify the uniform ``TYPE`` of the elements. ``CHUTYPE``
just puts a new ``TYPE`` code in this field. Each element is limited to
a one-word value: clearly ``PRIMTYPE`` ``STRING``\ s and ``BYTES``\ es
and stack objects can’t go in uniform vectors.

If the high-order bit is one and the ``TYPE`` bits are zero, then this
is a regular ``VECTOR``.

If the high-order bit is one and the ``TYPE`` bits are not all zero,
then this is either an ``ATOM``, a ``PROCESS``, an ``ASOC``, or a
``TEMPLATE``. The special internal format of these objects will be
described a little later in this appendix.

``length`` – The high-order bit is the mark bit, used by the garbage
collector. The rest of this field specifies the number of words in the
block, including the dope words. This differs from the length given in
pairs pointing to this vector, since such pairs may be the result of
``REST`` operations.

``grow`` – This is actually two nine-bit fields, specifying either
growth or shrinkage at both the high and low ends of the vector. The
fields are usually set only when a stack must be grown or shrunk.

``gc`` – This is used by the garbage collector to specify where this
vector is moving during compaction.

Examples (numbers in octal): the ``VECTOR`` ``[1 "bye" 3]`` looks like:

::

    ---------------
    | VECTOR |  0 |
    | - - - - - - |         -----------------
    |   -6   |  ----------->|  FIX  |       |
    ---------------         | - - - - - - - |
                            |       1       |
                            -----------------
                            | STRING |  3   |
                            | - - - - - - - |
                            |  byte pointer |
                            -----------------
                            |  FIX  |       |
                            | - - - - - - - |
                            |       3       |
                            -----------------
                            | 440000 |  0   |
                            | - - - - - - - |
                            |   10   |      |
                            -----------------

The ``UVECTOR`` ``![-1 7 -4!]`` looks like:

::

    ---------------
    | UVECTOR | 0 |
    | - - - - - - |         -----------------
    |   -3    | ----------->|       -1      |
    ---------------         -----------------
                            |        7      |
                            -----------------
                            |       -4      |
                            -----------------
                            | 40000+FIX | 0 |
                            | - - - - - - - |
                            |   5       |   |
                            -----------------

Atoms

Internally, atoms are special vector-like objects. An atom contains a
value cell (the first two words of the block, filled in whenever the
global or local value of the ``ATOM`` is referenced and is not already
there), an ``OBLIST`` pointer, and a print name (``PNAME``), in the
following format:

::

    ---------------------------------
    |      type     |     bindid    |
    ---------------------------------
    |       pointer-to-value        |
    ---------------------------------
    |       pointer-to-oblist       |
    ---------------------------------
    |           print-name          |
    /                               /
    /                               /
    |(ASCII with NUL padding on end)|
    ---------------------------------
    |      ATOM     |   valid-type  |
    | - - - - - - - - - - - - - - - |
    |     length    |       gc      |
    ---------------------------------

If the type field corresponds to ``TYPE`` ``UNBOUND``, then the ``ATOM``
is locally and globally unbound. (This is different from a pair, where
the same ``TYPE`` ``UNBOUND`` is used to mean unassigned.) If it
corresponds to ``TYPE`` ``LOCI`` (an internal ``TYPE``), then the value
cell points either to the global stack, if ``bindid`` is zero, or to a
local control stack, if ``bindid`` is non-zero. The ``bindid`` field is
used to verify whether the local value pointed to by the value cell is
valid in the current environment. The ``pointer-to-OBLIST`` is either a
counting pointer to an oblist (uvector). a positive offset into the
“transfer vector” (for pure ``ATOM``\ s), or zero, meaning that this
``ATOM`` is not on an ``OBLIST``. The ``valid-type`` field tells whether
or not the ``ATOM`` represents a ``TYPE`` and if so the code for that
``TYPE``: ``grow`` values are never needed for atoms.

Associations

Associations are also special vector-like objects. The first six words
of the block contain ``TYPE``/value pairs for the ``ITEM``,
``INDICATOR`` and ``AVALUE`` of the ``ASOC``. The next word contains
forward and backward pointers in the chain for that bucket of the
association hash table. The last word contains forward and backward
pointers in the chain of all the associations.

::

    ---------------------------------
    |             ITEM              |
    | - - - - - - - - - - - - - - - |
    |             pair              |
    ---------------------------------
    |          INDICATOR            |
    | - - - - - - - - - - - - - - - |
    |             pair              |
    ---------------------------------
    |            AVALUE             |
    | - - - - - - - - - - - - - - - |
    |             pair              |
    ---------------------------------
    |     bucket-chain-pointers     |
    ---------------------------------
    |  association-chain-pointers   |
    ---------------------------------
    |      ASOC     |       0       |
    | - - - - - - - - - - - - - - - |
    |    12 octal   |       gc      |
    ---------------------------------

``PROCESS``\ es

A ``PROCESS`` vector looks exactly like a vector of ``TYPE``/value
pairs. It is different only in that the garbage collector treats it
differently from a normal vector, and it contains extremely volatile
information when the ``PROCESS`` is ``RUNNING``.

Templates

In a template, the number in the type field (left half or first dope
word) identifies to which “storage allocation class” this ``TEMPLATE``
belongs, and it is used to find PDP-10 instructions in internal tables
(frozen uvectors) for performing ``LENGTH``, ``NTH``, and ``PUT``
operations on any object of this ``TYPE``. The programs to build these
tables are not part of the interpreter, but the interpreter does know
how to use them properly. The compiler can put these instructions
directly in compiled programs if a ``TEMPLATE`` is never ``REST``\ ed;
otherwise it must let the interpreter discover the appropriate
instruction. The value word of a template pair contains, not a counting
pointer, but the number of elements that have been ``REST``\ ed off in
the left half and a pointer to the first dope word in the right half.

The Control Stack
-----------------

Accumulators with symbolic names ``AB``, ``TB``, and ``TP`` are all
pointers into the ``RUNNING`` ``PROCESS``\ ’s control stack. ``AB``
(“argument base”) is a pointer to the arguments to the Subroutine now
being run. It is set up by the Subroutine-call mediator, and its old
value is always restored after a mediated Subroutine call returns.
``TB`` (“temporaries base”) points to the frame for the running
Subroutine and also serves as a stack base pointer. The ``TB`` pointer
is really all that is necessary to return from a Subroutine – given a
value to return, for example by ``ERRET`` – since the frame specifies
the entire state of the calling routine. ``TP`` (“temporaries pointer”)
is the actual stack pointer and always points to the current top of the
control stack.

While we’re on the subject of accumulators, we might as well be
complete. Each accumulator contains the value word of a pair, the
corresponding ``TYPE`` words residing in the ``RUNNING`` ``PROCESS``
vector. When a ``PROCESS`` is not ``RUNNING`` (or when the garbage
collector is running), the accumulator contents are stored in the
vector, so that the Objects they point to look like elements of the
``PROCESS`` and thus are not garbage-collectible.

Accumulators ``A``, ``B``, ``C``, ``D``, ``E`` and ``O`` are used almost
entirely as scratch accumulators, and they are not saved or restored
across Subroutine calls. Of course the interrupt machinery always saves
these and all other accumulators. ``A`` and ``B`` are used to return a
pair as the value of a Subroutine call. Other than that special feature,
they are just like the other scratch accumulators.

``M`` and ``R`` are used in running ``RSUBR``\ s. ``M`` is always set up
to point to the start of the ``RSUBR``\ ’s code, which is actually just
a uniform vector of instructions. All jumps and other references to the
code use ``M`` as an index register. This makes the code
location-insensitive, which is necessary because the code uvector will
move around. ``R`` is set up to point to the vector of objects needed by
the ``RSUBR``. This accumulator is necessary because objects in
garbage-collected space can move around, but the pointers to them in the
reference vector are always at the same place relative to its beginning.

``FRM`` is the internal frame pointer, used in compiled code to keep
track of pending Subroutine calls when the control stack is heavily
used. ``P`` is the internal-stack pointer, used primarily for internal
calls in the interpreter.

One of the nicest features of the MDL environment is the uniformity of
the calling and returning sequence. All Subroutines – both built-in
F/SUBRs and compiled ``RSUBR(-ENTRY)``\ s – are called in exactly the
same way and return the same way. Arguments are always passed on the
control stack and results always end up in the same accumulators. For
efficiency reasons, a lot of internal calls within the interpreter
circumvent the calling sequence. However, all calls made by the
interpreter when running user programs go through the standard calling
sequence.

A Subroutine call is initiated by one of three UUOs (PDP-10 instructions
executed by software rather than hardware). ``MCALL`` (“MDL call”) is
used when the number of arguments is known at assemble or compile time,
and this number is less than 16. ``QCALL`` (“quick call”) may be used
if, in addition, an ``RSUBR(-ENTRY)`` is being called that can be called
“quickly” by virtue of its having special information in its reference
vector. ``ACALL`` (“accumulator call”) is used otherwise. The general
method of calling a Subroutine is to ``PUSH`` (a PDP-10 instruction)
pairs representing the arguments onto the control stack via ``TP`` and
then either (1) ``MCALL`` or ``QCALL`` or (2) put the number of
arguments into an accumulator and ``ACALL``. Upon return the object
returned by the Subroutine will be in accumulators ``A`` and ``B``, and
the arguments will have been ``POP``\ ped off the control stack.

The call mediator stores the contents of ``P`` and ``TP`` and the
address of the calling instruction in the current frame (pointed to by
``TB``). It also stores MDL’s “binding pointer” to the topmost binding
in the control stack. (The bindings are linked together through the
control stack so that searching through them is more efficient than
looking at every object on the stack.) This frame now specifies the
entire state of the caller when the call occurred. The mediator then
builds a new frame on the control stack and stores a pointer back to the
caller’s frame (the current contents of ``TB``), a pointer to the
Subroutine being called, and the new contents of ``AB``, which is a
counting pointer to the arguments and is computed from the information
in the ``MCALL`` or ``QCALL`` instruction or the ``ACALL`` accumulator.
``TB`` is then set up to point to the new frame, and its left half is
incremented by one, making a new ``unique-id``. The mediator then
transfers control to the Subroutine.

A control stack frame has seven words as shown:

::

    ---------------------------------
    |     ENTRY     |  called-addr  |
    ---------------------------------
    |   unique-id   |  prev frame   |
    ---------------------------------
    |       argument pointer        |
    ---------------------------------
    |    saved binding pointer      |
    ---------------------------------
    |           saved P             |
    ---------------------------------
    |           saved TP            |
    ---------------------------------
    |    saved calling address      |
    ---------------------------------

The first three words are set up during the call to the Subroutine. The
rest are filled in when this routine calls another Subroutine. The left
half of ``TB`` is incremented every time a Subroutine call occurs and is
used as the ``unique-id`` for the frame, stored in frame and tuple pairs
as mentioned before. Obviously this ``id`` is not strictly unique, since
each 256K calls it wraps around to zero. The right half of ``TB`` is
always left pointing one word past the saved-calling-address word in the
frame. ``TP`` is also left pointing at that word, since that is the top
of the control stack at Subroutine entry. The arguments to the called
Subroutine are below the frame on the control stack (at lower storage
addresses), and the temporaries for the called Subroutine are above the
frame (at higher storage addresses). These arguments and temporaries are
just pairs stored on the control stack while needed: they are all that
remain of ``UNSPECIAL`` values in compiled programs.

The following figure shows what the control stack might look like after
several Subroutine calls.

::

    /               /
    |               |
    -----------------
    |               |
    |  args for S1  |
    |               |
    -----------------
    | frame for S1  |
    ----------------- <--
    |               |   |
    | temps for S1  |   |
    |               |   |
    -----------------   |
    |               |   |
    |  args for S2  |   |
    |               |   |
    -----------------   |
    | frame for S2  | ---
    ----------------- <------
    |               |       |
    | temps for S2  |       |
    |               |       |
    -----------------       |
    |  args for S3  |       |
    -----------------       |
    | frame for S3  | -------
    -----------------
    |               |
    | temps for S3  |
    |               |
    |               |
    -----------------
          (top)

The above figure shows the frames all linked together through the
control stack (the “execution path”), so that it is easy to return to
the caller of a given Subroutine (``ERRET`` or ``RETRY``).

Subroutine exit is accomplished simply by the call mediator, which loads
the right half of ``TB`` from the previous frame pointer, restores the
“binding pointer”, ``P``, and ``TP``, and transfers control back to the
instruction following the saved calling address.

Variable Bindings
-----------------

All local ``ATOM`` values are kept on the control stack of the
``PROCESS`` to which they are local. As described before, the atom
contains a word that points to the value on the control stack. The
pointer is actually to a six-word “binding block” on the control stack.
Binding blocks have the following format:

::

    ---------------------------------
    | BIND or UBIND |      prev     |
    ---------------------------------
    |        pointer to ATOM        |
    ---------------------------------
    |             value             |
    | - - - - - - - - - - - - - - - |
    |             pair              |
    ---------------------------------
    |     decl      |   unique-id   |
    ---------------------------------
    |       previous-binding        |
    ---------------------------------

where:

-  ``BIND`` means this is a binding for a ``SPECIAL`` ``ATOM`` (the only
   kind used by compiled programs), and ``UBIND`` means this is a
   binding for an ``UNSPECIAL`` ``ATOM`` – for ``SPECIAL`` checking by
   the interpreter;
-  ``prev`` points to the closest previous binding block for any
   ``ATOM`` (the “access path” – ``UNWIND`` objects are also linked in
   this chain);
-  ``decl`` points to a ``DECL`` associated with this value, for
   ``SET(LOC)`` to check;
-  ``unique-id`` is used for validation of this block; and
-  ``previous-binding`` points to the closest previous binding for this
   ``ATOM`` (used in unbinding).

Bindings are generated by an internal subroutine called ``SPECBIND``
(name comes from ``SPECIAL``). The caller to ``SPECBIND`` ``PUSH``\ es
consecutive six-word blocks onto the control stack via ``TP`` before
calling ``SPECBIND``. The first word of each block contains the ``TYPE``
code for ``ATOM`` in its left half and all ones in its right half.
``SPECBIND`` uses this bit pattern to identify the binding blocks.
``SPECBIND``\ ’s caller also fills in the next three words and leaves
the last two words empty. ``SPECBIND`` fills in the rest and leaves the
“binding pointer” pointing at the topmost binding on the control stack.
``SPECBIND`` also stores a pointer to the current binding in the value
cell of the atom.

Unbinding is accomplished during Subroutine return. When the previous
frame is being restored, the call mediator checks to see if the saved
“binding pointer” and the current one are different; if they are,
``SPECSTORE`` is called. ``SPECSTORE`` runs through the binding blocks,
restoring old value pointers in atoms until the “binding pointer” is
equal to the one saved in the frame.

Obviously variable binding is more complicated than this, because
``ATOM``\ s can have both local and global values and even different
local values in different ``PROCESS``\ es. The solution to all of these
additional problems lies in the ``bindid`` field of the atom. Each
``PROCESS`` vector also contains a current ``bindid``. Whenever an
ATOM’s local value is desired, the ``RUNNING`` ``PROCESS``\ ’s
``bindid`` is checked against that of the atom: if they are the same,
the atom points to the current value; if not, the current
``PROCESS``\ ’s control stack must be searched to find a binding block
for this ``ATOM``. This binding scheme might be called “shallow
binding”. The searching is facilitated by having all binding blocks
linked together. Accessing global variables is accomplished in a similar
way, using a ``VECTOR`` that is referred to as the “global stack”. The
global stack has only an ``ATOM`` and a value slot for each variable,
since global values never get rebound.

``EVAL`` with respect to a different environment causes some additional
problems. Whenever this kind of ``EVAL`` is done, a brand new ``bindid``
is generated, forcing all current local value cells of atoms to appear
invalid. Local values must now be obtained by searching the control
stack, which is inefficient compared to just pulling them out of the
atoms. (The greatest inefficiency occurs when an ``ATOM``\ ’s ``LVAL``
is never accessed twice in a row in the same environment.) A special
block is built on the control stack and linked into the binding-block
chain. This block is called a “skip block” or “environment splice”, and
it diverts the “access path” to the new environment, causing searches to
become relative to this new environment.
