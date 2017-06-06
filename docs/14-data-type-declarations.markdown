# Chapter 14. Data-type Declarations

In MDL, it is possible to declare the permissible range of "types"
and/or structures that an `ATOM`'s values or a function's arguments or
value may have. This is done using a special `TYPE`, the `DECL`
("declaration"). A `DECL` is of `PRIMTYPE` `LIST` but has a
complicated internal structure. `DECL`s are used by the interpreter to
find `TYPE` errors in function calling and by the compiler to generate
more efficient code.

There are two kinds of `DECL`s. The first kind of `DECL` is the most
common. It is called the `ATOM` `DECL` and is used most commonly to
specify the type/structure of the `LVAL`s of the `ATOM`s in the
argument `LIST` of a `FUNCTION` or *aux* `LIST` of a `PROG` or
`REPEAT`. This `DECL` has the form:

    #DECL (atoms:list Pattern ...)

where the pairing of a `LIST` of `ATOM`s and a "Pattern" can be
repeated indefinitely. This declares the `ATOM`s in a *list* to be of
the type/structure specified in the following *Pattern*. The special
`ATOM` `VALUE`, if it appears, declares the result of a `FUNCTION`
call or `PROG` or `REPEAT` evaluation to satisfy the Pattern
specified. An `ATOM` `DECL` is useful in only one place: immediately
following the argument `LIST` of a `FUNCTION`, `PROG`, or `REPEAT`. It
normally includes `ATOM`s in the argument `LIST` and `ATOM`s whose
`LVAL`s are otherwise used in the Function body.

The second kind of `DECL` is rarely seen by the casual MDL user,
except in appendix 2. It is called the `RSUBR` `DECL`. It is used to
specify the type/structure of the arguments and result of an `RSUBR`
or `RSUBR-ENTRY` (chapter 19). It is of the following form:

    #DECL ("VALUE" Pattern Pattern ...)

where the `STRING` `"VALUE"` precedes the specification of the
type/structure of the value of the call to the `RSUBR`, and the
remaining *Patterns* specify the arguments to the `RSUBR` in order.
The full specification of the `RSUBR` `DECL` will be given in section
14.9. The `RSUBR` `DECL` is useful in only one place: as an element of
an `RSUBR` or `RSUBR-ENTRY`.

## 14.1. Patterns

The simplest possible Pattern is to say that a value is exactly some
other object, by giving that object, `QUOTE`d. For example, to declare
that a variable is a particular `ATOM`:

    #DECL ((X) 'T)

declares that `.X` is always the `ATOM` `T`. When variables are
`DECL`ed as "being" some other object in this way, the test used is
`=?`, not `==?`. The distinction is usually not important, since
`ATOM`s, which are most commonly used in this construction, are `==?`
to each other is `=?` anyway.

It is more common to want to specify that a value must be of a given
`TYPE`. This is done with the simplest non-specific Pattern, a `TYPE`
name. For example,

    #DECL ((X) FIX (Y) FLOAT)

declares `.X` to be of `TYPE` `FIX`, and `.Y` of `TYPE` `FLOAT`. In
addition to the names of all of the built-in and created `TYPE`s, such
as `FIX`, `FLOAT` and `LIST`, a few "compound" type names are allowed:

* `ANY` allows any `TYPE`.
* `STRUCTURED` allows any structured `TYPE`, such as `LIST`, `VECTOR`,
`FALSE`, `CHANNEL`, etc. (appendix 3).
* `LOCATIVE` allows any locative `TYPE`, such as are returned by
`LLOC`, `GLOC`, `AT`, and so on (chapter 12).
* `APPLICABLE` allows any applicable `TYPE`, such as `FUNCTION`,
`SUBR`, `FIX` (!), etc. (appendix 3).
* Any other `ATOM` can be used to stand for a more complex construct,
if an association is established on that `ATOM` and the `ATOM` `DECL`.
A common example is to `<PUT NUMBER DECL '<OR FIX FLOAT>>` (see
below), so that `NUMBER` can be used as a "compound type name".

The single `TYPE` name can be generalized slightly, allowing anything
of a given `PRIMTYPE`, using the following construction:

    #DECL ((X) <PRIMTYPE WORD> (Y) <PRIMTYPE LIST>)

This construction consists of a two-element `FORM`, where the first
element is the `ATOM` `PRIMTYPE`, and the second the name of a
primitive type.

The next step is to specify the elements of a structure. This is done
in the simplest way as follows:

    < structured:type Pattern Pattern ...>

where there is a one-to-one correspondence between the *Pattern* and
the elements of the structure. For example:

    #DECL ((X) <VECTOR FIX FLOAT>)

declares `.X` to be a `VECTOR` having **at least** two elements, the
first of which is a `FIX` and the second a `FLOAT`. It is often
convenient to allow additional elements, so that only the elements
being used in the local neighborhood of the `DECL` need to be
declared. To disallow additional elements, a `SEGMENT` is used instead
of a `FORM` (the "excl-ed" brackets make it look more emphatic). For
example:

    #DECL ((X) !<VECTOR FIX FLOAT>)

declares `.X` to be a `VECTOR` having **exactly** two elements, the
first of which is a `FIX` and the second a `FLOAT`. Note that the
*Patterns* given for elements can be any legal Pattern:

    #DECL ((X) <VECTOR <VECTOR FIX FLOAT>> (Y) <<PRIMTYPE LIST> LIST>)

declares `.X` to be a `VECTOR` containing another `VECTOR` of at least
two elements, and `.Y` to be of `PRIMTYPE LIST`, containing a `LIST`.
In the case of a `BYTES`, the individual elements cannot be declared
(they must be `FIX`es anyway), only the size and number of the bytes:

    #DECL ((B) <BYTES 7 3>)

declares `.B` to be a `BYTES` with `BYTE-SIZE` 7 and at least three
elements.

It is possible to say that some number of elements of a structure
satisfy a given Pattern (or sequence of Patterns). This is called an
"`NTH` construction".

    [ number:fix Pattern Pattern ... ]

states that the sequence of *Patterns* which is `REST` of the `VECTOR`
is repeated the *number* of times given. For example:

    #DECL ((X) <VECTOR [3 FIX] FLOAT> (Y) <LIST [3 FIX FLOAT]>)

`.X` is declared to contain three `FIX`es and a `FLOAT`, perhaps
followed by other elements. `.Y` is declared to repeat the sequence
`FIX`-`FLOAT` three times. Note that there may be more repetitions of
the sequence in `.Y` (but not in `.X`): the `DECL` specifies only the
first six elements.

For indefinite repetition, the same construction is used, but, instead
of the number of repetitions of the sequence of Patterns, the `ATOM`
`REST` is given. This allows any number of repetitions, from zero on
up. For example:

    #DECL ((X) <VECTOR [REST FIX]> (Y) <LIST [3 FIX] [REST FIX]>)

A "`REST` construction" can contain any number of Patterns, just like
an `NTH` construction:

    #DECL ((X) <VECTOR [REST FIX FLOAT LIST]>)

declares that `.X` is a `VECTOR` wherein the sequence
`FIX`-`FLOAT`-`LIST` repeats indefinitely. It does not declare that
`<LENGTH .X>` is an even multiple of three: the `VECTOR` can end at
any point.

A variation on `REST` is `OPT` (or `OPTIONAL`), which is similar to
`REST` except that the construction is scanned once at most instead of
indefinitely, and further undeclared elements can follow. For example:

    #DECL ((X) <VECTOR [OPT FIX]>)

declares that `.X` is a `VECTOR` which is empty or whose first element
is a `FIX`. Only a `REST` construction can follow an "`OPT`
construction".

Note that the `REST` construction must always be the last element of
the structure declaration, since it gives a Pattern for the rest of
the structure. Thus, the `REST` construction is different from all
others in that it has an unlimited range. No matter how many times the
Pattern it gives is `REST`ed off of the structure, the remainder of
the structure still has that Pattern.

This exhausts the possible single Patterns that can be given in a
declaration. However, there is also a compound Pattern defined. It
allows specification of several possible Patterns for one value:

    <OR Pattern Pattern ... >

Any non-compound Pattern can be included as one of the elements of the
compound Pattern. Finally, compound Patterns can be used as Patterns
for elements of structures, and so on.

    #DECL ((X) <OR FIX FLOAT>
           (Y) <OR FIX <UVECTOR [REST <OR FIX FLOAT>]>>)

The `OR` construction can be extended to any level of ridiculousness,
but the higher the level of complexity and compoundedness the less
likely the compiler will find the `DECL` useful.

At the highest level, any Pattern at top level in an `ATOM` `DECL` can
be enclosed in the construction

    < specialty:atom Pattern >

which explicitly declares the specialty of the `ATOM`(s) in the
preceding `LIST`. *specialty* can be either `SPECIAL` or `UNSPECIAL`.
Specialty is important only when the program is to be compiled. The
word comes from the control stack, which is called "special" in Lisp
(Moon, 1974) because the garbage collector finds objects on it and
modifies their internal pointers when storage is compacted. (An
internal stack is used within the interpreter and is not accessible to
programs -- section 22.1) In an interpreted program all local values
are inherently `SPECIAL`, because all bindings are put on the control
stack (but see `SPECIAL-MODE` below). When the program is compiled,
only values declared `SPECIAL` (which may or may not be the
declaration used by default) remain in bindings on the control stack.
All others are taken care of simply by storing objects on the control
stack: the `ATOM`s involved are not needed and are not created on
loading. So, a program that `SET`s an `ATOM`'s local value for another
program to pick up must declare that `ATOM` to be `SPECIAL`. If it
doesn't, the `ATOM`'s binding will go away during compiling, and the
program that needs to refer to the `ATOM` will either get a no-value
error or refer to an erroneous binding. Usually only `ATOM`s which
have the opposite specialty from that of the current `SPECIAL-MODE`
are explicitly declared. The usual `SPECIAL-MODE` is `UNSPECIAL`, so
typically only `SPECIAL` declarations use this construction:

    #DECL ((ACT)) <SPECIAL ACTIVATION>)

explicitly declares `ACT` to be `SPECIAL`.

Most well-written, modular programs get all their information from
their arguments and from `GVAL`s, and thus they rarely use `SPECIAL`
`ATOM`s, except perhaps for `ACTIVATION`s and the `ATOM`s whose
`LVAL`s MDL uses by default: `INCHAN`, `OUTCHAN`, `OBLIST`, `DEV`,
`SNM`, `NM1`, `NM2`. `OUTCHAN` is a special case: the compiler thinks
that all conversion-output `SUBR`s are called with an explicit
`CHANNEL` argument, whether or not the program being compiled thinks
so. For example, `<CRLF>` is compiled as though it were `<CRLF
.OUTCHAN>`. So you may use (or see) the binding `(OUTCHAN .OUTCHAN)`
in an argument `LIST`, however odd that may appear, because that --
coupled with the usual `UNSPECIAL` declaration by default -- makes
only one reference to the current binding of `OUTCHAN` and stuffs the
result in a slot on the stack for use within the Function.

## 14.2. Examples

    #DECL ((Q) <OR VECTOR CHANNEL>)

declares .Q to be either a `VECTOR` or a `CHANNEL`.

    #DECL ((P Q R S) <PRIMTYPE LIST>)

declares `.P`, `.Q`, `.R`, and `.S` all to be of `PRIMTYPE` `LIST`.

    #DECL ((F) <FORM [3 ANY]>)

declares `.F` to be a `FORM` whose length is at least three,
containing objects of any old `TYPE`.

    #DECL ((LL) <<PRIMTYPE LIST> [4 <LIST [REST FIX]>]>)

declares `.LL` to be of `PRIMTYPE` `LIST`, and to have at least four
elements, each of which are `LIST`s of unspecified length (possibly
empty) containing `FIX`es.

    #DECL ((VV) <VECTOR FIX ATOM CHARACTER>)

declares `.VV` to be a `VECTOR` with at least three elements. Those
elements are, in order, of `TYPE` `FIX`, `ATOM`, and `CHARACTER`.

    #DECL ((EH) <LIST ATOM [REST FLOAT]>)

declares `.EH` to be a `LIST` whose first element is an `ATOM` and the
rest of whose elements are `FLOAT`s. It also says that `.EH` is at
least one element long.

    #DECL ((FOO) <LIST [REST 'T FIX]>)

declares `.FOO` to be a `LIST` whose odd-positioned elements are the
`ATOM` `T` and whose even-positioned elements are `FIX`es.

    <MAPR <>
          <FUNCTION (X)
            #DECL ((X) <VECTOR [1 FIX]>)
            <PUT .X 1 0>>
          .FOO>

declares `.X` to be a `VECTOR` containing at least one `FIX`. The more
restrictive `[REST FIX]` would take excessive checking time by the
interpreter, because the `REST` of the `VECTOR` would be checked on
each iteration of the `MAPR`. In this case both `DECL`s are equally
powerful, because checking the first element of all the `REST`s of a
structure eventually checks all the elements. Also, since the
`FUNCTION` refers only to the first element of `X`, this is as much
declaration as the compiler can effectively use. (If this `VECTOR`
always contains only `FIX`es, it should be a `UVECTOR` instead, for
space efficiency. Then a `[REST FIX]` `DECL` would make the
interpreter check only the `UTYPE`. If the `FIX`es cover a small
non-negative range, then a `BYTES` might be even better, with a `DECL`
of `<BYTES n 0>`.)

    <DEFINE FACT (N)
            #DECL ((N) <UNSPECIAL FIX>)
            <COND (<0? .N> 1) (ELSE <* .N <FACT <- .N 1>>>)>>

declares `.N` to be of `TYPE` `FIX` and `UNSPECIAL`. This specialty
declaration ensures that, independent of `SPECIAL-MODE` during
compiling, `.N` gets compiled into a fast control-stack reference.

    <PROG ((L (0))
            #DECL ((L VALUE) <UNSPECIAL <LIST [REST FIX]>>
                   (N <UNSPECIAL FIX>))
            <COND (<0? .N> <RETURN .L>)>
            <SET L (<+ .N <1 .L>> !.L)>
            <SET N <- .N 1>>>

The above declares `L` and `N` to be `UNSPECIAL`, says that `.N` is a
`FIX`, and says that `.L`, along with the value returned, is a `LIST`
of any length composed entirely of `FIX`es.

## 14.3. The DECL Syntax

This section gives quasi-BNF productions for the MDL `DECL` syntax. In
the following table MDL type-specifiers are distinguished *in this
way*.

    decl    ::=     #DECL (declprs)

    declprs ::=     (atlist) pattern | declprs declprs

    atlist  ::=     atom | atom atlist

    pattern ::=     pat | <UNSPECIAL pat> | <SPECIAL pat>

    pat     ::=     unit | <OR unit ... unit>

    unit    ::=     type | <PRIMTYPE type> | atom | 'any
                    | ANY | STRUCTURED | LOCATIVE |APPLICABLE
                    | <struc elts> | <<OR struc ... struc> elts>
                    | !<struc elts> | !<<OR struc ... struc> elts>
                    | <bstruc fix> | <bstruc fix fix>
                    | !<bstruc fix fix>

    struc   ::=     structured-type | <PRIMTYPE structured-type>

    bstruc  ::=     BYTES | <PRIMTYPE BYTES>

    elts    ::=     pat | pat elts
                    | [fix pat ... pat]
                    | [fix pat ... pat] elts
                    | [opt pat ... pat] | [REST pat ... pat]
                    | [opt pat ... pat] [REST pat ... pat]

    opt     ::=     OPT | OPTIONAL

## 14.4. Good DECLs

There are some rules of thumb concerning "good" `DECL`s. A "good"
`DECL` is one that is minimally offensive to the `DECL`-checking
mechanism as the compiler, but that gives the maximum amount of
information. It is simple to state what gives offense to the compiler
and `DECL`-checking mechanism: complexity. For example, a large
compound `DECL` like:

    #DECL ((X) <OR FIX LIST UVECTOR FALSE>)

is a `DECL` that the compiler will find totally useless. It might as
well be `ANY`. The more involved the `OR`, the less information the
compiler will find useful in it. For example, if the function takes
`<OR LIST VECTOR UVECTOR>`, maybe you should really say `STRUCTURED`.
Also, a very general `DECL` indicates a very general program, which is
not likely to be efficient when compiled (of course there is a
trade-off here). Narrowing the `DECL` to one `PRIMTYPE` gives a great
gain in compiled efficiency, to one `TYPE` still more.

Another situation to be avoided is the ordinary large `DECL`, even if
it is perfectly straightforward. If you have created a structure which
has a very specific `DECL` and is used all over your code, it might be
better as a `NEWTYPE` (see below). The advantage of a `NEWTYPE` over a
large explicit `DECL` is twofold. First, the entire structure must be
checked only when it is created, that is, `CHTYPE`d from its
`PRIMTYPE`. As a full `DECL`, it is checked completely on entering
each function and on each reassignment of `ATOM`s `DECL`ed to be it.
Second, the amount of storage saved in the `DECL`s of `FUNCTION`s and
so on is large, not to mention the effort of typing in and keeping up
to date several instances of the full `DECL`.

## 14.5. Global DECLs

### 15.4.1. GDECL and MANIFEST

There are two ways to declare `GVAL`s for the `DECL`-checking
mechanism. These are through the `FSUBR` `GDECL` ("global
declaration") and the `SUBR` `MANIFEST`.

    <GDECL atoms:list Pattern ...>

`GDECL` allows the type/structure of global values to be declared in
much the same way as local values. Example:

    <GDECL (X) FIX (Y) <LIST FIX>>

declares `,X` to be a `FIX`, and `,Y` to be a `LIST` containing at
least one `FIX`.

    <MANIFEST atom atom ...>

`MANIFEST` takes as arguments `ATOM`s whose `GVAL`s are declared to be
constants. It is used most commonly to indicate that certain `ATOM`s
are the names of offsets in structures. For example:

    <SETG X 1>
    <MANIFEST X>

allows the compiler to confidently open-compile applications of `X`
(getting the first element of a structure), knowing that `,X` will not
change. Any sort of object can be a `MANIFEST` value: if it does not
get embedded in the compiled code, it is included in the `RSUBR`'s
"reference vector", for fast access. However, as a general rule,
structured objects should not be made `MANIFEST`: the `SETG` will
instead refer to a **distinct** copy of the object in **each** `RSUBR`
that does a ` GVAL`. A structured object should instead be `GDECL`ed.

An attempt to `SETG` a `MANIFEST` atom will cause an error, unless
either:

1. the `ATOM` was previously globally unassigned;
2. the old value is `==?` to the new value; or
3. `.REDEFINE` is not `FALSE`.

### 14.5.2. MANIFEST? and UNMANIFEST

    <MANIFEST? atom>

returns `T` if *atom* is `MANIFEST`, `#FALSE ()` otherwise.

    <UNMANIFEST atom atom ...>

removes the `MANIFEST` of the global value of each of its arguments so
that the value can be changed.

### 14.5.3. GBOUND?

    <GBOUND? atom>

("globally bound") returns `T` if *atom* has a global value slot (that
is, if it has ever been `SETG`ed, `MANIFEST`, `GDECL`ed, or `GLOC`ed
(chapter 12) with a true second argument), `#FALSE ()` otherwise.

## 14.6. NEWTYPE (again)

`NEWTYPE` gives the programmer another way to `DECL` objects. The
third (and optional) argument of `NEWTYPE` is a `QUOTE`d Pattern. If
given, it will be saved as the value of an association (chapter 13)
using the name of the `NEWTYPE` as the item and the `ATOM` `DECL` as
the indicator, and it will be used to check any object that is about
to be `CHTYPE`d to the `NEWTYPE`. For example:

    <NEWTYPE COMPLEX-NUMBER VECTOR '<<PRIMTYPE VECTOR> FLOAT FLOAT>>

creates a new `TYPE`, with its first two elements declared to be
`FLOAT`s. If later someone types:

    #COMPLEX-NUMBER [1.0 2]

an error will result (the second element is not a `FLOAT`). The
Pattern can be replaced by doing another `NEWTYPE` for the same
`TYPE`, or by putting a new value in the association. Further
examples:

    <NEWTYPE FOO LIST '<<PRIMTYPE LIST> FIX FLOAT [REST ATOM]>>

causes `FOO`s to contain a `FIX` and a `FLOAT` and any number of
`ATOM`s.

    <NEWTYPE BAR LIST>

    <SET A #BAR (#BAR () 1 1.2 GRITCH)>

    <NEWTYPE BAR LIST '<<PRIMTYPE LIST> BAR [REST FIX FLOAT ATOM]>>

This is an example of a recursively `DECL`ed `TYPE`. Note that `<1
.A>` does not satisfy the `DECL`, because it is empty, but it was
`CHTYPE`d before the `DECL` was associated with `BAR`. Now, even
`<CHTYPE <1 .A> <TYPE <1 .A>>>` will cause an error.

In each of these examples, the `<<PRIMTYPE ...> ...>` construction was
used, in order to permit `CHTYPE`ing an object into itself. See what
happens otherwise:

    <NEWTYPE OOPS LIST '<LIST ATOM FLOAT>>$
    OOPS
    <SET A <CHTYPE (E 2.71828) OOPS>>$
    #OOPS (E 2.71828)

Now `<CHTYPE .A OOPS>` will cause an error. Unfortunately, you must

    <CHTYPE <CHTYPE .A LIST> OOPS>$
    #OOPS (E 2.71828)

## 14.7. Controlling DECL Checking

There are several `SUBR`s and `FSUBR`s in MDL that are used to control
and interact with the `DECL`-checking mechanism.

### 14.7.1. DECL-CHECK

This entire complex checking mechanism can get in the way during
debugging. As a result, the most commonly used `DECL`-oriented `SUBR`
is `DECL-CHECK`. It is used to enable and disable the entire
`DECL`-checking mechanism.

    <DECL-CHECK false-or-any>

If its single argument is non-`FALSE`, `DECL` checking is turned on;
if it is `FALSE`, `DECL` checking is turned off. The previous state is
returned as a value. If no argument is given, `DECL-CHECK` returns the
current state. In an initial MDL `DECL` checking is on.

When `DECL` checking is on, the `DECL` of an `ATOM` is checked each
time it is `SET`, the arguments and results of calls to `FUNCTION`s,
`RSUBR`s, and `RSUBR-ENTRY`s are checked, and the values returned by
`PROG` and `REPEAT` are checked. The same is done for `SETG`s and, in
particular, attempts to change `MANIFEST` global values. Attempts to
`CHTYPE` an object to a `NEWTYPE` (if the `NEWTYPE` has the optional
`DECL`) are also checked. When `DECL` checking is off, none of these
checks is performed.

### 14.7.2. SPECIAL-CHECK and SPECIAL-MODE

    <SPECIAL-CHECK false-or-any>

controls whether or not `SPECIAL` checking is performed at run time by
the interpreter. It is initially off. Failure to declare an `ATOM` to
be `SPECIAL` when it should be will produce buggy compiled code.

    <SPECIAL-MODE specialty:atom>

sets the declaration used by default (for `ATOM`s not declared either
way) and returns the previous such declaration, or the current such
declaration if no argument is given. The initial declaration used by
default is `UNSPECIAL`.

### 14.7.3. GET-DECL and PUT-DECL

`GET-DECL` and `PUT-DECL` are used to examine and change the current
`DECL` (of either the global or the local value) of an `ATOM`.

    <GET-DECL locd>

returns the `DECL` Pattern (if any, otherwise `#FALSE ()`) associated
with the global or local value slot of an `ATOM`. For example:

    <PROG (X)
          #DECL ((X) <OR FIX FLOAT>)
          ...
          <GET-DECL <LLOC X>>
          ...>

would return `<OR FIX FLOAT>` as the result of the application of
`GET-DECL`. Note that because of the use of `LLOC` (or `GLOC`, for
global values) the `ATOM` being examined must be bound; otherwise you
will get an error! This can be gotten around by testing first with
`BOUND?` (or `GBOUND?`, or by giving `GLOC` a second argument which is
not `FALSE`).

If the slot being examined is the global slot and the value is
`MANIFEST`, then the `ATOM` `MANIFEST` is returned. If the value being
examined is not `DECL`ed, `#FALSE ()` is returned.

    <PUT-DECL locd Pattern>

makes *Pattern* be the `DECL` for the value and returns *locd*. If
`<DECL-CHECK>` is true, the current value must satisfy the new
Pattern. `PUT-DECL` is normally used in debugging, to change the
`DECL` of an object to correspond to changes in the program. Note that
it is not legal to `PUT-DECL` a "Pattern" of `MANIFEST` or `#FALSE
()`.

### 14.7.4. DECL?

    <DECL? any Pattern>

specifically checks *any* against *Pattern*. For example:

    <DECL? '[1 2 3] '<VECTOR [REST FIX]>>$
    T
    <DECL? '[1 2.0 3.0] '<VECTOR [REST FIX]>>$
    #FALSE ()

## 14.8. OFFSET

An `OFFSET` is essentially a `FIX` with a Pattern attached, considered
as an `APPLICABLE` rather than a number. An `OFFSET` allows a program
to specify the type of structure that its `FIX` applies to. `OFFSET`s,
like `DECL`s -- if used properly -- can make debugging considerably
easier; they will eventually also help the compiler generate more
efficient code.

The `SUBR` `OFFSET` takes two arguments, a `FIX` and a Pattern, and returns an object of `TYPE` and `PRIMTYPE` `OFFSET`. An `OFFSET`, like a `FIX`, may be given as an argument to `NTH` or `PUT` and may be applied to arguments. The only difference is that the `STRUCTURED` argument must match the Pattern contained in the `OFFSET`, or an error will result. Thus:

    <SETG FOO <OFFSET 1 '<CHANNEL FIX>>>$
    %<OFFSET 1 '<CHANNEL FIX>>
    <FOO ,INCHAN>$
    1
    <FOO <ROOT>>$
    *ERROR*
    ARG-WRONG-TYPE
    NTH
    LISTENING-AT-LEVEL 2 PROCESS 1

Note: when the compiler gets around to understanding `OFFSET`s, it
will not do the right thing with them unless they are `MANIFEST`.
Since there's no good reason not to `MANIFEST` them, this isn't a
problem.

The `SUBR` `INDEX`, given an `OFFSET`, returns its `FIX`:

    <INDEX ,FOO>$
    1

`GET-DECL` of an `OFFSET` returns the associated Pattern; `PUT-DECL`
of an `OFFSET` and a Pattern returns a new `OFFSET` with the same
`INDEX` as the argument, but with a new Pattern:

    <GET-DECL ,FOO>$
    <CHANNEL FIX>
    <PUT-DECL ,FOO OBLIST>$
    %<OFFSET 1 OBLIST>
    ,FOO$
    %<OFFSET 1 '<CHANNEL FIX>>

An `OFFSET` is not a structured object, as this example should make
clear.

## 14.9. The RSUBR DECL

The `RSUBR` `DECL` is similar to the `ATOM` `DECL`, except that the
declarations are of argument positions and value rather than of
specific `ATOM`s. Patterns can be preceded by `STRING`s which further
describe the argument (or value).

The simplest `RSUBR` `DECL` is for an `RSUBR` or `RSUBR-ENTRY`
(chapter 19) which has all of its arguments evaluated and returns a
`DECL`ed value. For example:

    #DECL ("VALUE" FIX FIX FLOAT)

declares that there are two arguments, a `FIX` and a `FLOAT`, and a
result which is a `FIX`. While the `STRING` `"VALUE"` is not
constrained to appear at the front of the `DECL`, it does appear there
by custom. It need not appear at all, if the result is not to be
declared, but (again by custom) in this case it is usually declared
`ANY`.

If any arguments are optional, the `STRING` `"OPTIONAL"` (or `"OPT"`)
is placed before the Pattern for the first optional argument:

    #DECL ("VALUE" FIX FIX "OPTIONAL" FLOAT)

If any of the arguments is not to be evaluated, it is preceded by the
`STRING` `"QUOTE"`:

    #DECL ("VALUE" FIX "QUOTE" FORM)

declares one argument, which is not `EVAL`ed.

If the arguments are to be evaluated and gathered into a `TUPLE`, the
Pattern for it is preceded by the `STRING` `"TUPLE"`:

    #DECL ("VALUE" FIX "TUPLE" <TUPLE [REST FIX]>)

If the arguments are to be unevaluated and gathered into a `LIST`, or
if the calling `FORM` is the only "argument", the Pattern is preceded
by the appropriate `STRING`:

    #DECL ("VALUE" FIX "ARGS" LIST)

    #DECL ("VALUE" FIX "CALL" <PRIMTYPE LIST>)

In every case the special indicator `STRING` is followed by a Pattern
which describes the argument, even though it may sometimes produce
fairly ludicrous results, since the pattern for `"TUPLE"` always must
be a `TUPLE`; for `"ARGS"`, a `LIST`; and for `"CALL"`, a `FORM` or
`SEGMENT`.
