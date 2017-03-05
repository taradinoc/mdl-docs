# Chapter 6. Data Types

## 6.1 General [1]

A MDL object consists of two parts: its `TYPE` and its "data part" 
(appendix 1). The interpretation of the "data part" of an object 
depends of course on its `TYPE`. The structural organization of an 
object, that is, the way it is organized in storage, is referred to as 
its "primitive type". While there are many different `TYPE`s of 
objects in MDL, there are fewer primitive types.

All structured objects in MDL are ordered sequences of elements. As 
such, there are `SUBR`s which operate on all of them uniformly, as 
ordered sequences. On the other hand, the reason for having different 
primitive types of structured objects is that there are useful 
qualities of structured objects which are mutually incompatible. There 
are, therefore, `SUBR`s which do not work on all structured objects: 
these `SUBR`s exist to take full advantage of those mutually 
incompatible qualities. The most-commonly-used primitive types of 
structured objects are discussed in chapter 7, along with those 
special `SUBR`s operating on them.

It is very easy to make a new MDL object that differs from an old one 
only in `TYPE`, as long as the primitive type is unchanged. It is 
relatively difficult to make a new structured object that differs from 
an old one in primitive type, even if it has the same elements.

Before talking any more about structured objects, some information 
needs to be given about `TYPE`s in general.

## 6.2 Printed Representation [1]

There are many `TYPE`s for which MDL has no specific representation. 
There aren't enough different kinds of brackets. The representation 
used for `TYPE`s without any special representation is

```no-highlight
#type representation-as-if-it-were-its-primitive-type
```

`READ` will understand that format for **any** `TYPE`, and `PRINT` 
will use it by default. This representational format will be referred 
to below as "# notation". It was used above to represent `FUNCTION`s.

## 6.3 SUBRs Related to TYPEs

### 6.3.1 TYPE [1]

```no-highlight
<TYPE any>
```

returns an **`ATOM`** whose `PNAME` corresponds to the `TYPE` of 
*any*. There is no `TYPE` "TYPE". To type a `TYPE` (aren't homonyms 
wonderful?), just type the appropriate `ATOM`, like `FIX` or `FLOAT` 
or `ATOM` etc. However, in this document we will use the convention 
that a metasyntactic variable can have *type* for a "data type": for 
example, *foo:type* means that the `TYPE` of *foo* is `ATOM`, but the 
`ATOM` must be something that the `SUBR` `TYPE` can return.

Examples:

```no-highlight
<TYPE 1>$
FIX
<TYPE 1.0>$
FLOAT
<TYPE +>$
ATOM
<TYPE ,+>$
SUBR
<TYPE GEORGE>$
ATOM
```

### 6.3.2 PRIMTYPE [1]

```no-highlight
<PRIMTYPE any>
```

evaluates to the primitive type of *any*. The `PRIMTYPE` of *any* is 
an `ATOM` which also represents a `TYPE`. The way an object can be 
**manipulated** depends solely upon its `PRIMTYPE`; the way it is 
**evaluated** depends upon its `TYPE`.

Examples:

```no-highlight
<PRIMTYPE 1>$
WORD
<PRIMTYPE 1.0>$
WORD
<PRIMTYPE ,+>$
WORD
<PRIMTYPE GEORGE>$
ATOM
```

### 6.3.3 TYPEPRIM [1]

```no-highlight
<TYPEPRIM type>
```

returns the `PRIMTYPE` of an object whose `TYPE` is *type*. *type* is, 
as usual, an `ATOM` used to designate a `TYPE`.

Examples:

```no-highlight
<TYPEPRIM FIX>$
WORD
<TYPEPRIM FLOAT>$
WORD
<TYPEPRIM SUBR>$
WORD
<TYPEPRIM ATOM>$
ATOM
<TYPEPRIM FORM>$
LIST
```

### 6.3.4 CHTYPE [1]

```no-highlight
<CHTYPE any type>
```

("change type") returns a new object that has `TYPE` *type* and the 
same "data part" as *any* (appendix 1).

```no-highlight
<CHTYPE (+ 2 2) FORM>$
<+ 2 2>
```

An error is generated if the `PRIMTYPE` of *any* is not the same as 
the `TYPEPRIM` of *type*. An error will also be generated if the 
attempted `CHTYPE` is dangerous and/or senseless, for example, 
`CHTYPE`ing a `FIX` to a `SUBR`. Unfortunately, there are few useful 
examples we can do at this point.

[`CHTYPE`ing a `FIX` to a `FLOAT` or vice versa produces, in general, 
nonsense, since the bit formats for `FIX`es and `FLOAT`s are 
different. The `SUBR`s `FIX` and `FLOAT` convert between those 
formats. Useful obscurity: because of their internal representations 
on the PDP-10, `<CHTYPE <MAX> FIX>` gives the least possible `FIX`, 
and analogously for `MIN`.]

Passing note: "# notation" is just an instruction to `READ` saying 
"`READ` the representation of the `PRIMTYPE` normally and (literally) 
`CHTYPE` it to the specified `TYPE`". [Or, if the `PRIMTYPE` is 
`TEMPLATE`, "apply the `GVAL` of the `TYPE` name (which should be a 
`TEMPLATE` constructor) to the given elements of the `PRIMTYPE` 
`TEMPLATE` as arguments."]

## 6.3 More SUBRs Related to TYPEs

### 6.4.1 ALLTYPES

```no-highlight
<ALLTYPES>
```

returns a `VECTOR` (chapter 7) containing just those `ATOM`s which can 
currently be returned by `TYPE` or `PRIMTYPE`. This is the very 
"`TYPE` vector" (section 22.1) that the interpreter uses: look, but 
don't touch. No examples: try it, or see appendix 3.

### 6.4.2 VALID-TYPE?

```no-highlight
<VALID-TYPE? atom>
```

returns `#FALSE ()` if *atom* is not the name of a `TYPE`, and the 
same object that `<TYPE-C atom>` (section 19.5) returns if it is.

### 6.4.3 NEWTYPE

MDL is a type-extensible language, in the sense that the programmer 
can invent new `TYPE`s and use them in every way that the predefined 
`TYPE`s can be used. A program-defined `TYPE` is called a `NEWTYPE`. 
New `PRIMTYPE`s cannot be invented except by changing the interpreter; 
thus the `TYPEPRIM` of a `NEWTYPE` must be chosen from those already 
available. But the name of a `NEWTYPE` (an `ATOM` of course) can be 
chosen freely -- so long as it does not conflict with an existing 
`TYPE` name. More importantly, the program that defines a `NEWTYPE` 
can be included in a set of programs for manipulating objects of the 
`NEWTYPE` in ways that are more meaningful than the predefined `SUBR`s 
of MDL.

Typically an object of a `NEWTYPE` is a structure that is a model of 
some entity in the real world -- or whatever world the program is 
concerned with -- and the elements of the structure are models of 
parts or aspects of the real-world entity. A `NEWTYPE` definition is a 
convenient way of formalizing this correspondence, of writing it down 
for all to see and use rather than keeping it in your head. If the 
defining set of programs provides functions for manipulating the 
`NEWTYPE` objects in all ways that are meaningful for the intended 
uses of the `NEWTYPE`, then any other program that wants to use the 
`NEWTYPE` can call the manipulation functions for all its needs, and 
it need never know or care about the internal details of the `NEWTYPE` 
objects. This technique is a standard way of providing modularity and 
abstraction.

For example, suppose you wanted to deal with airline schedules. If you 
were to construct a set of programs that define and manipulate a 
`NEWTYPE` called `FLIGHT`, then you could make that set into a 
standard package of programs and call on it to handle all information 
pertaining to scheduled airline flights. Since all `FLIGHT`s would 
have the same quantity of information (more or less) and you would 
want quick access to individual elements, you would not want the 
`TYPEPRIM` to be `LIST`. Since the elements would be of various 
`TYPE`s, you would not the `TYPEPRIM` to be `UVECTOR` -- nor its 
variations `STRING` or `BYTES`. The natural choice would be a 
`TYPEPRIM` of `VECTOR` (although you could gain space and lose time 
with `TEMPLATE` instead).

Now, the individual elements of a `FLIGHT` would, no doubt, have 
`TYPE`s and meanings that don't change. The elements of a `FLIGHT` 
might be airline code, flight number, originating-airport code, list 
of intermediate stops, destination-airport code, type of aircraft, 
days of operation, etc. Each and every `FLIGHT` would have the airline 
code for its first element (say), the flight number for its second, 
and so on. It is natural to invent names (`ATOM`s) for these elements 
and always refer to the elements by name. For example, you could 
`<SETG AIRLINE 1>` or `<SETG AIRLINE <OFFSET 1 FLIGHT>>` -- and in 
either case `<MANIFEST AIRLINE>` so the compiler can generate more 
efficient code. Then, if the local value of `F` were a `FLIGHT`, 
`<AIRLINE .F>` would return the airline code, and `<AIRLINE .F AA>` 
would set the airline code to `AA`. Once that is done, you can forget 
about which element comes first: all you need to know are the names of 
the offsets.

The next step is to notice that, outside the package of `FLIGHT` 
functions, no one needs to know whether `AIRLINE` is just an offset or 
in fact a function of some kind. For example, the scheduled duration 
of a flight might not be explicitly stored in a `FLIGHT`, just the 
scheduled times of departure and arrival. But, if the package had the 
proper `DURATION` function for calculating the duration, then the call 
`<DURATION .F>` could return the duration, no matter how it is found. 
In this way the internal details of the package are conveniently 
hidden from view and abstracted away.

The form of `NEWTYPE` definition allows for the `TYPE`s of all 
components of a `NEWTYPE` to be declared (chapter 14), for use both by 
a programmer while debugging programs that use the `NEWTYPE` and by 
the compiler for generating faster code. It is very convenient to have 
the type declaration in the `NEWTYPE` definition itself, rather than 
replicating it everywhere the `NEWTYPE` is used. (If you think this 
declaration might be obtrusive while debugging the programs in the 
`NEWTYPE` package, when inconsistent improvements are being made to 
various programs, you can either dissociate any declaration from the 
`NEWTYPE` or turn off MDL type-checking completely. Actually this 
declaration is typically more useful to a programmer during 
development than it is to the compiler.)

```no-highlight
<NEWTYPE atom type>
```

returns *atom*, after causing it to become the representation of a 
brand-new `TYPE` whose `PRIMTYPE` is `<TYPEPRIM type>`. What `NEWTYPE` 
actually does is make *atom* a legal argument to `CHTYPE` and 
`TYPEPRIM`. (Note that names of new `TYPE`s can be blocked lexically 
to prevent collision with other names, just like any other `ATOM`s -- 
chapter 15.) Objects of a `NEWTYPE`-created `TYPE` can be generated by 
creating an object of the appropriate `PRIMTYPE` and using `CHTYPE`. 
They will be `PRINT`ed (initially), and can be directly typed in, by 
the use of "# notation" as described above. `EVAL` of any object whose 
`TYPE` was created by `NEWTYPE` is initially the object itself, and, 
initially, you cannot `APPLY` something of a generated `TYPE` to 
arguments. But see below.

Examples:

```no-highlight
<NEWTYPE GARGLE FIX>$
GARGLE
<TYPEPRIM GARGLE>$
WORD
<SET A <CHTYPE 1 GARGLE>>$
#GARGLE *000000000001*
<SET B #GARGLE 100>$
#GARGLE *000000000144*
<TYPE .B>$
GARGLE
<PRIMTYPE .B>$
WORD
```

### 6.4.4 PRINTTYPE, EVALTYPE and APPLYTYPE

```no-highlight
<PRINTTYPE type how>
```

```no-highlight
<EVALTYPE type how>
```

```no-highlight
<APPLYTYPE type how>
```

all return *type*, after specifying *how* MDL is to deal with it.

These three `SUBR`s can be used to make newly-generated `TYPE`s behave 
in arbitrary ways, or to change the characteristics of standard MDL 
`TYPE`s. `PRINTTYPE` tells MDL how to print *type*, `EVALTYPE` how to 
evaluate it, and `APPLYTYPE` how to apply it in a `FORM`.

*how* can be either a `TYPE` or something that can be applied to 
arguments.

If *how* is a `TYPE`, MDL will treat *type* just like the `TYPE` given 
as *how*. *how* must have the same `TYPEPRIM` as *type*.

If *how* is applicable, it will be used in the following way:

For `PRINTTYPE`, *how* should take one argument: the object being 
output. *how* should output something without formatting 
(`PRIN1`-style); its result is ignored. (Note: *how* cannot use an 
output `SUBR` on *how*'s own *type*: endless recursion will result. 
`OUTCHAN` is bound during the application to the `CHANNEL` in use, or 
to a pseudo-internal channel for `FLATSIZE` -- chapter 11.) If *how* 
is the `SUBR` `PRINT`, *type* will receive no special treatment in 
printing, that is, it will be printed as it was in an initial MDL or 
immediately after its defining `NEWTYPE`.

For `EVALTYPE`, *how* should take one argument: the object being 
evaluated. The value returned by *how* will be used as `EVAL` of the 
object. If *how* is the `SUBR` `EVAL`, *type* will receive no special 
treatment in its evaluation.

For `APPLYTYPE`, *how* should take at least one argument. The first 
argument will be the object being applied: the rest will be the 
objects it was given as arguments. The result returned by *how* will 
be used as the result of the application. If *how* is the `SUBR` 
`APPLY`, *type* will receive no special treatment in application to 
arguments.

If any of these `SUBR`s is given only one argument, that is if *how* 
is omitted, it returns the currently active *how* (a `TYPE` or an 
applicable object), or else `#FALSE ()` if *type* is receiving no 
special treatment in that operation.

Unfortunately, these examples are fully understandable only after you 
have read through chapter 11.

```no-highlight
<DEFINE ROMAN-PRINT (NUMB)
<COND (<OR <L=? .NUMB 0> <G? .NUMB 3999>>
       <PRINC <CHTYPE .NUMB TIME>>)
      (T
       <RCPRINT </ .NUMB 1000> '![!\M]>
       <RCPRINT </ .NUMB  100> '![!\C !\D !\M]>
       <RCPRINT </ .NUMB   10> '![!\X !\L !\C]>
       <RCPRINT    .NUMB       '![!\I !\V !\X]>)>>$
ROMAN-PRINT

<DEFINE RCPRINT (MODN V)
<SET MODN <MOD .MODN 10>>
<COND (<==? 0 .MODN>)
      (<==? 1 .MODN> <PRINC <1 .V>>)
      (<==? 2 .MODN> <PRINC <1 .V>> <PRINC <1 .V>>)
      (<==? 3 .MODN> <PRINC <1 .V>> <PRINC <1 .V>> <PRINC <1 .V>>)
      (<==? 4 .MODN> <PRINC <1 .V>> <PRINC <2 .V>>)
      (<==? 5 .MODN> <PRINC <2 .V>>)
      (<==? 6 .MODN> <PRINC <2 .V>> <PRINC <1 .V>>)
      (<==? 7 .MODN> <PRINC <2 .V>> <PRINC <1 .V>> <PRINC <1 .V>>)
      (<==? 8 .MODN>
       <PRINC <2 .V>>
       <PRINC <1 .V>>
       <PRINC <1 .V>>
       <PRINC <1 .V>>)
      (<==? 9 .MODN> <PRINC <1 .V>> <PRINC <3 .V>>)>>$
RCPRINT

<PRINTTYPE TIME FIX> ;"fairly harmless but necessary here"$
TIME
<PRINTTYPE FIX ,ROMAN-PRINT>    ;"hee hee!"$
FIX
<+ 2 2>$
IV
1984$
MCMLXXXIV
<PRINTTYPE FIX ,PRINT>$
FIX

<NEWTYPE GRITCH LIST>   ;"a new TYPE of PRIMTYPE LIST"$
GRITCH
<EVALTYPE GRITCH>$
#FALSE ()
<EVALTYPE GRITCH LIST>  ;"evaluated like a LIST"$
GRITCH
<EVALTYPE GRITCH>$
LIST
#GRITCH (A <+ 1 2 3> !<SET A "ABC">)    ;"Type in one."$
#GRTICH (A 6 !\A !\B !\C)

<NEWTYPE HARRY VECTOR>  ;"a new TYPE of PRIMTYPE VECTOR"$
HARRY
<EVALTYPE HARRY #FUNCTION ((X) <1 .X>)>
    ;"When a HARRY is EVALed, return its first element."$
HARRY
#HARRY [1 2 3 4]$
1

<NEWTYPE WINNER LIST>   ;"a TYPE with funny application"$
WINNER
<APPLYTYPE WINNER>$
#FALSE ()
<APPLYTYPE WINNER <FUNCTION (W "TUPLE" T) (!.W !.T)>>$
WINNER
<APPLYTYPE WINNER>$
#FUNCTION ((W "TUPLE" T (!.W !.T))
<#WINNER (A B C) <+ 1 2> q>$
(A B C 3 q)
```

The following sequence makes MDL look just like Lisp. (This example is 
understandable only if you know Lisp (Moon, 1974); it is included only 
because it is so beautiful.)

```no-highlight
<EVALTYPE LIST FORM>$
LIST
<EVALTYPE ATOM ,LVAL>$
ATOM
```

So now:

```no-highlight
(+ 1 2)$
3
(SET 'A 5)$
5
A$
5
```

To complete the job, of course, we would have to do some `SETG`'s: 
`car` is `1`, `cdr` is `,REST`, and `lambda` is `,FUNCTION`. If you 
really do this example, you should "undo" it before continuing:

```no-highlight
<EVALTYPE 'ATOM ,EVAL>$
ATOM
<EVALTYPE LIST ,EVAL>$
LIST
```
