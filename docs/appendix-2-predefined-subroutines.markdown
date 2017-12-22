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
