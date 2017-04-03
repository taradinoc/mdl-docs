# Chapter 13. Association (Properties)

There is an "associative" data storage and retrieval system embedded
in MDL which allows the construction of data structures with
arbitrary selectors. It is used via the `SUBR`s described in this
chapter.

## 13.1. Associative Storage

### 13.1.1. PUTPROP

	<PUTPROP item:any indicator:any value:any>

("put property") returns *item*, having associated *value* with
*item* under the indicator *indicator*.

### 13.1.2. PUT

	<PUT item:any indicator:any value:any>

is identical to `PUTPROP`, except that, if *item* is structured
**and** *indicator* is of `TYPE` `FIX` or `OFFSET`, it does `<SETLOC
<AT item indicator> value>`. In other words, an element with an
integral selector is stored in the structure itself, instead of in
association space. `PUT` (like `AT`) will get an error if *indicator*
is out of range; `PUTPROP` will not.

### 13.1.3. Removing Associations

If `PUTPROP` is used **without** its *value* argument, it removes any
association existing between its *item* argument and its *indicator*
argument. If an association did exist, using `PUTPROP` in this way
returns the *value* which was associated. If no association existed,
it returns `#FALSE ()`.

`PUT`, with arguments which refer to association, can be used in the
same way.

If either *item* or *indicator* cease to exist (that is, no one was
pointing to them, so they were garbage-collected), and no locatives
to the association exist, then the association between them ceases to
exist (is garbage-collected).

## 13.2. Associative Retrieval

### 13.2.1. GETPROP

	<GETPROP item:any indicator:any exp:any>

("get property") returns the *value* associated with *item* under
*indicator*, if any. If there is no such association, `GETPROP`
returns `EVAL` of *exp* (that is, *exp* gets `EVAL`ed both at call
time and later).

*exp* is optional. If not given, `GETPROP` returns `#FALSE ()` if it
cannot return a *value*.

Note: *item* and *indicator* in `GETPROP` must be the **same MDL
objects** used to establish the association; that is, they must be
`==?` to the objects used by `PUTPROP` or `PUT`.

### 13.2.2. GET

	<GET item:any indicator:any exp:any>

is the inverse of `PUT`, using `NTH` or `GETPROP` depending on the
test outlined in section 13.1.2. *exp* is optional and used as in
`GETPROP`.

## 13.3. Examples of Association

	<SET L '(1 2 3 4)>$
	(1 2 3 4)
	<PUT .L FOO "L is a list.">$
	(1 2 3 4)
	<GET .L FOO>$
	"L is a list."
	<PUTPROP .L 3 '![4]>$
	(1 2 3 4)
	<GETPROP .L 3>$
	![4!]
	<GET .L 3>$
	3
	<SET N 0>$
	0
	<PUT .N .L "list on a zero">$
	0
	<GET .N '(1 2 3 4)>$
	#FALSE ()

The last example failed because `READ` generated a new `LIST` -- not
the one which is `L`'s `LVAL`. However,

	<GET 0 .L>$
	"list on a zero"

works because `<==? .N 0>` is true.

To associate something with the Nth **position** in a structure, as
opposed to its Nth **element**, associate it with `<REST structure
N-1>`, as in the following:

	<PUT <REST .L 3> PERCENT 0.3>$
	(3 4)
	<GET <2 .L> PERCENT>$
	#FALSE ()
	<GET <REST .L 2> PERCENT>$
	0.30000000

Remember comments?

	<SET N '![A B C ;"third element" D E]>$
	![A B C D E!]
	<GET <REST .N 2> COMMENT>$
	"third element"

The `'` in the `<SET N ... >` is to keep `EVAL` from generating a new
`UVECTOR` ("Direct Representation"), which would not have the comment
on it (and which would be a needless duplicate). A "top-level"
comment -- one attached to the entire object returned by `READ` -- is
`PUT` on the `CHANNEL` in use, since there is no position in any
structure for it. If no top-level comment follows the object, `READ`
removes the value (`<PUT channel COMMENT>`); so anybody that wants to
see a top-level comment must look for it after each `READ`.

If you need to have a structure with selectors in more than one
dimension (for example, a sparse matrix that does not deserve to be
linearized), associations can be cascaded to achieve the desired
result. In effect an extra level of indirection maps two indicators
into one. For example, to associate *value* with *item* under
*indicator-1* and *indicator-2* simultaneously:

	<PUTPROP indicator-1 indicator-2 T>
	<PUTPROP item <GETPL indicator-1 indicator-2> value>

## 13.4. Examining Associations

Associations (created by `PUT` and `PUTPROP`) are chained together in
a doubly-linked list, internal to MDL. The order of associations in
the chain is their order of creation, newest first. There are several
`SUBR`s for examining the chain of associations. `ASSOCIATIONS`
returns the first association in the chain, or `#FALSE ()` if there
are none. `NEXT` takes an association as an argument and returns the
next association in the chain, or `#FALSE ()` if there are no more.
`ITEM`, `INDICATOR` and `AVALUE` all take an association as an
argument and return the item, indicator and value, respectively.
Associations print as:

	#ASOC (item indicator value)

(sic: only one `S`). Example: the following gathers all the existing
associations into a `LIST`.

	<PROG ((A <ASSOCIATIONS>))
	 <COND (<NOT .A> '())
	       (T (.A !<MAPF ,LIST
	                <FUNCTION () <COND (<SET A <NEXT .A>> .A)
	                                   (T <MAPSTOP>)>>>))>>
