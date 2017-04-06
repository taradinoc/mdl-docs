# Chapter 17. Macro-operations

## 17.1. READ Macros

### 17.1.1. % and %%

The tokens `%` and `%%` are interpreted by `READ` in such a way as to
give a "macro" capability to MDL similar to PL/I's.

Whenever `READ` encounters a single `%` -- anywhere, at any depth of
recursion -- it **immediately**, without looking at the rest of the
input, evaluates the object following the `%`.  The result of that
evaluation is used by `READ` in place of the object following the
`%`.  That is, `%` means "don't really `READ` this, use `EVAL` of it
instead." `%` is often used in files in front of calls to `ASCII`,
`BITS` (which see), etc., although when the `FUNCTION` is compiled
the compiler will do the evaluation if the arguments are constant. 
Also seen is `%.INCHAN`, read as the `CHANNEL` in use during `LOAD`
or `FLOAD`; for example, `<PUT %.INCHAN 18 8>` causes succeeding
`FIX`es to be read as octal.

Whenever `READ` encounters `%%`, it likewise immediately evaluates
the object following the `%%`.  However, it completely ignores the
result of that evaluation.  Side effects of that evaluation remain,
of course.

Example:

    <DEFINE SETUP () <SET A 0>>$
    SETUP
    <DEFINE NXT () <SET A <+ .A 1>>>$
    NXT
    [%%<SETUP> %<NXT> %<NXT> (%%<SETUP>) %<NXT>]$
    [1 2 () 1]

### 17.1.2. LINK

    <LINK exp:any string oblist>

creates an object of `TYPE` `LINK`, `PRIMTYPE` `ATOM`.  A `LINK`
looks vaguely like an `ATOM`; it has a `PNAME` (the *string*
argument), resides in an `OBLIST` (the *oblist* argument) and has a
"value" (the *exp* argument).  A `LINK` has the strange property
that, whenever it is encountered by `READ` (that is, its `PNAME` is
read, just like an `ATOM`, possibly with `OBLIST` trailers), `READ`
substitutes the `LINK`'s "value" for the `LINK` immediately.  The
effect of `READ`ing a `LINK`'s `PNAME` is exactly the same as the
effect of reading its "value".

The *oblist* argument is optional, `<1 .OBLIST>` by default.  `LINK`
returns its first argument.  The `LINK` is created via `INSERT`, so
an error results if there is already an `ATOM` or `LINK` in *oblist*
with the same `PNAME`.

The primary use of `LINK`s is in interactive work with MDL:
expressions which are commonly used, but annoyingly long to type, can
be "linked" to `PNAME`s which are shorter.  The standard example is
the following:

    <LINK '<ERRET> "^E" <ROOT>>

which links the `ATOM` of `PNAME` `^E` in the `ROOT` `OBLIST` to the
expression `<ERRET>`.

### 17.1.3. Program-defined Macro-characters

During `READ`ing from an input `CHANNEL` or `PARSE`ing a `STRING`,
any character can be made to have a special meaning.  A character can
cause an arbitrary routine to be invoked, which can then return any
number of elements to be put into the object being built by `READ`,
`PARSE`, or `LPARSE`.  Translation of characters is also possible. 
This facility was designed for those persons who want to use MDL
`READ` to do large parts of their input but have to modify its
actions for some areas: for example, one might want to treat left and
right parentheses as tokens, rather than as delimiters indicating a
`LIST`.

#### 17.1.3.1. READ (finally)

Associated with `READ` is an `ATOM`, `READ-TABLE!-`, whose local
value, if any, must be a `VECTOR` of elements, one for each character
up to and including all characters to be treated specially.  Each
element indicates, if not `0`, the action to be taken upon `READ`'s
encounter with that character.  A similar `VECTOR`, the local value
of `PARSE-TABLE!-`, if any, is used to find the action to take for
characters encountered when `PARSE` or `LPARSE` is applied to a
`STRING`.

These tables can have up to 256 elements, one for each ASCII
character and one for each possible exclamation-point/ASCII-character
pair.  In MDL, the exclamation-point is used as a method of expanding
the ASCII character set, and an exclamation-point/character pair is
treated as one logical character when not reading a `STRING`.

The element corresponding to a character is `<NTH table <+ 1 <ASCII
char>>>`.  The element corresponding to an
exclamation-point/ASCII-character pair is `<NTH table <+ 129 <ASCII
char>>>`.  The table can be shorter than 256 elements, in which case
it is treated as if it were 256 long with `0` elements beyond its
actual length.

An element of the tables must satisfy one of the following `DECL`
Patterns:

>`'0` indicates that no special action is to be taken when this
>character is encountered.

>`CHARACTER` indicates that the encountered character is to be
>translated into the given `CHARACTER` whenever it appears, except
>when as an object of `TYPE` `CHARACTER`, or in a `STRING`, or
>immediately following a `\`.

>`FIX` indicates that the character is to be given the same treatment
>as the character with the ASCII value of the `FIX`.  This allows you
>to cause other characters to be treated in the same way as A-Z for
>example.  The same exceptions apply as for a `CHARACTER`.

>`<LIST FIX>` indicates the same thing, except that the character
>does not by itself cause a break.  Therefore, if it occurs when
>reading an `ATOM` or number, it will be treated as part of that
>`ATOM` or number.

>`APPLICABLE` (to one argument) indicates that the character is to be
>a break character.  Whenever it is encountered, the reading of the
>current object is finished, and the corresponding element of the
>table is `APPLY`ed to the ASCII `CHARACTER`.  (If `READ` is called
>during the application, the end-of-file slot of the `CHANNEL`
>temporarily contains a special kind of `ACTIVATION` (`TYPE` `READA`)
>so that end-of-file can be signalled properly to the original
>`READ`.  Isn't that wonderful?) The value returned is taken to be
>what was read, unless an object of `TYPE` `SPLICE` is returned.  If
>so, the elements of this object, which is of `PRIMTYPE` `LIST`, are
>spliced in at the point where MDL is reading.  An empty `SPLICE`
>allows one to return nothing.  If a structured object is not being
>built, and a `SPLICE` is returned, elements after the first will be
>ignored.  A `SPLICE` says "expand me", whereas the structure
>containing a `SEGMENT` says "I will expand you".

>`<LIST APPLICABLE>` indicates the same thing, except that the
>character does not by itself cause a break.  Therefore, if it occurs
>when reading an `ATOM` or number, it will be treated as part of that
>`ATOM` or number.

`READ` takes an additional optional argument, which is what to use
instead of the local value of the `ATOM` `READ-TABLE` as the `VECTOR`
of read-macro characters.  If this argument is supplied, `READ-TABLE`
is rebound to it within the call to `READ`.  `READ` takes from zero
to four arguments.  The fullest call to `READ` is thus:

    <READ channel eof-routine look-up read-table:vector>

The other arguments are explained in sections 11.1.1.1, 11.3, and
15.7.1.

`ERROR` and `LISTEN` rebind `READ-TABLE` to the `GVAL` of
`READ-TABLE`, if any, else `UNASSIGN` it.

#### 17.1.3.2. Examples

Examples of each of the different kinds of entries in macro tables:

    <SET READ-TABLE <IVECTOR 256 0>>$
    [...]

    <PUT .READ-TABLE <+ 1 <ASCII !\a>> !\A>
                    ;"CHARACTER: translate a to A."$
    [...]
    abc$
    Abc

    <PUT .READ-TABLE <+ 1 <ASCII !\%>> <ASCII !\A>>
            ;"FIX: make % just a normal ASCII character."$
    [...]
    A%BC$
    A\%BC

    <PUT .READ-TABLE <+ 1 <ASCII !\.>> (<ASCII !\.>)>
            ;"<LIST FIX>: make comma no longer a break
              character, but still special if at a break."$
    [...]
    A,B$
    A\,B
    ;"That was an ATOM with PNAME A,B ."
    ',B$
    ,B
    ;"That was the FORM <GVAL B> ."

    <PUT .READ-TABLE <+ 1 <ASCII !\:>>
        #FUNCTION ((X) <LIST COLON <READ>>)>
            ;"APPLICABLE: make a new thing like ( < and [ ."$
    [...]
    B:A$
    B
    (COLON A)
    :::FOO$
    (COLON (COLON (COLON FOO)))

    <PUT .READ-TABLE <+ 1 <ASCII !\:>>
        '(#FUNCTION ((X) <LIST COLON <READ>>))>
            ;"<LIST APPLICABLE>: like above, but not a break
              now."$
    [...]
    B:A$
    B:A
    ;"That was an ATOM."
    :::FOO$
    (COLON (COLON (COLON FOO)))

#### 17.1.3.3. PARSE and LPARSE (finally)

    <PARSE string radix look-up parse-table:vector look-ahead:character>

is the fullest call to `PARSE`.  `PARSE` can take from zero to five
arguments.  If `PARSE` is given no arguments, it returns the first
object parsed from the local value of the `STRING` `PARSE-STRING` and
additionally `SET`s `PARSE-STRING` to the `STRING` having those
`CHARACTER`s which were parsed `REST`ed off.  If `PARSE` is given a
`STRING` to parse, the `ATOM` `PARSE-STRING` is rebound to the
`STRING` within that call.  If the *parse-table* argument is given to
`PARSE`, `PARSE-TABLE` is rebound to it within that call to `PARSE`. 
Finally, `PARSE` can take a *look-ahead* `CHARACTER`, which is
treated as if it were logically concatenated to the front of the
*string* being parsed.  Other arguments are described in sections
7.6.6.2 and 15.7.2.

`LPARSE` is exactly like `PARSE`, except that it tries to parse the
whole `STRING`, returning a `LIST` of the objects created.

## 17.2. EVAL Macros

An `EVAL` macro provides the convenience of a `FUNCTION` without the
overhead of calling, `SPECIAL`s, etc.  in the **compiled** version. 
A special-purpose function that is called often by `FUNCTION`s that
will be compiled is a good candidate for an `EVAL` macro.

### 17.2.1. DEFMAC and EXPAND

`DEFMAC` ("define macro") is syntactically exactly the same as
`DEFINE`.  However, instead of creating a `FUNCTION`, `DEFMAC`
creates a `MACRO`.  A `MACRO` is of `PRIMTYPE` `LIST` and in fact has
a `FUNCTION` (or other `APPLICABLE` `TYPE`) as its single element.

A `MACRO` can itself be applied to arguments.  A `MACRO` is applied
in a funny way, however: it is `EVAL`ed twice.  The first `EVAL`
causes the `MACRO`'s element to be applied to the `MACRO`'s
arguments.  Whatever that application returns (usually another
`FORM`) is also `EVAL`ed.  The result of the second `EVAL`uation is
the result of applying the `MACRO`.  `EXPAND` is used to perform the
first `EVAL` without the second.

To avoid complications, the first `EVAL` (by `EXPAND`, to create the
object to be `EVAL`ed the second time around) is done in a top-level
environment.  The result of this policy is that two syntactically
identical invocations of a `MACRO` always return the same expansion
to be `EVAL`ed in the second step.  The first `EVAL` generates two
extra `FRAME`s: one for a call to `EXPAND`, and one for a call to
`EVAL` the `MACRO` application in a top-level environment.

Example:

    <DEFMAC INC (ATM "OPTIONAL" (N 1))
            #DECL ((VALUE) FORM (ATM) ATOM (N) <OR FIX FLOAT>)
            <FORM SET .ATM <FORM + <FORM LVAL .ATM> .N>>>$
    INC
    ,INC$
    #MACRO (#FUNCTION ((ATM "OPTIONAL" (N 1)) ...))
    <SET X 1>$
    1
    <INC X>$
    2
    .X$
    2
    <EXPAND '<INC X>>$
    <SET X <+ .X 1>>

Perhaps the intention is clearer if `PARSE` and `%` are used:

    <DEFMAC INC (ATM "OPTIONAL" (N 1))
            #DECL (...)
            <PARSE "<SET %.ATM <+ %.ATM %.N>>">>

`MACRO`s really exhibit their advantages when they are compiled.  The
compiler will simply cause the first `EVAL`uation to occur (via
`EXPAND`) and compile the result.  The single element of a compiled
`MACRO` is an `RSUBR` or `RSUBR-ENTRY`.

### 17.2.2. Example

Suppose you want to change the following simple `FUNCTION` to a
`MACRO`:

    <DEFINE DOUBLE (X) #DECL ((X) FIX) <+ .X .X>>

You may be tempted to write:

    <DEFMAC DOUBLE (X) #DECL ((X) FIX) <FORM + .X .X>>

This `MACRO` works, but only when the argument does not use temporary
bindings.  Consider

    <DEFINE TRIPLE (Y) <+ .Y <DOUBLE .Y>>>

If this `FUNCTION` is applied, the top-level binding of `Y` is used,
not the binding just created by the application.  Compilation of this
`FUNCTION` would probably fail, because the compiler probably would
have no top-level binding for `Y`.  Well, how about

    <DEFMAC DOUBLE ('X) <FORM + .X .X>>  ;"The DECL has to go."

Now this is more like the original `FUNCTION`, because no longer is
the argument evaluated and the result evaluated again.  And `TRIPLE`
works.  But now consider

    <DEFINE INC-AND-DOUBLE (Y) <DOUBLE <SET Y <+ 1 .Y>>>>

You might hope that

    <INC-AND-DOUBLE 1> -> <DOUBLE <SET Y <+ 1 1>>>
                       -> <DOUBLE 2>
                       -> <+ 2 2>
                       -> 4

But, when `DOUBLE` is applied to that `FORM`, the argument is
`QUOTE`d, so:

    <INC-AND-DOUBLE 1> -> <DOUBLE <SET Y <+ 1 1>>>
                       -> <FORM + <SET Y <+ 1 .Y>> <SET Y <1 .Y>>>
                       -> <+ 2 3>
                       -> 5

So, since the evaluation of `DOUBLE`'s argument has a side effect,
you should ensure that the evaluation is done exactly once, say by
`FORM`:

    <DEFMAC DOUBLE ('ANY)
            <FORM PROG ((X .ANY)) #DECL ((X) FIX) '<+ .X .X>>>

As a bonus, the `DECL` can once more be used.

This example is intended to show that writing good `MACRO`s is a
little trickier than writing good `FUNCTION`s.  But the effort may be
worthwhile if the compiled program must be speedy.
