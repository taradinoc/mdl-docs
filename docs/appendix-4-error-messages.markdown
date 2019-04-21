# Appendix 4. Error Messages

This is a list of all error-naming ATOMs initially in the ERRORS OBLIST, in the left-hand column,
and appropriate examples or elucidations, where necessary, in the right-hand column.

|                                                           |                                                                                                          |
| ---                                                       | ---                                                                                                      |
| `ACCESS-FAILURE`                                          | `ACCESS`, `RESTORE` (Tenex and Tops-20 versions only)                                                    |
| `ALREADY-DEFINED-ERRET-NON-FALSE-TO-REDEFINE`             |                                                                                                          |
| `APPLY-OR-STACKFORM-OF-FSUBR`                             | First argument to `APPLY`, `STACKFORM`, MAPF/R doesn't `EVAL` all its arguments.                         |
| `ARG-WRONG-TYPE`                                          |                                                                                                          |
| `ARGUMENT-OUT-OF-RANGE`                                   | `<ASCII 999>$` Second argument to `NTH` or `REST` too big or small.                                      |
| `ATOM-ALREADY-THERE`                                      | `<INSERT "T" <ROOT>>$` `<LINK 'T "T" <ROOT>>$`                                                           |
| `ATOM-NOT-TYPE-NAME-OR-SPECIAL-SYMBOL`                    | `DECL` problem                                                                                           |
| `ATOM-ON-DIFFERENT-OBLIST`                                | `INSERT`, `LINK`, `REMOVE`                                                                               |
| `ATTEMPT-TO-BREAK-OWN-SEQUENCE`                           | `<BREAK-SEQ T <ME>>$`                                                                                    |
| `ATTEMPT-TO-CHANGE-MANIFEST-VARIABLE`                     |                                                                                                          |
| `ATTEMPT-TO-CLOSE-TTY-CHANNEL`                            | `<CLOSE ,INCHAN>$`                                                                                       |
| `ATTEMPT-TO-DEFER-UNDEFERABLE-INTERRUPT`                  | "Undeferable" interrupt (e.g. `"ERROR"`) while `INT-LEVEL` is too high to handle it                      |
| `ATTEMPT-TO-GROW-VECTOR-TOO-MUCH`                         | `GROW` argument greater than `<* 16 1024>`                                                               |
| `ATTEMPT-TO-MUNG-ATOMS-PNAME`                             | `<PUT <SPNAME T> 1 !\T>$`                                                                                |
| `ATTEMPT-TO-MUNG-PURE-STRUCTURE`                          | attempt to write into pure page                                                                          |
| `ATTEMPT-TO-SUICIDE-TO-SELF`                              | `<SUICIDE <ME>>$`                                                                                        |
| `BAD-ARGUMENT-LIST`                                       | `<GDECL ("HI") STRING>$`                                                                                 |
| `BAD-ASCII-CHARACTER`                                     | A character with wrong byte size or ASCII code more than 177 octal has been read (how?).                 |
| `BAD-BYTES-DECL`                                          |                                                                                                          |
| `BAD-CHANNEL`                                             |                                                                                                          |
| `BAD-CLAUSE`                                              | Argument to `COND` is non-`LIST` or empty `LIST`.                                                        |
| `BAD-DECLARATION-LIST`                                    | `DECL` in bad form                                                                                       |
| `BAD-DEFAULT-OBLIST-SPECIFICATION`                        | bad use of `DEFAULT` in `LIST` of `OBLIST`s                                                              |
| `BAD-ENTRY-BLOCK`                                         | `RSUBR-ENTRY` does not point to good `RSUBR`.                                                            |
| `BAD-ENVIRONMENT`                                         |                                                                                                          |
| `BAD-FIXUPS`                                              |                                                                                                          |
| `BAD-FUNARG`                                              | `CLOSURE` in bad form                                                                                    |
| `BAD-GC-READ-FILE`                                        |                                                                                                          |
| `BAD-INPUT-BUFFER`                                        | (for a `CHANNEL`)                                                                                        |
| `BAD-LINK`                                                | `<GUNASSIGN <CHTYPE link ATOM>>`                                                                         |
| `BAD-MACRO-TABLE`                                         | `.READ-TABLE` or `.PARSE-TABLE` is not a vector.                                                         |
| `BAD-OBLIST-OR-LIST-THEREOF`                              | Alleged look-up list is not of `TYPE` `OBLIST` or `LIST`.                                                |
| `BAD-PARSE-STRING`                                        | non-`STRING` argument to `PARSE`                                                                         |
| `BAD-PNAME`                                               | attempt to output `ATOM` with missing or zero-length `PNAME`                                             |
| `BAD-PRIMTYPEC`                                           |                                                                                                          |
| `BAD-TEMPLATE-DATA`                                       |                                                                                                          |
| `BAD-TYPE-CODE`                                           |                                                                                                          |
| `BAD-TYPE-NAME`                                           | `ATOM` purports to be a `TYPE` but isn't.                                                                |
| `BAD-TYPE-SPECIFICATION`                                  | `DECL` problem                                                                                           |
| `BAD-USE-OF-BYTE-STRING`                                  | `#3$`                                                                                                    |
| `BAD-USE-OF-MACRO`                                        |                                                                                                          |
| `BAD-USE-OF-SQUIGGLY-BRACKETS`                            | `{}$`                                                                                                    |
| `BAD-VECTOR`                                              | Bad argument to `RSUBR-ENTRY`                                                                            |
| `BYTE-SIZE-BAD`                                           | `"NET" CHANNEL`                                                                                          |
| `CANT-CHTYPE-INTO`                                        | `<CHTYPE 1 SUBR>$`                                                                                       |
| `CANT-FIND-TEMPLATE`                                      | attempt to `GC-READ` a structure containing a `TEMPLATE` whose `TYPE` does not exist                     |
| `CANT-OPEN-OUTPUT-FILE`                                   | `SAVE`                                                                                                   |
| `CANT-RETRY-ENTRY-GONE`                                   | attempt to `RETRY` a call to an `RSUBR-ENTRY` whose `RSUBR` cannot be found                              |
| `CANT-SUBSTITUTE-WITH-STRING-OR-TUPLE-AND-OTHER`          | `<SUBSTITUTE "T" T>$`                                                                                    |
| `CAN\'T-PARSE`                                            | `<PARSE "">$` `<PARSE ")">$`                                                                             |
| `CHANNEL-CLOSED`                                          | `<READ <CLOSE channel>>$`                                                                                |
| `CONTROL-G?`                                              | `^G`                                                                                                     |
| `COUNT-GREATER-THAN-STRING-SIZE`                          | `<PRINTSTRING "" ,OUTCHAN 1>$`                                                                           |
| `DANGEROUS-INTERRUPT-NOT-HANDLED`                         | (See section 21.8.15.) (ITS version only)                                                                |
| `DATA-CANT-GO-IN-UNIFORM-VECTOR`                          | `!["STRING"]$` `![<FRAME>]$`                                                                             |
| `DATA-CAN\'T-GO-IN-STORAGE`                               | `FREEZE ISTORAGE`                                                                                        |
| `DECL-ELEMENT-NOT-FORM-OR-ATOM`                           |                                                                                                          |
| `DECL-VIOLATION`                                          |                                                                                                          |
| `DEVICE-OR-SNAME-DIFFERS`                                 | `RENAME`                                                                                                 |
| `ELEMENT-TYPE-NOT-ATOM-FORM-OR-VECTOR`                    | `DECL` problem                                                                                           |
| `EMPTY-FORM-IN-DECL`                                      |                                                                                                          |
| `EMPTY-OR/PRIMTYPE-FORM`                                  | `<OR>` or `<PRIMTYPE>` in `DECL`                                                                         |
| `EMPTY-STRING`                                            | `<READSTRING "">$`                                                                                       |
| `END-OF-FILE`                                             |                                                                                                          |
| `ERRET-TYPE-NAME-DESIRED`                                 |                                                                                                          |
| `ERROR-IN-COMPILED-CODE`                                  |                                                                                                          |
| `FILE-NOT-FOUND`                                          | `RESTORE`                                                                                                |
| `FILE-SYSTEM-ERROR`                                       |                                                                                                          |
| `FIRST-ARG-WRONG-TYPE`                                    |                                                                                                          |
| `FIRST-ELEMENT-OF-VECTOR-NOT-CODE`                        | `RSUBR` in bad form.                                                                                     |
| `FIRST-VECTOR-ELEMENT-NOT-REST-OR-A-FIX`                  | `#DECL ((X) <LIST [FOO]>)`                                                                               |
| `FRAME-NO-LONGER-EXISTS`                                  | (unused)                                                                                                 |
| `HANDLER-ALREADY-IN-USE`                                  |                                                                                                          |
| `HAS-EMPTY-BODY`                                          | `<#FUNCTION ((X)) 1>$`                                                                                   |
| `ILLEGAL`                                                 |                                                                                                          |
| `ILLEGAL-ARGUMENT-BLOCK`                                  | attempt to `PRINT` a `TUPLE` that no longer exists                                                       |
| `ILLEGAL-FRAME`                                           |                                                                                                          |
| `ILLEGAL-LOCATIVE`                                        |                                                                                                          |
| `ILLEGAL-SEGMENT`                                         | Third and later arguments to MAPF/R not `STRUCTURED`.                                                    |
| `ILLEGAL-TENEX-FILE-NAME`                                 | (Tenex and Tops-20 versions only)                                                                        |
| `INT-DEVICE-WRONG-TYPE-EVALUATION-RESULT`                 | function for `"INT"` input `CHANNEL` returned non-`CHARACTER`.                                           |
| `INTERNAL-BACK-OR-TOP-OF-A-LIST`                          | in compiled code                                                                                         |
| `INTERNAL-INTERRUPT`                                      | (unused)                                                                                                 |
| `INTERRUPT-UNAVAILABLE-ON-TENEX`                          | (Tenex and Tops-20 versions only)                                                                        |
| `ITS-CHANNELS-EXHAUSTED`                                  | Interpreter couldn't open an ITS I/O channel.                                                            |
| `MEANINGLESS-PARAMETER-DECLARATION`                       | bad object in argument `LIST` of Function                                                                |
| `MESSAGE-TOO-BIG`                                         | IPC (ITS version only)                                                                                   |
| `MUDDLE-VERSIONS-DIFFER`                                  | `RESTORE` (version = release)                                                                            |
| `NEGATIVE-ARGUMENT`                                       |                                                                                                          |
| `NIL-LIST-OF-OBLISTS`                                     | `<SET OBLIST '()> T$`                                                                                    |
| `NO-FIXUP-FILE`                                           | MDL couldn't find fixup file (section 19.9).                                                             |
| `NO-ITS-CHANNELS-FREE`                                    | `IPC-ON` (ITS version only)                                                                              |
| `NO-MORE-PAGES`                                           | for pure-code mapping                                                                                    |
| `NO-PROCESS-TO-RESUME`                                    | `<OR <RESUMER> <RESUME>>$`                                                                               |
| `NO-ROOM-AVAILABLE`                                       | MDL couldn't allocate a page to map in pure code.                                                        |
| `NO-SAV-FILE`                                             | MDL couldn't find pure-code file (section 19.9).                                                         |
| `NO-STORAGE`                                              | No free storage available for `GROW`.                                                                    |
| `NON-6-BIT-CHARACTER-IN-FILE-NAME`                        |                                                                                                          |
| `NON-APPLICABLE-REP`                                      | `<VALUE REP>` not `APPLICABLE`                                                                           |
| `NON-APPLICABLE-TYPE`                                     |                                                                                                          |
| `NON-ATOMIC-ARGUMENT`                                     |                                                                                                          |
| `NON-ATOMIC-OBLIST-NAME`                                  | `T!-3$`                                                                                                  |
| `NON-DSK-DEVICE`                                          | (unused)                                                                                                 |
| `NON-EVALUATEABLE-TYPE`                                   | (unused)                                                                                                 |
| `NON-EXISTENT-TAG`                                        | (unused)                                                                                                 |
| `NON-STRUCTURED-ARG-TO-INTERNAL-PUT-REST-NTH-TOP-OR-BACK` | in compiled code                                                                                         |
| `NON-TYPE-FOR-PRIMTYPE-ARG`                               | `<PRIMTYPE not-type>` in `DECL`                                                                          |
| `NOT-A-TTY-TYPE-CHANNEL`                                  |                                                                                                          |
| `NOT-HANDLED`                                             | First argument to `OFF` not `ON`ed.                                                                      |
| `NOT-IN-ARG-LIST`                                         | `TUPLE` or `ITUPLE` called outside argument `LIST`.                                                      |
| `NOT-IN-MAP-FUNCTION`                                     | `MAPRET`, `MAPLEAVE`, `MAPSTOP` not within MAPF/R                                                        |
| `NOT-IN-PROG`                                             | `<RETURN>$` `<AGAIN>$`                                                                                   |
| `NTH-BY-A-NEGATIVE-NUMBER`                                | in compiled code                                                                                         |
| `NTH-REST-PUT-OUT-OF-RANGE`                               | in compiled code                                                                                         |
| `NULL-STRING`                                             | zero-length `STRING`                                                                                     |
| `NUMBER-OUT-OF-RANGE`                                     | `2E38$`                                                                                                  |
| `ON-AN-OBLIST-ALREADY`                                    | `<INSERT T <ROOT>>$`                                                                                     |
| `OUT-OF-BOUNDS`                                           | `<1 '()>$` `BLOAT` argument too large                                                                    |
| `OVERFLOW`                                                | `</ 1 0>$` `<* 1E30 1E30>$`                                                                              |
| `PDL-OVERFLOW-BUFFER-EXHAUSTED`                           | Stack overflow while trying to expand stack: use `RETRY`.                                                |
| `PROCESS-NOT-RESUMABLE`                                   | use of another `PROCESS`'s `FRAME`, etc.                                                                 |
| `PROCESS-NOT-RUNABLE-OR-RESUMABLE`                        |                                                                                                          |
| `PURE-LOAD-FAILURE`                                       | Pure-code file disappeared.                                                                              |
| `READER-SYNTAX-ERROR-ERRET-ANYTHING-TO-GO-ON`             |                                                                                                          |
| `RSUBR-ENTRY-UNLINKED`                                    | `RSUBR-ENTRY` whose `RSUBR` cannot be found                                                              |
| `RSUBR-IN-BAD-FORMAT`                                     |                                                                                                          |
| `RSUBR-LACKS-FIXUPS`                                      | `KEEP-FIXUPS` should have been true when `RSUBR` was input.                                              |
| `SECOND-ARG-WRONG-TYPE`                                   |                                                                                                          |
| `STORAGE-TYPES-DIFFER`                                    | `<CHTYPE 1 LIST>$` `<CHUTYPE '![1] LIST>$`                                                               |
| `STRUCTURE-CONTAINS-UNDUMPABLE-TYPE`                      | `<GC-DUMP <ME> <>>$`                                                                                     |
| `SUBSTITUTE-TYPE-FOR-TYPE`                                | `<SUBSTITUTE SUBR FSUBR>$`                                                                               |
| `TEMPLATE-TYPE-NAME-NOT-OF-TYPE-TEMPLATE`                 | attempt to `GC-READ` a structure containing a `TEMPLATE` whose `TYPE` is defined but is not a `TEMPLATE` |
| `TEMPLATE-TYPE-VIOLATION`                                 |                                                                                                          |
| `THIRD-ARG-WRONG-TYPE`                                    |                                                                                                          |
| `TOO-FEW-ARGUMENTS-SUPPLIED`                              |                                                                                                          |
| `TOO-MANY-ARGS-TO-PRIMTYPE-DECL`                          | `<PRIMTYPE any ...>`                                                                                     |
| `TOO-MANY-ARGS-TO-SPECIAL-UNSPECIAL-DECL`                 | `<SPECIAL any ...>`                                                                                      |
| `TOO-MANY-ARGUMENTS-SUPPLIED`                             |                                                                                                          |
| `TOP-LEVEL-FRAME`                                         | `<ERRET> <FRAME <FRAME <FRAME>>>$`                                                                       |
| `TYPE-ALREADY-EXISTS`                                     | `NEWTYPE`                                                                                                |
| `TYPE-MISMATCH`                                           | attempt to make a value violate its `DECL`                                                               |
| `TYPE-UNDEFINED`                                          |                                                                                                          |
| `TYPES-DIFFER-IN-STORAGE-OBJECT`                          | `ISTORAGE`                                                                                               |
| `TYPES-DIFFER-IN-UNIFORM-VECTOR`                          | `![T <>]$`                                                                                               |
| `UNASSIGNED-VARIABLE`                                     |                                                                                                          |
| `UNATTACHED-PATH-NAME-SEPARATOR`                          | `!-$`                                                                                                    |
| `UNBOUND-VARIABLE`                                        |                                                                                                          |
| `UNMATCHED`                                               | `ENDBLOCK` with no matching `BLOCK`                                                                      |
| `UVECTOR-PUT-TYPE-VIOLATION`                              | `PUT`, `SETLOC`, `SUBSTRUC` in compiled code                                                             |
| `VECTOR-LESS-THAN-2-ELEMENTS`                             | `#DECL ((X) <LIST [REST]>)`                                                                              |
| `WRONG-DIRECTION-CHANNEL`                                 | `<OPEN "MYFILE">$` (Mode missing or misspelt.)                                                           |
| `WRONG-NUMBER-OF-ARGUMENTS`                               |                                                                                                          |
