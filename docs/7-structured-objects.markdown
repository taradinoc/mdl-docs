# Chapter 7. Structured Objects

This chapter discusses structured objects in general and the five 
basic structured `PRIMTYPE`s. [We defer detailed discussion of the 
structured `PRIMTYPE`s `TUPLE` (section 9.2) and `STORAGE` (section 
22.2.2).]

## 7.1. Manipulation

The following `SUBR`s operate uniformly on all structured objects and 
generate an error if not applied to a structured object. Hereafter, 
*structured* represents a structured object.

### 7.1.1. LENGTH [1]

    <LENGTH structured>

evaluates to the number of elements in *structured*.

### 7.1.2. NTH [1]

    <NTH structured fix>

evaluates to the *fix*'th element of *structured*. An error occurs if 
*fix* is less than 1 or greater than `<LENGTH structured>`. *fix* is 
optional, 1 by default.

### 7.1.3. REST [1]

    <REST structured fix>

evaluates to *structured* without its first *fix* elements. *fix* is 
optional, 1 by default.

Obscure but important side effect: `REST` actually returns 
*structured* "`CHTYPE`d" (but not through application of `CHTYPE`) to 
its `PRIMTYPE`. For example, `REST` of a `FORM` is a `LIST`. `REST` 
with an explicit second argument of `0` has no effect except for this 
`TYPE` change.

### 7.1.4. PUT [1]

    <PUT structured fix anything-legal>

first makes *anything-legal* the *fix*'th element of *structured*, 
then evaluates to *structured*. *anything-legal* is anything which can 
legally be an element of *structured*; often, this is synonymous with 
"any MDL object", but see below. An error occurs if *fix* is less than 
1 or greater than `<LENGTH structured>`. (`PUT` is actually more 
general than this -- chapter 13.)

### 7.1.5. GET

    <GET structured fix>

evaluates the same as `<NTH structured fix>`. It is more general than 
`NTH`, however (chapter 13), and is included here only for symmetry 
with `PUT`.

### 7.1.6. APPLYing a FIX [1]

`EVAL` understands the application of an object of `TYPE` `FIX` as a 
"shorthand" call to `NTH` or `PUT`, depending on whether it is given 
one or two arguments, respectively [unless the `APPLYTYPE` of `FIX` is 
changed]. That is, `EVAL` considers the following two to be identical:

    <fix structured>
    <NTH structured fix>

and these:

    <fix structured object>
    <PUT structured fix object>

[However, the compiler (Lebling, 1979) cannot generate efficient code 
from the longer forms unless it is sure that *fix* is a `FIX` (section 
9.10). The two constructs are not identical even to `EVAL`, if the 
order of evaluation is significant: for example, these two:

    <NTH .X <LENGTH <SET X .Y>>>        <<LENGTH <SET X .Y>> .X>

are **not** identical.]

### 7.1.7. SUBSTRUC

`SUBSTRUC` ("substructure") facilitates the construction of structures 
that are composed of sub-parts of existing structures. A special case 
of this would be a "substring" function.

    <SUBSTRUC from:structured rest:fix amount:fix to:structured>

copies the first *amount* elements of `<REST from rest>` into another 
object and returns the latter. All arguments are optional except 
*from*, which must be of `PRIMTYPE` `LIST`, `VECTOR`, `TUPLE` (treated 
like a `VECTOR`), `STRING`, `BYTES`, or `UVECTOR`. *rest* is `0` by 
default, and *amount* is all the elements by default. *to*, if given, 
receives the copied elements, starting at its beginning; it must be an 
object whose `TYPE` is the `PRIMTYPE` of *from* (a `VECTOR` if *from* 
is a `TUPLE`). If *to* is not given, a new object is returned, of 
`TYPE` `<PRIMTYPE from>` (a `VECTOR` if *from* is a `TUPLE`), which 
**never** shares with *from*. The copying is done in one fell swoop, 
not an element at a time. Note: due to an implementation restriction, 
if *from* is of `PRIMTYPE` `LIST`, it must not share any elements with 
*to*.

## 7.2. Representation of Basic Structures

### 7.2.1. LIST [1]

    ( element-1 element-2 ... element-N )

represents a `LIST` of *N* elements.

### 7.2.2. VECTOR [1]

    [ element-1 element-2 ... element-N ]

represents a `VECTOR` of *N* elements. [A `TUPLE` is just like a 
`VECTOR`, but it lives on the control stack.]

### 7.2.3. UVECTOR [1]

    ![ element-1 element-2 ... element-N !]

represents a `UVECTOR` (uniform vector) of *N* elements. The second 
`!` (exclamation-point) is optional for input. [A `STORAGE` is an 
archaic kind of `UVECTOR` that is not garbage-collected.]

### 7.2.4. STRING [1]

    "characters"

represents a `STRING` of ASCII text. A `STRING` containing the 
character `"` (double-quote) is represented by placing a `\` 
(backslash) before the double-quote inside the `STRING`. A `\` in a 
`STRING` is represented by two consecutive backslashes.

### 7.2.5. BYTES

    #n {element-1 element-2 ... element-N}

represents a string of *N* uniformly-sized bytes of size *n* bits.

### 7.2.6. TEMPLATE

    { element-1 element-2 ... element-N }

represents a `TEMPLATE` of *N* elements when output, not input -- 
when input, a `#` and a `TYPE` must precede it.

## 7.3. Evaluation of Basic Structures

This section and the next two describe how `EVAL` treats the basic 
structured `TYPE`s [in the absence of any modifying `EVALTYPE` calls 
(section 6.4.4)].

`EVAL` of a `STRING` [or `BYTES` or `TEMPLATE`] is just the original 
object.

`EVAL` acts exactly the same with `LIST`s, `VECTOR`s, and `UVECTOR`s: 
it generates a **new** object with elements equal to `EVAL` of the 
elements it is given. This is one of the simplest means of 
constructing a structure. However, see section 7.7.

## 7.4. Examples [1]

    (1 2 <+ 3 4>)$
    (1 2 7)
    <SET FOO [5 <- 3> <TYPE "ABC">]>$
    [5 -3 STRING]
    <2 .FOO>$
    -3
    <TYPE <3 .FOO>>$
    ATOM
    <SET BAR ![("meow") (.FOO)]>$
    ![("meow") ([5 -3 STRING])!]
    <LENGTH .BAR>$
    2
    <REST <1 <2 .BAR>>>$
    [-3 STRING]
    [<SUBSTRUC <1 <2 .BAR>> 0 2>]$
    [[5 -3]]
    <PUT .FOO 1 SNEAKY>          ;"Watch out for .BAR !"$
    [SNEAKY -3 STRING]
    .BAR$
    ![("meow") ([SNEAKY -3 STRING])!]
    <SET FOO <REST <1 <1 .BAR>> 2>>$
    "ow"
    .BAR$
    ![("meow") ([SNEAKY -3 STRING])!]

## 7.5. Generation of Basic Structures

Since `LIST`s, `VECTOR`s, `UVECTOR`s, and `STRING`s [and `BYTES`es] 
are all generated in a fairly uniform manner, methods of generating 
them will be covered together here. [`TEMPLATE`s cannot be generated 
by the interpreter itself: see Lebling (1979).]

### 7.5.1. Direct Representation [1]

Since `EVAL` of a `LIST`, `VECTOR`, or `UVECTOR` is a new `LIST`, 
`VECTOR`, or `UVECTOR` with elements which are `EVAL` of the original 
elements, simply evaluating a representation of the object you want 
will generate it. (Care must be taken when representing a `UVECTOR` 
that all elements have the same `TYPE`.) This method of generation was 
exclusively used in the examples of section 7.4. Note that new 
`STRING`s [and `BYTES`es] will not be generated in this manner, since 
the contents of a `STRING` are not interpreted or copied by `EVAL`. 
The same is true of any other `TYPE` whose `TYPEPRIM` happens to be 
`LIST`, `VECTOR`, or `UVECTOR` [again, assuming it neither has been 
`EVALTYPE`d nor has a built-in `EVALTYPE`, as do `FORM` and 
`SEGMENT`].

### 7.5.2. QUOTE [1]

`QUOTE` is an `FSUBR` of one argument which returns its argument 
unevaluated. `READ` and `PRINT` understand the character `'` 
(single-quote) as an abbreviation for a call to `QUOTE`, the way 
period and comma work for `LVAL` and `GVAL`. Examples:

    <+ 1 2>$
    3
    '<+ 1 2>$
    <+ 1 2>

Any `LIST`, `VECTOR`, or `UVECTOR` in a program that is constant and 
need not have its elements evaluated should be represented directly 
and **inside a call to `QUOTE`.** This technique prevents the 
structure from being copied each time that portion of the program is 
executed. Examples hereafter will adhere to this dictum. (Note: one 
should **never** modify a `QUOTE`d object. The compiler will one day 
put it in read-only (pure) storage.)

### 7.5.3. LIST, VECTOR, UVECTOR, and STRING (the SUBRs) [1]

Each of the `SUBR`s `LIST`, `VECTOR`, `UVECTOR`, and `STRING` takes 
any number of arguments and returns an object of the appropriate 
`TYPE` whose elements are `EVAL` of its arguments. There are 
limitations on what the arguments to `UVECTOR` and `STRING` may `EVAL` 
to, due to the nature of the objects generated. See sections 7.6.5 and 
7.6.6.

`LIST`, `VECTOR`, and `UVECTOR` are generally used only in special 
cases, since Direct Representation usually produces exactly the same 
effect (in the absence of errors), and the intention is more apparent. 
[Note: if `.L` is a `LIST`, `<LIST !.L>` makes a copy of `.L` whereas 
`(!.L)` doesn't; see section 7.7.] `STRING`, on the other hand, 
produces effect very different from literal `STRING`s.

Examples:

    <LIST 1 <+ 2 3> ABC>$
    (1 5 ABC)
    (1 <+ 2 3> ABC)$
    (1 5 ABC)
    <STRING "A" <2 "QWERT"> <REST "ABC"> "hello">$
    "AWBChello"
    "A <+ 2 3> (5)"$
    "A <+ 2 3> (5)"

### 7.5.4. ILIST, IVECTOR, IUVECTOR, and ISTRING [1]

Each of the `SUBR`s `ILIST`, `IVECTOR`, `IUVECTOR`, and `ISTRING` 
("implicit" or "iterated" whatever) creates and returns an object of 
the obvious `TYPE`. The format of an application of any of them is

    < Ithing number-of-elements:fix expression:any >

where *Ithing* is one of `ILIST`, `IVECTOR`, `IUVECTOR`, or `ISTRING`. 
An object of `LENGTH` *number-of-elements* is generated, whose 
elements are `EVAL` of *expression*.

*expression* is optional. When it is not specified, `ILIST`, 
`IVECTOR`, and `IUVECTOR` return objects filled with objects of `TYPE` 
`LOSE` (`PRIMTYPE` `WORD`) as place holders, a `TYPE` which can be 
passed around and have its `TYPE` checked, but otherwise is an illegal 
argument. If *expression* is not specified in `ISTRING`, you get a 
`STRING` made up of `^@` characters.

When *expression* is supplied as an argument, it is re-`EVAL`uated 
each time a new element is generated. (Actually, `EVAL` of 
*expression* is re-`EVAL`uated, since all of these are `SUBR`s.) See 
the last example for how this argument may be used.

[By the way, in a construct like `<IUVECTOR 9 '.X>`, even if the 
`LVAL` of `X` evaluates to itself, so that the `'` could be omitted 
without changing the result, the compiler is much happier with the `'` 
in place.]

`IUVECTOR` and `ISTRING` again have limitations on what *expression* 
may `EVAL` to; again, see sections 7.6.5 and 7.6.6.

Examples:

    <ILIST 5 6>$
    (6 6 6 6 6)
    <IVECTOR 2>$
    [#LOSE *000000000000* #LOSE *000000000000*]

    <SET A 0>$
    0
    <IUVECTOR 9 '<SET A <+ .A 1>>>$
    ![1 2 3 4 5 6 7 8 9!]

### 7.5.5. FORM and IFORM

Sometimes the need arises to create a `FORM` without `EVAL`ing it or 
making it the body of a `FUNCTION`. In such cases the `SUBR`s `FORM` 
and `IFORM` ("implicit form") can be used (or `QUOTE` can be used). 
They are entirely analogous to `LIST` and `ILIST`. Example:

    <DEFINE INC-FORM (A)
            <FORM SET .A <FORM + 1 <FORM LVAL .A>>>>$
    INC-FORM
    <INC-FORM FOO>$
    <SET FOO <+ 1 .FOO>>

## 7.6. Unique Properties of Primitive TYPEs

### 7.6.1. LIST (the PRIMTYPE) [1]

An object of `PRIMTYPE` `LIST` may be considered as a "pointer chain" 
(appendix 1). Any MDL object may be an element of a `PRIMTYPE` `LIST`. 
It is easy to add and remove elements of a `PRIMTYPE` `LIST`, but the 
higher N is, the longer it takes to refer to the Nth element. The 
`SUBR`s which work only on objects of `PRIMTYPE` `LIST` are these:

#### 7.6.1.1. PUTREST [1]

    <PUTREST head:primtype-list tail:primtype-list>

changes *head* so that `<REST head>` is *tail* (actually 
`<CHTYPE tail LIST>`), then evaluates to *head*. Note that this 
actually changes *head*; it also changes anything having *head* as an 
element or a value. For example:

    <SET BOW [<SET ARF (B W)>]>$
    [(B W)]
    <PUTREST .ARF '(3 4)>$
    (B 3 4)
    .BOW$
    [(B 3 4)]

`PUTREST` is probably most often used to splice lists together. For 
example, given that `.L` is of `PRIMTYPE` `LIST`, to leave the first 
*m* elements of it intact and take out the next *n* elements of it, 
`<PUTREST <REST .L <- m 1>> <REST .L <+ m n>>>`. Specifically,

    <SET NUMS (1 2 3 4 5 6 7 8 9)>$
    (1 2 3 4 5 6 7 8 9)
    <PUTREST <REST .NUMS 3> <REST .NUMS 7>>$
    (4 8 9)
    .NUMS$
    (1 2 3 4 8 9)

#### 7.6.1.2. CONS

    <CONS new list>

("construct") adds *new* to the front of *list*, without copying 
*list*, and returns the resulting `LIST`. References to *list* are not 
affected.

[Evaluating `<CONS .E .LIST>` is equivalent to evaluating 
`(.E !.LIST)` (section 7.7) but is less preferable to the compiler 
(Lebling, 1979).]

### 7.6.2. "Array" PRIMTYPEs [1]

`VECTORS`, `UVECTOR`s, and `STRING`s [and `BYTES`es and `TEMPLATE`s] 
may be considered as "arrays" (appendix 1). It is easy to refer to the 
Nth element irrespective of how large N is, and it is relatively 
difficult to add and delete elements. The following `SUBR`s can be 
used only with an object of `PRIMTYPE` `VECTOR`, `UVECTOR`, or 
`STRING` [or `BYTES` or `TEMPLATE`]. (In this section *array* 
represents an object of such a `PRIMTYPE`.)

#### 7.6.2.1. BACK [1]

    <BACK array fix>

This is the opposite of `REST`. It evaluates to *array*, with *fix* 
elements put back onto its front end, and changed to its `PRIMTYPE`. 
*fix* is optional, 1 by default. If *fix* is greater than the number 
of elements which have been `REST`ed off, an error occurs. Example:

    <SET ZOP <REST '![1 2 3 4] 3>>$
    ![4!]
    <BACK .ZOP 2>$
    ![2 3 4!]
    <SET S <REST "Right is might." 15>>$
    ""
    <BACK .S 6>$
    "might."

#### 7.6.2.2. TOP [1]

    <TOP array>

"`BACK`s up all the way" -- that is, evaluates to *array*, with all 
the elements which have been `REST`ed off put back onto it, and 
changed to its `PRIMTYPE`. Example:

    <TOP .ZOP>$
    ![1 2 3 4!]

### 7.6.3. "Vector" PRIMTYPEs

#### 7.6.3.1. GROW

    <GROW vu end:fix beg:fix>

adds/removes elements to/from either or both ends of *vu*, and returns 
the entire (`TOP`ped) resultant object. *vu* can be of `PRIMTYPE` 
`VECTOR` or `UVECTOR`. *end* specifies a lower bound for the number of 
elements to be added to the **end** of *vu*; *beg* specifies the same 
for the **beginning**. A negative *fix* specifies removal of elements.

The number of elements added to each respective end is *end* or *beg* 
**increased** to an integral multiple of *X*, where *X* is 32 for 
`PRIMTYPE` `VECTOR` and 64 for `PRIMTYPE` `UVECTOR` (`1` produces 32 
or 64; `-1` produces 0). The elements added will be `LOSE`s if *vu* is 
of `PRIMTYPE` `VECTOR`, and "empty" whatever-they-are's if *vu* is of 
`PRIMTYPE` `UVECTOR`. An "empty" object of `PRIMTYPE` `WORD` contains 
zero. An "empty" object of any other `PRIMTYPE` has zero in its "value 
word" (appendix 1) and is not safe to play with: it should be replaced 
via `PUT`.

Note that, if elements are added to the beginning of *vu*, 
previously-existing references to *vu* will have to use `TOP` or 
`BACK` to get at the added elements.

**Caution:** `GROW` is a **very** expensive operation; it **requires** 
a garbage collection (section 22.4) **every** time it is used. It 
should be reserved for **very special** circumstances, such as where 
the pattern of shared elements is terribly important.

Example:

    <SET A '![1]>$
    ![1!]
    <GROW .A 0 1>$
    ![0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1!]
    .A$
    ![1!]

#### 7.6.3.2. SORT

This `SUBR` will sort `PRIMTYPE`s `VECTOR`, `UVECTOR` and `TUPLE` 
(section 9.2). It works most efficiently if the sort keys are of 
`PRIMTYPE` `WORD`, `ATOM` or `STRING`. However, the keys may be of any 
`TYPE`, and `SORT` will still work. `SORT` acts on fixed-length 
records which consist of one or more contiguous elements in the 
structure being sorted. One element in the record is declared to be 
the sort key. Also, any number of additional structures can be 
rearranged based on how the main structure is sorted.

    <SORT pred s1 l1 off s2 l2 s3 l3 sN lN>

where:

*pred* is either (see chapter 8 for information about predicates):

1. `TYPE` `FALSE`, in which case the `TYPE`s of all the sort keys must 
be the same; they must be of `PRIMTYPE` `WORD`, `STRING` or `ATOM`; 
and a radix-exchange sort is used; or
2. something applicable to two sort keys which returns `TYPE` `FALSE` 
if the first is not bigger than the second, in which case a shell sort 
is used. For example, `,G?` sorts numbers in ascending order, `,L?` in 
descending order. Note: if your *pred* is buggy, the `SORT` may never 
terminate.

*s1* ... *sN* are the (`PRIMTYPE`) `VECTOR`s, `UVECTOR`s or `TUPLE`s 
being sorted, and *s1* contains the sort keys;

*l1* ... *lN* are the corresponding lengths of sort records (optional, 
one by default); and

*off* is the offset from start of record to sort key (optional, zero 
by default).

`SORT` returns the sorted *s1* as a value.

Note: the `SUBR` `SORT` calls the `RSUBR` (chapter 19) `SORTX`; if the 
`RSUBR` must be loaded, you may see some output from the loader on 
your terminal.

Examples:

    <SORT <> <SET A <IUVECTOR 500 '<RANDOM>>>>$
    ![...!]

sorts a `UVECTOR` of random integers.

    <SET V [1 MONEY 2 SHOW 3 READY 4 GO]>$
    [...]
    <SORT <> .V 2 1>$
    [4 GO 1 MONEY 3 READY 2 SHOW]

    <SORT ,L? .V 2>$
    [4 GO 3 READY 2 SHOW 1 MONEY]
    .V$
    [4 GO 3 READY 2 SHOW 1 MONEY]

    <SORT <> ![2 1 4 3 6 5 8 7] 1 0 .V>$
    ![1 2 3 4 5 6 7 8!]
    .V$
    [GO 4 READY 3 SHOW 2 MONEY 1]

The first sort was based on the `ATOM`s' `PNAME`s, considering records 
to be two elements. The second one sorted based on the `FIX`es. The 
third interchanged pairs of elements of each of its structured 
arguments.

### 7.6.4. VECTOR (the PRIMTYPE) [1]

Any MDL object may be an element of a `PRIMTYPE` `VECTOR`. A 
`PRIMTYPE` `VECTOR` takes two words of storage more than an equivalent 
`PRIMTYPE` `LIST`, but takes it all in a contiguous chunk, whereas a 
`PRIMTYPE` `LIST` may be physically spread out in storage (appendix 
1). There are no `SUBR`s or `FSUBR`s which operate only on `PRIMTYPE` 
`VECTOR`.

### 7.6.5. UVECTOR (the PRIMTYPE) [1]

The difference between `PRIMTYPE`s `UVECTOR` and `VECTOR` is that 
every element of a `PRIMTYPE` `UVECTOR` must be of the same `TYPE`. A 
`PRIMTYPE` `UVECTOR` takes approximately half the storage of a 
`PRIMTYPE` `VECTOR` or `PRIMTYPE` `LIST` and, like a `PRIMTYPE` 
`VECTOR`, takes it in a contiguous chunk (appendix 1).

[Note: due to an implementation restriction (appendix 1), `PRIMTYPE` 
`STRING`s, `BYTES`es, `LOCD`s (chapter 12), and objects on the control 
stack (chapter 22) may **not** be elements of `PRIMTYPE` `UVECTOR`s.]

The "same `TYPE`" restriction causes an equivalent restriction to 
apply to `EVAL` of the arguments to either of the `SUBR`s `UVECTOR` or 
`IUVECTOR`. Note that attempting to say

    ![1 .A!]

will cause `READ` to produce an error, since you're attempting to put 
a `FORM` and a `FIX` into the same `UVECTOR`. On the other hand,

    <UVECTOR 1 .A>

is legal, and will `EVAL` to the appropriate `UVECTOR` without error 
if `.A` `EVAL`s to a `TYPE` `FIX`.

The following `SUBR`s work on `PRIMTYPE` `UVECTOR`s along.

#### 7.6.5.1. UTYPE [1]

    <UTYPE primtype-uvector>

("uniform type") evaluates to the `TYPE` of every element in its 
argument. Example:

    <UTYPE '![A B C]>$
    ATOM

#### 7.6.5.2. CHUTYPE [1]

    <CHUTYPE uv:primtype-uvector type>

("change uniform type") changes the `UTYPE` of *uv* to *type*, 
simultaneously changing the `TYPE` of all elements of *uv*, and 
returns the new, changed, *uv*. This works only when the `PRIMTYPE` of 
the elements of *uv* can remain the same through the whole procedure. 
(Exception: a *uv* of `UTYPE` `LOSE` can be `CHUTYPE`d to any *type* 
(legal in a `UVECTOR` of course); the resulting elements are "empty", 
as for `GROW`.)

`CHUTYPE` actually changes *uv*; hence **all** references to that 
object will reflect the change. This is quite different from `CHTYPE`.

Examples:

    <SET LOST <IUVECTOR 2>>$
    ![#LOSE *000000000000* #LOSE *000000000000*!]
    <UTYPE .LOST>$
    LOSE
    <CHUTYPE .LOST FORM>$
    ![<> <>!]
    .LOST$
    ![<> <>!]
    <CHUTYPE .LOST LIST>$
    ![() ()!]

### 7.6.6. STRING (the PRIMTYPE) and CHARACTER [1]

The best mental image of a `PRIMTYPE` `STRING` is a `PRIMTYPE` 
`UVECTOR` of `CHARACTER`s -- where `CHARACTER` is the MDL `TYPE` for a 
single ASCII character. The representation of a `CHARACTER`, by the 
way, is

    !\any-ASCII-character

That is, the characters `!\` (exclamation-point backslash) preceding a 
single ASCII character represent the corresponding object of `TYPE` 
`CHARACTER` (`PRIMTYPE` `WORD`). (The characters `!"` 
(exclamation-point double-quote) preceding a character are also 
acceptable for inputting a `CHARACTER`, for historical reasons.)

The `SUBR` `ISTRING` will produce an error if you give it an argument 
that produces a non-`CHARACTER`. `STRING` can take either `CHARACTER`s 
or `STRING`s.

There are no `SUBR`s which uniquely manipulate `PRIMTYPE` `STRING`s, 
but some are particularly useful in connection with them:

#### 7.6.6.1. ASCII [1]

    <ASCII fix-or-character>

If its argument is of `TYPE` `FIX`, `ASCII` evaluates to the 
`CHARACTER` with the 7-bit ASCII code of its argument. Example: 
`<ASCII 65>` evaluates to `!\A`.

If its argument is of `TYPE` `CHARACTER`, `ASCII` evaluates to the 
`FIX`ed-point number which is its argument's 7-bit ASCII code. 
Example: `<ASCII !\Z>` evaluates to `90`.

[Actually, a `FIX` can be `CHTYPE`d to a `CHARACTER` (or vice versa) directly, but `ASCII` checks in the former case that the `FIX` is within the permissible range.]

#### 7.6.6.2. PARSE [1]

    <PARSE string radix:fix>

`PARSE` applies to its argument `READ`'s algorithm for converting 
ASCII representations to MDL objects and returns the **first** object 
created. The remainder of *string*, after the first object 
represented, is ignored. *radix* (optional, ten by default) is used 
for converting any `FIX`es that occur. [See also sections 15.7.2 and 
17.1.3 for additional arguments.]

#### 7.6.6.3. LPARSE [1]

`LPARSE` ("list parse") is exactly like `PARSE` (above), except that 
it parses the **entire** *string* and returns a `LIST` of **all** 
objects created. If given an empty `STRING` or one containing only 
separators, `LPARSE` returns an empty `LIST`, whereas `PARSE` gets an 
error.

#### 7.6.6.4. UNPARSE [1]

    <UNPARSE any radix:fix>

`UNPARSE` applies to its argument `PRINT`'s algorithm for converting 
MDL objects to ASCII representations and returns a `STRING` which 
contains the `CHARACTER`s `PRINT` would have typed out. [However, this 
`STRING` will **not** contain any of the gratuitous carriage-returns 
`PRINT` adds to accommodate a `CHANNEL`'s finite line-width (section 
11.2.8).] *radix* (optional, ten by default) is used for converting 
any `FIX`es that occur.

### 7.6.7. BYTES

A (`PRIMTYPE`) `BYTES` is a string of uniformly-sized bytes. The bytes 
can be any size between 1 and 36 bits inclusive. A `BYTES` is similar 
in some ways to a `UVECTOR` of `FIX`es and in some ways to a `STRING` 
of non-seven-bit bytes. The elements of a `BYTES` are always of `TYPE` 
`FIX`.

The `SUBR`s `BYTES` and `IBYTES` are similar to `STRING` and 
`ISTRING`, respectively, except that each of the former takes a first 
argument giving the size of the bytes in the generated `BYTES`. 
`BYTES` takes one required argument which is a `FIX` specifying a byte 
size and any number of `PRIMTYPE` `WORD`s. It returns an object of 
`TYPE` `BYTES` with that byte size containing the objects as elements. 
These objects will be `ANDB`ed with the appropriate mask of 1-bits to 
fit in the byte size. `IBYTES` takes two required `FIX`es and one 
optional argument. It uses the first `FIX` to specify the byte size 
and the second to specify the number of elements. The third argument 
is repeatedly evaluated to generate `FIX`es that become elements of 
the `BYTES` (if it is omitted, bytes filled with zeros are generated). 
The analog to `UTYPE` is `BYTE-SIZE`. Examples:

    <BYTES 3 <+ 2 2> 9 -1>$
    #3 {4 1 7}
    <SET A 0>$
    0
    <IBYTES 3 9 '<SET A <+ .A 1>>>$
    #3 {1 2 3 4 5 6 7 0 1}
    <IBYTES 3 4>$
    #3 {0 0 0 0}
    <BYTE-SIZE <BYTES 1>>$
    1

### 7.6.8. TEMPLATE

A `TEMPLATE` is similar to a PL/I "structure" of one level: the 
elements are packed together and reduced in size to save storage 
space, while an auxiliary internal data structure describes the 
packing format and the elements' real `TYPE`s (appendix 1). The 
interpreter is not able to create objects of `PRIMTYPE` `TEMPLATE` 
(Lebling, 1979); however, it can apply the standard built-in 
Subroutines to them, with the same effects as with other "arrays".

## 7.7. SEGMENTs [1]

Objects of `TYPE` `SEGMENT` (whose `TYPEPRIM` is `LIST`) look very 
much like `FORM`s. `SEGMENT`s, however, undergo a non-standard 
evaluation designed to ease the construction of structured objects 
from elements of other structured objects.

### 7.7.1. Representation [1]

The representation of an object of `TYPE` `SEGMENT` is the following:

    !< func arg-1 arg-2 ... arg-N !>

where the second `!` (exclamation-point) is optional, and *fun* and 
*arg-1* through *arg-N* are any legal constituents of a `FORM` (that 
is, anything). The pointed brackets can be implicit, as in the period 
and comma notation for `LVAL` and `GVAL`.

All of the following are `SEGMENT`s:

    !<3 .FOO>    !.FOO    !,FOO

### 7.7.2. Evaluation [1]

A `SEGMENT` is evaluated in exactly the same manner as a `FORM`, with 
the following three exceptions:

1. It had better be done inside an `EVAL` of a structure; otherwise an 
error occurs. (See special case of `FORM`s in section 7.7.5.)
2. It had better `EVAL` to a structured object; otherwise an error 
occurs.
3. What actually gets inserted into the structure being built are the 
elements of the structure returned by the `FORM`-like evaluation.

### 7.7.3 Examples [1]

    <SET ZOP '![2 3 4]>$
    ![2 3 4!]
    <SET ARF (B 3 4)>$
    (B 3 4)
    (.ARF !.ZOP)$
    ((B 3 4) 2 3 4)
    ![!.ZOP !<REST .ARF>!]$
    ![2 3 4 3 4!]

    <SET S "STRUNG.">$
    "STRUNG."
    (!.S)$
    (!\S !\T !\R !\U !\N !\G !\.)

    <SET NIL ()>$
    ()
    [!.NIL]$
    []

### 7.7.4. Note on Efficiency [1]

Most of the cases in which is is possible to use `SEGMENT`s require 
`EVAL` to generate an entire new object. Naturally, this uses up both 
storage and time. However, there is one case which it is possible to 
handle without copying, and `EVAL` uses it. When the structure being 
built is a `PRIMTYPE` `LIST`, and the segment value of a `PRIMTYPE` 
`LIST` is the last (rightmost) element being concatenated, that last 
`PRIMTYPE` `LIST` is not copied. This case is similar to `CONS` and is 
the principle reason why `PRIMTYPE` `LIST`s have their structures more 
easily varied than `PRIMTYPE` `VECTOR` or `UVECTOR`.

Examples:

    .ARF$
    (B 3 4)

This does not copy ARF:

    (1 2 !.ARF)$
    (1 2 B 3 4)

These do:

    (1 !.ARF 2)              ;"not last element"$
    (1 B 3 4 2)
    [1 2 !.ARF]              ;"not PRIMTYPE LIST"$
    [1 2 B 3 4]
    (1 2 !.ARF !<REST '(1)>) ;"still not last element"$
    (1 2 B 3 4)

Note the following, which occurs because copying does **not** take 
place:

    <SET DOG (A !.ARF)>$
    (A B 3 4)
    <PUT .ARF 1 "BOWOW">$
    ("BOWOW" 3 4)
    .DOG$
    (A "BOWOW" 3 4)
    <PUT .DOG 3 "WOOF">$
    (A "BOWOW" "WOOF" 4)
    .ARF$
    ("BOWOW" "WOOF" 4)

Since `ARF` was not copied, it was literally part of `DOG`. Hence, 
when an element of `ARF` was changed, `DOG` was changed. Similarly, 
when an element of `DOG` which `ARF` shared was changed, `ARF` was 
changed too.

### 7.7.5. SEGMENTs in FORMs [1]

When a `SEGMENT` appears as an element of a `FORM`, the effect is 
approximately the same as if the elements of the `EVAL` of the 
`SEGMENT` were in the `FORM`. Example:

    <SET A '![1 2 3 4]>$
    ![1 2 3 4!]
    <+ !.A 5>$
    15

Note: the elements of the structure segment-evaluated in a `FORM` are 
**not** re-evaluated if the thing being applied is a `SUBR`. Thus if 
`.A` were `(1 2 <+ 3 4> 5)`, the above example would produce an error: 
you can't add up `FORM`s.

You could perform the same summation of `5` and the elements of `A` by 
using

    <EVAL <CHTYPE (+ !.A 5) FORM>>

(Note that `EVAL` must be explicitly called as a `SUBR`; if it were 
not so called, you would just get the `FORM` `<+ 1 2 3 4 5>` -- not 
its "value".) However, the latter is more expensive both in time and 
in storage: when you use the `SEGMENT` directly in the `FORM`, a new 
`FORM` is, in fact, **not** generated as it is in the latter case. 
(The elements are put on "the control stack" with the other 
arguments.)

## 7.8. Self-referencing Structures

It is possible for a structured object to "contain" itself, either as 
a subset or as an element, as an element of a structured element, etc. 
Such an object cannot be `PRINT`ed, because recursion begins and never 
terminates. Warning: if you try the examples in this section with a 
live MDL, be sure you know how to use `^S` (section 1.2) to save 
`PRINT` from endless agony. (Certain constructs with `ATOM`s can give 
`PRINT` similar trouble: see chapters 12 and 15.)

### 7.8.1. Self-subset

    <PUTREST head:primtype-list tail:primtype-list>

If *head* is a subset of *tail*, that is, if `<REST tail fix>` is the 
same object as `<REST head 0>` for some *fix*, then both *head* and 
*tail* will be "circular" (and this self-referencing) after the 
`PUTREST`. Example:

    <SET WALTZ (1 2 3)>$
    (1 2 3)
    <PUTREST <REST .WALTZ 2> .WALTZ>$
    (3 1 2 3 1 2 3 1 2 3 1 2 3 ...

### 7.8.2. Self-element

    <PUT s1:structured fix s2:structured>

If *s1* is the same object as *s2*, then it will "contain" itself (and 
thus be self-referencing) after the `PUT`. Examples:

    <SET S <LIST 1 2 3>>        ;"or VECTOR"$
    (1 2 3)
    <PUT .S 3 .S>$
    (1 2 (1 2 (1 2 (1 2 ...
    <SET U ![![]]>$
    ![![!]!]
    <PUT .U 1 .U>$
    ![![![![![![...

Test your reaction time or your terminal's bracket-maker. Amaze your 
friends.
