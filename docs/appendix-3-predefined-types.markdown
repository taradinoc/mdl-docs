# Appendix 3. Predefined Types 

On these two pages is a table showing each of MDL's predefined `TYPE`s, its primitive type if 
different, and various flags: `S` for `STRUCTURED`, `E` for `EVALTYPE` not `QUOTE`, and `A` for `APPLICABLE`. 

`X` means that an object of that `TYPE` cannot be `CHTYPE`d to and hence cannot be `READ` in (if 
attempted, a `CAN'T-CHTYPE-INTO` error is usual). 

`B` means that an object of that `TYPE` cannot be `READ` in (if attempted, a `STORAGE-TYPES-DIFFER` 
error is usual), that instead it is built by the interpreter or `CHTYPE`d to by a program, and that its 
`PRINT`ed representation makes it look as though its `TYPEPRIM` were different. 

`%` means that an object of that `TYPE` is `PRINT`ed using `%` notation and can be `READ` in only that way. 


| `TYPE`        | `TYPEPRIM`      | `S` | `E` | `A` |       | comments                                                    |
| ------        | ----------      | --- | --- | --- | ----- | --------                                                    |
| `ACTIVATION`  | `FRAME`         |     |     |     | `X`   |                                                             |
| `ASOC`        |                 |     |     |     | `B`   | sic: only one `S`                                           |
| `ATOM`        |                 |     |     |     |       |                                                             |
| `BITS`        | `WORD`          |     |     |     |       |                                                             |
| `BYTES`       |                 | `S` |     |     |       |                                                             |
| `CHANNEL`     | `VECTOR`        | `S` |     |     | `X`   |                                                             |
| `CHARACTER`   | `WORD`          |     |     |     |       |                                                             |
| `CLOSURE`     | `LIST`          | `S` |     | `A` |       |                                                             |
| `CODE`        | `UVECTOR`       | `S` |     |     |       |                                                             |
| `DECL`        | `LIST`          | `S` |     |     |       |                                                             |
| `DISMISS`     | `ATOM`          |     |     |     |       | can be returned by interrupt handler                        |
| `ENVIRONMENT` | `FRAME`         |     |     |     | `B`   |                                                             |
| `FALSE`       | `LIST`          | `S` |     |     |       |                                                             |
| `FIX`         | `WORD`          |     |     | `A` |       |                                                             |
| `FLOAT`       | `WORD`          |     |     |     |       |                                                             |
| `FORM`        | `LIST`          | `S` | `E` |     |       |                                                             |
| `FRAME`       |                 |     |     |     | `B`   |                                                             |
| `FSUBR`       | `WORD`          |     |     | `A` | `X`   |                                                             |
| `FUNCTION`    | `LIST`          | `S` |     | `A` |       |                                                             |
| `HANDLER`     | `VECTOR`        | `S` |     |     | `X`   |                                                             |
| `IHEADER`     | `VECTOR`        | `S` |     |     | `X`   | "interrupt header"                                          |
| `ILLEGAL`     | `WORD`          |     |     |     | `X`   | Garbage collector may put this on non-`LEGAL?` object.      |
| `INTERNAL`    | `INTERNAL-TYPE` |     |     |     | `X`   | should not be seen by programs                              |
| `LINK`        | `ATOM`          |     |     |     | `X`   | for terminal shorthand                                      |
| `LIST`        |                 | `S` | `E` |     |       |                                                             |
| `LOCA`        |                 |     |     |     | `B`   | locative to `TUPLE`                                         |
| `LOCAS`       |                 |     |     |     | `B`   | locative to `ASOC`                                          |
| `LOCB`        |                 |     |     |     | `B`   | locative to `BYTES`                                         |
| `LOCD`        |                 |     |     |     | `%`   | locative to `G/LVAL`                                        |
| `LOCL`        |                 |     |     |     | `B`   | locative to `LIST`                                          |
| `LOCR`        |                 |     |     |     | `%`   | locative to `GVAL` in pure program                          |
| `LOCS`        |                 |     |     |     | `B`   | locative to `STRING`                                        |
| `LOCT`        |                 |     |     |     | `B`   | locative to `TEMPLATE`                                      |
| `LOCU`        |                 |     |     |     | `B`   | locative to `UVECTOR`                                       |
| `LOCV`        |                 |     |     |     | `B`   | locative to `VECTOR`                                        |
| `LOSE`        | `WORD`          |     |     |     |       | a place holder                                              |
| `MACRO`       | `LIST`          | `S` |     | `A` |       |                                                             |
| `OBLIST`      | `UVECTOR`       | `S` |     |     | `X`   |                                                             |
| `OFFSET`      | `OFFSET`        |     |     | `A` | `%`   |                                                             |
| `PCODE`       | `WORD`          |     |     |     | `%`   | "pure code"                                                 |
| `PRIMTYPE-C`  | `WORD`          |     |     |     | `%`   | "primtype code"                                             |
| `PROCESS`     |                 |     |     |     | `B`   |                                                             |
| `QUICK-ENTRY` | `VECTOR`        | `S` |     | `A` | `%`   | an `RSUBR-ENTRY` that has been `QCALL`ed and `RSUBR-LINK`ed |
| `QUICK-RSUBR` | `VECTOR`        | `S` |     | `A` | `%/B` | an `RSUBR` that has been `QCALL`ed and `RSUBR-LINK`ed       |
| `READA`       | `FRAME`         |     |     |     | `X`   | in eof slot during recursive `READ` via `READ-TABLE`        |
| `RSUBR`       | `VECTOR`        | `S` |     | `A` | `%/B` | if code vector is pure/impure, respectively                 |
| `RSUBR-ENTRY` | `VECTOR`        | `S` |     | `A` | `%`   |                                                             |
| `SEGMENT`     | `LIST`          | `S` | `E` |     |       |                                                             |
| `SPLICE`      | `LIST`          | `S` |     |     |       | for returning many things via `READ-TABLE`                  |
| `STORAGE`     |                 | `S` |     |     |       | If possible, use `FREEZE` `SUBR` instead.                   |
| `STRING`      |                 | `S` |     |     |       |                                                             |
| `SUBR`        | `WORD`          |     |     | `A` | `X`   |                                                             |
| `TAG`         | `VECTOR`        | `S` |     |     | `X`   | for non-local `GO`s                                         |
| `TEMPLATE`    |                 | `S` |     |     | `B`   | The interpreter itself can't build one. See Lebling (1979). |
| `TIME`        | `WORD`          |     |     |     |       | used internally to identify `FRAME`s                        |
| `TUPLE`       |                 | `S` |     |     | `B`   | vector on the control stack                                 |
| `TYPE-C`      | `WORD`          |     |     |     | `%`   | "type code"                                                 |
| `TYPE-W`      | `WORD`          |     |     |     | `%`   | "type word"                                                 |
| `UNBOUND`     | `WORD`          |     |     |     | `X`   | value of unassigned but bound `ATOM`, as seen by locatives  |
| `UVECTOR`     |                 | `S` | `E` |     |       | "uniform vector"                                            |
| `VECTOR`      |                 | `S` | `E` |     |       |                                                             |
| `WORD`        |                 |     |     |     |       |                                                             |
