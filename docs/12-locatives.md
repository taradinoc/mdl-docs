# Chapter 12. Locatives

There is in MDL a facility for obtaining and working directly with
objects which roughly correspond to "pointers" in assembly language
or "lvals" in BCPL or PAL. In MDL, these are generically known as
**locatives** (from "location") and are of several `TYPE`s, as
mentioned below. Locatives exist to provide efficient means for
altering structures: direct replacement as opposed to re-copying.

Locatives **always** refer to elements in structures. It is not
possible to obtain a locative to something (for example, an `ATOM`)
which is not part of any structured. It is possible to obtain a
locative to any element in any structured object in MDL -- even to
associations (chapter 13) and to the values of `ATOM`s, structurings
which are normally "hidden".

In the following, the object occupying the structured position to
which you have obtained a locative will be referred to as the object
**pointed to** by the locative.

## 12.1. Obtaining Locatives

### 12.1.1. LLOC

	<LLOC atom env>

returns a locative (`TYPE` `LOCD`, "locative to iDentifier") to the
`LVAL` of *atom* in *env*. If *atom* is not bound in *env*, an error
occurs. *env* is optional, with the current `ENVIRONMENT` used by
default. The locative returned by `LLOC` is **independent of future
re-bindings** of *atom*. That is, `IN` (see below) of that locative
will return the same thing even if *atom* is re-bound to something
else; `SETLOC` (see below) will affect only that particular binding
of *atom*.

Since bindings are kept on a stack (tra la), any attempt to use a
locative to an `LVAL` which has become unbound will fetch up an
error. (It breaks just like a `TUPLE`....) `LEGAL?` can, once again,
be used to see if a `LOCD` is valid. Caution: `<SET A <LLOC A>>`
creates a self-reference and can make `PRINT` very unhappy.

### 12.1.2. GLOC

	<GLOC atom pred>

returns a locative (`TYPE` `LOCD`) to the `GVAL` of *atom*. If *atom*
has no `GVAL` **slot**, an error occurs, unless *pred* (optional) is
given and not `FALSE`, in which case a slot is created (chapter 22).
Caution: `<SETG A <GLOC A>>` creates a self-reference and can make
`PRINT` very unhappy.

### 12.1.3. AT

	<AT structured N:fix-or-offset>

returns a locative to the <em>N</em>th element in *structured*. *N*
is optional, `1` by default. The exact `TYPE` of the locative
returned depends on the `PRIMTYPE` of *structured*: `LOCL` for
`LIST`, `LOCV` for `VECTOR`, `LOCU` for `UVECTOR`, `LOCS` for
`STRING`, `LOCB` for `BYTES`, `LOCT` for `TEMPLATE`, and `LOCA` for
`TUPLE`. If *N* is greater than `<LENGTH structured>` or less than
`1`, or an `OFFSET` with a Pattern that doesn't match *structured*,
an error occurs. The locative is unaffected by applications of
`REST`, `BACK`, `TOP`, `GROW`, etc. to *structured*.

### 12.1.4. GETPL and GETL

	<GETPL item:any indicator:any default:any>

returns a locative (`TYPE` `LOCAS`) to the association of *item*
under *indicator*. (See chapter 13 for information about
associations.) If no such association exists, `GETPL` returns `EVAL`
of *default*. *default* is optional, `#FALSE ()` by default.

`GETPL` corresponds to `GETPROP` amongst the association machinery.
There also exists `GETL`, which corresponds to `GET`, returning
either a `LOCAS` or a locative to the *indicator*th element of a
structured *item*. `GETL` is like `AT` if *item* is a structure and
*indicator* is a `FIX` or `OFFSET`, and like `GETPL` if not.

## 12.2. LOCATIVE?

This `SUBR` is a predicate that tells whether or not is argument is a
locative. It is cheaper than `<MEMQ <PRIMTYPE arg> '![LOCD LOCL
...]>`.

## 12.3. Using Locatives

The following two `SUBR`s provide the means for working with
locatives. They are independent of the specific `TYPE` of the
locative. The notation *locative* indicates anything which could be
returned by `LLOC`, `GLOC`, `AT`, `GETPL` or `GETL`.

### 12.3.1. IN

	<IN locative>

returns the object to which *locative* points. The only way you can
get an error using `IN` is when *locative* points to an `LVAL` which
has become unbound from an `ATOM`. This is the same as the problem in
referencing `TUPLE`s as mentioned in section 9.2, and it can be
avoided by first testing `<LEGAL? locd>`.

Example:

	<SET A 1>$
	1
	<IN <LLOC A>>$
	1

### 12.3.2. SETLOC

	<SETLOC locative any>

returns *any*, after having made *any* the contents of that position
in a structure pointed to by *locative*. The structure itself is not
otherwise disturbed. An error occurs if *locative* is to a
non-`LEGAL?` `LVAL` or if you try to put an object of the wrong
`TYPE` into a `PRIMTYPE` `UVECTOR`, `STRING`, `BYTES`, or `TEMPLATE`.

Example:

	<SET A (1 2 3)>$
	(1 2 3)
	<SETLOC <AT .A 2> HI>$
	HI
	.A$
	(1 HI 3)

## 12.4. Note on Locatives

You may have noticed that locatives are, strictly speaking,
unnecessary; you can do everything locatives allow by appropriate use
of, for example, `SET`, `LVAL`, `PUT`, `NTH`, etc. What locatives
provide is generality.

Basically, how you obtained a locative is irrelevant to `SETLOC` and
`IN`; thus the same program can play with `GVAL`s, `LVAL`s, object in
explicit structures, etc., without being bothered by what function it
should use to do so. This is particularly true with respect to
locatives to `LVAL`s; the fact that they are independent of changes
in binding can save a lot of fooling around with `EVAL` and
`ENVIRONMENT`s.
