# Chapter 19. Compiled Programs

## 19.1. RSUBR (the TYPE)

`RSUBR`s ("relocatable subroutines") are machine-language programs
written to run in the MDL environment. They are usually produced by
the MDL assembler (often from output produced by the compiler)
although this is not necessary. All `RSUBR`s have two components: the
"reference vector" and the "code vector". In some cases the code
vector is in pure storage. There is also a set of "fixups" associated
with every `RSUBR`, although it may not be available in the running
MDL.

## 19.2. The Reference Vector

An `RSUBR` is basically a `VECTOR` that has been `CHTYPE`d to `TYPE`
`RSUBR` via the `SUBR` `RSUBR` (see below). This ex-`VECTOR` is the
reference vector. The first three elements of the reference vector
have predefined meanings:

* The first element is of `TYPE` `CODE` or `PCODE` and is the impure
or pure code vector respectively.
* The second element is an `ATOM` and specifies the name of the
`RSUBR`.
* The third element is of `TYPE` `DECL` and declares the
type/structure of the `RSUBR`'s arguments and result.

The rest of the elements of the reference vector are objects in
garbage-collected storage that the `RSUBR` needs to reference and any
impure slots that the `RSUBR` needs to use.

When the `RSUBR` is running, one of the PDP-10 accumulators (with
symbolic name `R`) is always pointing to the reference vector, to
permit rapid access to the various elements.

## 19.3. RSUBR Linking

`RSUBR`s can call any `APPLICABLE` object, all in a uniform manner. In
general, a call to an F/SUBR is linked up at assembly/compile time so
that the calling instruction (UUO) points directly at the code in the
interpreter for the F/SUBR. However, the locations of most other
`APPLICABLE`s are not known at assembly/compile time. Therefore, the
calling UUO is set up to point at a slot in the reference vector (by
indexing off accumulator `R`). This slot initially contains the `ATOM`
whose G/LVAL is the called object. The calling mechanism (UUO handler)
causes control to be transferred to the called object and, depending
on the state of the `RSUBR`-link flag, the `ATOM` will be replaced by
its G/LVAL. (If the call is of the "quick" variety, the called `RSUBR`
or `RSUBR-ENTRY` will be `CHTYPE`d to a `QUICK-RSUBR` or
`QUICK-ENTRY`, respectively, before replacement.) Regardless of the
`RSUBR`-link flag's state, calls to `FUNCTION`s are never permanently
linked. A call to a non-Subroutine generates an extra `FRAME`, whose
`FUNCT` is the dummy `ATOM` `CALLER`.

`RSUBR`s are linked together for faster execution, but linking may not
be desirable if the `RSUBR`s are being debugged, and various revisions
are being re-loaded. A linked call will forever after go to the same
code, regardless of the current G/LVAL of the called `ATOM`. Thus,
while testing `RSUBR`s, you may want to disable linking, by calling
the `RSUBR-LINK` `SUBR` with a `FALSE` argument. Calling it with a
non-`FALSE` argument enables linking thereafter. It returns the
previous state of the link flag, either `T` or `#FALSE ()`. Calling it
with no argument returns the current state.

## 19.4. Pure and Impure Code

The first element of an `RSUBR` is the code vector, of `TYPE` `CODE`
or `PCODE`. `TYPE` `CODE` is of `PRIMTYPE` `UVECTOR`, and the `UTYPE`
should be of `PRIMTYPE` `WORD`. The code vector is simply a block of
words that are the instructions which comprise the `RSUBR`. Since the
code vector is stored just like a standard `UVECTOR`, it will be moved
around by the garbage collector. Therefore, all `RSUBR` code is
required to be location-insensitive. The compiler guarantees the
location-insensitivity of its output. The assembler helps to make the
code location-insensitive by defining all labels as offsets relative
to the beginning of the code vector and causing instructions that
refer to labels to index automatically off the PDP-10 accumulator
symbolically named `M`. `M`, like `R`, is set up by the UUO handler,
but it points to the code vector instead of the reference vector. The
code vector of an `RSUBR` can be frozen (using the `FREEZE` `SUBR`) to
prevent it from moving during debugging by DDT in the superior
operating-system process.

If the first element of an `RSUBR` is of `TYPE` `PCODE` ("pure code"),
the code vector of the `RSUBR` is pure and sharable. `TYPE` `PCODE` is
of `PRIMTYPE` `WORD`. The left half of the word specifies an offset
into an internal table of pure `RSUBR`s, and the right half specifies
an offset into the block of code where this `RSUBR` starts. The
`PCODE` prints out as:

    %<PCODE name:string offset:fix>

where *name* names the entry in the user's pure-`RSUBR` table, and
*offset* is the offset. (Obviously, `PCODE` is also the name of a
`SUBR`, which generates a pure code vector.) Pure `RSUBR`s may also
move around, but only by being included in MDL's page map at different
places. Once again `M` can be used exactly as before to do
location-independent address referencing. Individual pure code vectors
can be "unmapped" (marked as being not in primary storage but in their
original pure-code disk files) if the space in storage allocated for
pure code is exhausted. An unmapped `RSUBR` is mapped in again
whenever needed. All pure `RSUBR`s are unmapped before a `SAVE` file
is written, so that the code is not duplicated on disk. A purified
`RSUBR` must use `RGLOC` ("relative GLOC") instead of `GLOC`. `RGLOC`
produces objects of `TYPE` `LOCR` instead of `LOCD`.

# 19.5. TYPE-C and TYPE-W

In order to handle user `NEWTYPE`s reasonably, the internal `TYPE`
codes for them have to be able to be different from one MDL run to
another. Therefore, references to the `TYPE` codes must be in the
reference vector rather than the code vector. To help handle this
problem, two `TYPE`s exist, `TYPE-C` ("type code") and `TYPE-W` ("type
word"), both of `PRIMTYPE` `WORD`. They print as:

    %<TYPE-C type primtype:atom>
    %<TYPE-W type primtype:atom>

The `SUBR` `TYPE-C` produces an internal `TYPE` code for the *type*,
and `TYPE-W` produces a prototype "`TYPE` word" (appendix 1) for an
object of that `TYPE`. The *primtype* argument is optional, included
only as a check against the call to `NEWTYPE`. `TYPE-W` can also take
a third argument, of `PRIMTYPE` `WORD`, whose right half is included
in the generated "`TYPE` word". If *type* is not a valid `TYPE`, a
`NEWTYPE` is automatically done.

To be complete, a similar `SUBR` and `TYPE` should be mentioned here.

    <PRIMTYPE-C type>

produces an internal "storage allocation code" (appendix 1) for the
*type*. The value is of `TYPE` `PRIMTYPE-C`, `PRIMTYPE` `WORD`. In
almost all cases the `SUBR` `TYPEPRIM` gives just as much information,
except in the case of `TEMPLATE`s: all `TYPE`s of `TEMPLATE`s have the
same `TYPEPRIM`, but they all have different `PRIMTYPE-C`s.

## 19.6. RSUBR (the SUBR)

    <RSUBR [code name decl ref ref ...]>

`CHTYPE`s its argument to an `RSUBR`, after checking it for legality.
`RSUBR` is rarely called other than in the MDL Assembler (Lebling,
1979). It can be used if changes must be made to an `RSUBR` that are
prohibited by MDL's built-in safety mechanisms. For example, if the
`GVAL` of *name* is an `RSUBR`:

    <SET FIXIT <CHTYPE ,name VECTOR>>$
    [...]

    ...(changes to .FIXIT)...

    <SETG name <RSUBR .FIXIT>>$
    #RSUBR [...]

## 19.7. RSUBR-ENTRY

`RSUBR`s can have multiple entry points. An `RSUBR-ENTRY` can be
applied to arguments exactly like an `RSUBR`.

    <RSUBR-ENTRY [rsubr-or-atom name:atom decl] offset:fix>

returns the `VECTOR` argument `CHTYPE`d to an `RSUBR-ENTRY` into the
*rsubr* at the specified *offset*. If the `RSUBR-ENTRY` is to have a
`DECL` (`RSUBR` style), it should come as shown.

    <ENTRY-LOC rsubr-entry>

("entry location") returns the *offset* into the `RSUBR` of this
entry.

## 19.8. RSUBRs in Files

There are three kinds of files that can contain `RSUBR`s, identified
by second names `BINARY`, `NBIN` and `FBIN`. There is nothing magic
about these names, but they are used by convention.

A `BINARY` file is a completely ASCII file containing complete impure
`RSUBR`s in character representation. Even a code vector appears as
`#CODE` followed by a `UVECTOR` of `PRIMTYPE` `WORD`s. `BINARY` files
are generally slow to load, because of all the parsing that must be
done.

An `NBIN` file contains a mixture of ASCII characters and binary code.
The start of a binary portion is signalled to `READ` by the character
control-C, so naive readers of an `NBIN` file under ITS may
incorrectly assume that it ends before any binary code appears. An
`NBIN` file cannot be edited with a text editor. An `RSUBR` is written
in `NBIN` format by being `PRINT`ed on a `"PRINTB"` `CHANNEL`. The
`RSUBR`s in `NBIN` files are not purified either.

An `FBIN` file is actually part of a triad of files. The `FBIN`
file(s) itself is the impure part of a collection of purified
`RSUBR`s. It is simply ASCII and can be edited at will. (Exception: in
the ITS and Tops-20 versions, the first object in the file should not
be removed or changed in any way, lest a "grim reaper" program for
`FBIN` files think that the other files in the triad are obsolete and
delete them.) The pure code itself resides (in the ITS and Tops-20
versions) in a special large file that contains all currently-used
pure code, or (in the Tenex version) in a file in a special disk
directory with first name the same as the *name* argument to `PCODE`
for the `RSUBR`. The pure-code file is page-mapped directly into MDL
storage in read-only mode. It can be unmapped when the pure storage
must be reclaimed, and it can be mapped at a different storage address
when pure storage must be compacted. There is also a "fixup" file (see
below) or portion of a file associated with the `FBIN` to round out
the triad.

An initial MDL can have pure `RSUBR`s in it that were "loaded" during
the initialization procedure. The files are not page-mapped in until
they are actually needed. The "loading" has other side effects, such
as the creation of `OBLIST`s (chapter 15). Exactly what is pre-loaded
is outside the scope of this document.

## 19.9. Fixups

The purpose of "fixups" is to correct references in the `RSUBR` to
parts of the interpreter that change from one release of MDL to the
next. The reason the fixups contain a release number is so that they
can be completely ignored when an `RSUBR` is loaded into the same
release of MDL as that from which it was last written out.

There are three forms of fixups, corresponding to the three kinds of
`RSUBR` files. ASCII `RSUBR`s, found in `BINARY` files, have ASCII
fixups. The fixups are contained in a `LIST` that has the following
format:

    (MDL-release:fix
        name:atom value:fix (use:fix use:fix ...)
        name:atom value:fix (use:fix use:fix ...)
        ...)

The fixups in `NBIN` files and the fixup files associated with `FBIN`
files are in a fast internal format that looks like a `UVECTOR` of
`PRIMTYPE` `WORD`s.

Fixups are usually discarded after they are used during the loading
procedure. However, if, while reading a `BINARY` or `NBIN` file the
`ATOM` `KEEP-FIXUPS!-` has a non-`FALSE` `LVAL`, the fixups will be
kept, via an association between the `RSUBR` and the `ATOM` `RSUBR`.
It should be noted that, besides correcting the code, the fixups
themselves are corrected when `KEEP-FIXUPS` is bound and true. Also,
the assembler and compiler make the same association when they first
create an `RSUBR`, so that it can be written out with its fixups.

In the case of pure `RSUBR`s (`FBIN` files), things are a little
different. If a pure-code file exists for this release of MDL, it is
used immediately, and the fixups are completely ignored. If a
pure-code file for this release doesn't exist, the fixup file is used
to create a new copy of the file from an old one, and also a new
version of the fixup file is created to go with the new pure-code
file. This all goes on automatically behind the user's back.