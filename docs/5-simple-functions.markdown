# Chapter 5. Simple Functions

## 5.1. General [1]

The MDL equivalent of a "program" (uncompiled) is an object of `TYPE` 
`FUNCTION`. Actually, full-blown "programs" are usually composed of 
sets of `FUNCTION`s, with most `FUNCTION`s in the set acting as 
"subprograms".

A `FUNCTION` may be considered to be a `SUBR` or `FSUBR` which you 
yourself define. It is "run" by using a `FORM` to apply it to 
arguments (for example, <*function arg-1 arg-2 ...*>), and it always 
"returns" a single object, which is used as the value of the `FORM` 
that applied it. The single object may be ignored by whatever "ran" 
the `FUNCTION` -- equivalent to "returning no value" -- or it may be a 
structured object containing many objects -- equivalent to "returning 
many values". MDL is an "applicative" language, in contrast to 
"imperative" languages like Fortran. In MDL it is impossible to return 
values through arguments in the normal case; they can be returned only 
as the value of the `FORM` itself, or as side effects to structured 
objects or global values.

In this chapter a simple subset of the `FUNCTION`s you can write is 
presented, namely `FUNCTION`s which "act like" `SUBR`s with a fixed 
number of arguments. While this class corresponds to about 90% of the 
`FUNCTION`s ever written, you won't be able to do very much with them 
until you read further and learn more about MDL's control and 
manipulatory machinery. However, all that machinery is just a bunch of 
`SUBR`s and `FSUBR`s, and you already know how to "use" them; you just 
need to be told what they do. Once you have `FUNCTION`s under your 
belt, you can immediately make use of everything presented from this 
point on in the document. In fact, we recommend that you do so.

## 5.2. Representation [1]

A `FUNCTION` is just another data object in MDL, of `TYPE` `FUNCTION`. 
It can be manipulated like any other data object. `PRINT` represents a 
`FUNCTION` like this:

```no-highlight
#FUNCTION (elements)
```

that is, a number sign, the `ATOM` `FUNCTION`, a left parenthesis, 
each of the elements of the `FUNCTION`, and a right parenthesis. Since 
`PRINT` represents `FUNCTION`s like this, you can type them in to 
`READ` this way. (But there are a few `TYPE`s for which that 
implication is false.)

The elements of a `FUNCTION` can be "any number of anythings"; 
however, when you **use** a `FUNCTION` (apply it with a `FORM`), 
`EVAL` will complain if the `FUNCTION` does not look like

```no-highlight
#FUNCTION (act:atom arguments:list decl body)
```

where *act* and *decl* are optional (section 9.8 and chapter 14); 
*body* is **at least one** MDL object -- any old MDL object; and, in 
this simple case, *arguments* is

```no-highlight
(any number of ATOMs)
```

that is, something `READ` and `PRINT`ed as: left parenthesis, any 
number -- including zero -- of `ATOM`s, right parenthesis. (This is 
actually a normal MDL object of `TYPE` `LIST`, containing only 
`ATOM`s.)

Thus, these `FUNCTION`s will cause errors -- but only **when used**:

 Input                     | Explanation
---------------------------|---------------
 `#FUNCTION ()`            | -- no argument `LIST` or body
 `#FUNCTION ((1) 2 7.3)`   | -- non-`ATOM` in argument `LIST`
 `#FUNCTION ((A B C D))`   | -- no body
 `#FUNCTION (<+ 1 2> A C)` | -- no argument `LIST`

These `FUNCTION`s will never cause errors because of format:

```no-highlight
#FUNCTION (() 1 2 3 4 5)
#FUNCTION ((A) A)
#FUNCTION (()()()()()()()())
#FUNCTION ((A B C D EE F G H HIYA) <+ .A .HIYA>)
#FUNCTION ((Q) <SETG C <* .Q ,C>> <+ <MOD ,C 3> .Q>)
```

and the last two actually do something which might be useful. (The 
first three are rather pathological, but legal.)

## 5.3. Application of FUNCTIONs: Binding [1]

`FUNCTION`s, like `SUBR`s and `FSUBR`s, are applied using `FORM`s. So,

```no-highlight
<#FUNCTION ((X) <* .X .X>) 5>$
25
```

applied the indicated `FUNCTION` to 5 and returned 25.

What `EVAL` does when applying a `FUNCTION` is the following:

1. Create a "world" in which the `ATOM`s of the argument `LIST` have
been **`SET`** to the values applied to the `FUNCTION`, and all other
`ATOM`s have their original values. This is called "binding".
  - In the above, this is a "world" in which `X` is `SET` to `5`.
2. In that new "world", evaluate all the objects in the body of the
`FUNCTION`, one after the other, from first to last.
  - In the above, this means evaluate `<* .X .X>` in a "world" where
`X` is `SET` to `5`.
3. Throw away the "world" created, and restore the `LVAL`s of all
`ATOM`s bound in this application of the `FUNCTION ` to their
originals (if any). This is called "unbinding".
  - In the above, this simply gives `X` back the local value, if any,
that it had before binding.
4. Return as a value the **last value obtained** when the `FUNCTION`'s
body was evaluated in step (2).
  - In the above, this means return `25` as the value.

The "world" mentioned above is actually an object of `TYPE` 
`ENVIRONMENT`. The fact that such "worlds" are separate from the 
`FUNCTION`s which cause their generation means that **all** MDL 
`FUNCTION`s can be used recursively.

The only thing that is at all troublesome in this sequence is the 
effect of creating these new "worlds", in particular, the fact that 
the **previous** world is completely restored. This means that if, 
inside a `FUNCTION`, you `SET` one of its argument `ATOM`s to 
something, that new `LVAL` will **not** be remembered when `EVAL` 
leaves the `FUNCTION`. However, if you `SET` an `ATOM` which is 
**not** in the argument `LIST` (or `SETG` **any** `ATOM`) the new 
local (or global) value **will** be remembered. Examples:

```no-highlight
<SET X 0>$
0
<#FUNCTION ((X) <SET X <* .X .X>>) 5>$
25
.X$
0
```

On the other hand,

```no-highlight
<SET Y 0>$
0
<#FUNCTION ((X) <SET Y <* .X .X>>) 5>$
25
.Y$
25
```

By using `PRINT` as a `SUBR`, we can "see" that an argument's `LVAL` 
really is changed while `EVAL`uating the body of a `FUNCTION`:

```no-highlight
<SET X 5>$
5
<#FUNCTION ((X) <PRINT .X> <+ .X 10>) 3>$
3 13
.X$
5
```

The first number after the application `FORM` was typed out by the 
`PRINT`; the second is the value of the applcation.

Remembering that `LVAL`s of `ATOM`s **not** in argument `LIST`s are 
not changed, we can reference them within `FUNCTION`s, as in

```no-highlight
<SET Z 100>$
100
<#FUNCTION ((Y) </ .Z .Y>) 5>$
20
```

`ATOM`s used like `Z` or `Y` in the above examples are referred to as 
"free variables". The use of free variables, while often quite 
convenient, is rather dangerous unless you know **exactly** how a 
`FUNCTION` will **always** be used: if a `FUNCTION` containing free 
variables is used within a `FUNCTION` within a `FUNCTION` within ..., 
one of those `FUNCTION`s might just happen to use your free variable 
in its argument `LIST`, binding it to some unknown value and possibly 
causing your use of it to be erroneous. Please note that "dangerous", 
as used above, really means that it may be effectively **impossible** 
(1) for other people to use your `FUNCTION`s, and (2) for **you** to 
use your `FUNCTION`s a month (two weeks?) later.

## 5.4. Defining FUNCTIONs (FUNCTION and DEFINE) [1]

Obviously, typing `#FUNCTION (...)` all the time is neither reasonable 
nor adequate for many purposes. Normally, you just want a `FUNCTION` 
to be the `GVAL` of some `ATOM` -- the way `SUBR`s and `FSUBR`s are -- 
so you can use it repeatedly (and recursively). Note that you 
generally do **not** want a `FUNCTION` to be the `LVAL` of an `ATOM`; 
this has the same problems as free variables. (Of course, there are 
always cases where you are being clever and **want** the `ATOM` to be 
re-bound....)

One way to "name" a `FUNCTION` is

```no-highlight
<SETG SQUARE #FUNCTION ((X) <* .X .X>)>$
#FUNCTION ((X) <* .X .X>
```

So that

```no-highlight
<SQUARE 5>$
25
<SQUARE 100>$
10000
```

Another way, which is somewhat cleaner in its typing:

```no-highlight
<SETG SQUARE <FUNCTION (X) <* .X .X>>>$
#FUNCTION ((X) <* .X .X>
```

`FUNCTION` is an `FSUBR` which simply makes a `FUNCTION` out of its 
arguments and returns the created `FUNCTION`.

This, however, is generally the **best** way:

```no-highlight
<DEFINE SQUARE (X) <* .X .X>>$
SQUARE
,SQUARE$
#FUNCTION ((X) <* .X .X>
```

The last two lines immediately above are just to prove that `DEFINE` 
did the "right thing".

`DEFINE` is an `FSUBR` which `SETG`s `EVAL` of its first argument to 
the `FUNCTION` it makes from the rest of its arguments, and then 
returns `EVAL` of its first argument. `DEFINE` obviously requires the 
least typing of the above methods, and is "best" from that standpoint. 
However, the real reason for using `DEFINE` is the following: If 
`EVAL` of `DEFINE`'s first argument **already has** a `GVAL`, `DEFINE` 
produces an error. This helps to keep you from accidentally redefining 
things -- like MDL `SUBR`s and `FSUBR`s. The `SETG` constructions 
should be used only when you really do want to redefine something. 
`DEFINE` will be used in the rest of this document.

[Actually, if it is absolutely necessary to use `DEFINE` to "redefine" 
things, there is a "switch" which can be used: if the `LVAL` of the 
`ATOM` `REDEFINE` is `T` (or anything not of `TYPE` `FALSE`), `DEFINE` 
will produce no errors. The normal state can be restored by evaluating 
`<SET REDEFINE <>>`. See chapter 8.]

## 5.5. Examples (Comments) [1]

Using `SQUARE` as defined above:

```no-highlight
<DEFINE HYPOT (SIDE-1 SIDE-2)
        ;"This is a comment. This FUNCTION finds the
          length of the hypotenuse of a right triangle
          of sides SIDE-1 and SIDE-2."
    <SQRT <+ <SQUARE .SIDE-1> <SQUARE .SIDE-2>>>>$
HYPOT
<HYPOT 3 4>$
5.0
```

Note that carriage-returns, line-feeds, tabs, etc. are just 
separators, like spaces. A comment is **any single** MDL object which 
follows a `;` (semicolon). A comment can appear between any two MDL 
objects. A comment is totally ignored by `EVAL` but remembered and 
associated by `READ` with the place in the `FUNCTION` (or any other 
structured object) where it appeared. (This will become clearer after 
chapter 13.) The `"`s (double-quotes) serve to make everything between 
them a single MDL object, whose `TYPE` is `STRING` (chapter 7). 
(`SQRT` is the `SUBR` which returns the square root of its argument. 
It always returns a `FLOAT`.)

A whimsical `FUNCTION`:

```no-highlight
<DEFINE ONE (THETA) ;"This FUNCTION always returns 1."
        <+ <SQUARE <SIN .THETA>>
           <SQUARE <COS .THETA>>>>$
ONE
<ONE 5>$
0.99999994
<ONE 0.23>$
0.99999999
```

`ONE` always returns (approximately) one, since the sum of the squares 
of sin(x) and cos(x) is unity for any x. (`SIN` and `COS` always 
return `FLOAT`s, and each takes its argument in radians. `ATAN` 
(arctangent) returns its value in radians. Any other trigonometric 
function can be compounded from these three.)

MDL doesn't have a general "to the power" `SUBR`, so let's define one 
using `LOG` and `EXP` (log base e, and e to a power, respectively; 
again, they return `FLOAT`s).

```no-highlight
<DEFINE ** (NUM PWR) <EXP <* .PWR <LOG .NUM>>>>$
**
<** 2 2>$
4.0000001
<** 5 3>$
125.00000
<** 25 0.5>$
5.0000001
```

Two `FUNCTION`s which use a single global variable (Since the `GVAL` 
is used, it cannot be rebound.):

```no-highlight
<DEFINE START () <SETG GV 0>>$
START
<DEFINE STEP () <SETG GV <+ ,GV 1>>>$
STEP
<START>$
0
<STEP>$
1
<STEP>$
2
<STEP>$
3
```

`START` and `STEP` take no arguments, so their argument `LIST`s are empty.

An interesting, but pathological, `FUNCTION`:

```no-highlight
<DEFINE INC (ATM) <SET .ATM <+ ..ATM 1>>>$
INC
<SET A 0>$
0
<INC A>$
1
<INC A>$
2
.A$
2
```

`INC` takes an **`ATOM`** as an argument, and `SET`s that `ATOM` to 
its current `LVAL` plus `1`. Note that inside `INC`, the `ATOM` `ATM` 
is `SET` to the `ATOM` which is its argument; thus `..ATM` returns the 
`LVAL` of the **argument**. However, there is a problem:

```no-highlight
<SET ATM 0>$
0
<INC ATM>$

*ERROR*
ARG-WRONG-TYPE
+
LISTENING-AT-LEVEL 2 PROCESS 1
<ARGS <FRAME <FRAME>>>$
[ATM 1]
```

The error occurred because `.ATM` was `ATM`, the argument to `INC`, 
and thus `..ATM` was `ATM` also. We really want the outermost `.` in 
`..ATM` to be done in the "world" (`ENVIRONMENT`) which existed **just 
before** `INC` was entered -- and this definition of `INC` does both 
applications of `LVAL` in its own "world". Techniques for doing `INC` 
"correctly" will be covered below. Read on.