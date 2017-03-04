# Chapter 4. Values of Atoms

## 4.1 General [1]

There are two kinds of "value" which can be attached to an `ATOM`. An 
`ATOM` can have either, both, or neither. They interact in no way 
(except that alternately referring to one and then the other is 
inefficient). These two values are referred to as the **local value** 
and the **global value** of an `ATOM`. The terms "local" and "global" 
are relative to `PROCESS`es (chapter 20), not functions or programs. 
The `SUBR`s which reference the local and global values of an `ATOM`, 
and some of the characteristics of local versus global values, follow.

## 4.2 Global Values

### 4.2.1 SETG [1]

A global value can be assigned to an `ATOM` by the `SUBR` `SETG` ("set 
global"), as in

```no-highlight
<SETG atom any>
```

where *atom* must `EVAL` to an `ATOM`, and *any* can `EVAL` to 
anything. `EVAL` of the second argument becomes the global value of 
`EVAl` of the first argument. The value returned by the `SETG` is its 
second argument, namely the new global value of *atom*.

Examples:

```no-highlight
<SETG FOO <SETG BAR 500>>$
500
```

The above made the global values of both the `ATOM` `FOO` and the 
`ATOM` `BAR` equal to the `FIX`ed-point number 500.

```no-highlight
<SETG BAR FOO>$
FOO
```

That made the global value of the `ATOM` `BAR` equal to the `ATOM` 
`FOO`.

### 4.2.2 GVAL [1]

The `SUBR` `GVAL` ("global value") is used to reference the global 
value of an `ATOM`.

```no-highlight
<GVAL atom>
```

returns as a value the global value of *atom*. If *atom* does not 
evaluate to an `ATOM`, or if the `ATOM` to which it evaluates has no 
global value, an error occurs.

`GVAL` applied to an `ATOM` anywhere, in any `PROCESS`, in any 
function, will return the same value. Any `SETG` anywhere changes the 
global value for everybody. Global values are context-independent.

`READ` understands the character `,` (comma) as an abbreviation for an 
application of `GVAL` to whatever follows it. `PRINT` always 
translates an application of `GVAL` into the comma format. The 
following are absolutely equivalent:

```no-highlight
,atom        <GVAL atom>
```

Assuming the examples in section 4.2.1 were carried out in the order 
given, the following will evaluate as indicated:

```no-highlight
,FOO$
500
<GVAL FOO>$
500
,BAR$
FOO
,,BAR$
500
```

### 4.2.3 Note on SUBRs and FSUBRs

The initial `GVAL`s of the `ATOM`s used to refer to MDL "built-in" 
Subroutines are the `SUBR`s and `FSUBR`s which actually get applied 
when those `ATOM`s are referenced. If you don't like the way those 
supplied routines work, you are perfectly free to `SETG` the `ATOM`s 
to your own versions.

### 4.2.4 GUNASSIGN

```no-highlight
<GUNASSIGN atom>
```

("global unassign") causes *atom* to have no assigned global value, 
whether or not it had one previously. The storage used for the global 
value can become free for other uses.

## 4.3 Local Values

### 4.3.1 SET [1]

The `SUBR` `SET` is used to assign a local value to an `ATOM`. 
Applications of `SET` are of the form

```no-highlight
<SET atom any>
```

`SET` returns `EVAL` of *any* just like `SETG`.

Examples:

```no-highlight
<SET BAR <SET FOO 100>>$
100
```

Both `BAR` and `FOO` have been given local values equal to the 
`FIX`ed-point number 100.

```no-highlight
<SET FOO BAR>$
BAR
```

`FOO` has been given the local value `BAR`.

Note that neither of the above did anything to any global values `FOO` 
and `BAR` might have had.

### 4.3.2 LVAL [1]

The `SUBR` used to extract the local value of an `ATOM` is named 
`LVAL`. As with `GVAL`, `READ` understands an abbreviation for an 
application of `LVAL`: the character `.` (period), and `PRINT` 
produces it. The following two representations are equivalent, and 
when `EVAl` operates on the corresponding MDL object, it returns the 
current local value of *atom*:

```no-highlight
<LVAL atom>        .atom
```

The local value of an `ATOM` is unique within a `PROCESS`. `SET`ting 
an `ATOM` in one `PROCESS` has no effect on its `LVAL` in another 
`PROCESS`, because each `PROCESS` has its own "control stack" 
(chapters 20 and 22).

Assume **all** of the previous examples in this chapter have been 
done. Then the following evaluate as indicated:

```no-highlight
.BAR$
100
<LVAL BAR>$
100
.FOO$
BAR
,.FOO$
FOO
```

### 4.3.3 UNASSIGN

```no-highlight
<UNASSIGN atom>
```

causes *atom* to have no assigned local value, whether or not it had 
one previously.

## 4.4 VALUE

`VALUE` is a `SUBR` which takes an `ATOM` as an argument, and then:

1. if the `ATOM` has an `LVAL`, returns the `LVAL`;
2. if the `ATOM` has no `LVAL` but has a `GVAL`, returns the `GVAL`;
3. if the `ATOM` has neither a `GVAL` nor an `LVAL`, calls the `ERROR` function.

This order of seeking a value is the **opposite** of that used when an 
`ATOM` is the first element of a `FORM`. The latter will be called the 
G/LVAL, even though that name is not used in MDL.

Example:

```no-highlight
<UNASSIGN A>$
A
<SETG A 1>$
1
<VALUE A>$
1
<SET A 2>$
2
<VALUE A>$
2
,A$
1
```
