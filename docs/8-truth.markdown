# Chapter 8. Truth

## 8.1 Truth Values [1]

MDL represents "false" with an object of a particular `TYPE`: `TYPE` 
`FALSE` (unsurprisingly). `TYPE` `FALSE` is structured: its `PRIMTYPE` 
is `LIST`. Thus, you can give reasons or excuses by making them 
elements of a `FALSE`. (Again, `EVAL`ing a `FALSE` neither copies it 
nor `EVAL`s its elements, so it is not necessary to `QUOTE` a `FALSE` 
appearing in a program.) Objects of `TYPE` `FALSE` are represented in 
"# notation":

```no-highlight
#FALSE list-of-its-elements
```

The empty `FORM` evaluates to the empty `FALSE`:

```no-highlight
<>$
#FALSE ()
```

Anything which is not `FALSE`, is, reasonably enough, true. In this 
document the "data type" *false-or-any* in metasyntactic variables 
means that the only significant attribute of the object in that 
context is whether its `TYPE` is `FALSE` or not.

## 8.2 Predicates [1]

There are numerous MDL F/SUBRs which can return a `FALSE` or a true. 
See appendix 2 to find them all. Most return either `#FALSE ()` or the 
`ATOM` with `PNAME` `T`. (The latter is for historical reasons, namely 
Lisp (Moon, 1974).) Some predicates which are meaningful now are 
described next.

### 8.2.1 Arithmetic [1]

```no-highlight
<0? fix-or-float>
```

evaluates to `T` only if its argument is identically equal to `0` or 
`0.0`.

```no-highlight
<1? fix-or-float>
```

evaluates to `T` only if its argument is identically equal to `1` or 
`1.0`.

```no-highlight
<G? n:fix-or-float m:fix-or-float>
```

evaluates to `T` only if *n* is algebraically greater than *m*. `L=?` 
is the Boolean complement of `G?`; that is, it is `T` only if *n* is 
not algebraically greater than *m*.

```no-highlight
<L? n:fix-or-float m:fix-or-float>
```

evaluates to `T` only if *n* is algebraically less than *m*. `G=?` is 
the Boolean complement of `L?`.

### 8.2.2 Equality and Membership [1]

```no-highlight
<==? e1:any e2:any>
```

evaluates to `T` only if *e1* is the **same object** as *e2* (appendix 
1). Two objects that look the same when `PRINT`ed may not be `==?`. 
Two `FIX`es of the same "value" are "the same object"; so are two 
`FLOAT`s of **exactly** the same "value". Empty objects of `PRIMTYPE` 
`LIST` (and no other structured `PRIMTYPE`) are `==?` if their `TYPE`s 
are the same. Example:

```no-highlight
<==? <SET X "RANDOM STRING"> <TOP <REST .X 6>>>$
T
<==? .X "RANDOM STRING">$
#FALSE ()
```

`N==?` is the Boolean complement of `==?`.

```no-highlight
<=? e1:any e2:any>
```

evaluates to `T` if *e1* and *e2* have the same `TYPE` and are 
structurally equal -- that is, they "look the same", their printed 
representations are the same. `=?` is much slower than `==?`. `=?` 
should be used only when its characteristics are necessary: they are 
not in any comparisons of unstructured objects. `==?` and `=?` always 
return the same value for `FIX`es, `FLOAT`s, `ATOM`s, etc. 
(Mnemonically, `==?` tests for "more equality" than `=?`; in fact, it 
tests for actual physical identity.)

Example, illustrating non-copying of a `SEGMENT` in Direct 
Representation of a `LIST`:

```no-highlight
<SET A '(1 2 3)>$
(1 2 3)
<==? .A (!.A)>$
T
<==? .A <SET B <LIST !.A>>>$
#FALSE ()
<=? .A .B>$
T
```

`N=?` is the Boolean complement of `=?`.

```no-highlight
<MEMBER object:any structured>
```

runs down *structured* from first to last element, comparing each 
element of *structured* with *object*. If it finds an element of 
*structured* which is `=?` to *object*, it returns
`<REST structured i>` (which is of `TYPE` `<PRIMTYPE structured>`), 
where the (*i*+1)th element of *structured* is `=?` to *object*. That 
is, the first element of what it returns is the **first** element of 
*structured* that is `=?` to *object*.

If no element of *structured* is `=?` to *object*, `MEMBER` returns 
`#FALSE ()`.

The search is more efficient if *structured* is of `PRIMTYPE` `VECTOR` 
(or `UVECTOR`, if possible) than if it is of `PRIMTYPE` `LIST`. As 
usual, if *structured* is constant, it should be `QUOTE`d.

If *object* and *structured* are of `PRIMTYPE` `STRING` [or `BYTES`], 
`MEMBER` does a substring search. Example:

```no-highlight
<MEMBER "PART" "SUM OF PARTS">$
"PARTS"
```

`<MEMQ object:any structured>` ("member quick") is exactly the same as `MEMBER`, except that the comparison test is `==?`.

```no-highlight
<STRCOMP s1 s2>
```

("string comparison") can be given either two `STRING`s or two `ATOM`s 
as arguments. In the latter case the `PNAME`s are used. It actually 
isn't a predicate, since it can return three possible values: `0` if 
*s1* is `=?` to *s2*; `1` if *s1* sorts alphabetically after *s2*; and 
`-1` if *s1* sorts alphabetically before *s2*. "Alphabetically" means, 
in this case, according to the numeric order of ASCII, with the 
standard alphabetizing rules.

[A predicate suitable for an ascending `SORT` (which see) is 
`<G? <STRCOMP .ARG1 .ARG2> 0>`.]

### 8.2.3 Boolean Operators [1]

```no-highlight
<NOT e:false-or-any>
```

evaluates to `T` only if *e* evaluates to a `FALSE`, and to 
`#FALSE ()` otherwise.

```no-highlight
<AND e1 e2 ... eN>
```

`AND` is an `FSUBR`. It evaluates its arguments from first to last as 
they appear in the `FORM`. As soon as one of them evaluates to a 
`FALSE`, it returns that `FALSE`, ignoring any remaining arguments. If 
none of them evaluate to `FALSE`, it returns `EVAL` of its last 
argument. `<AND>` returns `T`. `AND?` is the `SUBR` equivalent to 
`AND`, that is, all its arguments are evaluated before any of them is 
tested.

```no-highlight
<OR e1 e2 ... eN>
```

`OR` is an `FSUBR`. It evaluates its arguments from first to last as 
they appear in the `FORM`. As soon as one of them evaluates to a 
non-`FALSE`, it returns that non-`FALSE` value, ignoring any remaining 
arguments. If this never occurs, it returns the last `FALSE` it saw. 
`<OR>` returns `#FALSE ()`. `OR?` is the `SUBR` equivalent to `OR`.

### 8.2.4 Object Properties [1]

```no-highlight
<TYPE? any type-1 ... type-N>
```

evaluates to *type-i* only if `<==? type-i <TYPE any>>` is true. It is 
faster and gives more information than `OR`ing tests for each `TYPE`. 
If the test fails for all *type-i*'s, `TYPE?` returns `#FALSE ()`.

```no-highlight
<APPLICABLE? e>
```

evaluates to `T` only if *e* is of a `TYPE` that can legally be 
applied to arguments in a `FORM`, that is, be (`EVAL` of) the first 
element of a `FORM` being evaluated (appendix 3).

```no-highlight
<MONAD? e>
```

evaluates to `#FALSE ()` only if `NTH` and `REST` (with non-zero 
second argument) can be performed on its argument without error. An 
unstructured or empty structured object will cause `MONAD?` to return 
`T`.

```no-highlight
<STRUCTURED? e>
```

evaluates to `T` only if *e* is a structured object. It is **not** the 
inverse of `MONAD?`, since each returns `T` if its argument is an 
empty structure.

```no-highlight
<EMPTY? structured>
```

evaluates to `T` only if its argument, which must be a structured 
object, has no elements.

```no-highlight
<LENGTH? structured fix>
```

evaluates to `<LENGTH structured>` only if that is less than or equal 
to *fix*; otherwise, it evaluates to `#FALSE ()`. Mnemonically, you 
can think of the first two letters of `LENGTH?` as signifying the 
"less than or equal to" sense of the test.

This `SUBR` was invented to use on lists, because MDL can determine 
their lengths only by stepping along the list, counting the elements. 
If a program needs to know only how the length compares with a given 
number, `LENGTH?` will tell without necessarily stepping all the way 
to the end of the list, in contrast to `LENGTH`.

[If *structured* is a circular `PRIMTYPE` `LIST`, `LENGTH?` will 
return a value, whereas `LENGTH` will execute forever. To see if you 
can do `<REST structured <+ 1 fix>>` without error, do the test 
`<NOT <LENGTH? structured fix>>`.]

## 8.3 COND [1]

The MDL Subroutine which is most used for varying evaluation depending 
on a truth value is the `FSUBR` `COND` ("conditional"). A call to 
`COND` has this format:

```no-highlight
<COND clause-1:list ... clause-N:list>
```

where *N* is at least one.

`COND` always returns the result of the **last** evaluation it 
performs. The following rules determine the order of evaluations 
performed.

1. Evaluate the first element of each clause (from first to last) 
until either a non-`FALSE` object results or the clauses are 
exhausted.
2. If a non-`FALSE` object is found in (1), immediately evaluate the 
remaining elements (if any) of that clause and ignore any remaining 
clauses.

In other words, `COND` goes walking down its clauses, `EVAL`ing the 
first element of each clause, looking for a non-`FALSE` result. As 
soon as it finds a non-`FALSE`, it forgets about all the other clauses 
and evaluates, in order, the other elements of the current clause and 
returns the last thing it evaluates. If it can't find a non-`FALSE`, 
it returns the last `FALSE` it saw.

### 8.3.1 Examples

```no-highlight
<SET F '(1)>$
(1)
<COND (<EMPTY? .F> EMP) (<1? <LENGTH .F>> ONE)>$
ONE
<SET F ()>$
()
<COND (<EMPTY? .F> EMP) (<1? <LENGTH .F>> ONE)>$
EMP
<SET F '(1 2 3)>$
(1 2 3)
<COND (<EMPTY? .F> EMP) (<1? <LENGTH .F>> ONE)>$
#FALSE ()
<COND (<LENGTH? .F 2> SMALL) (BIG)>$
BIG

<DEFINE FACT (N)        ;"the standard recursive factorial"
        <COND (<0? .N> 1)
              (ELSE <* .N <FACT <- .N 1>>>)>>$
FACT
<FACT 5>$
120
```

## 8.4 Shortcuts with Conditionals

### 8.4.1 AND and OR as Short CONDs

Since `AND` and `OR` are `FSUBR`s, they can be used as miniature 
`COND`s. A construct of the form

```no-highlight
<AND pre-conditions action(s)>
```

or

```no-highlight
<OR pre-exclusions action(s)>
```

will allow *action(s)* to be evaluated only if all the 
*pre-conditions* are true or only if all the *pre-exclusions* are 
false, respectively. By nesting and using both `AND` and `OR`, fairly 
powerful constructs can be made. Of course, if *action(s)* are more 
than one thing, you must be careful that none but the last returns 
false or true, respectively. Watch out especially for `TERPRI` 
(chapter 11). Examples:

```no-highlight
<AND <ASSIGNED? FLAG> .FLAG <FCN .ARG>>
```

applies `FCN` only if someone else has `SET` `FLAG` to true. 
(`ASSIGNED?` is true if its argument `ATOM` has an `LVAL`.) No error 
can occur in the testing of `FLAG` because of the order of evaluation.

```no-highlight
<AND <SET C <OPEN "READ" "A FILE">> <LOAD .C> <CLOSE .C>>
```

effectively `FLOAD`s the file (chapter 11) without the possibility of 
getting an error if the file cannot be opened.

### 8.4.2 Embedded Unconditionals

One of the disadvantages of `COND` is that there is no straightforward 
way to do things unconditionally in between tests. One way around this 
problem is to insert a dummy clause that never succeeds, because its 
only `LIST` element is an `AND` that returns a `FALSE` for the test. 
Example:

```no-highlight
<COND   (<0? .N> <F0 .N>)
        (<1? .N> <F1 .N>)
        (<AND <SET N <* 2 <FIX </ .N 2>>>>
                        ;"Round .N down to even number."
              <>>)
        (<LENGTH? .VEC .N> '[])
        (T <REST .VEC <+ 1 .N>>)>
```

A variation is to make the last `AND` argument into the test for the 
`COND` clause. (That is, the third and fourth clauses in the above 
example can be combined.) Of course, you must be careful that no other 
`AND` argument evaluates to a `FALSE`; most Subroutines do not return 
a `FALSE` without a very good reason for it. (A notable exception is 
`TERPRI` (which see).) Even safer is to use `PROG` (section 10.1) 
instead of `AND`.

Another variation is to increase the nesting with a new `COND` after 
the unconditional part. At least this method does not make the code 
appear to a human reader as though it does something other than what 
it really does. The above example could be done this way:

```no-highlight
<COND   (<0? .N> <F0 .N>)
        (<1? .N> <F1 .N>)
        (T
         <SET N <* 2 <FIX </ .N 2>>>>
         <COND  (<LENGTH? .VEC .N> '[])
                (T <REST .VEC <+ 1 .N>>)>)>
```
