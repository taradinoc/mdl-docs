# Chapter 21. Interrupts

The MDL interrupt handling facilities provide the ability to say the
following: whenever "this event" occurs, stop whatever is being done
at the time and perform "this action"; when "this action" is finished,
continue with whatever was originally being done. "This event" can be
things like the typing of a character at a terminal, a time interval
ending, a `PROCESS` becoming blocked, or a program-defined and
-generated "event". "This action" is the application of a specified
`APPLICABLE` object to arguments provided by the MDL interrupt system.
The sets of events and actions can be changed in extremely flexible
ways, which accounts for both the variety of `SUBR`s and arguments,
and the rich interweaving of the topics in this chapter. Interrupt
handling is a kind of parallel processing: a program can be divided
into a "main-level" part and one or more interrupt handlers that
execute only when conditions are ripe.

## 21.1. Definitions of Terms

An **interrupt** is not an object in MDL, but rather a class of
events, for example, "ticks" of a clock, garbage collections, the
typing of a character at a terminal, etc.

An interrupt is said to **occur** when one of the events in its class
takes place.

An **external** interrupt is one whose occurrences are signaled to MDL
by the operating system, for example, "ticks" of a clock. An
**internal** interrupt is one whose occurrences are detected by MDL
itself, for example, garbage collections. MDL can arrange for the
operating system to not signal occurrences of an external interrupt to
it; then, as far as MDL is concerned, that interrupt does not occur.

Each interrupt has a **name** which is either a `STRING` (for example,
`"GC"`, `"CHAR"`, `"WRITE"`) or an `ATOM` with that `PNAME` in a
special `OBLIST`, named `INTERRUPTS!-`. (This `OBLIST` is returned by
`<INTERRUPTS>`.) Certain names must always be further specified by a
`CHANNEL` or a `LOCATIVE` to tell **which** interrupt by that name is
meant.

When an interrupt occurs, the interpreter looks for an association on
the interrupt's name. If there is an association, its `AVALUE` should
be an `IHEADER`, which heads a list of actions to be performed. In
each `IHEADER` is the name of the interrupt with which the `IHEADER`
is or was associated.

In each `IHEADER` is an element telling whether it is disabled. If an
`IHEADER` is **disabled**, then none of its actions is performed.
The opposite of disabled is **enabled**. It is sometimes useful to
disable an `IHEADER` temporarily, but removing its association with
the interrupt's name is better than long-term disabling. There are
`SUBR`s for creating an `IHEADER`, associating it with an interrupt,
and later removing the association.

In each `IHEADER` is a **priority**, a `FIX` greater than `0` which
specifies the interrupt's "importance". The processing of a
higher-priority (larger-numbered) interrupt will supersede the
processing of a lower-priority (smaller-numbered) interrupt until the
high-priority interrupt has been handled.

In each `IHEADER` is a (possibly empty) list of `HANDLER`s. (This list
is not a MDL `LIST`.) Each `HANDLER` corresponds to an action to
perform. There are `SUBR`s for creating a `HANDLER`, adding it to an
`IHEADER`'s list, and later removing it.

In each `HANDLER` is a function that we will call a **handler** (in
lower case), despite possible confusion, because that is really the
best name for it. An **action** consists of applying a handler to
arguments supplied by the interrupt system. The number and meaning of
the arguments depend on the name of the interrupt. In each `HANDLER`
is an element telling in which `PROCESS` the action should be
performed.

## 21.2. EVENT

    <EVENT name priority which>

creates and returns an enabled `IHEADER` with no `HANDLER`s. The
*name* may be an `ATOM` in the `INTERRUPTS` `OBLIST` or a `STRING`; if
it is a `STRING`, `EVENT` does a `LOOKUP` or `INSERT` in
`<INTERRUPTS>`. If there already is an `IHEADER` associated with
*name*, `EVENT` just returns it, ignoring the given *priority*.

*which* must be given only for certain *name*s:

* It must be a `CHANNEL` if and only if *name* is `"CHAR"` (or
`CHAR!-INTERRUPTS`). In this case it is the input `CHANNEL` from the
(pseudo-)terminal or Network socket whose received characters will
cause the interrupt to occur, or the output `CHANNEL` to the
pseudo-terminal or Network socket whose desired characters will cause
the interrupt to occur. (See below. Pseudo-terminals are not available
in the Tenex and Tops-20 versions.)
* The argument must be a `LOCATIVE` if and only if *name* is `"READ"`
(or `READ!-INTERRUPTS`) or `"WRITE"` (or `WRITE!-INTERRUPTS`). In this
case it specifies an object to be "monitored" for usage by
(interpreted) MDL programs (section 21.8.9).

If the interrupt is external, MDL arranges for the operating system to
signal its occurrences.

## 21.3. HANDLER (the SUBR)

    <HANDLER iheader applicable process>

creates a `HANDLER`, adds it to the front of *iheader*'s `HANDLER`
list (first action to be performed), and returns it as a value.
*applicable* may be any `APPLICABLE` object that takes the proper
number of arguments. (None of the arguments can be `QUOTE`d; they must
all be evaluated at call time.) *process* is the `PROCESS` in which
the handler will be applied, by default whatever `PROCESS` was running
when the interrupt occurred.

The value returned by the handler is ignored, unless it is of `TYPE`
`DISMISS` (`PRIMTYPE` `ATOM`), in which case none of the remaining
actions in the list will be performed.

The processing of an interrupt's actions can terminate prematurely if
a handler calls the `SUBR` `DISMISS` (see below.)

## 21.4. OFF

    <OFF iheader>

removes the association between *iheader* and the name of its
interrupt, and then disables *iheader* and returns it. (An error
occurs if there is no association.) If the interrupt is external, MDL
arranges for the operating system not to signal its occurrences.

    <OFF name which>

finds the `IHEADER` associated with *name* and proceeds as above,
returning the `IHEADER`. *which* must be given only for certain
*names*, as for `EVENT`. Caution: if you `<OFF "CHAR" ,INCHAN>`, MDL
will become deaf.

    <OFF handler>

returns *handler* after removing it from its list of actions. There is
no effect on any other `HANDLER`s in the list.

Now that you know how to remove `IHEADER`s and `HANDLER`s from their
normal places, you need to know how to put them back:

    <EVENT iheader>

If *iheader* was previously disabled or disassociated from its name,
`EVENT` will associate and enable it.

    <HANDLER iheader handler>

If *handler* was previously removed from its list, `HANDLER` will add
it to the front of *iheader*'s list of actions. Note that *process*
cannot be specified.

## 21.5. IHEADER and HANDLER (the TYPEs)

Both these `TYPE`s are of `PRIMTYPE` `VECTOR`, but they do not `PRINT`
that way, since they are self-referencing. Instead they `PRINT` as

    #type most-interesting-component

The contents of `IHEADER`s and `HANDLER`s can be changed by `PUT`, and
the new values will then determine the behavior of MDL.

Before describing the elements of these `TYPE`s in detail, here are a
picture and a Pattern, both purporting to show how they look:

```
#IHEADER [name:atom or which
          disabled?
          *-----------> #HANDLER [*-----------> #HANDLER [#HANDLER []
          priority] <-------------*                +------*
                                  applicable       |      applicable
                                  process] <-------+      process]

<IHEADER <OR ATOM CHANNEL LOCATIVE>
         <OR '#LOSE 0 '#LOSE -1>
         <HANDLER HANDLER <OR HANDLER IHEADER> APPLICABLE PROCESS>
         FIX>
```

### 21.5.1. IHEADER

The elements of an `IHEADER` are as follows:

1. name of interrupt (`ATOM`, or `CHANNEL` if the name is `"CHAR"`, or
`LOCATIVE` if the name is `"READ"` or `"WRITE"`)
2. non-zero if and only if disabled
3. first `HANDLER`, if any, else a zero-length `HANDLER`
4. priority

If you lose track of an `IHEADER`, you can get it via the association:

* For `"CHAR"` interrupts, `<GET channel INTERRUPT>` returns the
`IHEADER` or `#FALSE ()` if there is no association; `<EVENT "CHAR" 0
channel>` returns the `IHEADER`, creating it if there is no
association.
* For `"READ"` interrupts, `<GET locative READ!-INTERRUPTS>` returns
the `IHEADER` or `#FALSE ()` if there is no association; `<EVENT
"READ" 0 locative>` returns the `IHEADER`, creating it if there is no
association.
* For `"WRITE"` interrupts, `<GET locative WRITE!-INTERRUPTS>` returns
the `IHEADER` or `#FALSE ()` if there is no association: `<EVENT
"WRITE" 0 locative>` returns the `IHEADER`, creating it if there is no
association.
* Otherwise, the `IHEADER` is `PUT` on the name `ATOM` with the
indicator `INTERRUPT`. Thus, for example, `<GET CLOCK!-INTERRUPTS
INTERRUPT>` returns the `IHEADER` for the clock interrupt or `#FALSE
()` if there is no association; `<EVENT "CLOCK" 0>` returns the
`IHEADER`, creating it if there is no association.

### 21.5.2. HANDLER

A `HANDLER` specifies a **particular** action for a **particular**
interrupt. The elements of a `HANDLER` are as follows:

1. next `HANDLER` if any, else a zero-length `HANDLER`
2. previous `HANDLER` or the `IHEADER` (Thus the `HANDLER`s of a given
interrupt form a "doubly-linked list" chaining between each other and
back to the `IHEADER`.)
3. handler to be applied (anything but `APPLICABLE` that evaluates its
arguments -- the application is done not by `APPLY` but by `RUNINT`,
which can take a `PROCESS` argument: see next line)
4. `PROCESS` in which the handler will be applied, or `#PROCESS 0`,
meaning whatever `PROCESS` was running when the interrupt occurred (In
the former case, `RUNINT` is applied to the handler and its arguments
in the currently running `PROCESS`, which causes an `APPLY` in the
`PROCESS` stored in the `HANDLER`, which `PROCESS` must be
`RESUMABLE`. The running `PROCESS` becomes `RESUMABLE`, and the stored
`PROCESS` becomes `RUNNING`, but no other `PROCESS` variables (for
example `RESUMER`) are changed.)

## 21.6. Other SUBRs

    <ON name applicable priority:fix process which>

is equivalent to

    <HANDLER <EVENT name priority which>
             applicable process>

`ON` is a combination of `EVENT` and `HANDLER`: it creates (or finds)
the `IHEADER`, associates and enables it, adds a `HANDLER` to the
front the list (first to be performed), and returns the `HANDLER`.

    <DISABLE iheader>

is effectively `<PUT iheader 2 #LOSE -1>`. Actually the `TYPE` `LOSE`
is unimportant, but the `-1` signifies that *iheader* is disabled.

    <ENABLE iheader>

is effectively `<PUT iheader 2 #LOSE 0>`. Actually the `TYPE` `LOSE`
is unimportant, but the `0` signfies that *iheader* is enabled.

## 21.7. Priorities and Interrupt Levels

At any given time there is a defined **interrupt level**. This is a
`FIX` which determines which interrupts can really "interrupt" -- that
is, cause the current processing to be suspended while their wants are
satisfied. Normal, non-interrupt programs operate at an interrupt
level of 0 (zero.) An interrupt is processed at an interrupt level
equal to the interrupt's priority.

### 21.7.1. Interrupt Processing

Interrupts "actually" only occur at well-defined points in time:
during a call to a Subroutine, or at critical places within
Subroutines (for example, during each iteration of `MAPF` on a `LIST`,
which may be circular), or while a `PROCESS` is `"BLOCKED"` (see
below). No interrupts can occur during garbage collection.

What actually happens when an enabled interrupt occurs is that the
priority of the interrupt is compared with the current interrupt
level, and the following is done:

If the priority is **greater than** the current interrupt level, the
current processing is "frozen in its tracks" and processing of the
action(s) specified for that interrupt begins.

If the priority is less than or equal to the current interrupt level,
the interrupt occurrence is **queued** -- that is, the fact that it
occurred is saved away for processing when the interrupt level becomes
low enough.

When the processing of an interrupt's actions is completed, MDL
usually (1) "acts as if" the previously-existing interrupt level is
restored, and processing continues on what was left off (perhaps for
no time duration); and (2) "acts as if" any queued interrupt
occurrences actually occurred right then, in their original order of
occurrence.

### 21.7.2. INT-LEVEL

The `SUBR` `INT-LEVEL` is used to examine and change the current
interrupt level directly.

    <INT-LEVEL>

simply returns the current interrupt level.

    <INT-LEVEL fix>

changes the interrupt level to its argument and returns the
**previously**-existing interrupt level.

If `INT-LEVEL` lowers the priority of the interrupt level, it does not
"really" return until all queued occurrences of interrupts of higher
priority than the target priority have been processed.

Setting the `INT-LEVEL` extremely high (for example, `<INT-LEVEL
<CHTPE <MIN> FIX>>`) effectively disables all interrupts (but
occurrences of enabled interrupts will still be queued).

If `LISTEN` or `ERROR` is called when the `INT-LEVEL` is not zero,
then the typeout will be

    LISTENING-AT-LEVEL I PROCESS p INT-LEVEL i

### 21.7.3. DISMISS

`DISMISS` permits a handler to return an arbitrary value for an
arbitrary `ACTIVATION` at an arbitrary interrupt level. The call is as
follows:

    <DISMISS value:any activation int-level:fix>

where only the *value* is required. If *activation* is omitted, return
is to the place interrupted from, and *value* is ignored. If
*int-level* is omitted, the `INT-LEVEL` prior to the current interrupt
is restored.

## 21.8. Specific Interrupts

Descriptions of the characteristics of particular "built-in" MDL
interrupts follow. Each is named by its `STRING` name. Expect this
list to be incomplete yesterday.

`"CHAR"` is currently the most complex built-in interrupt, because it
serves duty in several ways. These different ways will be described in
several different sections. All ways are concerned with characters or
machine words that arrive or depart at unpredictable times, because
MDL is communicating with a person or another processor. Each `"CHAR"`
`IHEADER` has a `CHANNEL` for the element that names the interrupt,
and the mode of the `CHANNEL` tells what kinds of `"CHAR"` interrupts
occur to be handled through that `IHEADER`.

1. If the `CHANNEL` is for `INPUT`, "CHAR" occurs every time an
"interesting" character (see below) is received from the `CHANNEL`'s
real terminal, or any character is received from the `CHANNEL`'s
pseudo-terminal, or a character or word is received from the
`CHANNEL`'s Network socket, or indeed (in the ITS version) the
operating system generates an interrupt for any reason.
2. If the `CHANNEL` is for output to a pseudo-terminal or Network
socket, `"CHAR"` occurs every time a character or word is wanted.
3. If the `CHANNEL` is for output to a terminal, `"CHAR"` occurs every
time a line-feed character is output or (in the ITS version) the
operating system generates a screen-full interrupt for the terminal.

### 21.8.1. "CHAR" received

A handler for an input `"CHAR"` interrupt on a real terminal must take
two arguments: the `CHARACTER` which was typed, and the `CHANNEL` on
which it was typed.

In the ITS version, the "interesting" characters are those "enabled
for interrupts" on a real terminal, namely <kbd>^@</kbd> through
<kbd>^G</kbd>, <kbd>^K</kbd> through <kbd>^_</kbd>, and
<kbd>DEL</kbd> (that is, ASCII codes 0-7, 13-37, and 177 octal.)

In the Tenex and Tops-20 versions, the operating system can be told
which characters typed on a terminal should cause this interrupt to
occur, by calling the `SUBR` `ACTIVATE-CHARS` with a `STRING`
argument containing those characters (no more than six, all with
ASCII codes less than 33 octal). If called with no argument,
`ACTIVATE-CHARS` returns a `STRING` containing the characters that
currently interrupt. Initially, only <kbd>^G</kbd>, <kbd>^S</kbd>,
and <kbd>^O</kbd> interrupt.

An initial MDL already has `"CHAR"` enabled on `,INCHAN` with a
priority 8 (eight), the `SUBR` `QUITTER` for a handler to run in
`#PROCESS 0` (the running `PROCESS`); this is how <kbd>`^G`</kbd> and
<kbd>`^S`</kbd> are processed. In addition, every time a new
`CHANNEL` is `OPEN`ed in `"READ"` mode to a terminal, a similar
`IHEADER` and `HANDLER` are associated with that new `CHANNEL`
automatically. These automatically-generated `IHEADER`s and
`HANDLER`s use the standard machinery, and they can be `DISABLE`d or
`OFF`ed at will. **However**, the `IHEADER` for `,INCHAN` should not
be `OFF`ed: MDL knows that `$` is typed only by an interrupt!

Example: the following causes the given message to be printed out
whenever a <kbd>`^Y`</kbd> is typed on `.INCHAN`:

```
<SET H <HANDLER <GET .INCHAN INTERRUPT>
     #FUNCTION ((CHAR CHAN)
      #DECL ((VALUE) ANY (CHAR) CHARACTER (CHAN) CHANNEL)
      <AND <==? .CHAR !\^Y>
           <PRINC " [Some of the best friends are ^Ys.] ">>)>>$
#HANDLER #FUNCTION **CHAR CHAN) ...)
<+ 2 ^Y [Some of my best friends are ^Ys.] 2>$
4
<OFF .H>$
#HANDLER #FUNCTION (...)
```

Note that occurrences of `"CHAR"` do **not** wait for the `$` to be
typed, and the interrupting character is omitted from the input
stream.

A `"CHAR"` interrupt can also be associated with an input `CHANNEL`
open to a Network socket (`"NET"` device). A handler gets applied to
a `NETSTATE` array (which see) and the `CHANNEL`.

In the ITS version, a `"CHAR"` interrupt can also be associated with
an input `CHANNEL` open to a pseudo-terminal ("STY" device and
friends). An interrupt occurs when a character is available for
input. These interrupts are set up in exactly the same way as
real-terminal interrupts, except that a handler gets applied to only
**one** argument, the `CHANNEL`. Pseudo-terminal are not available in
the Tenex and Tops-20 versions.

For any other flavor of ITS channel interrupt, a handler gets applied
to only **one** argument, the `CHANNEL`.

### 21.8.2. "CHAR" wanted

A `"CHAR"` interrupt can be associated with an output `CHANNEL` open
to a Network socket (`"NET"` device). A handlers gets applied to a
`NETSTATE` array (which see) and the `CHANNEL`.

In the ITS version, a `"CHAR"` interrupt can also be associated with
an output `CHANNEL` open to a pseudo-terminal (`"STY"` device and
friends). An interrupt occurs when the program at the other end needs
a character (and the operating-system buffer is empty). A handler gets
applied to one argument, the `CHANNEL`. Pseudo-terminals are not
available in the Tenex and Tops-20 versions.

### 21.8.3. "CHAR" for new line

A handler for an output `"CHAR"` interrupt on a real terminal must
take **one or two** arguments (using `"OPTIONAL"` or `"TUPLE"`): if
two arguments are supplied by the interrupt system, they are the line
number (`FIX`) and the `CHANNEL`, respectively, and the interrupt is
for a line-feed; if only one argument is supplied (only in the ITS
version), it is the `CHANNEL`, and the interrupt is for a full
terminal screen. Note: the supplied line number comes from the
`CHANNEL`, and it may not be accurate if the program alters it in
subtle ways, for example, via `IMAGE` calls or special control
characters. (The program can compensate by putting the proper line
number into the `CHANNEL`.)

### 21.8.4. "GC"

`"GC"` occurs just **after** every garbage collection. Enabling this
interrupt is the only way a program can know that a garbage collection
has occurred. A handler for `"GC"` takes three arguments. The first is
a FLOAT indicating the number of seconds the garbage collection took.
The second argument is a FIX indicating the cause of the garbage
collection, as follows (chapter 22):

0. Program called GC.
1. Movable storage was exhausted.
2. Control stack overflowed.
3. Top-level LVALs overflowed.
4. GVAL vector overflowed.
5. TYPE vector overflowed.
6. Immovable garbage-collected storage was exhausted.
7. Internal stack overflowed.
8. Both control and internal stacks overflowed (rare).
9. Pure storage was exhausted.
10. Second, exhaustive garbage collection occurred.

The third argument is an ATOM indicating what initiated the garbage
collection: `GC-READ`, `BLOAT`, `GROW`, `LIST`, `VECTOR`, `SET`,
`SETG`, `FREEZE`, `GC`, `NEWTYPE`, `PURIFY`, `PURE-PAGE-LOADER` (pure
storage was exhausted), or `INTERRUPT-HANDLER` (stack overflow,
unfortunately).

### 21.8.5. "DIVERT-AGC"

`"DIVERT-AGC"` ("Automatic Garbage Collection") occurs just **before**
a deferrable garbage collection that is needed because of exhausted
movable garbage-collected storage. Enabling this interrupt is the only
way a program can know that a garbage collection is about to occur. A
handler takes two arguments: A `FIX` telling the number of machine
words needed and an `ATOM` telling what initiated the garbage
collection (see above). If it wishes, a handler can try to prevent a
garbage collection by calling `BLOAT` with the `FIX` argument. If the
pending request for garbage-collected storage cannot then be
satisfied, a garbage collection occurs anyway. `AGC-FLAG` is `SET` to
`T` while the handler is running, so that new storage requests do not
try to cause a garbage collection.

### 21.8.6. "CLOCK"

`"CLOCK"`, when enabled, occurs every half second (the ITS
"slow-clock" tick.) It is not available in the Tenex or Tops-20
versions. It wants handlers which take no arguments. Example:

    <ON "CLOCK" <FUNCTION () <PRINC "TICK ">> 1>

### 21.8.7. "BLOCKED"

`"BLOCKED"` occurs whenever **any** `PROCESS` (not only the `PROCESS`
which may be in a `HANDLER`) starts waiting or terminal input: that
is, an occurrence indicates that somewhere, somebody did a `READ`,
`READCHR`, `NEXTCHR`, `TYI`, etc. to a console. The handler for a
`"BLOCKED"` interrupt should take one argument, namely the `PROCESS`
which started waiting (which will also be the `PROCESS` in which the
handler runs, if no specific one is in the `HANDLER`).

Example: the following will cause MDL to acquire a `*` prompting
character.

    <ON "BLOCKED" #FUNCTION ((IGNORE) <PRINC !\*>) 5>

### 21.8.8. "UNBLOCKED"

`"UNBLOCKED"` occurs whenever a `$` (<kbd>`ESC`</kbd>) is typed on a
terminal if a program was hanging and waiting for input, or when a
TYI call (which see) is satisfied. A handler takes one argument: the
`CHANNEL` via which the `$` or character is input.

### 21.8.9. "READ" and "WRITE"

`"READ"` and `"WRITE"` are associated with read or write references to
MDL objects. These interrupts are often called "monitors", and
enabling the interrupt is often called "monitoring" the associated
object. A "read reference" to an `ATOM`'s local value includes
applying `BOUND?` or `ASSIGNED?` to the `ATOM`; similarly for a global
value and `GASSIGNED?`. If the `INT-LEVEL` is too high when `"READ"`
or `"WRITE"` occurs, an error occurs, because occurrences of these
interrupts cannot be queued.

Monitors are set up with `EVENT` or `ON`, using a locative to the
object being monitored as the extra *which* argument, just as a
`CHANNEL` is given for `"CHAR"`. A handler for `"READ"` takes two
arguments: the locative and the `FRAME` of the function application
that make the reference. A handler for `"WRITE"` takes three
arguments: the locative, the new value, and the `FRAME`. For example:

```
<SET A (1 2 3)>$
(1 2 3)
<SET B <AT .A 2>>$
#LOCL 2
<ON "WRITE" <FUNCTION (OBJ VAL FRM)
        #DECL ((VALUE VAL ANY (OBJ) LOCATIVE (FRM) FRAME)
        <CRLF>
        <PRINC "Program changed ">
        <PRIN1 .OBJ>
        <PRINC " to ">
        <PRIN1 .VAL>
        <PRINC " via ">
        <PRINC .FRM>
        <CRLF>>
        4 0 .B>$
#HANDLER FUNCTION (...)
<1 .A 10>$
(10 2 3)
<2 .A 20>$
Program changed #LOCL 2 to 20 via #FRAME PUT
(10 20 3)
<OFF "WRITE" .B>$
#IHEADER #LOCL 20
```

### 21.8.10. "SYSDOWN"

`"SYSDOWN"` occurs when a system-going-down or system-revived signal
is received from ITS. It is not available in the Tenex or Tops-20
versions. If no `IHEADER` is associated and enabled, a warning message
is printed on the terminal. A handler takes one argument: a `FIX`
giving the number of thirtieths of a second until the shutdown (-1
for a reprieve).

### 21.8.11. "ERROR"

In an effort to simplify error handling by programs, MDL has a
facility allowing errors to be handled like interrupts. `SETG`ing
`ERROR` to a user function is a distasteful method, not safe if any
bugs are around. An `"ERROR"` interrupt wants a handler that takes any
number of arguments, via `"TUPLE"`. When an error occurs, handlers are
applied to the `FRAME` of the `ERROR` call and the `TUPLE` of `ERROR`
arguments. If a given handler "takes care of the error", it can
`ERRET` with a value from the `ERROR` `FRAME`, after having done
`<INT-LEVEL 0>`. If no handler takes care of the error, it falls into
the normal `ERROR`.

If an error occurs at an `INT-LEVEL` greater than or equal to that of
the `"ERROR"` interrupt, real `ERROR` will be called, because
`"ERROR"`interrupts cannot be queued.

### 21.8.12. "IPC"

`"IPC"` occurs when a message is received on the ITS IPC device
(chapter 23). It is not available in the Tenex and Tops-20 versions.

### 21.8.13. "INFERIOR"

`"INFERIOR"` occurs when an inferior ITS process interrupts the MDL
process. It is not available in the Tenex and Tops-20 versions. A
handler takes one argument: A `FIX` between `0` and `7` inclusive,
telling which inferior process is interrupting.

### 21.8.14. "RUNT and "REALT"

These are not available in the Tenex and Tops-20 versions.

`"RUNT"`, if enabled, occurs **once**, *N* seconds of MDL running
time (CPU time) after calling `<RUNTIMER N:fix-or-float>`, which
returns its argument. A handler takes no arguments. If `RUNTIMER` is
called with no argument, it returns a `FIX`, the number of run-time
seconds left until the interrupt occurs, or `#FALSE ()` if the
interrupt is not going to occur.

`"REALT"`, if enabled, occurs **every** *N* seconds of real-world time
after calling `<REALTIMER N:fix-or-float>`, which returns its
argument. A handler takes no arguments. `<REALTIMER 0>` tells the
operating system not to generate real-time interrupts. If `REALTIMER`
is called with no argument, it returns a `FIX`, the number of
real-time seconds given in the most recent call to `REALTIMER` with an
argument, or `#FALSE ()` if `REALTIMER` has not been called.

### 21.8.15. "Dangerous" Interrupts

`"MPV"` ("memory protection violation") occurs if MDL tries to refer
to a storage address not in its address space. `"PURE"` occurs if MDL
tries to alter read-only storage. `"ILOPR"` occurs if MDL executes and
illegal instruction ("operator"). `"PARITY"` occurs if the CPU detects
a parity error in MDL's address space. All of these require a handler
that takes one argument: the address (`TYPE` `WORD`) following the
instruction that was being executed at the time.

`"IOC"` occurs if MDL tries to deal illegally with an I/O channel. A
handler must take two arguments: a three-element `FALSE` like one
that `OPEN` might return, and the `CHANNEL` that got the error.

Ideally these interrupts should never occur. In fact, in the Tenex and
Tops-20 versions, these interrupts always go to the superior operating
system process instead of to MDL. In the ITS version, if and when a
"dangerous" interrupt does occur:

* If no `IHEADER` is associated with the interrupt, then the interrupt
goes to the superior operating system process.
* If an `IHEADER` is associated but disabled, the error
`DANGEROUS-INTERRUPT-NOT-HANDLED` occurs (`FILE-SYSTEM-ERROR` for
`"IOC").
* If an `IHEADER` is associated and enabled, but the `INT-LEVEL` is
too high, the error `ATTEMPT-TO-DEFER-UNDEFERABLE-INTERRUPT` occurs.

## 21.9. User-Defined Interrupts

If the interrupt name given to `EVENT` or `ON` is **not** one of the
standard predefined interrupts of MDL, they will gleefully create an
`ATOM` in `<INTERRUPTS>` and an associated `IHEADER` anyway, making
the assumption that you are setting up a "program-defined" interrupt.

Program-defined interrupts are made to occur by applying the `SUBR`
`INTERRUPT`, as in

    <INTERRUPT name arg1 ... argN>

where *name* is a `STRING`, `ATOM` or `IHEADER`, and *arg1* through
*argN* are the arguments wanted by the handlers for the interrupt.

If the interrupt specified by `INTERRUPT` is enabled, `INTERRUPT`
returns `T`; otherwise it returns `#FALSE ()`. All the usual priority
and queueing rules hold, so that even if `INTERRUPT` returns `T`, it
is possible that nothing "really happened" (yet).

`INTERRUPT` can also be used to cause "artificial" occurrences of
standard predefined MDL interrupts.

Making a program-defined interrupt occur is similar to calling a
handler directly, but there are differences. The value returned by a
handler is ignored, so side effects must be used in order to
communicate information back to the caller, other than whether any
handler ran or will run. One good use for a program-defined interrupt
is to use the priority and queueing machinery of `INT-LEVEL` to
control the execution of functions that must not run concurrently. For
example, if a `"CHAR"` handler just deposits characters in a buffer,
then a function to process the buffered characters should probably run
at a higher priority level -- to prevent unpredictable changes to the
buffer during the processing -- and it is natural to invoke the
processing with `INTERRUPT`.

In more exotic applications, `INTERRUPT` can signal a condition to be
handled by an unknown number of independent and "nameless" functions.
The functions are "nameless" because the caller doesn't know their
name, only the name of the interrupt. This programming style is
modular and event-driven, and it is one way of implementing
"heuristic" algorithms. In addition, each `HANDLER` has a `PROCESS`
in which to run its handler, and so the different handlers for a
given condition can do their thing in different environments quite
easily, with less explicit control than when using `RESUME`.

## 21.10. Waiting for Interrupts

### 21.10.1. HANG

    <HANG pred>

hangs interruptibly, without consuming any CPU time, potentially
forever. `HANG` is nice for a program that cannot do anything until an
interrupt occurs. If the optional *pred* is given, it is evaluated
every time an interrupt occurs and is dismissed back into the `HANG`;
if the result of evaluation is not `FALSE`, `HANG` unhangs and returns
it as a value. If *pred* is not given, there had better be a named
`ACTIVATION` somewhere to which a handler can return.

### 21.10.2. SLEEP

    <SLEEP time:fix-or-float pred>

suspends execution, interruptibly, without consuming any CPU time,
for *time* seconds, where *time* is non-negative, and then returns
`T`. *pred* is the same as for `HANG`.
