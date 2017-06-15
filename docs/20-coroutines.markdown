# Chapter 20. Coroutines

This chapter purports to explain the coroutine primitives of MDL. It
does make some attempt to explain coroutines as such, but only as
required to specify the primitives. If you are unfamiliar with the
basic concepts, confusion will probably reign.

A coroutine in MDL is implemented by an object of `TYPE` `PROCESS`. In
this manual, this use of the word "process" is distinguished by a
capitalization from its normal use of denoting an operating-system
process (which various systems call a process, job, fork, task, etc.).

MDL's built-in coroutine primitives do not include a "time-sharing
system". Only one `PROCESS` is ever running at a time, and control is
passed back and forth between `PROCESS`es on a coroutine-like basis.
The primitives are sufficient, however, to allow the writing of a
"time-sharing system" **in MDL**, with the additional use of the MDL
interrupt primitives. This has, in fact, been done.

## 20.1. PROCESS (the TYPE)

A `PROCESS` is an object which contains the "current state" of a
computation. This includes the `LVAL`s of `ATOM`s ("bindings"),
"depth" of functional application, and "position" within the
application of each applied function. Some of the things which are
**not** part of any specific `PROCESS` are the `GVAL`s of `ATOM`s,
associations (`ASOC`s), and the contents of `OBLIST`s. `GVAL`s (with
`OBLIST`s) are a chief means of communication and sharing between
`PROCESS`es (all `PROCESS`es can refer to the `SUBR` which is the
`GVAL` of `+`, for instance.) Note that an `LVAL` in one `PROCESS`
cannot easily be directly referenced from another `PROCESS`.

A `PROCESS` `PRINT`s as `#PROCESS` *p*, where *p* is a `FIX` which
uniquely identifies the `PROCESS`; *p* is the "`PROCESS` number" typed
out by `LISTEN`. A `PROCESS` cannot be read in by `READ`.

The term "run a `PROCESS`" will be used below to mean "perform some
computation, using the `PROCESS` to record the intermediate state of
that computation".

N.B.: A `PROCESS` is a rather large object; creating one will often
cause a garbage collection.

## 20.2. STATE of a PROCESS

    <STATE process>

returns an `ATOM` (in the `ROOT` `OBLIST`) which indicates the "state"
of the `PROCESS` *process*. The `ATOM`s which `STATE` can return, and
their meanings, are as follows:

- `RUNABLE` (sic) -- *process* has never ever been run.
- `RUNNING` -- *process* is currently running, that is, it did the
application of `STATE`.
- `RESUMABLE` -- *process* has been run, is not currently running, and
can run again.
- `DEAD` -- *process* has been run, but it can **not** run again; it
has "terminated".

In addition, an interrupt (chapter 21) can be enabled to detect the
time at which a `PROCESS` becomes "blocked" (waiting for terminal
input) or "unblocked" (terminal input arrived). (The `STATE` `BLOCKED`
has not been implemented.)

## 20.3. PROCESS (the SUBR)

    <PROCESS starter:applicable>

creates and returns a new `PROCESS` but does **not** run it; the
`STATE` of the returned `PROCESS` is `RUNABLE` (sic).

*starter* is something applicable to **one** argument, which must be
evaluated. *starter* is used both in starting and "terminating" a
`PROCESS`. In particular, if the *starter* of a `PROCESS` **ever**
returns a value, that `PROCESS` becomes `DEAD`.

## 20.4. RESUME

The `SUBR` `RESUME` is used to cause a computation to start or to
continue running in another `PROCESS`. An application of `RESUME`
looks like this:

    <RESUME retval:any process>

where *retval* is the "returned value" (see below) of the `PROCESS`
that does the `RESUME`, and *process* is the `PROCESS` to be started
or continued.

The *process* argument to `RESUME` is optional, by default the last
`PROCESS`, if any, to `RESUME` the `PROCESS` in which this `RESUME` is
applied. If and when the current `PROCESS` is later `RESUME`d by
another `PROCESS`, that `RESUME`'s *retval* is returned as the value
of this `RESUME`.

## 20.5. Switching PROCESSes

### 20.5.1. Starting Up a New PROCESS

Let us say that we are running in some `PROCESS`, and that this
original `PROCESS` is the `GVAL` of `P0`. Somewhere, we have evaluated

    <SETG P1 <PROCESS ,STARTER>>

where `,STARTER` is some appropriate function. Now, **in `,P0`** we
evaluate

    <RESUME .A ,P1>

and the following happens:

1. **In `,P0`** the arguments of the `RESUME` are evaluated: that is,
we get that `LVAL` of `A` which is current in `,P0` and the `GVAL` of
`P1`.
2. The `STATE` of `,P0` is changed to `RESUMABLE` and `,P0` is
"frozen" right where it is, in the middle of the `RESUME`.
3. The `STATE` of `,P1` is changed to `RUNNING`, and `,STARTER` is
applied to `,P0`'s `LVAL` of `A` **in `,P1`**. `,P1` now continues on
its way, evaluating the body of `,STARTER.`

The `.A` in the `RESUME` could have been anything, of course. The
important point is that, whatever it is, it is evaluated in `,P0`.

What happens next depends, of course, on what `,STARTER` does.

### 20.5.2. Top-level Return

Let us initially assume that `,STARTER` does nothing relating to
`PROCESS`es, but instead simply returns a value -- say *starval*. What
happens when `,STARTER` returns is this:

1. The `STATE` of `,P1` is changed to `DEAD`. `,P1` can never again be
`RESUME`d.
2. The last `PROCESS` to `RESUME` `,P1` is found, namely `,P0`, and
its `STATE` is changed to `RUNNING`.
3. *starval* is returned in `,P0` as the value of the original
`RESUME`, and `,P0` continues where it left off.

All in all, this simple case looks just like an elaborate version of
applying `,STARTER` to `.A` in `,P0`.

### 20.5.3. Symmetric RESUMEing

Now suppose that while still in `,P1`, the following is evaluated,
either in `,STARTER` or in something called by `,STARTER`:

    <RESUME .BAR ,P0>

This is what happens:

1. The arguments of the `RESUME` are evaluated **in `,P1`**.
2. The `STATE` of `,P1` is changed to `RESUMABLE`, and `,P1` is
"frozen" right in the middle of the `RESUME`.
3. The `STATE` of `,P0` is changed to `RUNNING`, and `,P1`'s `LVAL` of
`BAR` is returned as the value of **`,P0'`s** original `RESUME`
`,P0` then continues right where it left off.

This is **the** interesting case, because `,P0` can now do **another**
`RESUME` of `,P1`; this will "turn off" `,P0`, pass a value to `,P1`
and "turn on" `,P1`. `,P1` can now again `RESUME` `,P0`. which can
`RESUME` `,P1` back again, etc. **ad nauseam**, with everything done
in a perfectly symmetric manner. This can obviously also be done with
three or more `PROCESS`es in the same manner.

Note how this differs from normal functional application: you cannot
"return" from a function without destroying the state that function is
in. The whole point of `PROCESS`es is that you can "return"
(`RESUME`), remembering your state, and later continue where you left
off.

## 20.6. Example

```
;"Initially, we are in LISTEN in some PROCESS.
<DEFINE SUM3 (A)
        #DECL ((A) (OR FIX FLOAT>)
        <REPEAT ((S .A))
                #DECL ((S) <OR FIX FLOAT>)
                <SET S <+ .S <RESUME "GOT 1">>>
                <SET S <+ .S <RESUME "GOT 2">>>
                <SET S <RESUME .S>>>>$
SUM3
;"SUM3, used as the startup function of another PROCESS,
gets RESUMEd with numbers. It returns the sum of the last
three numbers it was given every third RESUME."
<SETG SUMUP <PROCESS ,SUM3>>$
;"Now we start SUMUP and give SUM3 its three numbers."
<RESUME 5 ,SUMUP>$
"GOT 1"
<RESUME 1 ,SUMUP>$
"GOT 2"
<RESUME 2 ,SUMUP>$
8
```

Just as a note, by taking advantage of MDL's order of evaluation, SUM3
could be have been written as:

```
<DEFINE SUM3 (A)
        <REPEAT ((S .A))
           #DECL ((A S0 <OR FIX FLOAT>)
           <SET S <RESUME <+ .S <RESUME "GOT 1"> <RESUME "GOT 2">>>>>>
```

## 20.7. Other Coroutining Features

### 20.7.1. BREAK-SEQ

    <BREAK-SEQ any process>

("break evaluation sequence") returns *process*, which must be
`RESUMABLE`, after having modified it so that when it is next
`RESUME`d, it will **first** evaluate *any* and **then** do an
absolutely normal `RESUME`; the value returned by any is thrown away,
and the value given by the `RESUME` is used normally.

If a `PROCESS` is `BREAK-SEQ`ed more than once between `RESUME`s,
**all** of the *any*s `BREAK-SEQ`ed onto it will be remembered and
evaluated when the `RESUME` is finally done. The *any*s will be
evaluated in "last-in first-out" order. The `FRAME` generated by
`EVAL`ing more than one *any* will have as its `FUNCT` the dummy
`ATOM` `BREAKER`.

### 20.7.2. MAIN

When you initially start up MDL, the `PROCESS` in which you are
running is slightly "special" in these two ways:

1. Any attempt to cause it become `DEAD` will be met with an error.
2. `<MAIN>` always returns that `PROCESS`.

The `PROCESS` number of `<MAIN>` is always `1`. The initial `GVAL` of
`THIS-PROCESS` is what `MAIN` always returns, `#PROCESS 1`.

### 20.7.3. ME

    <ME>

returns the `PROCESS` in which it is evaluated. The `LVAL` of
`THIS-PROCESS` in a `RUNABLE` (new) `PROCESS` is what `ME` always
returns.

### 20.7.4. RESUMER

    <RESUMER process>

returns the `PROCESS` which last `RESUME`d *process*. If no `PROCESS`
has ever `RESUME`d process, it returns `#FALSE ()`. *process* is
optional, `<ME>` by default. Note that `<MAIN>` does not ever have any
resumer. Example:

```
<PROG ((R <RESUMER>))           ;"not effective in <MAIN>"
   #DECL ((R) <OR PROCESS FALSE>)
   <AND .R
        <==? <STATE .R> RESUMABLE>
        <RESUME T .R>>>
```

### 20.7.5. SUICIDE

    <SUICIDE retval process>

acts just like `RESUME`, but clobbers the `PROCESS` (which cannot be
`<MAIN>`) in which it is evaluated to the `STATE` `DEAD`.

### 20.7.6. 1STEP

    <1STEP process>

returns *process*, after putting it into "single-step mode".

A `PROCESS` in single-step mode, whenever `RESUME`d, runs only until
an application of `EVAL` in it begins or finishes. At that point in
time, the `PROCESS` that did the `1STEP` is `RESUME`d, with a *retval*
which is a `TUPLE`. If an application of `EVAL` just began, the
`TUPLE` contains the `ATOM` `EVLIN` and the arguments to `EVAL`. If an
application of `EVAL` just finished, the `TUPLE` contains the `ATOM`
`EVLOUT` and the result of the evaluation.

*process* will remain in single-step mode until `FREE-RUN` (below) is
applied to it. Until then, it will stop before and after each `EVAL`
in it. Exception: if it is `RESUME`d from an `EVLIN` break with a
*retval* of `TYPE` `DISMISS` (`PRIMTYPE` `ATOM`), it will leave
single-step mode only until the current call to EVAL is about to
return. Thus lower-level `EVAL`s are skipped over without leaving the
mode. The usefulness of this mode in debugging is obvious.

### 20.7.7. FREE-RUN

    <FREE-RUN process>

takes its argument out of single-step mode. Only the `PROCESS` that
put *process* into single-step mode can take it out of the mode; if
another `PROCESS` tries, `FREE-RUN` returns a `FALSE`.

## 20.8. Sneakiness with PROCESSes

`FRAME`s, `ENVIRONMENT`s, `TAG`s, and `ACTIVATION`s are specific to
the `PROCESS` which created them, and each "knows its own father".
**Any** `SUBR` which takes these objects as arguments can take one
which was generated by **any** `PROCESS`, no matter where the `SUBR`
is really applied. This provides a rather sneaky means of crossing
between `PROCESS`es. The various cases are as follows:

`GO`, `RETURN`, `AGAIN`, and `ERRET`, given arguments which lie in
another `PROCESS`, each effectively "restarts" the `PROCESS` of its
argument and acts as if it were evaluated over there. If the `PROCESS`
in which it was executed is later `RESUME`d, it **returns** a value
just like `RESUME`!

`SET`, `UNASSIGN`, `BOUND?`, `ASSIGNED?`, `LVAL`, `VALUE`, and `LLOC`,
given optional `ENVIRONMENT` arguments which lie in another `PROCESS`,
will gleefully change, or return, the local values of `ATOM`s in the
other `PROCESS`. The optional argument can equally well be a
`PROCESS`, `FRAME`, or `ACTIVATION` in another `PROCESS`; in those
cases, each uses the `ENVIRONMENT` which is current in the place
specified.

`FRAME`, `ARGS`, and `FUNCT` will be glad to return the `FRAME`s,
argument `TUPLE`s, and applied Subroutine names of another `PROCESS`.
If one is given a `PROCESS` (including `<ME>`) as an argument instead
of a `FRAME`, it returns all or the appropriate part of the topmost
`FRAME` on that `PROCESS`'s control stack.

If `EVAL` is applied in `PROCESS` `P1` with an `ENVIRONMENT` argument
from a `PROCESS` `P2`, it will do the evaluation **in `P1`** but with
`P2`'s `ENVIRONMENT` (!). That is, the other `PROCESS`'s `LVAL`s, etc.
will be used, but (1) any **new** `FRAME`s needed in the course of the
evaluation will be created in `P1`; and (2) **`P1`** will be `RUNNING`
-- not `P2`. Note the following: if the `EVAL` in `P1` eventually
causes a `RESUME` of `P2`, `P2` could functionally return to below the
point where the `ENVIRONMENT` used in `P1` is defined; a `RESUME` of
`P1` at this point would cause an `ERROR` due to an invalid
`ENVIRONMENT`. (Once again, `LEGAL?` can be used to forestall this.)

## 20.9. Final Notes

1. A `RESUMABLE` `PROCESS` can be used in place of an `ENVIRONMENT` in
any application. The "current" `ENVIRONMENT` of the `PROCESS` is
effectively used.
2. `FRAME`s and `ENVIRONMENT`s can be `CHTYPE`d arbitrarily to one
another, or an `ACTIVATION` can be `CHTYPE`d to either of them, and
the result "works". Historically, these different `TYPE`s were first
used with different `SUBR`s -- `FRAME` with `ERRET`, `ENVIRONMENT`
with `LVAL`, `ACTIVATION` with `RETURN` -- hence the invention of
different `TYPE`s with similar properties.
3. Bugs in multi-`PROCESS` programs usually exhibit a degree of
subtlety and nastiness otherwise unknown to the human mind. If when
attempting to work with multiple processes you begin to feel that you
are rapidly going insane, you are in good company.