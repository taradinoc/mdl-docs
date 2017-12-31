# Appendix 2. Predefined Subroutines

The following is a very brief description of all the primitives 
(F/SUBRs) currently available in MDL. These descriptions are in no 
way to be considered a definition of the effects or values produced 
by the primitives. They just try to be as complete and as accurate as 
is possible in a single-statement description. However, because of 
the complexity of most primitives, many important assumptions and 
restrictions have been omitted. Even though all primitives return a 
value, some descriptions mention only the side effects produced by a 
primitive, because these primitives are most often used for this 
effect rather than the value.

A description is given in this format:

*name* (*arguments*)  
*decl*  
English description

This format is intended to look like a `FUNCTION` definition, 
omitting the call to `DEFINE` and all internal variable and code. The 
*name* is just the ATOM that is used to refer to the primitive. The 
names of the *arguments* are intended to be mnemonic or suggestive of 
their meanings. The *decl* is a `FUNCTION`-style `DECL` (chapter 14) 
for the primitive. In some cases the `DECL` may look unusual, because 
it is intended to convey information to a person about the uses of 
arguments, not to convey information to the MDL interpreter or 
compiler. For example, `<OR FALSE ANY>` is functionally equivalent to 
`ANY`, but it indicates that only the "truth" of the argument is 
significant. Indeed, the `[OPT ...]` construction is often used 
illegally, with other elements following it: be warned that MDL would 
not accept it. An argument is included in the same `LIST` with 
`VALUE` (the value of the primitive) only if the argument is actually 
returned by the primitive as a value. In other words, `#DECL ((VALUE 
ARG) ...)` implies `<==? .VALUE .ARG>`.

```
* ("TUPLE" FACTORS)
 #DECL ((VALUE <OR FIX FLOAT>
           (FACTORS) <TUPLE [REST <OR FIX FLOAT>]>)
```
multiplies all arguments together (arithmetic)

```
+ ("TUPLE" TERMS)
 #DECL ((VALUE) <OR FIX FLOAT>
        (TERMS <TUPLE [REST <OR FIX FLOAT>]>)
```
adds all arguments together (arithmetic)

```
- ("OPTIONAL" MINUEEND "TUPLE" SUBTRAHENDS)
 #DECL ((VALUE <OR FIX FLOAT>
       (MINUEND ) <OR FIX FLOAT>
       (SUBTRAHENDS) <TUPLE [REST <OR FIX FLOAT>]>)
```
subtracts other arguments from the first (arithmetic)

```
/ ("OPTIONAL" DIVIDEND "TUPLE" DIVISORS)
 #DECL ((VALUE) <OR FIX FLOAT>
       (DIVIDEND) <OR FIX FLOAT>
       (DIVISORS) <TUPLE [REST <OR FIX FLOAT>]>)
```
divides first argument by other arguments (arithmetic)

```
0? (NUMBER)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (NUMBER) <OR FIX FLOAT>)
```
tells whether a number is zero (predicate)

```
1? (NUMBER)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (NUMBER <OR FIX FLOAT>)
```
tells whether a number is one (predicate)

```
1STEP (PROCESS)
 #DECL ((VALUE PROCESS) PROCESS)
```
causes a `PROCESS` to enter single-step mode

```
==? (OBJECT-1 OBJECT-2)
 #DECL ((VALUE <OR 'T '#FALSE ()>
        (OBJECT-1 OBJECT-2) ANY)
```
tells whether two objects are "exactly" equal (predicate)

```
=? (OBJECT-1 OBJECT-2)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (OBJECT-1 OBJECT-2) ANY)
```
tells whether two objects are "structurally" equal (predicate)

```
ABS (NUMBER)
 #DECL ((VALUE <OR FIX FLOAT>
        (NUMBER <OR FIX FLOAT>)
```
returns absolute value of a number (arithmetic)

```
ACCESS (CHANNEL ACCESS-POINTER)
 #DECL ((VALUE CHANNEL) CHANNEL
        (ACCESS-POINTER) FIX)
```
sets access pointer for the next I/O transfer via a `CHANNEL`

```
ACTIVATE-CHARS ("OPTIONAL" STRING)
 #DECL ((VALUE STRING) STRING)
```
sets or returns interrupt characters for terminal Typing (Tenex and 
Tops-20 versions only)

```
AGAIN ("OPTIONAL" (ACTIVATION .LPROG\ !-INTERRUPTS))
 #DECL ((VALUE ANY
        (ACTIVATION) ACTIVATION)
```
resumes execution at the given `ACTIVATION`

```
ALLTYPES ()
 #DECL ((VALUE) <VECTOR [REST ATOM]>)
```
returns the `VECTOR` of all type names

```
AND ("ARGS" ARGS)
 #DECL ((VALUE) <OR FALSE ANY>
        (ARGS) LIST)
```
computes logical "and" of truth-values, evaluated by the Subroutine

```
AND? ("TUPLE" TUPLE)
 #DECL ((VALUE <OR FALSE ANY>
        (TUPLE) TUPLE)
```
computes logical "and" of truth-values, evaluated at call time

```
ANDB ("TUPLE" WORDS)
 #DECL ((VALUE) WORD
        (WORDS <TUPLE [REST <PRIMTYPE WORD>]>)
```
computers bitwise "and" of machine words

```
APPLICABLE? (OBJECT)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (OBJECT ANY)
```
tells whether argument is applicable (predicate)

```
APPLY (APPLICABLE "TUPLE") ARGUMENTS
 $DECL ((VALUE) ANY
        (APPLICABLE) APPLICABLE (ARGUMENTS) TUPLE)
```
applies first argument to the other arguments

```
APPLYTYPE (TYPE "OPTIONAL" HOW)
 #DECL ((VALUE <OR ATOM APPLICABLE '#FALSE ()>
        (TYPE) ATOM (HOW) <OR ATOM APPLICABLE>)
```
specifies or returns how a data type is applied

```
ARGS (CALL)
 #DECL ((VALUE) TUPLE
        (CALL) <OR FRAME ENVIRONMENT ACTIVATION PROCESS>)
```
returns arguments of a given un-returned Subroutine call

```
ASCII (CODE-OR-CHARACTER)
 #DECL ((VALUE) <OR CHARACTER FIX>
        (CODE-OR-CHARACTER) <OR FIX CHARACTER>)
```
returns `CHARACTER` with given ASCII code or vice versa

```
ASSIGNED? (ATOM "OPTIONAL" ENV)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (ATOM) ATOM (ENV) <OR FRAME ENVIRONMENT ACTIVATION PROCESS>)
```
tells whether an ATOM has a local value (predicate)

```
ASSOCIATIONS ()
 #DECL ((VALUE) <OR ASOC '#FALSE ()>)
```
returns the first object in the association chain

```
AT (STRUCTURED "OPTIONAL" (N 1))
 #DECL ((VALUE) LOCATIVE
        (STRUCTURED) STRUCTURED (N) <OR FIX OFFSET>)
```
returns a locative to the Nth element of a structure

```
ATAN (NUMBER)
 #DECL ((VALUE) FLOAT
        (#NUMBER) <OR FIX FLOAT>
```
returns arc tangent of a number (arithmetic)

```
ATOM (PNAME)
 #DECL ((VALUE) ATOM
        (PNAME) STRING)
```
creates an `ATOM` with a given name

```
AVALUE (ASSOCIATION)
 #DECL ((VALUE) ANY
        (ASSOCIATION) ASSOC)
```
returns the "value" field of an association

```
BACK (STRUCTURE "OPTIONAL" N)
 #DECL ((VALUE) <OR VECTOR TUPLE UVECTOR STORAGE STRING BYTES TEMPLATE>
        (N) FIX
        (STRUCTURE) <OR <PRIMTYPE VECTOR>  <PRIMTYPE TUPLE>
                        <PRIMTYPE UVECTOR> <PRIMTYPE STORAGE>
                        <PRIMTYPE STRING>  <PRIMTYPE BYTES>
                        <PRIMTYPE TEMPLATE>>)
```
replaces some elements removed from a non-list structure by `REST`ing and changes to primitive data type

```
BIND ("ARGS" ARGS)
 #DECL ((VALUE) ANY
        (ARGS) <LIST [OPT ATOM] LIST [OPT DECL] ANY>)
```
executes sequential expressions without providing a bound `ACTIVATION`

```
BITS (WIDTH "OPTIONAL" (RIGHT-EDGE 0))
 #DECL ((VALUE) BITS
        (WIDTH RIGHT-EDGE) FIX)
```
creates a bit mask for `PUTBITS` and `GETBITS`

```
BLOAT ("OPTIONAL"
       (FREE 0) (STACK 0) (LOCALS 0) (GLOBALS 0) (TYPES 0) (STORAGE 0) (P-STACK 0)0
       MIN GROW-LOCAL GROW-GLOBAL GROW-TYPE GROW-STORAGE PURE P-STACK-SIZE STACK-SIZE)
 #DECL ((VALUE) FIX
        (FREE STACK LOCALS GLOBALS TYPES STORAGE P-STACK MIN GROW-LOCAL GROW-GLOBAL
         GROW-TYPE GROW-STORAGE PURE P-STACK SIZE STACK-SIZE) FIX)
```
allocates extra storage temporarily

```
BLOAT-STAT ("OPTIONAL" STATS)
 #DECL ((VALUE) <UVECTOR [27 FIX]>
        (STATS) <UVECTOR [27 ANY]>)

```
gives garbage-collector and storage statistics

```
BLOCK (LOOK-UP)
 #DECL ((VALUE LOOK-UP) <OR OBLIST <LIST [REST <OR OBLIST 'DEFAULT>]>>)
```
`SET`s `OBLIST` for looking up `ATOM`s during `READ`ing and `PARSE`ing

```
BOUND? (ATOM "OPTIONAL" ENV)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (ATOM) ATOM (ENV) <OR FRAME ENVIRONMENT ACTIVATION PROCESS>)
```
tells whether an `ATOM` is locally bound (predicate)

```
BREAK-SEQ (OBJECT PROCESS)
 #DECL ((VALUE PROCESS) PROCESS
        (OBJECT) ANY)
```
modifies execution of sequence of another `PROCESS`

```
BUFOUT ("OPTIONAL" (CHANNEL .OUTCHAN))
 #DECL ((VALUE CHANNEL) CHANNEL)
```
writes out all internal Muddle buffers for an output `CHANNEL`

```
BYTE-SIZE (BYTES)
 #DECL ((VALUE) FIX
        (BYTES) BYTES)
```
returns size of bytes in a byte string

```
BYTES (SIZE "TUPLE" ELEMENTS)
 #DECL ((VALUE) BYTES
        (SIZE) FIX (ELEMENTS) <TUPLE [REST FIX]>)
```
creates a byte-string from explicit arguments

```
CHANLIST ()
 #DECL ((VALUE) <LIST [REST CHANNEL]>)
```
returns a `LIST` of currently open I/O `CHANNEL`s

```
CHANNEL ("OPTIONAL" (MODE "READ") "TUPLE" FILE-NAME)
 #DECL (VALUE) CHANNEL
       (MODE) STRING (FILE-NAME) TUPLE)
```
creates an unopened I/O `CHANNEL`

```
CHTYPE (OBJECT TYPE)
 #DECL ((VALUE) ANY
        (OBJECT) ANY (TYPE) ATOM)
```
makes a new pair with a given data type from an old one

```
CHUTYPE (UVECTOR TYPE)
 #DECL ((VALUE UVECTOR) <PRIMTYPE UVECTOR>
        (TYPE) ATOM)
```
changes the data type of the elements to a uniform vector

```
CLOSE (CHANNEL)
 #DECL ((VALUE CHANNEL) CHANNEL)
```
closes an I/O `CHANNEL`

```
CLOSURE (FUNCTION "TUPLE" VARIABLES)
 #DECL ((VALUE) CLOSURE
        (FUNCTION) FUNCTION (VARIABLES) <TUPLE [REST ATOM]>)
```
"binds" the free variables of a `FUNCTION` to current values

```
COND ("ARGS" CLAUSES)
 #DECL ((VALUE) ANY
        (CLAUSES) <LIST <LIST <OR FALSE ANY>> [REST <LIST <OR FALSE ANY>>]>)
```
evaluates conditions and selected expression

```
CONS (NEW-ELEMENT LIST)
 #DECL ((VALUE) LIST
        (NEW-ELEMENT) ANY (LIST) (LIST)
```
add an element to the front of a `LIST`

```
COS (NUMBER)
 #DECL ((VALUE) FLOAT
        (NUMBER) <OR FIX FLOAT>)
```
prints a cosine of a number (arithmetic)

```
CRLF ("OPTIONAL" (CHANNEL .OUTCHAN))
 #DECL ((VALUE) 'T
        (CHANNEL) CHANNEL)
```
prints a carriage-return and line-feed via an open `CHANNEL`

```
DECL-CHECK ("OPTIONAL" SWITCH)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (SWITCH) <OR FALSE ANY>)
```
enables or disables type-declaration checking

```
DECL? (OBJECT PATTERN)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (OBJECT) ANY (PATTERN) <OR ATOM FORM>)
```
tells whether any object matches a type declaration (predicate)

```
DEFINE ('NAME "ARGS" ARGS)
 #DECL ((VALUE ATOM
        (NAME ) ANY (ARGS) <LIST [OPT ATOM] LIST [OPT DECL] ANY>)
```
sets the global value of an `ATOM` to a `FUNCTION`

```
DEFMAC ('NAME "ARGS" ARGS)
 #DECL ((VALUE) ATOM
        (NAME) ANY (ARGS) <LIST [OPT AROM] LIST [OPT DECL] ANY>)
```
sets the global value of an `ATOM` to a `MACRO`

```
DEMSIG (NAME)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (NAME) STRING)
```
signals an ITS daemon

```
DISABLE (INTERRUPT)
 #DECL ((VALUE INTERRUPT) HEADER)
```
disables an interrupt

```
DISMISS (VAL "OPTIONAL" ACTIVATION INT-LEVEL)
 #DECL ((VALUE VAL) ANY
        (ACTIVATION) ACTIVATION INT-LEVEL) FIX)
```
dismisses an interrupt sequence

```
ECHOPAIR (IN OUT)
 #DECL ((VALUE IN) CHANNEL
        (OUT) CHANNEL)
```
coordinate I/O `CHANNEL`s for echoing characters on rubout

```
EMPTY? (OBJECT)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (OBJECT) STRUCTURED)
```
tells whether a structure has zero elements (predicate)

```
ENABLE (INTERRUPT)
 #DECL ((VALUE INTERRUPT) IHEADER)
```
enables an interrupt

```
ENDBLOCK ()
 #DECL ((VALUE) <OR OBLIST <LIST [REST <OR OBLIST 'DEFAULT>]>>)
```
restores the .OBLIST that existed before the corresponding call to `BLOCK`

```
ENTRY-LOC (ENTRY)
 #DECL ((VALUE) FIX
        (ENTRY) RSUBR-ENTRY)
```
returns the offset in the code vector of an RSUBR-ENTRY

```
EQVB ("TUPLE" WORDS)
 #DECL ((VALUE) WORD
        (WORDS) <TYPLE [REST <PRIMTYPE WORD>]>)
```
computes bitwise "equivalence" of machine words

```
ERRET ("OPTIONAL" VAL (FRAME .LERR\ !-INTERRUPTS))
 #DECL ((VALUE) ANY
        (VALUE ANY (FRAME) FRAME)
```
continues evaluation from the last `ERROR` or `LISTEN` or from a given `FRAME`

```
ERROR ("TUPLE" INFO)
 #DECL ((VALUE) ANY
        (INFO) TUPLE
```
stops and informs users of an error

```
ERRORS ()
 #DECL ((VALUE) OBLIST)
```
returns the `OBLIST` where error messages are located

```
EVAL (ANY "OPTIONAL" ENV)
 #DECL ((VALUE) ANY
        (ENV <OR FRAME ENVIRONMENT ACTIVATION PROCESS>)
```
evaluates an expression in a given environment

```
EVALTYPE (TYPE "OPTIONAL" HOW)
 #DECL ((VALUE) <OR ATOM APPLICABLE '#FALSE ()>
        (TYPE ATOM (HOW) <OR ATOM APPLICABLE>)
```
specifies or returns how a data type is evaluated

```
EVENT (NAME "OPTIONAL" PRIORITY WHICH)
 #DECL ((VALUE) IHEADER
        (NAME) <OR STRING ATOM IHEADER> (PRIORITY) FIX (WHICH) <OR CHANNEL LOCATIVE>
```
sets up an interrupt

```
EXP (NUMBER)
 #DECL ((VALUE) FLOAT
        (NUMBER) <OR FIX FLOAT>)
```
returns "e" to the power of a number (arithmetic)

```
EXPAND (ANY)
 #DECL ((VALUE) ANY
        (ANY) ANY)
```
evaluates its argument (only once if a `MACRO` is involved) in the top-level environment

```
FILE-EXISTS? ("TUPLE" FILE-NAME)
 #DECL ((VALUE) <OR 'T <FALSE STRING FIX>>
        (FILE-NAME) TUPLE)
```
tests for existence of a file (predicate)

```
FILE-LENGTH (INCH)
 #DECL ((VALUE) FIX
        (INCH) CHANNEL)
```
returns the system-provided length of a file open on an input `CHANNEL`

```
FILECOPY ("OPTIONAL" (INCH .INCHAN) (OUCH .OUTCHAN))
 #DECL ((VALUE) FIX
        (INCH OUCH) CHANNEL)
```
copies characters from one `CHANNEL` to another until end-of-file on the input `CHANNEL`

```
FIX (NUMBER)
 #DECL ((VALUE) FIX
        (NUMBER) <OR FLOAT FIX>
```
returns integer part of a number (arithmetic)

```
FLATSIZE (ANY MAX "OPTIONAL" (RADIX 10))
 #DECL ((VALUE) <OR FIX '#FALSE ()>
        (ANY) ANY (MAX RADIX) FIX)
```
returns number of characters needed to PRIN1 an object, if not greate than given maximum.

```
FLOAD ("TUPLE" FILE-NAME-AND-LOOK-UP)
 #DECL ((VALUE) '"DONE"
        (FILE-NAME-AND-LOOK-UP) TUPLE)
```
reads and evaluates all object in a file

```
FLOAT (NUMBER)
 #DECL ((VALUE) FLOAT
        (NUMBER) <OR FIX FLOAT>)
```
returns floating-point value of a number (arithmetic)

```
FORM ("TUPLE" ELEMENTS)
 #DECL ((VALUE) FORM
        (ELEMENTS) TUPLE
```
creates a `FORM` from explicit arguments

```
FRAME ("OPTIONAL" (FRAME .LERR\ !-INTERRUPTS))
 #DECL ((VALUE) FRAME
        (FRAME) <OR FRAME ENVIRONMENT ACTIVATION PROCESS>)
```
returns a previous Subroutine call

```
FREE-RUN (PROCESS)
 #DECL ((VALUE) <OR PROCESS '#FALSE ()>
        (PROCESS) PROCESS)
```
causes a `PROCESS` to leave single-step mode

```
FREEZE (STRUCTURE)
 #DECLINE ((VALUE) <OR VECTOR UVECTOR STRING BYTES>
           (STRUCTURE) <OR <PRIMTYPE VECTOR> <PRIMTYPE TUPLE> <PRIMTYPE UVECTOR>
                           <PRIMTYPE STRING> <PRIMTYPE BYTES>>)
```
makes a copy of an arugment in non-moving garbage-collected space

```
FUNCT (FRAME)
 #DECL ((VALUE) ATOM
        (FRAME) <OR FRAME ENVIRONMENT ACTIVATION PROCESS>)
```
returns Subroutine name of a given previous Subroutine call

```
FUNCTION ("ARGS" ARGS)
 #DECL ((VALUE) FUNCTION
        (ARGS) <LIST [OPT ATOM] LIST [OPT DECL] ANY>)
```
creates a `FUNCTION`

```
G=? (NUMBER-1 NUMBER-2)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (NUMBER-1 NUMBER-2) <OR FIX FLOAT>)
```
tells whether first argument is greater than or equal to the second (predicate)

```
G? (NUMBER-1 NUMBER-2)
 #DECL ((VALUE) <OR 'T' '#FALSE ()>
        (NUMBER-1 NUMBER-2) <OR FIX FLOAT>)
```
tells whether first argument is greater than the second (predicate)

```
GASSIGNED? (ATOM)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (ATOM) ATOM)
```
tells whether an `ATOM` has a global value (predicate)

```
GBOUND? (ATOM
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (ATOM) ATOM)
```
tells whether an `ATOM` has a global value (predicate)

```
GC ("OPTIONAL" MIN (EXHAUSTIVE? <>) MS-FREQ)
 #DECL ((VALUE) FIX
        (MIN MS-FREQ) FIX (EXHAUSTIVE?) <OR FALSE ANY>)
```
causes a garbage collection and changes garbage-collection parameters

```
GC-DUMP (ANY PRINTB)
 #DECL ((VALUE) <OR ANY <UVECTOR <PRIMTYPE WORD>>>
        (ANY) ANY (PRINTB) <OR CHANNEL FALSE>)
```
dumps an object so that it can be reproduced exactly

```
GC-MON ("OPTIONAL" SWITCH)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (SWITCH) <OR FALSE ANY>)
```
turns garbage-collection monitoring off or on

```
GC-READ (READB "OPTIONAL" (EOF-ROUTINE '<ERROR ...>))
 #DECL ((VALUE) ANY
        (READB) CHANNEL (EOF-ROUTINE) ANY)
```
inputs an object that was previously `GC-DUMP`ed

```
GDECL ("ARGS" ARGS)
 #DECL ((VALUE) ANY
        (ARGS <LIST [REST <LIST [REST ATOM]> <OR ATOM FORM>]>)
```
declates the type/structure of the global value of `ATOM`s

```
GET (ITEM INDICATOR "OPTIONAL" (IF-NONE <>))
 #DECL ((VALUE) ANY
        (ITEM <OR STRUCTURED ANY> (INDICATOR) <OR FIX OFFSET ANY> (IF-NONE) ANY)
```
does `NTH` or `GETPROP`

```
GET-DECL (ATOM-OR-OFFSET)
 #DECL ((VALUE) <OR ATOM FORM '#FALSE ()>
        (ATOM-OR-OFFSET) <OR LOCD OFFSET>)
```
gets the type declaration for an `ATOM`'s value or an `OFFSET`

```
GETBITS (FROM FIELD)
 #DECL ((VALUE) WORD
        (FROM ) <OR <PRIMTYPE WORD> <PRIMTYPE STORAGE>> (FIELD) BITS)
```
returns a bit field of a machine word or `STORAGE` address

```
GETL (ITEM INDICATOR "OPTIONAL" (IF-NONE <>))
 #DECL ((VALUE <OR LOCATIVE LOCAS ANY>
        (ITEM) <OR STRUCTURED ANY> (INDICATOR) <OR FIX OFFSET ANY> (IF-NONE) ANY)
```
does `AT` or `GETPL`

```
GETPL (ITEM INDICATOR "OPTIONAL" (IF-NONE <>))
 #DECL ((VALUE) <OR LOCAS ANY>
        (ITEM INDICATOR IF-NONE) ANY)
```
returns a locative to an association

```
GETPROP (ITEM INDICATOR "OPTIONAL" (IF-NONE <>))
 #DECL ((VALUE) ANY
        (ITEM INDICATOR IF-NONE) ANY)
```
returns the value associated with an item under an indicator

```
GLOC (ATOM "OPTIONAL" (MAKE-SLOT <>))
 #DECL ((VALUE) LOCD)
        (ATOM) ATOM (MAKE-SLOT) <OR FALSE ANY>)
```
returns a locative to thje global-value cell of an `ATOM`

```
GO (LABEL)
 #DECL ((VALUE) ANY
        (LABEL) <OR ATOM TAG>)
```
goes to a label and continues evaluation from there

```
GROW (U/VECTOR END BEG)
 #DECL ((VALUE)    <OR <PRIMTYPE VECTOR> <PRIMTYPE UVECTOR>
        (U/VECTOR) <OR <PRIMTYPE VECTOR> <PRIMTYPE UVECTOR>> (END BEG) FIX)
```
increases the size of a vector or uniform vector

```
GUNASSIGN (ATOM)
 #DECL ((VALUE ATOM) ATOM)
```
causes an ATOM to have no global value

```
GVAL (ATOM)
 #DECL ((VALUE) ANY
        (ATOM) ATOM)
```
returns the global value of an `ATOM`

```
HANDLER (IHEADER HANDLER "OPTIONAL" (PROCESS #PROCESS 0))
 #DECL ((VALUE) HANDLER
        (IHEADER) IHEADER (HANDLER) <OR HANDLER APPLICABLE> (PROCESS) PROCESS)
```
creates an interrupter `HANDLER`

```
HANG ("OPTIONAL" (UNHANG <>))
 #DECL ((VALUE) ANY
        (UNHANG) ANY)
```
Does nothing, interruptibly, potentially forever

```
IBYTES (SIZE LENGTH "OPTIONAL" (ELEMENT 0))
 #DECL ((VALUE) BYTES
        (SIZE LENGTH) FIX (ELEMENT) ANY)
```
creates a byte-sized string from implicit arguments

```
IFORM (LENGTH "OPTIONAL" (ELEMENT #LOSE 0))
 #DECL ((VALUE FORM
        (LENGTH FIX ELEMENT) ANY)
```
creates a `FORM` from implicit arguments

```
ILIST (LENGTH "OPTIONAL" (ELEMENT #LOSE 0))
 #DECL ((VALUE) LIST
        (LENGTH) DIX (ELEMENT) ANY)
```
creates a `LIST` from implicit arguments

```
IMAGE (CODE "OPTIONAL" (CHANNEL .OUTCHAN))
 #DECL ((VALUE CODE) FIX
        (CHANNEL) CHANNEL)
```
sends an image-mode characters via an output `CHANNEL`

```
IN (POINTER)
 #DECL ((VALUE) ANY
        (POINTER) LOCATIVE)
```
returns the object pointed to by a locative

```
INDEX (OFFSET)
 #DECL ((VALUE) FIX
        (OFFSET) OFFSET)
```
fetches the integral part of an `OFFSET`

```
INDICATOR (ASSOCIATION)
 #DECL ((VALUE) ANY
        (ASSOCIATION) ASSOC)
```
returns the "indicator" field of an association

```
INSERT (PNAME OBLIST)
 #DECL ((VALUE) ATOM
        (PNAME <OR ATOM STRING> (OBLIST) OBLIST)
```
adds an `ATOM` to an `OBLIST`

```
INT-LEVEL ("OPTIONAL" NEW-INT-LEVEL)
 #DECL ((VALUE) FIX
        (NEW-INT-LEVEL) FIX)
```
returns or sets current interrupt level

```
INTERRUPT (NAME "TUPLE" HANDLER-ARGS)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (NAME <OR STRING ATOM IHEADER> (HANDLER-ARGS) TUPLE)
```
causes an interrupt to occur

```
INTERRUPTS ()
 #DECL ((VALUE) OBLIST)
```
returns an `OBLIST` on which interrupt names are kept

```
IPC-HANDLER (BODY TYPE OTHER-NAME-1 OTHER-NAME-2
             "OPTIONAL" (MY-NAME-1 <UNAME>) (MY-NAME-2 <JNAME>))
 #DECL ((VALUE) 'T
        (BODY) <OR STRING VECTOR> (TYPE) FIX
        (OTHER-NAME-1 OTHER-NAME-2 MY-NAME-2) STRING)
```
is the built-in handler for "IPC" (ITS version only)

```
IPC-OFF ()
 #DECL ((VALUE) 'T)
```
stops listening on the IPC device (ITS version only)

```
IPC-ON ("OPTIONAL" (MY-NAME-1 <UNAME>) (MY-NAME-2 <JNAME>))
 #DECL ((VALUE) 'T
        (MY-NAME -1 MY-NAME-2) STRING)
```
listens on the IPC device (ITS version only)

```
ISTORAGE (LENGTH "OPTIONAL" (ELEMENT #LOSE 0))
 #DECL ((VALUE) STORAGE
        (LENGTH) FIX (ELEMENT) ANY)
```
creates a non-garbage-collected `STORAGE` from implicit arguments

```
ISTRING (LENGTH "OPTIONAL" (ELEMENT !\^@))
 #DECL ((VALUE) STRING
        (LENGTH) FIX (ELEMENT) ANY)
```
creates a character-string from implicit arguments

```
ITEM (ASSOCIATION)
 #DECL ((VALUE) ANY
        (ASSOCIATION) ASSOC)
```
returns the "item" field of an association

```
ITUPLE (LENGTH "OPTIONAL" (ELEMENT #LOSE 0))
 #DECL ((VALUE) TUPLE
        (LENGTH) FIX (ELEMENT) ANY)
```
creates a `TUPLE` from implicit arguments

```
IUVECTOR (LENGTH "OPTIONAL" (ELEMENT #LOSE 0))
 #DECL ((VALUE) UVECTOR
        (LENGTH) FIX (ELEMENT) ANY)
```
creates a UVECTOR from implicit arguments

```
IVECTOR (LENGTH "OPTIONAL" (ELEMENT #LOSE 0))
 #DECL ((VALUE) VECTOR
        (LENGTH) FIX (ELEMENT) ANY)
```
creates a `VECTOR` from implicit arguments

```
JNAME ()
 #DECL ((VALUE) STRING)
```
returns the "job name" of MDL's process

```
L=? (NUMBER-1 NUMBER-2)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (NUMBER-1 NUMBER-2) <OR FIX FLOAT>)
```
tells whether the first argument is less than or equal to second (predicate)

```
L? (NUMBER-1 NUMBER-2)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (NUMBER-1 NUMBER-2) <OR FIX FLOAT>)
```
tells whether first argument is less than second (predicate)

```
LEAL? (STACK-OBJECT)
 #DECL ((VALUE <OR 'T '#FALSE ()>
        (STACK-OBJECT) ANY)
```
tells whether argument (which might live on the control stack) is still legal (predicate)

```
LENGTH (OBJECT)
 #DECL ((VALUE) FIX
        (OBJECT) STRUCTURED)
```
returns the number of elements in a structure

```
LENGTH? (OBJECT MAX)
 #DECL ((VALUE <OR FIX '#FALSE ()>
        (OBJECT) STRUCTURED (MAX) FIX)
```
tells whether length of structure is less than or equal to an interger (predicate)

```
LINK (EXPR PNAME "OPTIONAL" (OBLIST <` .OBLIST>))
 #DECL ((VALUE EXPR) ANY
        (PNAME) STRING (OBLIST) OBLIST)
```
creates a symbolic `LINK` in any expression for `READ`ing

```
LIST ("TUPLE" ELEMENTS)
 #DECL ((VALUE) LIST
        (ELEMENTS) TUPLE)
```
creates a `LIST` from explicit arguments

```
LISTEN ("TUPLE" INFO)
 #DECL ((VALUE) ANY
        (INFO) TUPLE)
```
stops and informs user that MDL is listening

```
LLOC (ATOM "OPTIONAL" ENV)
 #DECL ((VALUE) LOCD
        (ENV) <OR FRAME ENVIRONMENT ACTIVATION PROCESS>)
```
returns a locative to the local-value cell of an `ATOM`

```
LOAD (CHANNEL "OPTIONAL" (LOOK-PU .OBLIST))
 #DECL ((VALUE '"DONE"
        (LOOK-UP) <OR OBLIST <LIST [REST <OR OBLIST 'DEFAULT>]>>)
```
reads and evaluates all objects via an input `CHANNEL`

```
LOCATIVE? (OBJECT)
 #DECL ((VALUE <OR 'T '#FALSE ()>
        (OBJECT) ANY)
```
tells whether an object is a locative (predicate)

```
LOG (NUMBER)
 #DECL ((VALUE) FLOAT
        (NUMBER) <OR FIX FLOAT>)
```
returns natural logarithm of a number (arithmetic)

```
LOGOUT ()
 #DECL ((VALUE) '#FALSE ())
```
logs out of the operating system (useful for background processes)

```
LOOKUP (PNAME OBLIST)
 #DECL ((VALUE) <OR ATOM '#FALSE ()>
        (PNAME) STRING (OBLIST) OBLIST)
```
returns an `ATOM` found on a given `OBLIST`

```
LPARSE ("OPTIONAL"
        (STRING .PARSE-STRING) (RADIX 10) (LOOK-UP .OBLIST) PARSE-TABLE LOOK-AHEAD)
 #DECL ((VALUE) LIST
        (STRING) STRING (RADIX) FIX (PARSE-TABLE) VECTOR (LOOK-AHEAD) CHARACTER
        (LOOK-UP) <OR OBLIST <LIST [REST <OR OBLIST 'DEFAULT>]>>_
```
returns a `LIST` of the object parsed from a `STRING` (sections 7.6.6.3, 15.7.2, 17.1.3)

```
LSH (WORD AMOUNT)
 #DECL ((VALUE) WORD
        (WORD) <PRIMTYPE WORD> (AMOUNT) FIX)
```
shifts bits in a machine word

```
LVAL (ATOM "OPTIONAL" ENV)
 #DECL ((VALUE) ANY
        (ENV) <OR FRAME ENVIRONMENT ACTIVATION PROCESS>)
```
returns the local value of an `ATOM`

```
MAIN ()
 #DECL ((VALUE) PROCESS)
```
returns `#PROCESS 1` (the main `PROCESS`)

```
MANIFEST ("TUPLE" ATOMS)
 #DECL ((VALUE 'T
        (ATOMS) <TUPLE [REST ATOM]>)
```
declares the global values of `ATOM`s to be constant

```
MANIFEST? (ATOM)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (ATOM) ATOM)
```
tells whether the global value of an `ATOM` is a constant (predicate)

```
MAPF (FINAL-FN LOOP-FCN "TUPLE" STRUCTURE)
 #DECL ((VALUE) ANY
        (FINAL-FCN) <OR APPLICABLE FALSE> (LOOP-FCN) APPLICABLE
        (STRUCTURES) <TUPLE [REST STRUCTURED]>)
```
maps function onto elements of structures

```
MAPLEAVE ("OPTIONAL" (VAL T))
 #DECL (
        (VAL) ANY)
```
leaves the most recent `MAPF/R` with a value

```
MAPR (FINAL-FCN LOOP-FCN "TUPLE" STRUCTURES)
 #DECL ((VALUE) ANY
        (FINAL-FCN) <OR APPLICABLE FALSE> (LOOP-FCN) APPLICABLE
        (STRUCTURES) <TUPLE [REST STRUCTURED]>)
```
maps function onto `REST`s of structures

```
MAPRET ("TUPLE" ELEMENTS)
 #DECL (
        (ELEMENTS) TUPLE)
```
returns a variable number of objects to the current `MAPF/R`

```
MAPSTOP ("TUPLE" ELEMENTS)
 #DECL (
        (ELEMENTS) TUPLE)
```
`MAPRET`s, then stops looping of `MAPF/R` and causes application

```
MAX ("TUPLE" NUMBERS)
 #DECL ((VALUE) <OR FIX FLOAT>
        (NUMBERS) <TUPLE [REST <OR FIX FLOAT>]>)
```
returns the greatest of its arguments (arithmetic)

```
ME ()
 #DECL ((VALUE) PROCESS)
```
returns the current `PROCESS`

```
MEMBER (OBJECT STRUCTURE)
 #DECL ((VALUE) <OR STRUCTURED '#FALSE ()>
        (OBJECT) ANY (STRUCTURE) STRUCTURED)
```
tells whether an object is "structurally" equal to some elements of a structure (predicate)

```
MEMQ (OBJECT STRUCTURE)
 #DECL ((VALUE) <OR STRUCTURED '#FALSE ()>
        (OBJECT) ANY (STRUCTURE) STRUCTURED)
```
tells whether an object is "exactly" equal to some element of a structure (predicate)

```
MIN ("TUPLE") NUMBERS)
 #DECL ((VALUE) <OR FIX FLOAT>
        (NUMBERS) <TUPLE [REST <OR FIX FLOAT>]>)
```
returns the least of its arguments (arithmetic)

```
MOBLIST "NAME "OPTIONAL" (LENGTH 13))
 #DECL ((VALUE) OBLIST
        (NAME) ATOM (LENGTH) FIX)
```
creates a gets an `OBLIST`

```
MOD (NUMBER MODULUS)
 #DECL ((VALUE FIX
        (NUMBER MODULUS) FIX)
```
returns number-theoretic remainder (fixed-point residue) (arithmetic)

```
MONAD? (OBJECT)
 #DECL ((VALUE) <OR 'T '#FALSE ()>
        (OBJECT) ANY)
```
tells whether an object is either unstructured or an empty structure (predicate)
