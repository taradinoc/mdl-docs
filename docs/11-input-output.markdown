# Chapter 11. Input/Output

The MDL interpreter can transmit information between an object in MDL
and an external device in three ways. Historically, the first way was
to **convert** an object into a string of characters, or vice versa.
The transformation is nearly one-to-one (although some MDL objects,
for example `TUPLE`s, cannot be input in this way) and is similar in
style to Fortran's formatted I/O. It is what `READ` and `PRINT` do,
and it is the normal method for terminal I/O.

The second way is used for the contents of MDL objects rather than
the objects themselves. Here an **image** of numbers or characters
within an object is transmitted, similar in style to Fortran's
unformatted I/O.

The third way is to **dump** an object in a clever format so that it
can be reproduced exactly when input the next time. Exact
reproduction means that any sharing between structures or
self-reference is preserved: only the garbage collector itself can do
I/O in this way.

## 11.1. Conversion I/O

All conversion-I/O `SUBR`s in MDL take an optional argument which
directs their attention to a specific I/O channel. This section will
describe `SUBR`s without their optional arguments. In this situation,
they all refer to a particular channel by default, initially the
terminal running the MDL. When given an optional argument, that
argument follows any arguments indicated here. Some of these `SUBR`s
also have additional optional arguments, relevant to conversion,
discussion of which will be deferred until later.

### 11.1.1. Input

All of the following input Subroutines, when directed at a terminal,
hang until `$` (<kbd>ESC</kbd>) is typed and allow normal use of
<kbd>rubout</kbd>, <kbd>^D</kbd>, <kbd>^L</kbd> and <kbd>^@</kbd>.

#### 11.1.1.1. READ

    <READ>

This returns the entire MDL object whose character representation is
next in the input stream. Successive `<READ>`s return successive
objects. This is precisely the `SUBR` `READ` mentioned in chapter 2.
See also sections 11.3, 15.7.1, and 17.1.3 for optional arguments.

#### 11.1.1.2. READCHR

    <READCHR>

("read character") returns the next `CHARACTER` in the input stream.
Successive `<READCHR>`s return successive `CHARACTER`s.

#### 11.1.1.3. NEXTCHR

    <NEXTCHR>

("next character") returns the `CHARACTER` which `READCHR` will
return the next time `READCHR` is called. Multiple `<NEXTCHR>`s, with
no input operations between them, all return the same thing.

### 11.1.2. Output

If an object to be output requires (or can tolerate) separators
within it (for example, between the elements in a structured object
or after the `TYPE` name in "# notation"), these conversion-output
`SUBR`s will use a carriage-return/line-feed separator to prevent
overflowing a line. Overflow is detected in advance from elements of
the `CHANNEL` in use (section 11.2.8).

#### 11.1.2.1. PRINT

    <PRINT any>

This outputs, in order,

1. a carriage-return line-feed,
2. the character representation of `EVAL` of its argument (`PRINT` is
a `SUBR`), and
3. a space

and then returns `EVAL` of its argument. This is precisely the `SUBR`
`PRINT` mentioned in chapter 2.

#### 11.1.2.2. PRIN1

    <PRIN1 any>

outputs just the representation of, and returns, `EVAL` of *any*.

#### 11.1.2.3. PRINC

    <PRINC any>

("print characters") acts exactly like `PRIN1`, except that

1. if its argument is a `STRING` or a `CHARACTER`, it suppresses the
surrounding `"`s or initial `!\` respectively; or
2. if its argument is an `ATOM`, it suppresses any `\`s or `OBLIST`
trailers (chapter 15) which would otherwise be necessary.

If `PRINC`'s argument is a structure containing `STRING`s,
`CHARACTER`s, or `ATOM`s, the service mentioned will be done for all
of them. Ditto for the `ATOM` used to name the `TYPE` in "#
notation".

#### 11.1.2.4. TERPRI

    <TERPRI>

("terminate printing") outputs a carriage-return line-feed and then
returns `# FALSE ()`!

#### 11.1.2.5. CRLF

("carriage-return line-feed") outputs a carriage-return line-feed and
then returns `T`.

#### 11.1.2.6. FLATSIZE

    <FLATSIZE any max:fix radix:fix>

does not actually cause any output to occur and does not take a
`CHANNEL` argument. Instead, or compares *max* with the number of
characters `PRIN1` would take to print *any*. If *max* is less than
the number of characters needed (including the case where *any* is
self-referencing, `FLATSIZE` returns `#FALSE ()`; otherwise, it
returns the number of characters needed by `PRIN1` *any*. *radix*
(optional, ten by default) is used for converting any `FIX`es that
occur.

This `SUBR` is especially useful in conjunction with (section 11.2.8)
those elements of a `CHANNEL` which specify the number of characters
per output line and the current position on an input line.

## CHANNEL (the TYPE)

I/O channels are dynamically assigned in MDL, and are represented by
an object of `TYPE` `CHANNEL`, which is of `PRIMTYPE` `VECTOR`. The
format of a `CHANNEL` will be explained later, in section 11.2.8.
First, how to generate and use them.

### 11.2.1. OPEN

    <OPEN mode file-spec>

or

    <OPEN mode name1 name2 device dir>

`OPEN` is a `SUBR` which creates and returns a `CHANNEL`. All its
arguments must be of `TYPE` `STRING`, and **all** are optional. The
preceding statement is false when the *device* is `"INT"` or `"NET"`;
see sections 11.9 and 11.10. If the attempted opening of an
operating-system I/O channel fails, `OPEN` returns `#FALSE
(reason:string file-spec:string status:fix)`, where the *reason* and
the *status* are supplied by the operating system, and the
`file-spec` is the standard name of the file (after any name
transformations by the operating system) that MDL was trying to open.

The choice of *mode* is usually determined by which `SUBR`s will be
used on the `CHANNEL`, and whether or not the *device* is a terminal.
The following table tells which `SUBR`s can be used with which modes,
where `OK` indicates an allowed use:

| "READ" | "PRINT" | "READB" | "PRINTB", "PRINTO" | mode / SUBRs   |
|--------|---------|---------|--------------------|----------------|
| OK     |         | OK      |                    | `READ` `READCHR` `NEXTCHR` `READSTRING` `FILECOPY` `FILE-LENGTH LOAD` |
|        | OK      |         | OK*                | `PRINT` `PRIN1` `PRINC` `IMAGE` `CRLF` `TERPRI` `FILECOPY` `PRINTSTRING` `BUFOUT` `NETS` `RENAME`   |
|        |         | OK      |                    | `READB` `GC-READ`  |
|        |         |         | OK                 | `PRINTB` `GC-DUMP` |
| OK     |         | OK      | OK                 | `ACCESS`         |
| OK     | OK      | OK      | OK                 | `RESET`          |
| OK     | OK      |         |                    | `ECHOPAIR`       |
| OK     |         |         |                    | `TTYECHO` `TYI`    |

`*` PRINTing (or `PRIN1`ing) an `RSUBR` (chapter 19) on a `"PRINTB"`
or `"PRINTO"` `CHANNEL` has special effects.

`"PRINTB"` differs from `"PRINTO"` in that the latter mode is used to
update a `"DSK"` file without copying it. `"READB"` and `"PRINTB"`
are not used with terminals. `"READ"` is the mode used by default.

The next one to four arguments to `OPEN` specify the file involved.
If only one `STRING` is used, it can contain the entire
specification, according to standard operating-system syntax.
Otherwise, the string(s) are intepreted as follows:

*name1* is the first file name, that part to the left of the space
(in the ITS version) or period (in the Tenex and Tops-20 versions).
The name used by default is `<VALUE NM1>`, if any, otherwise
`"INPUT"`.

*name2* is the second fail name, that part to the right of the space
(ITS) or period (Tenex and Tops-20). The name used by default is
`<VALUE NM2>`, if any, otherwise `">"` or `"MUD"` and highest version
number (Tenex) or generation number (Tops-20).

*device* is the device name. The name used by default is `<VALUE
DEV>`, if any, otherwise `"DSK"`. (Devices about which MDL has no
special knowledge are assumed to behave like `"DSK"`.)

*dir* is the disk-directory name. The name used by default is `<VALUE
SNM>`, if any, otherwise the "working-directory" name as defined by
her operating system.

Examples:

`<OPEN "PRINT" "TPL:">` opens a conversion-output channel to the TPL
device.

`<OPEN "PRINT" "DUMMY" "NAMES" "IPL">` does the same.

`<OPEN "PRINT" "TPL">` opens a `CHANNEL` to the file `DSK:TPL >` (ITS
version) or `DSK:TPL.MUD` (Tenex and Tops-20 versions).

`<OPEN "READ" "FOO" ">" "DSK" "GUEST">` opens up a conversion-input
`CHANNEL` to the given file.

`<OPEN "READ" "GUEST;FOO">` does the same in the ITS version.

### 11.2.2. OPEN-NR

`OPEN-NR` is the same as `OPEN`, except that the date and time of
last reference of the opened file are not changes.

### 11.2.3. CHANNEL (the SUBR)

`CHANNEL` is called exactly like `OPEN`, but it **always** return an
unopened `CHANNEL`, which can later be opened by `RESET` (below) just
as if it had once been open.

### 11.2.4. FILE-EXISTS?

`FILE-EXISTS?` tests for the existence of a file without creating a
`CHANNEL`, which occupies about a hundred machine words of storage.
It takes file-name arguments just like `OPEN` (but no *mode*
argument) and returns either T, `#FALSE (reason:string status:fix),

### 11.2.5. CLOSE

    <CLOSE channel>

closes *channel* and returns its argument, with its "state" changed
to "closed". If *channel* is for output, all buffered output is
written out first. No harm is done if *channel* is already `CLOSE`d.

### 11.2.6. CHANLIST

    <CHANLIST>

returns a `LIST` whose elements are all the currently open
`CHANNEL`s. The first two elements are usually `.INCHAN` and
`.OUTCHAN` (see below). A `CHANNEL` not referenced by anything except
`<CHANLIST>` will be `CLOSEd` during garbage collection.

### 11.2.7. INCHAN and OUTCHAN

The channel used by default for input `SUBR`s is the local value of
the `ATOM` `INCHAN`. The channel used by default for output SUBRs is
the local value of the `ATOM` `OUTCHAN`.

You can direct I/O to a `CHANNEL` by `SET`ting `INCHAN` or `OUTCHAN`
(remembering their old values somewhere), or by giving the `SUBR` you
with to use an argument of `TYPE` `CHANNEL`. (These actually have the
same effect, because `READ` binds `INCHAN` to an explicit argument,
and `PRINT` binds `OUTCHAN` similarly. Thus the `CHANNEL` being used
is available for `READ` macros (section 17.1), or by giving the
`SUBR` you wish to use an argument of `TYPE` `CHANNEL`. Thus the
`CHANNEL` being used is available for `READ` macros (section 17.1)
and `PRINTTYPE`s (section 6.4.4).)

By the way, a good trick for playing with `INCHAN` and `OUTCHAN`
values within a function is to use the `ATOM`s `INCHAN` and `OUTCHAN`
as `"AUX"` variables, re-binding their local values to the `CHANNEL`
you want. When you leave , of course, the old `LVAL`s are expanded
(which is the whole point). The `ATOM`s must be declared `SPECIAL`
(chapter 14) for this trick to compile correctly.

`INCHAN` and `OUTCHAN` also have global values, initially the
`CHANNEL`s directed at the terminal running `MDL`. Initially,
`INCHAN`'s and `OUTCHAN`s local and global values are the same.

### 11.2.8. Contents of CHANNELs

The contents of an object of `TYPE` `CHANNEL` are referred to by the
I/O `SUBR`s each time such a `SUBR` is used. If you change the
contents of a `CHANNEL` (for example, with `PUT`), the next use of
that `CHANNEL` will be changed accordingly. Some elements of
`CHANNEL`s, however, should be played with seldom, if ever, and only
at your own peril. These are marked below with an `*` (asterisk).
Caveat user.

There follows a table of the contents of a `CHANNEL`, the `TYPE` of
each element, and an interpretation. The format used is the
following:

*element-number: type interpretation*

| element-number | type     | interpretation                    |
|----------------|----------|-----------------------------------|
|   -1           | `LIST`   | transcript channel(s) (see below) |
| \* 0           | varies   | device-dependent information      |
| \* 1           | `FIX`    | channel number (ITS) or JFN (Tenex and Tops-20), `0` for internal or closed |
| \* 2           | `STRING` | mode                              |
| \* 3           | `STRING` | first file name argument          |
| \* 4           | `STRING` | second file name argument         |
| \* 5           | `STRING` | device name argument              |
| \* 6           | `STRING` | directory name argument           |
| \* 7           | `STRING` | real first file name              |
| \* 8           | `STRING` | real second file name             |
| \* 9           | `STRING` | real device name                  |
| \* 10          | `STRING` | real directory name               |
| \* 11          | `FIX`    | various status bits               |
| \* 12          | `FIX`    | PDP-10 instruction used to do one I/O operation |
|    13          | `FIX`    | number of characters per line of output |
|    14          | `FIX`    | current character position on a line |
|    15          | `FIX`    | number of lines per page          |
|    16          | `FIX`    | current line number on a page     |
|    17          | `FIX`    | access pointer for file-oriented devices |
|    18          | `FIX`    | radix for `FIX` conversion        |
|    19          | `FIX`    | sink for an internal `CHANNEL`    |

N.B.: The elements of a `CHANNEL` below number 1 are usually
invisible but are obtainable via `<NTH <TOP channel> fix>`, for some
appropriate *fix*.

The transcript-channels slot has this meaning: if this slot contains
a `LIST` of `CHANNEL`s, then anything input or output on the original
`CHANNEL` is output on these `CHANNEL`s. Caution: do not use a
`CHANNEL` as its own transcript channel; you probably won't live to
tell about it.

#### 11.2.8.2. Input CHANNELs

The contents of the elements up to number 12 of a `CHANNEL` used for
input are the same as that for output. The remaining elements are as
follows ((same) indicates that the use is the same as that for
output):

| element-number | type     | interpretation                    |
|----------------|----------|-----------------------------------|
|    13          | varies   | object evaluated when end of file is reached |
| \* 14          | `FIX`    | one "look-ahead" character, used by `READ` |
| \* 15          | `FIX`    | PDP-10 instruction executed waiting for input |
|    16          | `LIST`   | queue of buffers for input from a terminal |
|    17          | `FIX`    | access pointer for file-oriented devices (same) |
|    18          | `FIX`    | radix for `FIX` conversion (same) |
|    19          | `STRING` | buffer for input or source for internal `CHANNEL` |

## 11.3. End-of-File "Routine"

As mentioned above, an explicit `CHANNEL` is the first optional
argument of all `SUBR`s used for conversion I/O. The second optional
argument for conversion-**input** `SUBR`s is an "end-of-file routine"
-- that is, something for the input `SUBR` to `EVAL` and return, if
it reaches the end of the file it is reading. A typical end-of-file
argument is a `QUOTE`d `FORM` which applies a function of yours. The
value of this argument used by default is a call to `ERROR`. Note:
the `CHANNEL` has been `CLOSE`d by the time this argument is
evaluated.

Example: the following `FUNCTION` counts the occurrences of a
character in a file, according to its arguments. The file names,
device, and directory are optional, with the usual names used by
default.

    <DEFINE COUNT-CHAR
            (CHAR "TUPLE" FILE "AUX" (CNT 0) (CHN <OPEN "READ" !.FILE>))
        <COND (.CHN                 ;"If CHN is FALSE, bad OPEN: return the FALSE
                                    so result can be tested by another FUNCTION."
               <REPEAT ()
                    <AND <==? .CHAR <READCHR .CHN '<RETURN>>>
                         <SET CNT <+ 1 .CNT>>>>
                    ;"Until EOF, keep reading and testing a character at a time."
                .CNT                ;"Then return the count.")>>

## 11.4. Imaged I/O

### 11.4.1. Input

#### 11.4.1.1. READB

    <READB buffer:uvector-or-storage channel eof:any>

The *channel* must be open in `"READB"` mode. `READB` will read as
many 36-bit binary words as necessary to fill the *buffer* (whose
`UTYPE` must be of `PRIMTYPE` `WORD`), unless it hits the end of the
file. `READB` returns the number of words actually read, as a
`FIX`ed-point number. This will normally be the length of the
*buffer*, unless the end of file was read, in which case it will be
less, and only the beginning of *buffer* will have been filled
(`SUBSTRUC` may help). An attempt to `READB` again, after *buffer* is
not filled, will evaluate the end-of-file routine *eof*, which is
optional, a call to `ERROR` by default.

#### 11.4.1.2. READSTRING

    <READSTRING buffer:string channel stop:fix-or-string eof>

is the `STRING` analog to `READB`, where *buffer* and *eof* are as in
`READB`, and *channel* is any input `CHANNEL` (`.INCHAN` by default).
*stop* tells when to stop inputting: if a `FIX`, read this many
`CHARACTER`s (fill up *buffer* by default); if a `STRING`, stop
reading if any `CHARACTER` in this `STRING` is read (don't include
this `CHARACTER` in final `STRING`).

### 11.4.2. Output

#### 11.4.2.1. PRINTB

    <PRINTB buffer:uvector-or-storage channel>

This call writes the entire contents of the *buffer* into the
specified channel open in `"PRINTB"` or `"PRINTO"` mode. It returns
*buffer*.

#### 11.4.2.2. PRINTSTRING

    <PRINTSTRING buffer:string channel count:fix>

is analogous to `READSTRING`. It outputs *buffer* on *channel*,
either the whole thing or the first *count* characters, and returns
the number of characters output.

#### 11.4.2.3. IMAGE

    <IMAGE fix channel>

is a rather special-purpose `SUBR`. When any conversion-output
routine outputs an ASCII control character (with special exceptions
like carriage-returns, line-feeds, etc.), it actually outputs two
characters: `^` (circumflex), followed by the upper-case character
which has been control-shifted. `IMAGE`, on the other hand, always
outputs the real thing: that ASCII character whose ASCII 7-bit code
is *fix*. It is guaranteed not to give any gratuitous linefeeds or
such. *channel* is optional, `.OUTCHAN` by default, and its slots for
current character position (number 14) and current line number (16)
are not updated. `IMAGE` returns *fix*.

## 11.5 Dumped I/O

### 11.5.1. Output: GC-DUMP

    <GC-DUMP any printb:channel-or-false>

dumps *any* on *printb* in a clever format so that `GC-READ` (below)
can reproduce *any* exactly, including sharing. *any* cannot live on
the control stack, not can it be of `PRIMTYPE` `PROCESS` or `LOCD` or
`ASOC` (which see). *any* is returned as a value.

If *printb* is a `CHANNEL`, it must be open in `"PRINTB"` or
`"PRINTO"` mode. If *printb* is a `FALSE`, `GC-DUMP` instead returns
a `UVECTOR` (of `UTYPE` `PRIMTYPE` `WORD`) that contains what it
would have output on a `CHANNEL`. This `UVECTOR` can be `PRINTB`ed
anywhere you desire, but, if it is changed **in any way**, `GC-READ`
will not be able to input it. Probably the only reason to get it is
to check its length before output.

Except for the miniature garbage collection required, `GC-DUMP` is
about twice as fast as `PRINT`, but the amount of external storage
used is two or three times as much.

### 11.5.2. Input: GC-READ

    <GC-READ readb:channel eof:any>

returns one object from the *channel*, which must be open in
`"READB"` mode. The file must have been produced by `GC-DUMP`. *eof*
is optional. `GC-READ` is about ten times faster than `READ`.

## 11.6. SAVE Files

The entire state of MDL can be saved away in a file for later
restoration: this is done with the `SUBR`s `SAVE` and `RESTORE`. This
is a very different form of I/O from any mentioned up to now; the
file used contains an actual image of your MDL address space and is
not, in general, "legible" to other MDL routines. `RESTORE`ing a
`SAVE` file is **much** faster than re-`READ`ing the objects it
contains.

Since a `SAVE` file does not contain all extant MDL objects, only the
impure and `PURIFY`ed (section 22.9.2) ones, a change to the
interpreter has the result of making all previous `SAVE` files
unusable. To prevent errors from arising from this, the interpreter
has a release number, which is incremented whenever changes are
installed. The current release number is printed out on initially
starting up the program and is available as the `GVAL` of the `ATOM`
`MUDDLE`. This release number is written out as the very first part
of each `SAVE` file. If `RESTORE` attempts to re-load a `SAVE` file
whose release number is not the same as the interpreter being used,
an error is produced. If desired, the release number of a `SAVE` file
can be obtained by doing a `READ` of that file. Only that initial
`READ` will work; the rest of the file is not ASCII.

### 11.6.1. SAVE

    <SAVE file-spec:string gc?:false-or-any>

or

    <SAVE name1 name2 device dir gc?:false-or-any>

saves the entire state of your MDL away in the file specified by its
arguments, and then returns `"SAVED"`. All `STRING` arguments are
optional, with `"MUDDLE"`, `"SAVE"`, `"DSK"`, and `<VALUE SNM>` used
by default. *gc?* is optional and, if supplied and of `TYPE` `FALSE`,
causes no garbage collection to occur before `SAVE`ing. (`FSAVE` is
an alias for `SAVE` that may be seen in old programs.)

If, after restoring, `RESTORE` finds that `<VALUE SNM>` is the null
`STRING` (`""`), it will ask the operating system for the name of the
"working directory" and call `SNAME` with the result. This mechanism
is handy for "public" `SAVE` files, which should not point the user
at a particular disk directory.

In the ITS version, the file is actually written with the name
`_MUDS_ >` and renamed to the argument(s) only when complete, to
prevent losing a previous `SAVE` file if a crash occurs. In the Tenex
and Tops-20 versions, version/generation numbers provide the same
safety.

Example:

    <DEFINE SAVE-IT ("OPTIONAL"
                     (FILE '("PUBLIC" "SAVE" "DSK" "GUEST"))
                     "AUX" (SNM ""))
            <SETUP>
            <COND (<=? "SAVED" <SAVE !.FILE>>   ;"See below."
                   <CLEANUP>
                   "Saved.")
                  (T
                   <CRLF>
                   <PRINC "Amazing program at your service.">
                   <CRLF>
                   <START-RUNNING>)>>

### 11.6.2. RESTORE

    <RESTORE file-spec>

or

    <RESTORE name1 name2 device dir>

**replaces** the entire current state of your MDL with that `SAVE`d
in the file specified. All arguments are optional, with the same
values used by default as by `SAVE`.

`RESTORE` completely replaces the contents of the MDL, including the
state of execution existing when the `SAVE` was done and the state of
all open I/O `CHANNEL`s. If a file which was open when the `SAVE` was
done does not exist when the `RESTORE` is done, a message to that
effect will appear on the terminal.

A `RESTORE` **never** returns (unless it gets an error): it causes a
`SAVE` done some time ago to return **again** (this time with the
value `"RESTORED"`), even if the `SAVE` was done in the midst of
running a program. In the latter case, the program will continue its
execution upon `RESTORE`ation.

## 11.7. Other I/O Functions

### 11.7.1. LOAD

    <LOAD input:channel look-up>

eventually returns `"DONE"`. First, however, it `READ`s and `EVAL`s
every MDL object in the file pointed to by *input*, and then `CLOSE`s
*input*. Any occurrences of <kbd>rubout</kbd>, <kbd>^@</kbd>,
<kbd>^D</kbd>, <kbd>^L</kbd>, etc., in the file are given no special
meaning; they are simply `ATOM` constituents.

*look-up* is optional, used to specify a `LIST` of `OBLIST`s for the
`READ`. `.OBLIST` is used by default (chapter 15).

### 11.7.2. FLOAD

    <FLOAD file-spec look-up>

or

    <FLOAD name1 name2 device dir look-up>

("file load") acts just like `LOAD`, except that it takes arguments
(with values used by default) like `OPEN`, `OPEN`s the `CHANNEL`
itself for reading, and `CLOSE`s the `CHANNEL` when done. *look-up*
is optional, as in `LOAD`. If the `OPEN` fails, an error occurs,
giving the reason for failure.

### 11.7.3. SNAME

`<SNAME string>` ("system name", a hangover from ITS) is identical in
effect with `<SETG SNM string>`, that is, it causes *string* to
become the *dir* argument used by default by all `SUBR`s which want
file specifications (in the absence of a local value for `SNM`).
`SNAME` returns its argument.

`<SNAME>` is identical in effect with `<GVAL SNM>`, that is, it
returns the current *dir* used by default.

### 11.7.4. ACCESS

    <ACCESS channel fix>

returns *channel*, after making the next character or binary word
(depending on the mode of *channel*, which should not be `"PRINT"`)
which will be input from or output to *channel* the (*fix*+1)st one
from the beginning of the file. *channel* must be open to a randomly
accessible device (`"DSK"`, `"USR"`, etc.). A *fix* of `0` positions
*channel* at the beginning of the file.

### 11.7.5. FILE-LENGTH

    <FILE-LENGTH input:channel>

returns a `FIX`, the length of the file open on *input*. This
information is supplied by the operating system, and it may not be
available, for example, with the `"NET"` device (section 11.10). If
*input*'s mode is `"READ"`, the length is in characters (rounded up
to a multiple of five); if `"READB"`, in binary words. If `ACCESS` is
applied to *input* and this length or more, then the next input
operation will detect the end of file.

### 11.7.6. FILECOPY

    <FILECOPY input:channel output:channel>

copies characters from *input* to *output* until the end of file on
*input* (thus closing *input*) and returns the number of characters
copied. Both arguments are optional, with `.INCHAN` and `.OUTCHAN`
used by default, respectively. The operation is essentially a
`READSTRING` -- `PRINTSTRING` loop. Neither `CHANNEL` need be freshly
`OPEN`ed, and *output* need not be immediately `CLOSE`d. Restriction:
internally a `<FILE-LENGTH input>` is done, which must succeed; thus
`FILECOPY` might lose if *input* is a `"NET"` `CHANNEL`.

### 11.7.7. RESET

    <RESET channel>

returns *channel*, after "resetting" it. Resetting a `CHANNEL` is
like `OPEN`ing it afresh, with only the file-name slots preserved.
For an input `CHANNEL`, this means emptying all input buffers and, if
it is a `CHANNEL` to a file, doing an `ACCESS` to `0` on it. For an
output `CHANNEL`, this means returning to the beginning of the file
-- which implies, if the mode is not `"PRINTO"`, destroying any
output done to it so far. If the opening fails (for example, if the
mode slot of *channel* says input, and if the file specified in its
real-name slots does not exist), `RESET` (like `OPEN`) returns
`#FALSE (reason:string file-spec:string status:fix)`.

### 11.7.8. BUFOUT

    <BUFOUT output:channel>

causes all internal MDL buffers for *output* to be written out and
returns its argument. This is helpful if the operating system or MDL
is flaky and you want to attempt to minimize your losses. The output
may be padded with up to four extra spaces, if *output*'s mode is
`"PRINT"`.

### 11.7.9. RENAME

`RENAME` is for renaming and deleting files. It takes three kinds of
arguments:

* (a) two file names, in either single- or multi-`STRING` format,
  separated by the `ATOM` `TO`,
* (b) one file name in either format, or
* (c) a `CHANNEL` and a file name in either format (only in the ITS
  version).

Omitted file-name parts use the same values by default as does
`OPEN`. If the operation is successful, `RENAME` returns `T`,
otherwise `#FALSE (reason:string status:fix)`.

In case (a) the file specified by the first argument is renamed to
the second argument. For example:

    <RENAME "FOO 3" TO "BAR">       ;"Rename FOO 3 to BAR >."

In case (b) the single file name specifies a file to be deleted. For
example:

    <RENAME "FOO FOO DSK:HARRY;">  ;"Rename FOO 3 to BAR >."

In case (c) the `CHANNEL` must be open in either `"PRINT"` or
`"PRINTB"` mode, and a rename while open for writing is attempted.
The real-name slots in the `CHANNEL` are updated to reflect any
successful change.

## 11.8. Terminal CHANNELs

MDL behaves like the ITS version of the text editor Teco with respect
to typing in carriage-return, in that it automatically adds a
line-feed. In order to type in a lone carriage-return, a
carriage-return followed by a rubout must be typed. Also `PRINT`,
`PRINT1` and `PRINC` do not automatically add a line-feed when a
carriage-return is output. This enables overstriking on a terminal
that lacks backspacing capability. It also means that what goes on a
terminal and what goes in a file are more likely to look the same.

In the ITS version, MDL's primary terminal output channel (usually
`,OUTCHAN`) is normally not in "display" mode, except when `PRINC`ing
a `STRING`. Thus errors will rarely occur when a user is typing in
text containing display-mode control codes.

In the ITS version, MDL can start up without a terminal, give control
of the terminal away to an inferior operating-system process or get
it back while running. Doing a `RESET` on either of the terminal
channels causes MDL to find out if it now has the terminal; if it
does, the terminal is reopened and the current screen size and device
parameters are updated. If it doesn't have the terminal, an internal
flag is set, causing output to the terminal to be ignored and
attempted input from the terminal to make the operating-system
process go to sleep.

In the ITS version, there are some peculiarities associated with
pseudo-terminals (`"STY"` and `"STn"` devices). If the `CHANNEL`
given to `READCHR` is open in `"READ"` mode to a pseudo-terminal, and
if no input is available, `READCHR` returns `-1`, `TYPE` `FIX`. If
the `CHANNEL` given to `READSTRING` is open in `"READ"` mode to a
pseudo-terminal, reading also stops if and when no more characters
are available, that is, when `READCHR` would return `-1`.

## 11.8.1. ECHOPAIR

    <ECHOPAIR terminal-in:channel terminal-out:channel>

returns its first argument, after making the two `CHANNEL`s "know
about each other" so that <kbd>rubout</kbd>, <kbd>^@</kbd>,
<kbd>^D</kbd> and <kbd>^L</kbd> on *terminal-in* will cause the
appropriate output on *terminal-out*.

### 11.8.2. TTYECHO

    <TTYECHO terminal-input:channel pred>

turns the echoing of typed characters on *channel* off or on,
according to whether or not *pred* is `TYPE` `FALSE`, and returns
*channel*. It is useful in conjunction with `TYI` (below) for a
program that wants to do character input and echoing in its own
fashion.

### 11.8.3. TYI

    <TYI terminal-input:channel>

returns one `CHARACTER` from *channel* (optional, `.INCHAN` by
default) when it is typed, rather than after `$` (<kbd>ESC</kbd>) is
typed, as is the case with `READCHR`. The following example echos
input characters as their ASCII values, until a carriage-return is
typed:

    <REPEAT ((FOO <TTYECHO .INCHAN <>>))
       <AND <==? 13 <PRINC <ASCII <TYI .INCHAN>>>>
            <RETURN <TTYECHO .INCHAN T>>>>

## 11.9. Internal CHANNELs

If the *device* specified in an `OPEN` is `"INT"`, a `CHANNEL` is
created which does not refer to any I/O device outside MDL. In this
case, the mode must be `"READ"` or `"PRINT"`, and there is another
argument, which must be a function.

For a `"READ"` `CHANNEL`, the function must take no arguments.
Whenever a `CHARACTER` is desired from this `CHANNEL`, the function
will be applied to no arguments and must return a `CHARACTER`. This
will occur once per call to `READCHR` using this `CHANNEL`, and
several times per call to `READ`. In the ITS version, the function
can signal that its "end-of-file" has been reached by returning
`<CHTYPE *777777000003* CHARACTER>` (-1 in left half, control-C in
right), which is the standard ITS end-of-file signal. In the Tenex
and Tops-20 versions, the function should return either that or
`<CHTYPE *777777000032* CHARACTER>` (-1 and control-Z), the latter
being their standard end-of-file signal.

For a `"PRINT"` `CHANNEL`, the function must take one argument, which
will be a `CHARACTER`. It can dispose of its argument in any way it
pleases. The value returned by the function is ignored.

Example: `<OPEN "PRINT" "INT:" ,FCN>` opens an internal output
`CHANNEL` with `,FCN` as its character-gobbler.

## 11.10. The "NET" Device: the ARPA Network

The `"NET"` device is different in many ways from conventional
devices. In the ITS version, it is the only device besides `"INT"`
that does not take all strings as its arguments to `OPEN`, and it
must take an additional optional argument to specify the byte size of
the socket. The format of a call to open a network socket is

    <OPEN mode:string local-socket:fix "NET" foreign-host:fix byte-size:fix>

where:

* *mode* is the mode of the desired `CHANNEL`. This must be either
  `"READ"`, `"PRINT"`, `"READB"` or `"PRINTB"`.
* *local-socket* is the local socket number. If it is `-1`, the
  operating system will generate a unique local socket number. If it
  is not, in the Tenex and Tops-20 versions, the socket number is
  "fork-relative".
* *foreign-socket* is the foreign socket number. If it is `-1`, this
  is an `OPEN` for "listening".
* *foreign-host* is the foreign host number. If it is an `OPEN` for
  listening, this argument is ignored.
* *byte-size* is the optional byte size. For `"READ"` or `"PRINT"`
  this must be either `7` (used by default) or `8`. For `"READB"` or
  `"PRINTB"`, it can be any integer from `1` to `36` (used by
  default).

In the Tenex and Tops-20 versions, `OPEN` can instead be given a
`STRING` argument of the form `"NET:..."`. In this case the local
socket number can be "directory-relative".

Like any other `OPEN`, either a `CHANNEL` or a `FALSE` is returned.
Once open, a network `CHANNEL` can be used like any other `CHANNEL`,
except that `FILE-LENGTH`, `ACCESS`, `RENAME`, etc., cannot be done.
The "argument" first-name, second-name, and directory-name slots in
the `CHANNEL` are used for local socket, foreign socket, and foreign
host (as specified in the call to `OPEN`), respectively. The
corresponding "real" slots are used somewhat differently. If a
channel is `OPEN`ed with local socket `-1`, the "real" first-name
slot will contain the unique socket number generated by the operating
system. If a listening socket is `OPEN`ed, the foreign socket and
host numbers of the answering host are stored in the "real"
second-name and directory-name slots of the `CHANNEL` when the
Request For Connection is received.

An interrupt (chapter 21) can be associated with a `"NET"`-device
`CHANNEL`, so that a program will know that the `CHANNEL` has or
needs data, according to its *mode*.

There also exist several special-purpose `SUBR`s for the `"NET"`
device. These are described next.

### 11.10.1. NETSTATE

    <NETSTATE network:channel>

returns a `UVECTOR` of three `FIX`es. The first is the state of the
connection, the second is a code specifying why a connection was
closed, and the last is the number of bits available on the
connection for input. The meaning of the state and close codes are
installation-dependent and so are not included here.

### 11.10.2. NETACC

    <NETACC network:channel>

accepts a connection to a socket that is open for listening and
returns its argument. It will return a `FALSE` if the connection is
in the wrong state.

### 11.10.3. NETS

    <NETS network:channel>

returns its argument, after forcing any system-buffered network
output to be sent. ITS normally does this every half second anyway.
Tenex and Tops-20 do not do it unless and until `NETS` is called.
`NETS` is similar to `BUFOUT` for normal `CHANNEL`s, except that even
operating-system buffers are emptied **now**.

