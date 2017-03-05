# Chapter 10. Looping

## 10.1 PROG and REPEAT [1]

`PROG` and `REPEAT` are almost identical `FSUBR`s which make it 
possible to vary the order of `EVAL`uation arbitrarily -- that is, to 
have "jumps". The syntax of `PROG` ("program") is

```no-highlight
<PROG act:atom aux:list body>
```

where

* *act* is an optional `ATOM`, which is bound to the `ACTIVATION` of 
the `PROG`.
* *aux* is a `LIST` which looks exactly like that part of a 
`FUNCTION`'s argument `LIST` which follows an `"AUX"`, and serves 
exactly the same purpose. It is not optional. If you need no temporary 
variables of `"ACT"`, make it `()`.
* *body* is a non-zero number of arbitrary MDL expressions.

The syntax of `REPEAT` is identical, except that, of course, `REPEAT` 
is the first element of the `FORM`, not `PROG`.

### 10.1.1 Basic EVALuation [1]

Upon entering a `PROG`, an `ACTIVATION` is **always** generated. If 
there is an `ATOM` in the right place, the `ACTIVATION` is also bound 
to that `ATOM`. The variables in the *aux* (if any) are then bound as 
indicated in the *aux*. All of the expressions in *body* are then 
`EVAL`uated in their order of occurrence. If nothing untoward happens, 
you leave the `PROG` upon evaluating the last expression in *body*, 
returning the value of that last expression.

`PROG` thus provides a way to package together a group of things you 
wish to do, in a somewhat more limited way than can be done with a 
`FUNCTION`. But `PROG`s are generally used for their other properties.

`REPEAT` acts in all ways **exactly** like a `PROG` whose last 
expression is `<AGAIN>`. The only way to leave a `REPEAT` is to 
explicitly use `RETURN` (or `GO` with a `TAG` -- section 10.4).

### 10.1.2 AGAIN and RETURN in PROG and REPEAT [1]

Within a `PROG` or `REPEAT`, you always have a defined `ACTIVATION`, 
whether you bind it to an `ATOM` or not. [In fact the interpreter 
binds it to the `ATOM` `LPROG\ !-INTERRUPTS` ("last PROG"). The 
`FSUBR` `BIND` is identical to `PROG` except that `BIND` does not bind 
that `ATOM`, so that `AGAIN` and `RETURN` with no `ACTIVATION` 
argument will not refer to it. This feature could be useful within 
`MACRO`s.]

If `AGAIN` is used with no arguments, it uses the `ACTIVATION` of the 
closest surrounding `PROG` or `REPEAT` **within the current function** 
(an error occurs if there is none) and re-starts the `PROG` or 
`REPEAT` without rebinding the *aux* variables, just the way it works 
in a `FUNCTION`. With an argument, it can of course re-start any 
Function (`PROG` or `REPEAT` or `FUNCTION`) within which it is 
embedded at run time.

As with `AGAIN`, if `RETURN` is given no `ACTIVATION` argument, it 
uses the `ACTIVATION` of the closest surrounding `PROG` or `REPEAT` 
within the current function and causes that `PROG` or `REPEAT` to 
terminate and return `RETURN`'s first argument. If `RETURN` is given 
**no** arguments, it causes the closest surrounding `PROG` or `REPEAT` 
to return the `ATOM` `T`. Also like `AGAIN`, it can, with an 
`ACTIVATION` argument, terminate any Function within which it is 
embedded at run time.

### 10.1.3 Examples [1]

Examples of the use of `PROG` are difficult to find, since it is 
almost never necessary, and it slows down the interpreter (chapter 
24). `PROG` can be useful as a point of return from the middle of a 
computation, or inside a `COND` (which see), but we won't exemplify 
those uses. Instead, what follows is an example of a typically poor 
use of `PROG` which has been observed among Lisp (Moon, 1974) 
programmers using MDL. Then, the same thing is done using `REPEAT`. In 
both cases, the example `FUNCTION` just adds up all its arguments and 
returns the sum. (The `SUBR` `GO` is discussed in section 10.4.)

```no-highlight
;"Lisp style"
    <DEFINE MY+ ("TUPLE" TUP)
            <PROG (SUM)
                    <SET SUM 0>
              LP    <COND (<EMPTY? .TUP> <RETURN .SUM>)>
                    <SET SUM <+ .SUM <1 .TUP>>>
                    <SET TUP <REST .TUP>>
                    <GO LP>>>

;"MDL style"
    <DEFINE MY+ ("TUPLE" TUP)
            <REPEAT ((SUM 0))
                    <COND (<EMPTY? .TUP> <RETURN .SUM>)>
                    <SET SUM <+ .SUM <1 .TUP>>
                    <SET TUP <REST .TUP>>>>
```

Of course, neither of the above is optimal MDL code for this problem, 
since `MY+` can be written using `SEGMENT` evaluation as

```no-highlight
<DEFINE MY+ ("TUPLE" TUP) <+ !.TUP>>
```

There are, of course, lots of problems which can't be handled so 
simply, and lots of uses for `REPEAT`.

## 10.2 MAPF and MAPR: Basics [1]

`MAPF` ("map first") and `MAPR` ("map rest") are two `SUBR`s which 
take care of a majority of cases which require loops over data. The 
basic idea is the following:

Suppose you have a `LIST` (or other structure) of data, and you want 
to apply a particular function to each element. That is exactly what 
`MAPF` does: you give it the function and the structure, and it 
applies the function to each element of the structure, starting with 
the first.

On the other hand, suppose you want to **change** each element of a 
structure according to a particular algorithm. This can be done only 
with great pain using `MAPF`, since you don't have easy access to the 
**structure** inside the function: you have only the structure's 
elements. `MAPR` solves the problem by applying a function to `REST`s 
of a structure: first to `<REST structure 0>`, then to 
`<REST structure 1>`, etc. Thus, the function can change the structure 
by changing its argument, for example, by a 
`<PUT argument 1 something>`. It can even `PUT` a new element farther 
down the structure, which will be seen by the function on subsequent 
applications.

Now suppose, in addition to applying a function to a structure, you 
want to record the results -- the values returned by the function -- 
in another structure. Both `MAPF` and `MAPR` can do this: they both 
take an additional function as an argument, and, when the looping is 
over, apply the additional function to **all** the results, and then 
return the results of that application. Thus, if the additional 
function is `,LIST`, you get a `LIST` of the previous results; if it 
is `.VECTOR`, you get a `VECTOR` of results; etc.

Finally, it might be the case that you really want to loop a function 
over more than one structure simultaneously. For instance, consider 
creating a `LIST` whose elements are the element-by-element sum of the 
contents of two other `LIST`s. Both `MAPF` and `MAPR` allow this; you 
can, in fact, give each of them any number of structures full of 
arguments for your looping function.

This was all mentioned because `MAPF` and `MAPR` appear to be complex 
when seen baldly, due to the fact that the argument descriptions must 
take into account the general case. Simpler, degenerate cases are 
usually the ones used.

### 10.2.1 MAPF [1]

```no-highlight
<MAPF finalf loopf s1 s2 ... sN>
```

where (after argument evaluation)

* *finalf* is something applicable that evaluates all its arguments, 
or a `FALSE`;
* *loopf* is something applicable to *N* arguments that evaluates all 
its arguments; and
* *s1* through *sN* are structured objects (any `TYPE`)

does the following:

1. First, it applies *loopf* to *N* arguments: the first element of 
each of the structures. Then it `REST`s each of the structures, and 
does the application again, looping until **any** of the structures 
runs out of elements. Each of the values returned by *loopf* is 
recorded in a `TUPLE`.
2. Then, it applies *finalf* to all the recorded values 
simultaneously, and returns the result of that application. If 
*finalf* is a `FALSE`, the recorded values are "thrown away" (actually 
never recorded in the first place) and the `MAPF` returns only the 
last value returned by *loopf*. If any of the *si* structures is 
empty, to that *loopf* is never invoked, *finalf* is applied to **no** 
arguments; if *finalf* is a `FALSE`, `MAPF` returns `#FALSE ()`.

### 10.2.2 MAPR [1]

```no-highlight
<MAPR finalf loopf s1 s2 ... sN>
```

acts just like `MAPF`, but, instead of applying *loopf* to `NTH`s of 
the structures -- that is, `<NTH si 1>`, `<NTH si 2>`, etc. -- it 
applies it to `REST`s of the structures -- that is, `<REST si 0>`, 
`<REST si 1>`, etc.

### 10.2.3 Examples [1]

Make the element-wise sum of two `LIST`s:

```no-highlight
<MAPF .LIST .+ '(1 2 3 4) '(10 11 12 13)>$
(11 13 15 17)
```

Change a `UVECTOR` to contain double its values:

```no-highlight
<SET UV '![5 6 7 8 9]>$
![5 6 7 8 9!]
<MAPR <>
       #FUNCTION ((L) <PUT .L 1 <* <1 .L> 2>>)
       .UV>$
![18!]
.UV$
![10 12 14 16 18!]
```

Create a `STRING` from `CHARACTER`s:

```no-highlight
<MAPF ,STRING 1 '["MODELING" "DEVELOPMENT" "LIBRARY"]>$
"MDL"
```

Sum the squares of the elements of a `UVECTOR`:

```no-highlight
<MAPF ,+ #FUNCTION ((N) <* .N .N>) '![3 4]>$
25
```

A parallel assignment `FUNCTION` (Note that the arguments to `MAPF` 
are of different lengths.):

```no-highlight
<DEFINE PSET ("TUPLE" TUP)
        <MAPF <>
              ,SET
              .TUP
              <REST .TUP </ <LENGTH .TUP> 2>>>>$
PSET
<PSET A B C 1 2 3>$
3
.A$
1
.B$
2
.C$
3
```

Note: it is easy to forget that *finalf* **must** evaluate its 
arguments, which precludes the use of an `FSUBR`. It is primarily for 
this reason that the `SUBR`s `AND?` and `OR?` were invented. As an 
example, the predicate `=?` could have been defined this way:

```no-highlight
<DEFINE =? (A B)
        <COND (<MONAD? .A> <==? .A .B>)
              (<AND <NOT <MONAD? .B>>
                    <==? <TYPE .A> <TYPE .B>>
                    <==? <LENGTH .A> <LENGTH .B>>>
               <MAPF ,AND? ,=? .A .B>)>>
```

[By the way, the following shows how to construct a value that has the 
same `TYPE` as an argument.

```no-highlight
<DEFINE MAP-NOT (S)
 <COND (<MEMQ <PRIMTYPE .S> '![LIST VECTOR UVECTOR STRING]>
        <CHTYPE <MAPF ,<PRIMTYPE .S> ,NOT .S>
                <TYPE .S>>)>>
```

It works because the `ATOM`s that name the common `STRUCTURED` 
`PRIMTYPS`s (`LIST`, `VECTOR`, `UVECTOR` and `STRING`) have as `GVAL`s 
the corresponding `SUBR`s to build objects of those `TYPE`s.]

## 10.3 More on MAPF and MAPR

### 10.3.1 MAPRET

`MAPRET` is a `SUBR` that enables the *loopf* being used in a `MAPR` 
or `MAPF` (and lexically within it, that is, not separated from it by 
a function call) to return from zero to any number of values as 
opposed to just one. For example, suppose a `MAPF` of the following 
form is used:

```no-highlight
<MAPF ,LIST <FUNCTION (E) ...> ...>
```

Now suppose that the programmer wants to add no elements to the final 
`LIST` on some calls to the `FUNCTION` and add many on other calls to 
the `FUNCTION`. To accomplish this, the `FUNCTION` simply calls 
`MAPRET` with the elements it wants added to the `LIST`. More 
generally, `MAPRET` causes its arguments to be added to the final 
`TUPLE` of arguments to which the *finalf* will be applied.

Warning: `MAPRET` is guaranteed to work only if it is called from an 
explicit `FUNCTION` which is the second argument to a `MAPF` or 
`MAPR`. In other words, the second argument to `MAPF` or `MAPR` must 
be `#FUNCTION (...)` or `<FUNCTION ...>` if `MAPRET` is to be used.

Example: the following returns a `LIST` of all the `ATOM`s in an 
`OBLIST` (chapter 15):

```no-highlight
<DEFINE ATOMS (OB)
        <MAPF .LIST
              <FUNCTION (BKT) <MAPRET !.BKT>>
              .OB>>
```

### 10.3.2 MAPSTOP

`MAPSTOP` is the same as `MAPRET`, except that, after adding its 
arguments, if any, to the final `TUPLE`, it forces the application of 
*finalf* to occur, whether or not the structured objects have run out 
of objects. Example: the following copies the first ten (or all) 
elements of its argument into a `LIST`:

```no-highlight
<DEFINE FIRST-TEN (STRUC "AUX" (I 10))
 <MAPF ,LIST
      <FUNCTION (E)
          <COND (<0? <SET I <- .I 1>>> <MAPSTOP .E>)>
          .E>
      .STRUC>>
```

### 10.3.3 MAPLEAVE

`MAPLEAVE` is analogous to `RETURN`, except that it works in 
(lexically within) `MAPF` or `MAPR` instead of `PROG` or `REPEAT`. It 
flushes the accumulated `TUPLE` of results and returns its argument 
(optional, `T` by default) as the value of the `MAPF` or `MAPR`. (It 
finds the MAPF/R that should returns in the current binding of the 
`ATOM` `LMAP\ !-INTERRUPTS` ("last map").) Example: the following 
finds and returns the first non-zero element of its argument, or 
`#FALSE ()` if there is none:

```no-highlight
<DEFINE FIRST-N0 (STRUC)
        <MAPF <>
              <FUNCTION (X)
                <COND (<N==? .X 0> <MAPLEAVE .X>)>>
              .STRUC>>
```

### 10.3.4 Only two arguments

If `MAPF` or `MAPR` is given only two arguments, the iteration 
function *loopf* is applied to no arguments each time, and the looping 
continues indefinitely until a `MAPLEAVE` or `MAPSTOP` is invoked. 
Example: the following returns a `LIST` of the integers from one less 
than its argument to zero.

```no-highlight
<DEFINE LNUM (N)
        <MAPF ,LIST
              <FUNCTION ()
                <COND (<=? <SET N <- .N 1>>> <MAPSTOP 0>)
                      (ELSE .N)>>>>
```

One principle use of this form of MAPF/R involves processing input 
characters, in cases where you don't know how many characters are 
going to arrive. The example below demonstrates this, using `SUBR`s 
which are more fully explained in chapter 11. Another example can be 
found in chapter 13.

Example: the following `FUNCTION` reads characters from the current 
input channel until an `$` (<kbd>ESC</kbd>) is read, and then returns 
what was read as one `STRING`. (The `SUBR` `READCHR` reads one 
character from the input channel and returns it. `NEXTCHR` returns the 
next `CHARACTER` which `READCHR` will return -- chapter 11.)

```no-highlight
<DEFINE RDSTR ()
  <MAPF .STRING
        <FUNCTION () <COND (<NOT <==? <NEXTCHR> <ASCII 27>>>
                            <READCHR>)
                           (T
                            <MAPSTOP>)>>>>$
RDSTR

<PROG () <READCHR> ;"Flush the ESC ending this input."
	     <RDSTR>>$
ABC123<+ 3 4>$"ABC123<+ 3 4>"
```

### 10.3.5 STACKFORM

The `FSUBR` `STACKFORM` is archaic, due to improvements in the 
implementation of MAPF/R, and it should not be used in new programs.

```no-highlight
<STACKFORM function arg pred>
```

is exactly equivalent to

```no-highlight
<MAPF function
      <FUNCTION () <COND (pred arg) (T <MAPSTOP>)>>>
```

In fact MAPF/R is more powerful, because `MAPRET`, `MAPSTOP`, and 
`MAPLEAVE` provide flexibility not available with `STACKFORM`.

## 10.4 GO and TAG

`GO` is provided in MDL for people who can't recover from a youthful 
experience with Basic, Fortran, PL/I, etc. The `SUBR`s previously 
described in this chapter are much more tasteful for making good, 
clean, "structured" programs. `GO` just bollixes things.

`GO` is a `SUBR` which allows you to break the normal order of 
evaluation and re-start just before any top-level expression in a 
`PROG` or `REPEAT`. It can take two `TYPE`s of arguments: `ATOM` or 
`TAG`.

Given an `ATOM`, `GO` searches the *body* of the immediately 
surrounding `PROG` or `REPEAT` within the current Function, starting 
after *aux*, for an occurrence of that `ATOM` at the top level of 
*body*. (This search is effectively a `MEMQ`.) If it doesn't find the 
`ATOM`, an error occurs. If it does, evaluation is resumed at the 
expression following the `ATOM`.

The `SUBR` `TAG` generates and returns objects of `TYPE` `TAG`. This 
`SUBR` takes one argument: an `ATOM` which would be a legal argument 
for a `GO`. An object of `TYPE` `TAG` contains sufficient information 
to allow you to `GO` to any top-level position in a `PROG` or `REPEAT` 
from within any function called inside the `PROG` or `REPEAT`. `GO` 
with a `TAG` is vaguely like `AGAIN` with an `ACTIVATION`; it allows 
you to "go back" to the middle of any `PROG` or `REPEAT` which called 
you. Also like `ACTIVATION`s, `TAG`s into a `PROG` or `REPEAT` can no 
longer be used after the `PROG` or `REPEAT` has returned. `LEGAL?` can 
be used to see if a `TAG` is still valid.

## 10.5 Looping versus Recursion

Since any program in MDL can be called recursively, champions of "pure 
Lisp" (Moon, 1974) or somesuch may be tempted to implement any 
repetitive algorithm using recursion. The advantage of the looping 
techniques described in this chapter over recursion is that the 
overhead of calls is eliminated. However, a long program (say, bigger 
than half a printed page) may be more difficult to write iteratively 
than recursively and hence more difficult to maintain. A program whose 
repetition is controlled by a structured object (for example, "walking 
a tree" to visit each monad in the object) often should use looping 
for covering one "level" of the structure and recursion to change 
"levels".
