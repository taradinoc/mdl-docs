# Chapter 15. Lexical Blocking

Lexical, or static, blocking is another means of preventing identifier
collisions in MDL. (The first was dynamic blocking -- binding and
`ENVIRONMENT`s.) By using a subset of the MDL lexical blocking
facilities, the "block structure" of such languages as Algol, PL/I,
SAIL, etc., can be simulated, should you wish to do so.

## 15.1. Basic Considerations

Since what follows appears to be rather complex, a short discussion of
the basic problem lexical blocking solves and MDL's basic solution
will be given first.

`ATOM`s are identifiers. It is thus essential that whenever you type
an `ATOM`, `READ` should respond with the unique identifier you wish
to designate. The problem is that it is unreasonable to expect the
`PNAME`s of all `ATOM`s to be unique. When you use an `ATOM` `A` in a
program, do you mean the `A` you typed two minutes ago, the `A` you
used in another one of your programs, or the `A` used by some library
program?

Dynamic blocking (pushing down of `LVAL`s) solves many such problems.
However, there are some which it does not solve -- such as state
variables (whether they are impure or pure). Major problems with a
system having only dynamic blocking usually arise only when attempts
are made to share large numbers of significant programs among many
people.

The solution used in MDL is basically as follows: `READ` must maintain
at least one table of `ATOM`s to guarantee any uniqueness. So, MDL
allows many such tables and makes it easy for the user to specify
which one is wanted. Such a table is an object of `TYPE` `OBLIST`
("object list"). All the complication which follows arises out of a
desire to provide a powerful, easily used method of working with
`OBLIST`s, with reasonable values used by default.

## 15.2. OBLISTs

An `OBLIST` is of `PRIMTYPE` `UVECTOR` with `UTYPE` `LIST`; the `LIST`
holds `ATOM`s. The `ATOM`s are ordered by a hash coding on their
`PNAME`s: each `LIST` is a hashing bucket.) What follows is
information about `OBLIST`s as such.

### 15.2.1. OBLIST Names

Every normally constituted `OBLIST` has a name. The name of an
`OBLIST` is an `ATOM` associated with the `OBLIST` under the indicator
`OBLIST`. Thus,

    <GETPROP oblist OBLIST>

or

    <GET oblist OBLIST>

returns the name of *oblist*.

Similarly, every name of an `OBLIST` is associated with its `OBLIST`,
again under the indicator `OBLIST`, so that

    <GETPROP oblist-name:atom OBLIST>

or

    <GET oblist-name:atom OBLIST>

returns the `OBLIST` whose name is *oblist-name*.

Since there is nothing special about the association of `OBLIST`s and
their names, the name of an `OBLIST` can be changed by the use of
`PUTPROP`, both on the `OBLIST` and its name. It is not wise to
change the `OBLIST` association without changing the name association,
since you are likely to confuse `READ` and `PRINT` terribly.

You can also use `PUT` or `PUTPROP` to remove the association between
an `OBLIST` and its name completely. If you want the `OBLIST` to go
away (be garbage collected), **and** you want to keep its name around,
this must be done: otherwise the association will force it to stay,
even if there are no other references to it. (If you have no
references to either the name or the `OBLIST` (an `ATOM` -- including
a `TYPE` name -- points to its `OBLIST`), both of them -- and their
association -- will go away without your having to remove the
association, of course.) It is not recommended that you remove the
name of an `OBLIST` without having it go away, since then `ATOM`s in
that `OBLIST` will `PRINT` the name as if they were in no `OBLIST` --
which is defeating the purpose of this whole exercise.

### 15.2.2. MOBLIST

    <MOBLIST atom fix>

("make oblist") creates and returns a new `OBLIST`, containing no
`ATOM`s, whose name is *atom*, unless there already exists an
`OBLIST` of that name, in which case it returns the existing `OBLIST`.
*fix* is the size of the `OBLIST` created -- the number of hashing
buckets. *fix* is optional (ignored if the `OBLIST` already exists),
13 by default. If specified, *fix* should be a prime number, since
that allows the hashing to work better.

### 15.2.3. OBLIST?

    <OBLIST? atom>

returns `#FALSE ()` if *atom* is not in any `OBLIST`. If *atom* is
in an `OBLIST`, it returns that `OBLIST`.

## 15.3. READ and OBLISTs

`READ` can be explicitly told to look up an `ATOM` in a particular
`OBLIST` by giving the `ATOM` a **trailer**. A trailer consists of the
characters `!-` (exclamation-point dash) following the `ATOM`,
immediately followed by the name of the `OBLIST`. For example,

    A!-OB

specifies the unique `ATOM` of `PNAME` `A` which is in the `OBLIST`
whose name is the `ATOM` `OB`.

Note that the name of the `OBLIST` must follow the `!-` with **no**
separators (like space, tab, carriage-return, etc.). There is a name
used by default (section 15.5) which types out and is typed in as
`!-`*separator*.

Trailers can be used recursively:

    B!-A!-OB

specified the unique `ATOM` of `PNAME` `B` which is in the `OBLIST`
whose name is the unique `ATOM` of `PNAME` `A` which is in the
`OBLIST` whose name is `OB`. (Whew!) The repetition is terminated by
the look-up and insertion described below.

If an `ATOM` with a given `PNAME` is not found in the `OBLIST`
specified by a trailer, a new `ATOM` with that `PNAME` is created and
inserted into that `OBLIST`.

If an `OBLIST` whose name is given in a trailer does not exist, `READ`
creates one, of length 13 buckets.

If trailer notation is not used (the "normal" case), and for an `ATOM`
that terminates a trailer, `READ` looks up the `PNAME` of the `ATOM`
in a `LIST` of `OBLIST`s, the `LVAL` of the `ATOM` `OBLIST` by
default. This look-up starts with `<1 .OBLIST>` and continues until
`.OBLIST` is exhausted. If the `ATOM` is not found. `READ` usually
inserts it into `<1 .OBLIST>`. (It is possible to force `READ` to use
a different element of the `LIST` of `OBLIST`s for new insertions. If
the `ATOM` `DEFAULT` is in that `LIST`, the `OBLIST` following that
`ATOM` will be used.)

## 15.4. PRINT and OBLISTs

When `PRINT` is given an `ATOM` to output, it outputs as little of the
trailer as is necessary to specify the `ATOM` uniquely to `READ`. That
is, if the `ATOM` is the **first** `ATOM` of that `PNAME` which `READ`
would find in its normal look-up in the current `.OBLIST`, no trailer
is output. Otherwise, `!-` is output and the name of the `OBLIST` is
recursively `PRIN1`ed.

Warning: there are obscure cases, which do not occur in normal
practice, for which the `PRINT` trailer does not terminate. For
instance, if an `ATOM` must have a trailer printed, and the name of
the `OBLIST` is an `ATOM` in that very same `OBLIST`, death. Any
similar case will also give `PRINT` a hernia.

## 15.5. Initial State

In an initial MDL, `.OBLIST` contains two `OBLIST`s. `<1 .OBLIST>`
initially contains no `ATOM`s, and `<2 .OBLIST>` contains all the
`ATOM`s whose `GVAL` are `SUBR`s or `FSUBR`s, as well as `OBLIST`,
`DEFAULT`, `T`, etc. It is difficult to lose track of the latter; the
specific trailer `!-`*separator* will **always** cause references to
that `OBLIST`. In addition, the `SUBR` `ROOT`, which takes no
arguments, always returns that `OBLIST`.

The name of `<ROOT>` is `ROOT`; this `ATOM` is in `<ROOT>` and would
cause infinite recursion were it not for the use of `!-`*separator*.
The name of the initial `<1 .OBLIST>` is `INITIAL` (really `INITIAL!-
`).

The `ATOM` `OBLIST` also has a `GVAL`. `,OBLIST` is initially the same
as `.OBLIST`; however, `,OBLIST` is not affected by the `SUBR`s used
to manipulate the `OBLIST` structure. It is instead used only when
errors occur.

In the case of an error, the current `.OBLIST` is checked to see if it
is "reasonable" -- that is, contains nothing of the wrong `TYPE`. (It
is reasonable, but not standard, for `.OBLIST` to be a single `OBLIST`
instead of a `LIST` of them.) If it is reasonable, that value stays
current. Otherwise, `OBLIST` is `SET` to `,OBLIST`. Note that changes
made to the `OBLIST`s on `,OBLIST` -- for example, new `ATOM`s added
-- remain. If even `,OBLIST` is unreasonable, `OBLIST` is `SET` and
`SETG`ed to its initial value. `<ERRET>` (section 16.4) always assumes
that `.OBLIST` is unreasonable.

Three other `OBLIST`s exist in a virgin MDL: their names and purposes
are as follows:

`ERRORS!-` contains `ATOM`s whose `PNAME`s are used as error messages.
It is returned by `<ERRORS>`.

`INTERRUPTS!-` is used by the interrupt system (section 21.5.1). It is
returned by `<INTERRUPTS>`.

`MUDDLE!-` is used infrequently by the interpreter when loading
compiled programs to fix up references to locations within the
interpreter.

The pre-loading of compiled programs may create other `OBLIST`s in an
initialized MDL (Lebling, 1979).

## 15.6. BLOCK and ENDBLOCK

These `SUBR`s are analogous to **begin** and **end** in Algol, etc.,
in the way they manipulate static blocking (and in **no** other way.)

    <BLOCK look-up:list-of-oblists>

returns its argument after "pushing" the current `LVAL` of the `ATOM`
`OBLIST` and making its argument the current `LVAL`. You usually want
`<ROOT>` to be an element of *look-up*, normally its last.

    <ENDBLOCK>

"pops" the LVAL of the `ATOM` `OBLIST` and returns the resultant
`LIST` of `OBLIST`s.

Note that this "pushing" and "popping" of `.OBLIST` is entirely
independent of functional application, binding, etc.

## 15.7. SUBRs Associated with Lexical Blocking

### 15.7.1. READ (again)

    <READ channel eof-routine look-up>

This is a fuller call to `READ`. *look-up* is an `OBLIST` or a `LIST`
of them, used as stated in section 15.3 to look up `ATOM`s and insert
them in `OBLIST`s. If not specified, `.OBLIST` is used. See also
section 11.1.1.1, 11.3, and 17.1.3 for other arguments.

### 15.7.2. PARSE and LPARSE (again)

    <PARSE string radix:fix look-up>

as was previously mentioned, applies `READ`'s algorithm to *string*
and returns the first MDL object resulting. This **includes** looking
up prospective `ATOM`s on *look-up*, if given, or `.OBLIST`. `LPARSE`
can be called in the same way. See also section 7.6.6.2 and 17.1.3 for
other arguments.

### 15.7.3. LOOKUP

    <LOOKUP string oblist>

returns the `ATOM` of `PNAME` *string* in the `OBLIST` *oblist*, if
there is such an `ATOM`; otherwise, it returns `#FALSE ()`. If
*string* would `PARSE` into an `ATOM` anyway, `LOOKUP` is faster,
although it looks in only one `OBLIST` instead of a `LIST` of them.

### 15.7.4. ATOM

    <ATOM string>

creates and returns a spanking new `ATOM` of `PNAME` *string* which is
guaranteed not to be on **any** `OBLIST`.

An `ATOM` which is not on any `OBLIST` is `PRINT`ed with a trailer of
`!-#FALSE ()`.

### 15.7.5. REMOVE

    <REMOVE string oblist>

removes the `ATOM` of `PNAME` *string* from *oblist* and returns that
ATOM. If there is no such `ATOM`, `REMOVE` returns `#FALSE ()`. Also,

    <REMOVE atom>

removes *atom* from its `OBLIST`, if it is on one. It returns *atom*
if it was on an `OBLIST`; otherwise it returns `#FALSE ()`.

### 15.7.6. INSERT

    <INSERT string-or-atom oblist>

creates an `ATOM` of `PNAME` *string*, inserts it into *oblist* and
returns it. If there is already an `ATOM` with the same `PNAME` as
*atom* in *oblist*, an error occurs. The standard way to avoid the
error and always get your *atom* is

    <OR <LOOKUP string oblist> <INSERT string oblist>>

As with `REMOVE`, `INSERT` can also take an `ATOM` as its first
argument; this `ATOM` must not be on any `OBLIST` -- it must have been
`REMOVE`d, or just created by `ATOM` -- else an error occurs. The
`OBLIST` argument is **never** optional. If you would like the new
`ATOM` to live in the `OBLIST` that `READ` would have chosen, you can
`<PARSE string>` instead.

### 15.7.7. PNAME

    <PNAME atom>

returns a `STRING` (newly created) which is *atom*'s `PNAME` ("printed
name"). If trailers are not needed, `PNAME` is much faster than
`UNPARSE` on *atom*. (In fact, `UNPARSE` has to go all the way through
the `PRINT` algorithm **twice**, the first time to see how long a
`STRING` is needed.)

### 15.7.8. SPNAME

`SPNAME` ("shared printed name") is identical to `PNAME`, except that
the `STRING` it returns shares storage with *atom* (appendix 1), which
is more efficient if the `STRING` will not be modified. `PUT`ting into
such a `STRING` will cause an error.

## 15.8. Example: Another Solution to the INC Problem

What follows is an example of the way `OBLIST`s are "normally" used to
provide "externally available" `ATOM`s and "local" `ATOM`s which are
not so readily available externally. Lebling (1979) describes a
systematic way to accomplish the same thing and more.

```
<MOBLIST INCO 1>
        ;"Create an OBLIST to hold your external symbols.
        Its name is INCO!-INITIAL!- ."

INC!-INCO
        ;"Put your external symbols into that OBLIST.
	If you have many, just write them successively."

<BLOCK (<MOBLIST INCI!-INCO 1> <GET INCO OBLIST> <ROOT>)>
	;"Create a local OBLIST, naming it INCI!-INCO, and set up
	.OBLIST for reading in your program. The OBLIST INCO is
	included in the BLOCK so that as your external symbols are
	used, they will be found in the right place. Note that the
	ATOM INCO is not in any OBLIST of the BLOCK; therefore,
	trailer notation of !-INCO will not work within the current
	BLOCK-ENDBLOCK pair."

<DEFINE INC	;"INC is found in the INCO OBLIST."
	(A)	;"A is not found and is therefore put into INCI by
READ."
	#DECL ((VALUE A) <OR FIX FLOAT>)
	<SET .A <+ ..A 1>>>	;"All other ATOMs are found in the
ROOT."
<ENDBLOCK>
```

This example is rather trivial, but it contains all of the issues, of
which there are three.

The first idea is that you should create two `OBLIST`s, one to hold
`ATOM`s which are to be known to other users (`INCO`), and the other
to hold internal `ATOM`s which are not normally of interest to other
(`INCI`). The case above has one `ATOM` in each category.

Second, `INCO` is explicitly used **without** trailers so that
surrounding `BLOCK` and `ENDBLOCK`s will have an effect on it. Thus
`INCO` will be in the `OBLIST` desired by the user; `INC` will be in
`INCO`, and the user can refer to it by saying `INC!-INCO`; `INCI`
will also be in `INCO`, and can be referred to in the same way;
finally,  `A` is really `A!-INCI!-INCO`. The point of all this is to
structure the nesting of `OBLIST`s.

Finally, if for some reason (like saving storage space) you wish to
throw `INCI` away, you can follow the `ENDBLOCK` with

    <REMOVE "INCI" <GET INCO OBLIST>>

and thus remove all references to it. The ability to do such pruning
is one reason for structuring `OBLIST` references.

Note that, even after removing `INCI`, you can "get `A` back" -- that
is, be able to type it in -- by saying something of the form

    <INSERT <1 <1 ,INC!-INCO>> <1 .OBLIST>>

thereby grabbing `A` out of the structure of `INC` and re-inserting it
into an `OBLIST`. however, this resurrects the name collision caused
by `<INC!-INCO A>`.
