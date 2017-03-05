# Chapter 2. Read, Evaluate, and Print

## 2.1 General [1]

Once you type `$` and all brackets are correctly paired and nested, 
the current contents of the input buffer go through processing by 
three functions successively: first `READ`, whcih passes its output to 
`EVAL` ("evaluate"), which passes its output to `PRINT`, whose output 
is typed on the terminal.

[Actually, the sequence is more like `READ`, `CRLF`, `EVAL`, `PRINT`, 
`CRLF` (explained in chapter 11); MDL gives you a carriage-return 
line-feed when the `READ` is complete, that is, when all brackets are 
paired.]

Functionally:

* `READ`: printable representations → MDL objects
* `EVAL`: MDL objects → MDL objects
* `PRINT`: MDL objects → printable representations

That is, `READ` takes ASCII text, such as is typed in at a terminal, 
and creates the MDL objects represented by that text. `PRINT` takes 
MDL objects, creates ASCII text representations of them, and types 
them out. `EVAL`, which is the really important one, performs 
transformations on MDL objects.

## 2.2 Philosophy (TYPEs) [1]

In a general sense, when you are interacting with MDL, you are dealing 
with a world inhabited only by a particular set of objects: MDL 
objects.

MDL objects are best considered as abstract entities with abstract 
properties. The properties of a particular MDL object depend on the 
class of MDL objects to which it belongs. This class is the `TYPE` of 
the MDL object. Every MDL object has a `TYPE`, and every `TYPE` has 
its own peculiarities. There are many different `TYPE`s in MDL: they 
will gradually be introduced below, but in the meantime here is a 
representative sample: `SUBR` (the `TYPE` of `READ`, `EVAL`, and 
`PRINT`), `FSUBR`, `LIST`, `VECTOR`, `FORM`, `FUNCTION`, etc. Since 
every object has a `TYPE`, one often abbreviates "an object of `TYPE` 
*type*" by saying "a *type*".

The laws of the MDL world are defined by `EVAL`. In a very real sense, 
`EVAL` is the only MDL object which "acts", which "does something". In 
"acting", `EVAL` is always "following the directions" of some MDL 
object. Every MDL object should be looked upon as supplying a set of 
directions to `EVAL`; what these directions are depends heavily on the 
`TYPE` of the MDL object.

Since `EVAL` is so ever-present, an abbreviation is in order: 
"evaluates to *something*" or "`EVAL`s to *something*" should be taken 
as an abbreviation for "when given to `EVAL`, causes `EVAL` to return 
*something*".

As abstract entities, MDL objects are, of course, not "visible". There 
is, however, a standard way of representing abstract MDL objects in 
the real world. The standard way of representing any given `TYPE` of 
MDL object will be given below when the `TYPE` is introduced. These 
standard representations are what `READ` understands, and what `PRINT` 
produces.

## 2.3 Example (TYPE FIX) [1]

```no-highlight
1$
1
```

The following has occurred:

First, `READ` recognized the character `1` as the representation for 
an object of `TYPE` `FIX`, in particular the one which corresponds to 
the integer one. (`FIX` means integer, because the decimal point is 
understood always to be in a fixed position: at the right-hand end.) 
`READ` build the MDL object corresponding to the decimal 
representation typed, and returned it.

Then `EVAL` noted that its input was of `TYPE` `FIX`. An object of 
`TYPE` `FIX` evaluates to itself, so `EVAL` returned its input 
undisturbed.

Then `PRINT` saw that its input was of `TYPE` `FIX`, and printed on 
the terminal the decimal characer representation of the corresponding 
integer.

## 2.4 Example (TYPE FLOAT) [1]

```no-highlight
1.0$
1.0
```

What went on was entirely analogous to the preceding example, except 
that the MDL object was of `TYPE` `FLOAT`. (`FLOAT` means a real 
number (of limited precision), because the decimal point can float 
around to any convenient position: an internal exponent part tells 
where it "really" belongs.)

## 2.5 Example (TYPE ATOM, PNAME) [1]

```no-highlight
GEORGE$
GEORGE
```

This time a lot more has happened.

`READ` noted that what was typed had no special meaning, and therefore 
assumed that it was the representation of an identifier, that is, an 
object of `TYPE` `ATOM`. ("Atom" means more or less *indivisible*.) 
`READ` therefore attempted to look up the representation in a table it 
keeps for such purposes [a `LIST` of `OBLISTS`, available as the local 
value of the `ATOM` `OBLIST`]. If `READ` finds an `ATOM` in its table 
corresponding to the representation, that `ATOM` is returned as 
`READ`'s value. If `READ` fails in looking up, it creates a new 
`ATOM`, puts it in the table with the representation read [`INSERT` 
into `<1 .OBLIST>` usually], and returns the new `ATOM`. Nothing which 
could in any way be referenced as a legal "value" is attached to the 
new `ATOM`. The initially-typed representation of an `ATOM` becomes 
its `PNAME`, meaning its name for `PRINT`. One often abbreviates 
"object of `TYPE` `ATOM` with `PNAME` *name*" by saying "`ATOM` 
*name*".

`EVAL`, given an `ATOM`, returned just that `ATOM`.

`PRINT`, given an `ATOM`, typed out its `PNAME`.

At the end of this chapter, the question "what is a legal `PNAME`" 
will be considered. Further on, the mehtods used to attach values to 
`ATOM`s will be described.

## 2.6 FIXes, FLOATs, and ATOMs versus READ: Specifics

### 2.6.1 READ and FIXed-point Numbers

`READ` considers any grouping of characters which are solely digits to 
be a `FIX`, and the radix of the representation is decimal by default. 
A `-` (hyphen) immediately preceding such a grouping represents a 
negative `FIX`. The largest `FIX` representable on the PDP-10 is two 
to the 35th power minus one, or 34,359,738,367 (decimal): the smallest 
is one less than the negative of that number. If you attempt to type 
in a `FIX` outside that range, `READ` converts it to a `FLOAT`; if a 
program you write attempts to produce a `FIX` outside that range, an 
overflow error will occur (unless it is disabled).

The radix used by `READ` and `PRINT` is changeable by the user; 
however, there are two formats for representations of `FIX`es which 
cause `READ` to use a specified radix independent of the current one. 
These are as follows:

1. If a group of digits is immediately followed by a period (`.`), 
`READ` interprets that group as the decimal representation of a `FIX`. 
For example, `10.` is always interpreted by `READ` as the decimal 
representation of ten.

2.  If a group of digits is immediately enclosed on both sides with 
asterisks (`*`), `READ` interprets that group as the octal 
representation of a `FIX`. For example, `*10*` is always interpreted 
by `READ` as the octal representation of eight.

### 2.6.2 READ and PRINT versus FLOATing-point Numbers

`PRINT` can produce, and `READ` can understand, two different formats 
for objects of `TYPE` `FLOAT`. The first is "decimal-point" notation, 
the second is "scientific" notation. Decimal radix is always used for 
representations of `FLOAT`s.

"Decimal-point" notation for a `FLOAT` consists of an arbitrarily long 
string of digits containing one `.` (period) which is followed by at 
least one digit. `READ` will make a `FLOAT` out of any such object, 
with a limit of precision of one part in 2 to the 27th power.

"Scientific" notation consists of:

1. a number,

2. immediately followed by `E` or `e` (upper or lower case letter E),

3. immediately followed by an exponent,

where a "number" is an arbitrarily long string of digits, with or 
without a decimal point (see following note): an an "exponent" is up 
to two digits worth of `FIX`. This notation represents the "number" to 
the "exponent" power of ten. Note: if the "number" as above would by 
itself be a `FIX`, and if the "exponent" is positive, and if the 
result is within the allowed range of `FIX`es, then the result will be 
a `FIX`. For example, `READ` understands `10E1` as `100` (a `FIX`), 
but `10E-1` as `1.0000000` (a `FLOAT`).

The largest-magnitude `FLOAT` which can be handled without overflow is 
`1.7014118E+38` (decimal radix). The smallest-magnitude `FLOAT` which 
can be handled without underflow is `.14693679E-38`.

### 2.6.3 READ and PNAMEs

The question "what is a legal `PNAME`?" is actually not a reasonable 
one to ask: **any** non-empty string of **arbitrary** characters can 
be the `PNAME` of an `ATOM`, However, some `PNAME`s are easier to type 
to `READ` than others. But even the question "what are easily typed 
`PNAME`s?" is not too reasonable, because: `READ` decides that a group 
of characters is a `PNAME` by **default**: if it can't possibly be 
anything else, it's a `PNAME`. So, the rules governing the 
specification of `PNAME`s are messy, and best expressed in terms of 
what is not a `PNAME`. For simplicity, you can just consider any 
uninterrupted group of upper- and lower-case letters and (customarily) 
hyphens to be a `PNAME`; that will always work. If you neither a 
perfectionist nor a masochist, skip to the next chapter.

#### 2.6.3.1 Non-PNAMEs

A group of characters is **not** a `PNAME` if:

1. It represents a `FLOAT` or a `FIX`, as described above—that is, it 
is composed wholly of digits, or digits and a single `.` (period) or 
digits and a `.` and the letter `E` or `e` (with optional minus signs 
in the right places).

2. It begins with a `.` (period).

3. It contains—if typed interactively—any of the characters which have 
special interactive effects: `^@`, `^D`, `^L`, `^G`, `^O`, `$` 
(`ESC`), rubout.

4. It contains a format character—space, carriage-return, line-feed, 
form-feed, horizontal tab, vertical tab.

5. It contains a `,` (comma) or a `#` (number sign) or a `'` (single 
quote) or a `;` (semicolon) or a `%` (percent sign).

6. It contains any variety of bracket—`(` or `)` or `[` or `]` or `<` 
or `>` or `{` or `}` or `"`.

In addition, the character `\` (backslash) has a special 
interpretation, as mentioned below. Also the pair of characters `!-` 
(exclamation-point hyphen) has an extremely special interpretation, 
which you will reach at chapter 15.

The characters mentioned in cases 4 through 6 are "separators"—that 
is, they signal to `READ` that whatever it was that the preceding 
characters represented, it's done now. They can also indicate the 
start of a new object's representation (all the opening "brackets" do 
just that).

#### 2.6.3.2 Examples

The following examples are not in the "standard format" of "*line 
typed in*`$` *result printed*", because they are not, in some cases, 
completed objects; hence, `READ` would continue waiting for the 
brackets to be closed. In other cases, they will produce errors during 
`EVAL`uation if other—currently irrelevant—conditions are not met. 
Instead, the right-hand column will be used to state just what `READ` 
thought the input in the left-hand column really was.

 Input                    | Explanation
--------------------------|--------------------------------------------------------
`ABC$`                    | an `ATOM` of `PNAME` `ABC`
`abc$`                    | an `ATOM` of `PNAME` `abc`
`ARBITRARILY-LONG-PNAME$` | an `ATOM` of `PNAME` `ARBITRARILY-LONG-PNAME`
`1.2345$`                 | a `FLOAT`, `PRINT`ed as `1.2345000`
`1.2.345$`                | an `ATOM` of `PNAME` `1.2.345`
`A.or.B$`                 | a `ATOM` of `PNAME` `A.or.B`
`.A.or.B$`                | not an `ATOM`, but (as explained later) a `FORM` containing an `ATOM` of `PNAME` `A.or.B`.
`MORE THAN ONE$`          | three `ATOM`s, with `PNAME`s `MORE`, and `THAN`, and `ONE`.
`ab(cd$`                  | an `ATOM` of `PNAME` `ab`, followed by the start of something else (The something else will contain an `ATOM` of `PNAME` beginning `cd.`)
`12345A34$`               | an `ATOM` of `PNAME` `12345A35` (If the A had been an E, the object would have been a `FLOAT`.)


#### 2.6.3.3 \ (Backslash) in ATOMs

If you have a strange, uncontrollable compulsion to have what were 
referred to as "separators" above as part of the `PNAME`s of your 
`ATOM`s, you cn do so by preceding them with the character `\` 
(backslash). `\` will also magically turn an otherwise normal `FIX` or 
`FLOAT` into an `ATOM` if it appears amongst the digits. In fact, 
backslash in front of **any** character changes it from something 
special to "just another character" (including the character `\`). It 
is an escape character.

When `PRINT` confronts an `ATOM` which had to be backslashed in order 
to be an `ATOM`, it will dutifully type out the required `\`s. They 
will not, however, necessarily be where you typed them; they will 
instead be at those positions which will cause `READ` the least grief. 
For example, `PRINT` will type out a `PNAME` which consists wholly of 
digits by first typing a `\` and then typing the digits—no matter 
where you originally typed the `\` (or `\`s).

#### 2.6.3.4 Examples of Awful ATOMs

The following examples illustrate the amount of insanity that can be 
perpetrated by using `\`. The format of the examples is again 
non-standard, this time not because anything is unfinished or in 
error, but because commenting is needed: `PRINT` doesn't do it full 
justice.

 Input                 | Explanation
-----------------------|--------------------------------------------------------
`a\ one\ and\ a\ two$` | one `ATOM`, whose `PNAME` has four spaces in it
`1234\56789$`          | an `ATOM` of `PNAME` `123456789`, which `PRINT`s as `\1233456789`
`123\ $`               | an `ATOM` of `PNAME` `123space`, which `PRINT`s as `\123\ `, with a space on the end
`\\$`                  | an `ATOM` whose `PNAME` is a single backslash
